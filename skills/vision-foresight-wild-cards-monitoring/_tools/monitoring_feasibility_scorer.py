#!/usr/bin/env python3
"""
monitoring_feasibility_scorer.py
결정론 환원 모듈 — monitoring_feasibility 산출

출처: Petersen & Steinmüller (2009) Section III.3 verbatim
  "Obviously, Wild Cards of the third category (the 'unknown unknowns')
   escape from any kind of observation or monitoring."
  → Type 3 = not_observable

목적: LLM이 monitoring_feasibility 값을 임의로 선택하는 것을 차단.
  Wild Card type과 detected weak signal 수를 기반으로 결정론적으로 산출한다.

결정 규칙:
  not_observable_type_3 : wc_type == 3  (PDF 명시 — 관찰 불가)
  high                  : wc_type in (1, 2) AND n_detected >= 3
  medium                : wc_type in (1, 2) AND n_detected in (1, 2)
  low                   : wc_type in (1, 2) AND n_detected == 0

refresh cadence 연동:
  not_observable_type_3 → cadence = None (모니터링 불필요)
  low                   → cadence = "quarterly"
  medium                → cadence = "monthly" or "weekly" (source availability에 따름)
  high                  → cadence = "daily" or "weekly"

PDF §III.3 "9-step institutional process" Step 5 연계:
  "Structure incoming information: early indicators, linkages, new events,
   unknowns, and confirmations."
"""
import argparse
import json
import sys

FEASIBILITY_OPTIONS = ["high", "medium", "low", "not_observable_type_3"]
WC_TYPE_OPTIONS = [1, 2, 3]

FEASIBILITY_DEFINITIONS = {
    "high": (
        "Many precursor events and indicators detectable (≥3 weak signals). "
        "PDF §III.3: 'We may find precursor events that make the Wild Card more probable.'"
    ),
    "medium": (
        "Some indicators detectable (1-2 weak signals). Monitoring possible but incomplete. "
        "PDF §III.3: 'indicators that hint at a rising probability.'"
    ),
    "low": (
        "No weak signals currently detected. Monitoring theoretically possible for Type 1/2 "
        "but no active indicators yet. Quarterly scan recommended."
    ),
    "not_observable_type_3": (
        "Type 3 Wild Card — PDF §III.3 verbatim: 'Wild Cards of the third category "
        "(the unknown unknowns) escape from any kind of observation or monitoring.' "
        "No monitoring cadence assigned."
    ),
}

CADENCE_MAP = {
    "not_observable_type_3": None,
    "low": "quarterly",
    "medium_low_sources": "monthly",
    "medium_high_sources": "weekly",
    "high": "weekly",
    "high_quantitative": "daily",
}


def score_feasibility(wc_type: int, n_detected_signals: int) -> dict:
    """Deterministically assign monitoring_feasibility."""
    errors = []
    if wc_type not in WC_TYPE_OPTIONS:
        errors.append(f"wc_type={wc_type} not in {WC_TYPE_OPTIONS}")
    if n_detected_signals < 0:
        errors.append(f"n_detected_signals must be >= 0, got {n_detected_signals}")
    if errors:
        return {"error": errors, "source": "Petersen & Steinmüller (2009) Section III.3"}

    if wc_type == 3:
        feasibility = "not_observable_type_3"
        rule = "Type 3 — PDF §III.3 verbatim: 'escape from any kind of observation or monitoring'"
        default_cadence = None
    elif n_detected_signals >= 3:
        feasibility = "high"
        rule = f"Type {wc_type} + {n_detected_signals} detected signals ≥ 3 threshold"
        default_cadence = "weekly"
    elif n_detected_signals >= 1:
        feasibility = "medium"
        rule = f"Type {wc_type} + {n_detected_signals} detected signals (1-2 range)"
        default_cadence = "monthly"
    else:
        feasibility = "low"
        rule = f"Type {wc_type} + 0 detected signals — no active indicators"
        default_cadence = "quarterly"

    return {
        "wc_type": wc_type,
        "n_detected_signals": n_detected_signals,
        "monitoring_feasibility": feasibility,
        "definition": FEASIBILITY_DEFINITIONS[feasibility],
        "decision_rule": rule,
        "recommended_cadence": default_cadence,
        "source": "Petersen & Steinmüller (2009) Section III.3",
    }


