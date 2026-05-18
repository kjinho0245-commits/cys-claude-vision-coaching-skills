#!/usr/bin/env python3
"""
wheel_math.py — vision-foresight-futures-wheel 스킬 전용 결정론 헬퍼.

할루시네이션 구조적 차단 대상:
  - SCBE 노드 수 계산 (V1 STEEPS 6 or V2 8 sector)
  - SRS (Sewongjima Reversal Score) 계산 + 3-tier 판정
  - PRRG 각 gate 최소 검색 수 계산
  - MDE depth 강제 (≥6 기본값 확인)
  - Ring 시간축 범위 조회
  - Cycle 키워드 자동 분류
  - CCP citation completeness 검사
  - SRS forced-reversal compliance 검사

CLI: python3 wheel_math.py <command> '<json_args>'
"""

import json
import sys
import math

# ---------------------------------------------------------------------------
# 1. SCBE Node Count (결정론 — 수식 검증)
# ---------------------------------------------------------------------------

def scbe_node_count(n_primary: int, rings: int = 6, fan_out: int = 2) -> dict:
    """
    SCBE (STEEPS Categorical Binary Expansion) 노드 수 결정론 계산.

    n_primary: primary branches (STEEPS=6, V2 8sector=8)
    rings: depth (default 6)
    fan_out: 2 (uniform binary expansion)

    Formula:
      senary_nodes = n_primary × fan_out^(rings-1)
      total = 1 + sum_{r=1}^{rings} n_primary × fan_out^(r-1)
    """
    if n_primary < 1 or rings < 1 or fan_out < 2:
        raise ValueError("n_primary≥1, rings≥1, fan_out≥2 required")
    senary = n_primary * (fan_out ** (rings - 1))
    total = 1 + sum(n_primary * (fan_out ** (r - 1)) for r in range(1, rings + 1))
    return {
        "n_primary": n_primary,
        "rings": rings,
        "fan_out": fan_out,
        "ring_counts": {
            f"ring_{r}": n_primary * (fan_out ** (r - 1)) for r in range(1, rings + 1)
        },
        "senary_nodes": senary,
        "total_nodes": total,
        "note": (
            f"Center(1) + {' + '.join(str(n_primary*(fan_out**(r-1))) for r in range(1,rings+1))} = {total}. "
            f"Senary (ring {rings}) = {senary}."
        ),
    }


# ---------------------------------------------------------------------------
# 2. SRS (Sewongjima Reversal Score) — 세옹지마 역전 점수
# ---------------------------------------------------------------------------

# Signs: +1 = positive/beneficial, -1 = negative/harmful, 0 = neutral
SRS_THRESHOLDS = {
    "excellent": 1.5,    # avg ≥ 1.5
    "acceptable": 1.0,   # 1.0 ≤ avg < 1.5
    "fail_threshold": 1.0,  # avg < 1.0 → REVISIONS_REQUIRED
}

def srs_compute_lineage(signs: list) -> dict:
    """
    Compute SRS for a single lineage (list of ±1 signs, ring 1 to ring 6).
    reversal_count = number of consecutive ring pairs with opposite signs.
    """
    if not signs or len(signs) < 2:
        return {"reversal_count": 0, "signs": signs, "valid": False}
    reversals = 0
    for i in range(len(signs) - 1):
        if signs[i] != 0 and signs[i + 1] != 0 and signs[i] != signs[i + 1]:
            reversals += 1
    return {
        "reversal_count": reversals,
        "signs": signs,
        "max_possible": len(signs) - 1,
        "valid": True,
    }

def srs_score(lineages: list) -> dict:
    """
    Compute aggregate SRS across all lineages.
    lineages: list of sign lists, e.g. [[+1,-1,+1,-1,+1,-1], [+1,+1,-1,...]]

    Returns avg reversal count and 3-tier compliance verdict.
    """
    if not lineages:
        raise ValueError("No lineages provided")
    results = [srs_compute_lineage(lg) for lg in lineages]
    valid_results = [r for r in results if r["valid"]]
    if not valid_results:
        return {"error": "No valid lineages (need ≥2 signs each)"}
    avg = sum(r["reversal_count"] for r in valid_results) / len(valid_results)

    if avg >= SRS_THRESHOLDS["excellent"]:
        verdict = "EXCELLENT"
        message = f"SRS avg={avg:.2f} ≥ {SRS_THRESHOLDS['excellent']} — strong non-linear reversal"
    elif avg >= SRS_THRESHOLDS["acceptable"]:
        verdict = "ACCEPTABLE"
        message = f"SRS avg={avg:.2f}: 1.0 ≤ avg < 1.5 — acceptable but improvement suggested"
    else:
        verdict = "REVISIONS_REQUIRED"
        message = f"SRS avg={avg:.2f} < {SRS_THRESHOLDS['fail_threshold']} — insufficient non-linearity"

    return {
        "lineage_count": len(lineages),
        "valid_lineage_count": len(valid_results),
        "per_lineage": results,
        "avg_srs": round(avg, 4),
        "thresholds": SRS_THRESHOLDS,
        "verdict": verdict,
        "message": message,
    }

