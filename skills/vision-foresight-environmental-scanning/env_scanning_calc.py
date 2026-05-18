#!/usr/bin/env python3
"""
Environmental Scanning Orchestrator — deterministic engine.

Handles:
  1. Cycle routing (user command → Cycle A-I keyword mapping)
  2. Implications Domain lookup (number/name → canonical domain)
  3. PI Chart calculation (Probability × Impact per issue)
  4. Issues Committee scoring aggregation (median, IQR, consensus check)
  5. Input validation for domain numbers and cycle commands

Source: Gordon, T.J. & Glenn, J.C. (2009). Environmental Scanning.
        In Glenn, J.C. & Gordon, T.J. (Eds.),
        Futures Research Methodology Version 3.0.
        The Millennium Project. Chapter 02.

Usage:
    python3 env_scanning_calc.py --fn cycle_route   '{"command":"AGI 환경 스캐닝"}'
    python3 env_scanning_calc.py --fn domain_lookup '{"input":"2,7"}'
    python3 env_scanning_calc.py --fn pi_chart      '{"issues":[{"name":"Issue A","scores":[{"p":70,"i":8},...]}]}'
    python3 env_scanning_calc.py --fn committee_agg '{"issue":"X","p_scores":[70,60,80],"i_scores":[8,7,9]}'
    python3 env_scanning_calc.py --fn validate_domains '{"input":"2,7,15"}'
"""

import sys
import json
import re
import statistics
import math
from typing import List, Dict, Optional, Tuple


# ─── CYCLE ROUTING TABLE ─────────────────────────────────────────────────────
# Source: SKILL.md Orchestration Matrix (user commands → cycles)
# Each entry: list of keywords (lowercase, partial match)

CYCLE_ROUTES = {
    "A": {
        "label": "풀 사이클 (수집→템플릿→패턴→평가→전략→보고서)",
        "sub_skills": ["techniques", "weak-signal-template", "issues-management", "quest-workshop", "report"],
        "keywords": ["환경 스캐닝", "environmental scanning", "futures scanning", "full cycle",
                     "scanning", "full scan", "horizon scan", "horizon scanning"],
        "priority": 1
    },
    "B": {
        "label": "정보 수집 + 템플릿화 + 패턴 분석",
        "sub_skills": ["techniques", "weak-signal-template"],
        "keywords": ["weak signal", "위크 시그널", "약신호", "신호 탐지"],
        "priority": 2
    },
    "C": {
        "label": "Records 종합 + 보고서 자동 작성",
        "sub_skills": ["issues-management", "report"],
        "keywords": ["월간 보고서", "분기 보고서", "연간 보고서", "weekly report", "monthly report",
                     "보고서", "report"],
        "priority": 3
    },
    "D": {
        "label": "AI QUEST Workshop 4 phases",
        "sub_skills": ["quest-workshop"],
        "keywords": ["quest", "퀘스트", "quest 워크숍", "quest workshop"],
        "priority": 2
    },
    "E": {
        "label": "Renfro 4-stage cycle (식별·연구·평가·전략)",
        "sub_skills": ["issues-management"],
        "keywords": ["이슈 평가", "issue 평가", "이슈 관리", "issues management", "renfro",
                     "이슈 식별", "issue identification"],
        "priority": 2
    },
    "F": {
        "label": "수집·패턴만 (Cycle A 단축형)",
        "sub_skills": ["techniques", "weak-signal-template"],
        "keywords": ["horizon scan", "horizon scanning", "지평 스캔"],
        "priority": 3
    },
    "G": {
        "label": "Records 평가 + PI Chart + Top 5 + Strategy",
        "sub_skills": ["issues-management"],
        "keywords": ["top 5", "top5", "상위 5", "상위5", "pi chart", "pi 차트",
                     "top issues", "핵심 이슈"],
        "priority": 2
    },
    "H": {
        "label": "시스템 설계·자동화 구축",
        "sub_skills": ["techniques", "weak-signal-template", "report"],
        "keywords": ["정기 모니터링", "모니터링 셋업", "monitoring setup", "시스템 구축",
                     "자동화", "cron", "automation setup"],
        "priority": 2
    },
    "I": {
        "label": "Generic Futures Scanning System 전 단계 설계",
        "sub_skills": ["techniques", "weak-signal-template", "issues-management", "quest-workshop", "report"],
        "keywords": ["처음 만들어", "시스템 처음", "새 시스템", "new system",
                     "generic futures", "generic scanning"],
        "priority": 0,  # highest priority — specific system design overrides general scanning
    },
}