def assign_refresh_cadence(
    feasibility: str,
    has_quantitative_threshold: bool,
    source_availability: str,
) -> dict:
    """Assign refresh cadence from feasibility and source context."""
    errors = []
    if feasibility not in FEASIBILITY_OPTIONS:
        errors.append(f"feasibility='{feasibility}' not in {FEASIBILITY_OPTIONS}")
    if source_availability not in ("high", "moderate", "low"):
        errors.append(f"source_availability must be high/moderate/low")
    if errors:
        return {"error": errors}

    if feasibility == "not_observable_type_3":
        cadence = None
        rule = "Type 3 — no cadence (not observable)"
    elif feasibility == "low":
        cadence = "quarterly"
        rule = "low feasibility → quarterly scan"
    elif feasibility == "medium":
        cadence = "weekly" if source_availability == "high" else "monthly"
        rule = f"medium feasibility + source_availability={source_availability}"
    else:  # high
        cadence = "daily" if has_quantitative_threshold else "weekly"
        rule = f"high feasibility + quantitative_threshold={has_quantitative_threshold}"

    return {
        "feasibility": feasibility,
        "has_quantitative_threshold": has_quantitative_threshold,
        "source_availability": source_availability,
        "refresh_cadence": cadence,
        "decision_rule": rule,
        "allowed_cadences": ["daily", "weekly", "monthly", "quarterly", None],
        "source": "Petersen & Steinmüller (2009) Section III.3",
    }


def list_rules() -> dict:
    return {
        "feasibility_decision_matrix": {
            "not_observable_type_3": "wc_type == 3",
            "high": "wc_type in (1,2) AND n_detected >= 3",
            "medium": "wc_type in (1,2) AND n_detected in (1,2)",
            "low": "wc_type in (1,2) AND n_detected == 0",
        },
        "cadence_rules": {
            "not_observable_type_3": "None",
            "low": "quarterly",
            "medium + source_availability=high": "weekly",
            "medium + source_availability=moderate/low": "monthly",
            "high + has_quantitative_threshold=True": "daily",
            "high + has_quantitative_threshold=False": "weekly",
        },
        "definitions": FEASIBILITY_DEFINITIONS,
        "source": "Petersen & Steinmüller (2009) Section III.3",
    }


def main():
    parser = argparse.ArgumentParser(
        description="Monitoring feasibility scorer + refresh cadence assigner"
    )
    subparsers = parser.add_subparsers(dest="cmd")

    # score
    sc = subparsers.add_parser("score", help="Score monitoring_feasibility")
    sc.add_argument("--type", type=int, required=True, choices=WC_TYPE_OPTIONS, help="WC type")
    sc.add_argument("--n", type=int, required=True, help="Number of detected signals")

    # cadence
    cad = subparsers.add_parser("cadence", help="Assign refresh cadence")
    cad.add_argument("--feasibility", required=True, choices=FEASIBILITY_OPTIONS)
    cad.add_argument("--quant", action="store_true", help="Has quantitative threshold")
    cad.add_argument("--sources", required=True, choices=["high", "moderate", "low"])

    # list
    subparsers.add_parser("list", help="List all rules")

    args = parser.parse_args()

    if args.cmd == "score":
        result = score_feasibility(args.type, args.n)
    elif args.cmd == "cadence":
        result = assign_refresh_cadence(args.feasibility, args.quant, args.sources)
    elif args.cmd == "list":
        result = list_rules()
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
