#!/usr/bin/env python3
"""
foresight_factor_revalidator.py
결정론 환원 모듈 — Foresight Factor A-F 재검증 (monitoring 기준)

출처: Petersen & Steinmüller (2009) Section III.3 verbatim
  "This factor reflects the theoretical possibility of anticipating the event."
  "The Foresight Factor depends on the number, quality and reliability of
   sources (for indicators, Weak Signals)."

목적:
  impact-index sub-skill에서 초기 Foresight Factor를 산출하지만,
  monitoring sub-skill이 실제 weak signal 커버리지를 분석한 후 *재검증*한다.
  LLM이 주관적으로 A-F를 재평가하는 것을 방지.

결정 규칙 (decision matrix — PDF verbatim 기반):
  A: n_detected_signals >= 5 AND source_quality == "high" AND prediction_tech == True
  B: n_detected_signals >= 3 AND source_quality in ("high", "moderate")
  C: n_detected_signals >= 2 AND source_quality == "moderate"
  D: n_detected_signals == 1 OR (n_detected >= 2 AND source_quality == "low")
  E: n_detected_signals == 0 AND wc_type in (1, 2)   # hypothetical but knowable
  F: wc_type == 3   # Type 3 unknown unknowns — PDF "escape from any observation"

Foresight Factor 정의:
  A = many high-quality sources, robust prediction technology available
  B = several reliable sources
  C = some sources, moderate reliability
  D = few sources, lower reliability
  E = very few / zero sources, hypothetical indicators only
  F = no known sources (Type 3 "unknown unknowns")

mismatch 처리:
  impact-index FF vs monitoring FF 차이 시 → monitoring FF 우선 (더 많은 증거 기반)
  mismatch 시 mismatch_explanation 필드 강제 생성
"""
import argparse
import json
import sys

FF_DESCRIPTIONS = {
    "A": "many high-quality sources, robust prediction technology available (PDF §III.3)",
    "B": "several reliable sources (PDF §III.3)",
    "C": "some sources, moderate reliability (PDF §III.3)",
    "D": "few sources, lower reliability (PDF §III.3)",
    "E": "very few / zero sources, hypothetical indicators only (PDF §III.3)",
    "F": "no known sources — Type 3 unknown unknowns escape any observation (PDF §III.3)",
}

SOURCE_QUALITY_OPTIONS = ["high", "moderate", "low"]
WC_TYPE_OPTIONS = [1, 2, 3]


def assign_ff(
    n_detected_signals: int,
    source_quality: str,
    prediction_tech: bool,
    wc_type: int,
) -> dict:
    """Assign Foresight Factor A-F deterministically."""
    errors = []
    if source_quality not in SOURCE_QUALITY_OPTIONS:
        errors.append(f"source_quality='{source_quality}' not in {SOURCE_QUALITY_OPTIONS}")
    if wc_type not in WC_TYPE_OPTIONS:
        errors.append(f"wc_type={wc_type} not in {WC_TYPE_OPTIONS}")
    if n_detected_signals < 0:
        errors.append(f"n_detected_signals={n_detected_signals} must be >= 0")
    if errors:
        return {
            "error": errors,
            "source": "Petersen & Steinmüller (2009) Section III.3 Foresight Factor",
        }

    # Decision matrix
    if wc_type == 3:
        ff = "F"
        rule = "Type 3 unknown unknowns — PDF verbatim: 'escape from any kind of observation or monitoring'"
    elif n_detected_signals >= 5 and source_quality == "high" and prediction_tech:
        ff = "A"
        rule = "≥5 detected signals + high-quality sources + prediction technology available"
    elif n_detected_signals >= 3 and source_quality in ("high", "moderate"):
        ff = "B"
        rule = "≥3 detected signals + high/moderate source quality"
    elif n_detected_signals >= 2 and source_quality == "moderate":
        ff = "C"
        rule = "≥2 detected signals + moderate source quality"
    elif n_detected_signals == 1 or (n_detected_signals >= 2 and source_quality == "low"):
        ff = "D"
        rule = "1 detected signal OR ≥2 signals with low-quality sources"
    elif n_detected_signals == 0 and wc_type in (1, 2):
        ff = "E"
        rule = "0 detected signals — hypothetical; WC is Type 1 or 2 (theoretically knowable)"
    else:
        ff = "D"  # conservative fallback
        rule = "conservative fallback — insufficient data for precise determination"

    return {
        "foresight_factor": ff,
        "description": FF_DESCRIPTIONS[ff],
        "decision_rule": rule,
        "inputs": {
            "n_detected_signals": n_detected_signals,
            "source_quality": source_quality,
            "prediction_tech": prediction_tech,
            "wc_type": wc_type,
        },
        "source": "Petersen & Steinmüller (2009) Section III.3 verbatim",
    }