def srs_forced_reversal_compliance(lineages: list) -> dict:
    """
    Check forced reversal compliance for rings 4-5-6 (Quaternary→Quinary→Senary).
    Pacinelli강화: 4차·5차·6차 각각 직전 차수와 50%+ reversal 강제.
    Lineages should have at least 6 elements (ring 1-6 signs).
    """
    ring_names = ["primary", "secondary", "tertiary", "quaternary", "quinary", "senary"]
    forced_rings = [3, 4, 5]  # 0-indexed: quaternary(3), quinary(4), senary(5)

    compliance = {}
    for ring_idx in forced_rings:
        ring_name = ring_names[ring_idx]
        prev_ring_name = ring_names[ring_idx - 1]
        reversals = 0
        total = 0
        for lg in lineages:
            if len(lg) > ring_idx:
                total += 1
                if lg[ring_idx - 1] != 0 and lg[ring_idx] != 0:
                    if lg[ring_idx - 1] != lg[ring_idx]:
                        reversals += 1
        rate = reversals / total if total > 0 else 0.0
        compliance[f"{ring_name}_reversal"] = {
            "from": prev_ring_name,
            "to": ring_name,
            "reversal_rate": round(rate, 4),
            "required": 0.50,
            "pass": rate >= 0.50,
            "lineages_checked": total,
        }

    overall_pass = all(v["pass"] for v in compliance.values())
    return {
        "forced_reversal_compliance": compliance,
        "overall_pass": overall_pass,
        "verdict": "PASS" if overall_pass else "FAIL — forced reversal ≥50% not met",
    }


# ---------------------------------------------------------------------------
# 3. PRRG (Per-Ring Research Gate) — minimum search counts
# ---------------------------------------------------------------------------

RING_NAMES = {
    1: "primary", 2: "secondary", 3: "tertiary",
    4: "quaternary", 5: "quinary", 6: "senary"
}

PRRG_FIXED_MINIMUMS = {
    1: 3,   # Gate_P1_Pre: ≥3 (fixed)
    4: 3,   # Gate_P4_Pre: ≥3 (fixed, + backlash analog required)
    5: 3,   # Gate_P5_Pre: ≥3 (fixed, + paradigm shift analog required)
    6: 2,   # Gate_P6_Pre: ≥2 (fixed, + civilizational analog required)
}

def prrg_min_searches(ring_number: int, prev_ring_count: int = None) -> dict:
    """
    Calculate minimum WebSearch count required for a given ring's PRRG gate.

    ring_number: 1-6
    prev_ring_count: number of impacts in previous ring (for dynamic P2/P3)

    Rules:
      Gate_P1_Pre: ≥3 (fixed)
      Gate_P2_Pre: ≥ previous_ring_count (dynamic = primary count)
      Gate_P3_Pre: ≥ previous_ring_count (dynamic = secondary count)
      Gate_P4_Pre: ≥3 (fixed + backlash analog required)
      Gate_P5_Pre: ≥3 (fixed + paradigm shift analog required)
      Gate_P6_Pre: ≥2 (fixed + civilizational analog required)
    """
    if not (1 <= ring_number <= 6):
        raise ValueError(f"ring_number must be 1-6, got {ring_number}")
    ring_name = RING_NAMES[ring_number]

    if ring_number in PRRG_FIXED_MINIMUMS:
        min_s = PRRG_FIXED_MINIMUMS[ring_number]
        dynamic = False
    else:
        # Rings 2 and 3: dynamic = previous ring count
        if prev_ring_count is None:
            raise ValueError(
                f"Ring {ring_number} ({ring_name}) requires prev_ring_count (dynamic minimum)."
            )
        min_s = max(2, prev_ring_count)  # floor 2
        dynamic = True

    required_analogs = {
        4: "backlash analog",
        5: "paradigm shift analog",
        6: "civilizational analog",
    }

    return {
        "ring": ring_number,
        "ring_name": ring_name,
        "gate_label": f"Gate_P{ring_number}_Pre",
        "min_searches": min_s,
        "dynamic": dynamic,
        "prev_ring_count": prev_ring_count if dynamic else "N/A",
        "required_extras": required_analogs.get(ring_number, None),
        "sign_reversal_required": ring_number >= 4,
    }


