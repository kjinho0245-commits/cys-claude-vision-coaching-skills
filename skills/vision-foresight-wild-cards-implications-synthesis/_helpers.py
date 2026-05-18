#!/usr/bin/env python3
"""
vision-foresight-wild-cards-implications-synthesis / _helpers.py

결정론적 계산 함수 모음 — LLM 자연어 추론 완전 제외.
할루시네이션 구조적 차단 대상 연산:
  1. domain 선택값 검증
  2. hidden swing WC 필터 (I_AI ≥ 18 AND foresight_factor ∈ {D,E,F})
  3. catalogue coverage ratio 계산
  4. next_review_date 계산 (analysis_date + 90일)
  5. per-WC output schema 필수 필드 검증
  6. WC 목록 카운트 요약

Source of thresholds:
  I_AI ≥ 18 — Petersen, J.L. (1997). Out of the Blue. Arlington Institute.
               Impact Index scale 1-25 (P×B×S / 5),
               18 ≈ top ~28% high-impact zone.
  foresight D-F — monitoring sub-skill 정의 (A=최고가시 → F=불감지),
                  D-F = early-warning 불가 구간.

Usage (all commands write JSON to stdout):
  python3 _helpers.py validate_domain "6"
  python3 _helpers.py filter_hidden_swing wc_list.json
  python3 _helpers.py coverage_ratio 5 2 3
  python3 _helpers.py next_review_date 2026-05-18
  python3 _helpers.py validate_wc wc_entry.json
  python3 _helpers.py count_summary wc_list.json
"""

import json
import sys
from datetime import date, timedelta

# ─── Constants (결정론적, 변경 불가) ─────────────────────────────────────────

VALID_DOMAINS: set[str] = {str(i) for i in range(1, 11)} | {"Custom", "Skip"}
FORESIGHT_LOW_VIS: set[str] = {"D", "E", "F"}
I_AI_THRESHOLD: int = 18
REVIEW_INTERVAL_DAYS: int = 90

REQUIRED_WC_FIELDS: list[str] = [
    "wc_id", "title", "I_AI", "foresight_factor",
    "possible_implications", "domain_specific_implications",
    "hidden_swing_flag", "catalogue_ref", "confidence", "counter_narrative",
]
REQUIRED_PI_FIELDS: list[str] = [
    "reality", "habitat", "activity", "group_relationships",
]
VALID_CONFIDENCE: set[str] = {"high", "medium", "low"}
VALID_FORESIGHT: set[str] = {"A", "B", "C", "D", "E", "F", "MISSING_SCORE"}


# ─── Functions ────────────────────────────────────────────────────────────────

def validate_domain(raw: str) -> dict:
    """
    도메인 선택값 검증.
    범위 외 입력 → Skip 자동 적용 (LLM 판단 불허).
    """
    clean = raw.strip()
    if clean in VALID_DOMAINS:
        return {"domain": clean, "auto_skip": False}
    return {"domain": "Skip", "auto_skip": True, "original": clean}


def filter_hidden_swing(wc_list: list[dict]) -> dict:
    """
    Hidden Swing WC 필터.
    조건: I_AI ≥ 18 AND foresight_factor ∈ {D, E, F}
    I_AI 또는 foresight_factor 누락 WC → missing_score 목록에 별도 수집.
    """
    hidden: list[dict] = []
    missing_score: list[str] = []
    errors: list[str] = []

    for wc in wc_list:
        wid = wc.get("wc_id", "UNKNOWN")
        i_ai = wc.get("I_AI")
        ff = wc.get("foresight_factor", "")

        if i_ai is None or ff is None or ff == "" or ff == "MISSING_SCORE":
            missing_score.append(wid)
            continue

        if not isinstance(i_ai, (int, float)):
            errors.append(f"{wid}: I_AI is not numeric ({i_ai!r})")
            continue
        if ff not in VALID_FORESIGHT:
            errors.append(f"{wid}: foresight_factor invalid ({ff!r})")
            continue

        if i_ai >= I_AI_THRESHOLD and ff in FORESIGHT_LOW_VIS:
            hidden.append({
                "id": wid,
                "title": wc.get("title", ""),
                "I_AI": i_ai,
                "foresight_factor": ff,
            })

    return {
        "hidden_swing_wcs": hidden,
        "n_hidden_swing": len(hidden),
        "missing_score_wcs": missing_score,
        "errors": errors,
        "threshold": {"I_AI": I_AI_THRESHOLD, "foresight": sorted(FORESIGHT_LOW_VIS)},
    }


def compute_coverage_ratio(
    petersen_used: int, steinmuller_used: int, invented: int
) -> dict:
    """
    78+55 catalogue coverage ratio 결정론 계산.
    분모가 0이면 ratio를 null로 반환.
    """
    if not all(isinstance(x, int) and x >= 0 for x in [petersen_used, steinmuller_used, invented]):
        return {"error": "All counts must be non-negative integers"}

    total = petersen_used + steinmuller_used + invented
    if total == 0:
        return {
            "petersen": None, "steinmuller": None, "invented": None,
            "total": 0, "note": "No WCs provided — ratio undefined",
        }
    return {
        "petersen": round(petersen_used / total, 4),
        "steinmuller": round(steinmuller_used / total, 4),
        "invented": round(invented / total, 4),
        "total": total,
        "petersen_used": petersen_used,
        "steinmuller_used": steinmuller_used,
        "invented_count": invented,
    }