def compare_with_impact_index(monitoring_ff: str, impact_index_ff: str) -> dict:
    """Compare monitoring FF with impact-index FF — detect mismatch."""
    match = monitoring_ff == impact_index_ff
    result = {
        "monitoring_ff": monitoring_ff,
        "impact_index_ff": impact_index_ff,
        "match": match,
    }
    if not match:
        result["mismatch_explanation"] = (
            f"monitoring sub-skill assigned FF={monitoring_ff} based on actual weak signal "
            f"coverage, overriding impact-index FF={impact_index_ff}. "
            f"Monitoring FF takes precedence as it uses direct evidence of weak signal detection."
        )
        result["final_ff"] = monitoring_ff
        result["authority"] = "monitoring sub-skill FF supersedes impact-index FF per SKILL.md §산출3"
    else:
        result["final_ff"] = monitoring_ff
    return result


def list_scale() -> dict:
    return {
        "scale": FF_DESCRIPTIONS,
        "decision_matrix": {
            "F": "wc_type == 3 (Type 3 unknown unknowns)",
            "A": "n_detected >= 5 AND source_quality=high AND prediction_tech=True",
            "B": "n_detected >= 3 AND source_quality in (high, moderate)",
            "C": "n_detected >= 2 AND source_quality=moderate",
            "D": "n_detected == 1 OR (n_detected >= 2 AND source_quality=low)",
            "E": "n_detected == 0 AND wc_type in (1, 2)",
        },
        "mismatch_rule": "monitoring FF supersedes impact-index FF",
        "source": "Petersen & Steinmüller (2009) Section III.3",
    }


def main():
    parser = argparse.ArgumentParser(
        description="Foresight Factor A-F revalidator — monitoring evidence-based"
    )
    subparsers = parser.add_subparsers(dest="cmd")

    # assign
    asgn = subparsers.add_parser("assign", help="Assign Foresight Factor")
    asgn.add_argument("--n", type=int, required=True, help="Number of detected signals")
    asgn.add_argument("--quality", required=True, choices=SOURCE_QUALITY_OPTIONS)
    asgn.add_argument("--tech", action="store_true", help="Prediction technology available")
    asgn.add_argument("--type", type=int, required=True, choices=WC_TYPE_OPTIONS, help="WC type (1/2/3)")

    # compare
    cmp = subparsers.add_parser("compare", help="Compare monitoring FF vs impact-index FF")
    cmp.add_argument("--monitoring-ff", required=True, choices=list("ABCDEF"))
    cmp.add_argument("--impact-index-ff", required=True, choices=list("ABCDEF"))

    # list
    subparsers.add_parser("list", help="List scale and decision matrix")

    args = parser.parse_args()

    if args.cmd == "assign":
        result = assign_ff(args.n, args.quality, args.tech, args.type)
    elif args.cmd == "compare":
        result = compare_with_impact_index(args.monitoring_ff, args.impact_index_ff)
    elif args.cmd == "list":
        result = list_scale()
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