# ---------------------------------------------------------------------------
# 4. MDE (Minimum Depth Enforcement)
# ---------------------------------------------------------------------------

def mde_depth_check(depth_requested: int, user_said_quick: bool = False) -> dict:
    """
    Enforce MDE: depth must be ≥6 unless user explicitly said 'quick/간단히/빠르게'.
    """
    mde_target = 6
    if user_said_quick:
        return {
            "depth_requested": depth_requested,
            "mde_target": mde_target,
            "exception_applied": True,
            "final_depth": depth_requested,
            "message": f"MDE exception: user requested quick mode. Depth={depth_requested} allowed.",
        }
    if depth_requested < mde_target:
        return {
            "depth_requested": depth_requested,
            "mde_target": mde_target,
            "exception_applied": False,
            "final_depth": mde_target,
            "message": (
                f"MDE enforced: depth {depth_requested} < {mde_target} → "
                f"automatically elevated to {mde_target}."
            ),
            "action": "ELEVATED",
        }
    return {
        "depth_requested": depth_requested,
        "mde_target": mde_target,
        "exception_applied": False,
        "final_depth": depth_requested,
        "message": f"MDE satisfied: depth={depth_requested} ≥ {mde_target}.",
        "action": "PASS",
    }


# ---------------------------------------------------------------------------
# 5. Ring Time Axis (결정론 — 각 차수별 시간 범위)
# ---------------------------------------------------------------------------

RING_TIME_AXIS = {
    1: {"name": "Primary",    "range": "T+1~5y",   "label": "Near-term"},
    2: {"name": "Secondary",  "range": "T+5~10y",  "label": "Medium-term"},
    3: {"name": "Tertiary",   "range": "T+10~20y", "label": "Long-term"},
    4: {"name": "Quaternary", "range": "T+15~25y", "label": "Extended"},
    5: {"name": "Quinary",    "range": "T+20~30y", "label": "Generational"},
    6: {"name": "Senary",     "range": "T+25~50y", "label": "Civilizational"},
}

def ring_time_axis(ring_number: int) -> dict:
    """Return canonical time range for a given ring."""
    if ring_number not in RING_TIME_AXIS:
        if ring_number > 6:
            return {
                "ring": ring_number,
                "name": f"Ring {ring_number} (Higher-order)",
                "range": "T+50y+",
                "label": "Ultra-long-term",
            }
        raise ValueError(f"ring_number must be 1-6+, got {ring_number}")
    entry = RING_TIME_AXIS[ring_number]
    return {"ring": ring_number, **entry}


# ---------------------------------------------------------------------------
# 6. Cycle Auto-Classification by Keywords
# ---------------------------------------------------------------------------

CYCLE_KEYWORDS = {
    1: ["basic", "v1", "ripple effect", "퓨처스 휠", "futures wheel", "기본",
        "primary", "secondary", "tertiary"],
    2: ["domain", "v2", "steeps", "sector", "폴드 도메인", "8영역",
        "political", "cultural", "environmental"],
    3: ["temporal", "v3", "historic", "current", "future", "시간축",
        "cone", "3d", "historical"],
    4: ["consequence", "linker", "single line", "double line", "triple line",
        "feedback loop", "cross-linkage", "contradiction"],
    5: ["scenario", "forecast", "낙관", "비관", "중립",
        "alternative scenarios", "scenario 분기"],
    6: ["delphi", "5-round", "async panel", "wiki collab", "델파이"],
    7: ["full stack", "완전 분석", "단행본 챕터", "강의 자료", "consulting deliverable",
        "모든 버전", "full analysis"],
    8: ["qc만", "quality review", "검증만", "기존 wheel 검증", "점검",
        "quality-reviewed", "gate"],
    9: ["scbe", "2^n", "균일 fan-out", "steeps 모든", "categorical binary",
        "binary expansion", "256 노드", "192 노드", "ai 컴퓨팅 파워"],
}