# ─── IMPLICATIONS DOMAIN LOOKUP TABLE ────────────────────────────────────────
# Canonical domain definitions from SKILL.md

IMPLICATIONS_DOMAINS = {
    1:  {"name": "정부·정책", "en": "Policy", "desc": "정부 자문·정책 수립·입법·규제"},
    2:  {"name": "기업·경영", "en": "Business", "desc": "전략 기획·신사업·M&A·운영"},
    3:  {"name": "학계·연구", "en": "Academia", "desc": "연구 방향·논문·학술 publication"},
    4:  {"name": "미디어·언론", "en": "Media", "desc": "보도·논평·기획 기사·다큐멘터리"},
    5:  {"name": "교육·학습", "en": "Education", "desc": "커리큘럼·교육 프로그램·평생학습"},
    6:  {"name": "종교·목회", "en": "Religious/Pastoral", "desc": "사역·설교·종교적 응답"},
    7:  {"name": "금융·투자", "en": "Investment", "desc": "포트폴리오·자산 배분·종목·리스크"},
    8:  {"name": "비영리·시민사회", "en": "Nonprofit/Civic", "desc": "NGO 활동·시민운동·공익"},
    9:  {"name": "개인·생애설계", "en": "Personal/Life", "desc": "진로·가족·생애 의사결정"},
    10: {"name": "Custom", "en": "Custom", "desc": "사용자 정의 고유 영역"},
}

# Korean name aliases for lookup
DOMAIN_NAME_ALIASES = {
    "정부": 1, "정책": 1, "policy": 1, "government": 1,
    "기업": 2, "경영": 2, "business": 2, "비즈니스": 2,
    "학계": 3, "연구": 3, "academia": 3, "academic": 3,
    "미디어": 4, "언론": 4, "media": 4,
    "교육": 5, "education": 5, "학습": 5,
    "종교": 6, "목회": 6, "pastoral": 6, "religious": 6, "church": 6,
    "금융": 7, "투자": 7, "investment": 7, "finance": 7,
    "비영리": 8, "시민": 8, "nonprofit": 8, "ngo": 8, "civic": 8,
    "개인": 9, "생애": 9, "personal": 9, "life": 9,
    "custom": 10, "커스텀": 10, "사용자 정의": 10,
}

# ─── FUNCTION 1: CYCLE ROUTER ─────────────────────────────────────────────────

def cycle_route(command: str) -> dict:
    """
    Deterministically map user command text to Cycle A-I.
    Uses keyword matching — first high-priority match wins.
    Fallback: Cycle A (full cycle).

    Source: SKILL.md Orchestration Matrix.
    """
    if not command or not command.strip():
        return {
            "error": True,
            "message": "Empty command — cannot route to cycle"
        }

    cmd_lower = command.lower()

    # Collect all matches with priority
    matches = []
    for cycle_id, info in CYCLE_ROUTES.items():
        for kw in info["keywords"]:
            if kw.lower() in cmd_lower:
                matches.append({
                    "cycle": cycle_id,
                    "matched_keyword": kw,
                    "priority": info["priority"],
                    "label": info["label"],
                    "sub_skills": info["sub_skills"]
                })
                break  # one match per cycle is enough

    if not matches:
        # Fallback to Cycle A
        info = CYCLE_ROUTES["A"]
        return {
            "error": False,
            "cycle": "A",
            "label": info["label"],
            "matched_keyword": "(fallback — no keyword match)",
            "sub_skills": info["sub_skills"],
            "note": "No keyword matched; defaulting to Cycle A (full cycle). "
                    "Review command or specify cycle explicitly."
        }

    # Sort by priority (lower number = higher priority), then by cycle ID
    matches.sort(key=lambda x: (x["priority"], x["cycle"]))
    best = matches[0]

    return {
        "error": False,
        "cycle": best["cycle"],
        "label": best["label"],
        "matched_keyword": best["matched_keyword"],
        "sub_skills": best["sub_skills"],
        "all_matches": [{"cycle": m["cycle"], "kw": m["matched_keyword"]} for m in matches],
        "reference": "SKILL.md Orchestration Matrix — Cycle A-I keyword routing"
    }