def compute_next_review_date(analysis_date_iso: str | None = None) -> dict:
    """
    다음 리뷰 날짜 결정론 계산: analysis_date + REVIEW_INTERVAL_DAYS(90일).
    analysis_date_iso = None이면 오늘 날짜 사용.
    """
    if analysis_date_iso:
        try:
            base = date.fromisoformat(analysis_date_iso)
        except ValueError:
            return {"error": f"Invalid ISO date: {analysis_date_iso!r}", "next_review_date": None}
    else:
        base = date.today()

    next_date = base + timedelta(days=REVIEW_INTERVAL_DAYS)
    return {
        "analysis_date": base.isoformat(),
        "interval_days": REVIEW_INTERVAL_DAYS,
        "next_review_date": next_date.isoformat(),
    }


def validate_wc_schema(wc: dict) -> dict:
    """
    단일 WC output entry 필수 필드 검증.
    결과: {"valid": bool, "missing_fields": [...], "invalid_values": [...]}
    """
    missing: list[str] = []
    invalid: list[str] = []

    for f in REQUIRED_WC_FIELDS:
        if f not in wc:
            missing.append(f)

    if "possible_implications" in wc:
        pi = wc["possible_implications"]
        if isinstance(pi, dict):
            for f in REQUIRED_PI_FIELDS:
                if f not in pi:
                    missing.append(f"possible_implications.{f}")
        else:
            invalid.append("possible_implications must be a dict")

    if "confidence" in wc and wc["confidence"] not in VALID_CONFIDENCE:
        invalid.append(f"confidence must be one of {VALID_CONFIDENCE}, got {wc['confidence']!r}")

    if "foresight_factor" in wc and wc["foresight_factor"] not in VALID_FORESIGHT:
        invalid.append(f"foresight_factor invalid: {wc['foresight_factor']!r}")

    if "hidden_swing_flag" in wc and not isinstance(wc["hidden_swing_flag"], bool):
        invalid.append("hidden_swing_flag must be bool")

    return {
        "wc_id": wc.get("wc_id", "UNKNOWN"),
        "valid": len(missing) == 0 and len(invalid) == 0,
        "missing_fields": missing,
        "invalid_values": invalid,
    }


def count_summary(wc_list: list[dict]) -> dict:
    """WC 목록 카운트 요약 — output meta 섹션용."""
    petersen = sum(1 for w in wc_list if w.get("catalogue_ref", {}).get("petersen") is not None)
    steinmuller = sum(1 for w in wc_list if w.get("catalogue_ref", {}).get("steinmuller") is not None)
    invented = sum(1 for w in wc_list if w.get("catalogue_ref", {}).get("invented") is not None)
    return {
        "n_total": len(wc_list),
        "n_petersen_78_used": petersen,
        "n_steinmuller_55_used": steinmuller,
        "n_invented": invented,
    }


# ─── CLI dispatcher ───────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No command specified. See docstring for usage."}))
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "validate_domain":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: validate_domain <value>"}))
            sys.exit(1)
        print(json.dumps(validate_domain(sys.argv[2])))

    elif cmd == "filter_hidden_swing":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: filter_hidden_swing <wc_list.json>"}))
            sys.exit(1)
        try:
            data = json.load(open(sys.argv[2], encoding="utf-8"))
            if not isinstance(data, list):
                data = data.get("top_wc_list", data.get("wc_list", []))
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(json.dumps({"error": str(e)}))
            sys.exit(1)
        print(json.dumps(filter_hidden_swing(data), ensure_ascii=False, indent=2))

    elif cmd == "coverage_ratio":
        if len(sys.argv) < 5:
            print(json.dumps({"error": "Usage: coverage_ratio <petersen_n> <steinmuller_n> <invented_n>"}))
            sys.exit(1)
        try:
            p, s, inv = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
        except ValueError:
            print(json.dumps({"error": "All three arguments must be integers"}))
            sys.exit(1)
        print(json.dumps(compute_coverage_ratio(p, s, inv)))

    elif cmd == "next_review_date":
        d = sys.argv[2] if len(sys.argv) > 2 else None
        print(json.dumps(compute_next_review_date(d)))

    elif cmd == "validate_wc":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: validate_wc <wc_entry.json>"}))
            sys.exit(1)
        try:
            wc = json.load(open(sys.argv[2], encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(json.dumps({"error": str(e)}))
            sys.exit(1)
        print(json.dumps(validate_wc_schema(wc), ensure_ascii=False, indent=2))

    elif cmd == "count_summary":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Usage: count_summary <wc_list.json>"}))
            sys.exit(1)
        try:
            data = json.load(open(sys.argv[2], encoding="utf-8"))
            if not isinstance(data, list):
                data = data.get("top_wc_list", data.get("wc_list", []))
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(json.dumps({"error": str(e)}))
            sys.exit(1)
        print(json.dumps(count_summary(data)))

    else:
        print(json.dumps({"error": f"Unknown command: {cmd!r}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