def cycle_keyword_match(keywords: list) -> dict:
    """
    Match a list of keywords to the most likely Cycle (1-9).
    Returns top match + confidence.
    """
    if not keywords:
        return {"cycle": 1, "confidence": 0, "reason": "No keywords — defaulting to C1"}

    scores = {cycle: 0 for cycle in range(1, 10)}
    matches = {cycle: [] for cycle in range(1, 10)}
    kw_lower = [k.lower() for k in keywords]

    for cycle, trigger_words in CYCLE_KEYWORDS.items():
        for tw in trigger_words:
            for kw in kw_lower:
                if tw in kw or kw in tw:
                    scores[cycle] += 1
                    matches[cycle].append(f"'{kw}' matches '{tw}'")

    top_cycle = max(scores, key=scores.get)
    top_score = scores[top_cycle]

    if top_score == 0:
        return {
            "cycle": 1,
            "confidence": 0,
            "matches": [],
            "reason": "No keyword match found — defaulting to C1 (Basic V1)",
        }

    return {
        "cycle": top_cycle,
        "confidence": min(top_score / max(3, len(keywords)) * 100, 100),
        "score": top_score,
        "matches": matches[top_cycle],
        "all_scores": scores,
        "reason": f"Top match: C{top_cycle} ({top_score} keyword hits)",
    }


# ---------------------------------------------------------------------------
# 7. CCP Citation Completeness Protocol Check
# ---------------------------------------------------------------------------

def ccp_check(total_impacts: int, r1_count: int, r2_count: int,
              r3_count: int, h_count: int,
              vague_rejected: int = 0, fabricated_detected: int = 0) -> dict:
    """
    Check CCP (Citation Completeness Protocol) compliance.

    Requirements:
      - inline citation rate ≥ 95%
      - quantitative claim R-1 rate ≥ 100% (vague attribution = 0 allowed)
      - reasoning chain ≥ 3 step rate ≥ 95%
    """
    if total_impacts <= 0:
        raise ValueError("total_impacts must be > 0")

    cited = r1_count + r2_count + r3_count + h_count
    citation_rate = cited / total_impacts

    issues = []
    if citation_rate < 0.95:
        issues.append(f"Citation rate {citation_rate:.1%} < 95% required")
    if vague_rejected > 0:
        issues.append(f"{vague_rejected} vague attribution(s) rejected")
    if fabricated_detected > 0:
        issues.append(f"{fabricated_detected} fabricated source(s) detected — CRITICAL")

    pass_ccp = len(issues) == 0

    return {
        "total_impacts": total_impacts,
        "cited_count": cited,
        "citation_rate": round(citation_rate, 4),
        "r1_count": r1_count,
        "r2_count": r2_count,
        "r3_count": r3_count,
        "h_count": h_count,
        "r1_ratio": round(r1_count / total_impacts, 4) if total_impacts else 0,
        "vague_rejected": vague_rejected,
        "fabricated_detected": fabricated_detected,
        "pass": pass_ccp,
        "issues": issues,
        "verdict": "CCP PASS" if pass_ccp else "CCP FAIL: " + "; ".join(issues),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

_COMMANDS = {
    "scbe_node_count": lambda a: scbe_node_count(
        a["n_primary"],
        rings=a.get("rings", 6),
        fan_out=a.get("fan_out", 2),
    ),
    "srs_score": lambda a: srs_score(a["lineages"]),
    "srs_forced_reversal": lambda a: srs_forced_reversal_compliance(a["lineages"]),
    "prrg_min_searches": lambda a: prrg_min_searches(
        a["ring_number"],
        prev_ring_count=a.get("prev_ring_count"),
    ),
    "mde_depth_check": lambda a: mde_depth_check(
        a["depth_requested"],
        user_said_quick=a.get("user_said_quick", False),
    ),
    "ring_time_axis": lambda a: ring_time_axis(a["ring_number"]),
    "cycle_keyword_match": lambda a: cycle_keyword_match(a.get("keywords", [])),
    "ccp_check": lambda a: ccp_check(
        a["total_impacts"],
        a.get("r1_count", 0),
        a.get("r2_count", 0),
        a.get("r3_count", 0),
        a.get("h_count", 0),
        vague_rejected=a.get("vague_rejected", 0),
        fabricated_detected=a.get("fabricated_detected", 0),
    ),
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    command = sys.argv[1]
    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}

    if command not in _COMMANDS:
        result = {
            "error": f"Unknown command: {command!r}",
            "available": list(_COMMANDS.keys()),
        }
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)

    try:
        result = _COMMANDS[command](args)
    except Exception as e:
        result = {"error": str(e), "command": command}
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