# ─── FUNCTION 2: IMPLICATIONS DOMAIN LOOKUP ──────────────────────────────────

def domain_lookup(user_input: str) -> dict:
    """
    Parse user's Implications Domain selection and return canonical domain names.
    Accepts: numbers (1-10), Korean names, English names, comma-separated combos.

    Source: SKILL.md Implications Domain Selection (10 options).
    """
    if not user_input or not user_input.strip():
        return {
            "error": False,
            "selected_domains": [],
            "mode": "generic",
            "note": "No selection — running in Generic Universal Implications mode"
        }

    raw = user_input.lower().strip()
    if raw in ("skip", "generic", "통과", "없음", "0"):
        return {
            "error": False,
            "selected_domains": [],
            "mode": "generic",
            "note": "User skipped — Generic Universal Implications mode"
        }

    # Tokenize on commas, spaces, 그리고 Korean/English words
    tokens = [t.strip() for t in re.split(r'[,\s]+', raw) if t.strip()]

    selected = []
    errors = []
    seen_ids = set()

    for token in tokens:
        domain_id = None

        # Try numeric
        if token.isdigit():
            num = int(token)
            if num in IMPLICATIONS_DOMAINS:
                domain_id = num
            else:
                errors.append(f"'{token}' is out of range [1-10]")
                continue
        else:
            # Try alias lookup
            token_clean = token.rstrip('·')
            if token_clean in DOMAIN_NAME_ALIASES:
                domain_id = DOMAIN_NAME_ALIASES[token_clean]
            else:
                # Try partial match
                for alias, did in DOMAIN_NAME_ALIASES.items():
                    if token_clean in alias or alias in token_clean:
                        domain_id = did
                        break

        if domain_id is None:
            errors.append(f"'{token}' could not be matched to any of the 10 domains")
            continue

        if domain_id not in seen_ids:
            seen_ids.add(domain_id)
            d = IMPLICATIONS_DOMAINS[domain_id]
            selected.append({
                "id": domain_id,
                "name": d["name"],
                "en": d["en"],
                "desc": d["desc"]
            })

    if errors and not selected:
        return {"error": True, "messages": errors}

    return {
        "error": False,
        "selected_domains": selected,
        "n_selected": len(selected),
        "mode": "custom" if selected else "generic",
        "warnings": errors if errors else [],
        "reference": "SKILL.md — Implications Domain Selection, 10 options"
    }


# ─── FUNCTION 3: PI CHART CALCULATION ────────────────────────────────────────

