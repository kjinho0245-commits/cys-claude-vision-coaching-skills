#!/usr/bin/env python3
"""
factor_scale_validator.py
결정론 환원 모듈 — 7 Factor 범위 검증

출처: Petersen & Steinmüller (2009) Section III.2 scale definitions + PDF Figure 1
  West Coast Disaster 검증값: ΔC=3, R=3, V=3, O=3, T=4, Op=0, P=3 → I_AI=19

목적: LLM이 factor 점수를 범위 밖으로 할당하는 것을 차단.
"""
import argparse
import json

SCALES = {
    "delta_c": {
        "min": 1, "max": 3,
        "labels": {1: "years", 2: "months", 3: "days"},
        "source": "Section III.2: 'Wild Cards come fast... rate of change'"
    },
    "r": {
        "min": 1, "max": 5,
        "labels": {1: "local (city/county)", 2: "regional (state/province)",
                   3: "national", 4: "continental/multi-national", 5: "global/planetary"},
        "source": "Section III.2: 'How broad is its effect?'"
    },
    "v": {
        "min": 1, "max": 3,
        "labels": {1: "less vulnerable (resilient)", 2: "moderate", 3: "more vulnerable"},
        "source": "Section III.2: 'How vulnerable is the system?'"
    },
    "o": {
        "min": 1, "max": 3,
        "labels": {1: "less uncertain", 2: "moderate uncertainty", 3: "more uncertain"},
        "source": "Section III.2: 'How unpredictable is the outcome?'"
    },
    "t": {
        "min": 1, "max": 4,
        "labels": {1: "later (2039+)", 2: "medium (2033-2038)",
                   3: "soon (2029-2032)", 4: "imminent (2026-2028)"},
        "source": "Section III.2: 'Does the Wild Card happen sooner rather than later?'",
        "note": "Windows are 2026-based. See timing_windows.py for details."
    },
    "op": {
        "min": -2, "max": 2,
        "labels": {-2: "much support", -1: "some support", 0: "neutral",
                   1: "some opposition", 2: "much opposition"},
        "source": "Section III.2 PDF Figure: '2→-2 / much opposition→much support'"
    },
    "p": {
        "min": 1, "max": 4,
        "labels": {1: "Tools", 2: "Actions", 3: "Sustenance", 4: "Being"},
        "source": "Section III.2: 'At what level does the event affect individuals?'"
    }
}


def validate_score(factor: str, value: int) -> dict:
    if factor not in SCALES:
        return {"valid": False, "error": f"Unknown factor '{factor}'"}
    spec = SCALES[factor]
    in_range = spec["min"] <= value <= spec["max"]
    label = spec["labels"].get(value, f"(value {value} — no label)")
    result = {
        "factor": factor,
        "value": value,
        "valid": in_range,
        "allowed_range": [spec["min"], spec["max"]],
        "label": label,
        "source": spec["source"],
    }
    if spec.get("note"):
        result["note"] = spec["note"]
    if not in_range:
        result["error"] = f"Value {value} outside allowed range [{spec['min']}, {spec['max']}]"
    return result


def validate_all(delta_c, r, v, o, t, op, p) -> dict:
    factors = {"delta_c": delta_c, "r": r, "v": v, "o": o, "t": t, "op": op, "p": p}
    results = {k: validate_score(k, v) for k, v in factors.items()}
    errors = [f for f, res in results.items() if not res["valid"]]
    return {
        "all_valid": len(errors) == 0,
        "error_count": len(errors),
        "failed_factors": errors,
        "per_factor": results,
    }


def main():
    parser = argparse.ArgumentParser(description="Factor scale validator")
    parser.add_argument("--dc", type=int, help="ΔC (1-3)")
    parser.add_argument("--r", type=int, help="R (1-5)")
    parser.add_argument("--v", type=int, help="V (1-3)")
    parser.add_argument("--o", type=int, help="O (1-3)")
    parser.add_argument("--t", type=int, help="T (1-4)")
    parser.add_argument("--op", type=int, help="Op (-2 to +2)")
    parser.add_argument("--p", type=int, help="P (1-4)")
    parser.add_argument("--list", action="store_true", help="List all factor scales")
    args = parser.parse_args()

    if args.list:
        print(json.dumps(SCALES, ensure_ascii=False, indent=2))
    elif all(v is not None for v in [args.dc, args.r, args.v, args.o, args.t, args.op, args.p]):
        result = validate_all(args.dc, args.r, args.v, args.o, args.t, args.op, args.p)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Provide all 7 factors or use --list")


if __name__ == "__main__":
    main()