def pi_chart(issues: List[Dict]) -> dict:
    """
    Calculate PI (Probability × Impact) score for each issue.

    Each issue dict:
        name: str
        scores: list of {p: 0-100, i: 0-10, time_horizon: str (optional)}

    PI = P × I / 100  (normalized to [0,10] range)
    Aggregate PI per issue = median of individual PI scores.

    Source: Gordon-Glenn (2009) Chapter 02 — Issues management evaluation,
    Secret balloting, PI Chart methodology.
    """
    if not issues:
        return {"error": True, "message": "issues list is empty"}

    results = []
    errors = []

    for issue in issues:
        name = issue.get("name", "Unnamed")
        scores = issue.get("scores", [])

        if not scores:
            errors.append(f"Issue '{name}': no scores provided")
            continue

        pi_values = []
        for i, s in enumerate(scores):
            p = s.get("p")
            imp = s.get("i")
            if p is None or imp is None:
                errors.append(f"Issue '{name}' score {i+1}: missing 'p' or 'i' field")
                continue
            if not (0 <= p <= 100):
                errors.append(f"Issue '{name}' score {i+1}: p={p} out of [0,100]")
                continue
            if not (0 <= imp <= 10):
                errors.append(f"Issue '{name}' score {i+1}: i={imp} out of [0,10]")
                continue
            pi = round(p * imp / 100, 4)
            pi_values.append(pi)

        if not pi_values:
            continue

        n = len(pi_values)
        median_pi = round(statistics.median(pi_values), 4)
        max_pi = round(max(pi_values), 4)
        min_pi = round(min(pi_values), 4)

        if n >= 3:
            sorted_v = sorted(pi_values)
            q1 = statistics.median(sorted_v[:n//2])
            q3 = statistics.median(sorted_v[(n+1)//2:]) if n > 2 else sorted_v[-1]
            iqr = round(q3 - q1, 4)
        else:
            iqr = round(max_pi - min_pi, 4)

        # Consensus check: IQR ≤ 25% of max possible PI (10×100/100=10)
        tight_iqr = iqr <= 2.5  # 25% of max PI=10

        results.append({
            "issue": name,
            "n_scores": n,
            "pi_values": pi_values,
            "median_pi": median_pi,
            "iqr": iqr,
            "max_pi": max_pi,
            "min_pi": min_pi,
            "consensus": tight_iqr,
            "formula": "PI = P × I / 100"
        })

    # Rank by median_pi descending
    results.sort(key=lambda x: x["median_pi"], reverse=True)
    for rank, r in enumerate(results, 1):
        r["rank"] = rank

    return {
        "error": False,
        "n_issues": len(results),
        "pi_table": results,
        "top_issues": [r["issue"] for r in results[:5]],
        "errors": errors,
        "reference": (
            "Gordon, T.J. & Glenn, J.C. (2009). Environmental Scanning. "
            "Futures Research Methodology V3.0, Chapter 02 — PI Chart methodology."
        )
    }


# ─── FUNCTION 4: COMMITTEE SCORING AGGREGATION ───────────────────────────────

def committee_agg(
    issue: str,
    p_scores: List[float],
    i_scores: List[float]
) -> dict:
    """
    Aggregate Issues Committee secret ballot scores for one issue.
    Computes median probability, median impact, median PI, IQR, consensus check.

    p_scores: probability scores 0-100 (one per committee member)
    i_scores: impact scores 0-10 (one per committee member)

    Source: Gordon-Glenn (2009) Chapter 02 — Secret balloting with median + IQR.
    """
    if len(p_scores) != len(i_scores):
        return {
            "error": True,
            "message": f"p_scores length ({len(p_scores)}) != i_scores length ({len(i_scores)})"
        }
    if not p_scores:
        return {"error": True, "message": "No scores provided"}

    bad_p = [p for p in p_scores if not (0 <= p <= 100)]
    bad_i = [i for i in i_scores if not (0 <= i <= 10)]
    if bad_p:
        return {"error": True, "message": f"p_scores out of [0,100]: {bad_p}"}
    if bad_i:
        return {"error": True, "message": f"i_scores out of [0,10]: {bad_i}"}

    n = len(p_scores)
    med_p = round(statistics.median(p_scores), 4)
    med_i = round(statistics.median(i_scores), 4)
    med_pi = round(med_p * med_i / 100, 4)

    # IQR for P (handle n=1 and n=2 edge cases)
    sp = sorted(p_scores)
    if n >= 3:
        p_q1 = statistics.median(sp[:n//2])
        p_q3 = statistics.median(sp[(n+1)//2:])
        p_iqr = round(p_q3 - p_q1, 4)
    elif n == 2:
        p_iqr = round(abs(sp[1] - sp[0]), 4)
    else:
        p_iqr = 0.0  # single scorer: no spread

    # IQR for I (same edge case handling)
    si = sorted(i_scores)
    if n >= 3:
        i_q1 = statistics.median(si[:n//2])
        i_q3 = statistics.median(si[(n+1)//2:])
        i_iqr = round(i_q3 - i_q1, 4)
    elif n == 2:
        i_iqr = round(abs(si[1] - si[0]), 4)
    else:
        i_iqr = 0.0  # single scorer

    # Consensus: P IQR ≤ 25 (25% of 100) AND I IQR ≤ 2.5 (25% of 10)
    consensus = p_iqr <= 25.0 and i_iqr <= 2.5

    return {
        "error": False,
        "issue": issue,
        "n_members": n,
        "probability": {
            "scores": p_scores,
            "median": med_p,
            "iqr": p_iqr,
            "range": [round(min(p_scores),4), round(max(p_scores),4)]
        },
        "impact": {
            "scores": i_scores,
            "median": med_i,
            "iqr": i_iqr,
            "range": [round(min(i_scores),4), round(max(i_scores),4)]
        },
        "median_pi": med_pi,
        "consensus": consensus,
        "consensus_check": {
            "p_iqr_le_25": p_iqr <= 25.0,
            "i_iqr_le_2.5": i_iqr <= 2.5,
            "note": "Consensus = both IQR ≤ 25% of respective scale"
        },
        "formula": "PI = median(P) × median(I) / 100",
        "reference": (
            "Gordon, T.J. & Glenn, J.C. (2009). Environmental Scanning. "
            "Futures Research Methodology V3.0, Chapter 02."
        )
    }


# ─── FUNCTION 5: VALIDATE DOMAINS ─────────────────────────────────────────────

def validate_domains(user_input: str) -> dict:
    """
    Validate user's Implications Domain input and report any errors.
    Returns valid domains and error list.
    """
    result = domain_lookup(user_input)
    if result.get("mode") == "generic":
        return {
            "error": False,
            "valid": True,
            "selected_domains": [],
            "mode": "generic",
            "message": "Generic mode — all domains equally implied"
        }

    has_errors = bool(result.get("warnings")) or result.get("error")
    return {
        "error": result.get("error", False),
        "valid": not result.get("error", False),
        "selected_domains": result.get("selected_domains", []),
        "n_valid": len(result.get("selected_domains", [])),
        "warnings": result.get("warnings", []),
        "messages": result.get("messages", [])
    }


# ─── CLI INTERFACE ────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    function_name: str = ""
    json_str: str = ""

    i = 0
    while i < len(args):
        if args[i] == "--fn" and i + 1 < len(args):
            function_name = args[i + 1]
            i += 2
        elif not args[i].startswith("--"):
            json_str = args[i]
            i += 1
        else:
            i += 1

    if not json_str:
        json_str = sys.stdin.read().strip()

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": True, "message": f"JSON parse error: {e}"}))
        sys.exit(1)

    DISPATCH = {
        "cycle_route":    lambda d: cycle_route(d["command"]),
        "domain_lookup":  lambda d: domain_lookup(d["input"]),
        "pi_chart":       lambda d: pi_chart(d["issues"]),
        "committee_agg":  lambda d: committee_agg(d["issue"], d["p_scores"], d["i_scores"]),
        "validate_domains": lambda d: validate_domains(d["input"]),
    }

    if function_name not in DISPATCH:
        result = {
            "error": True,
            "message": f"Unknown --fn '{function_name}'. Valid: {list(DISPATCH.keys())}"
        }
    else:
        try:
            result = DISPATCH[function_name](data)
        except KeyError as e:
            result = {"error": True, "message": f"Missing required field: {e}"}
        except Exception as e:
            result = {"error": True, "message": f"{type(e).__name__}: {e}"}

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
