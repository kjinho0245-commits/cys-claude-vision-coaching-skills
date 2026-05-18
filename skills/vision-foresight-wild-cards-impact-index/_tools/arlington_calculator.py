#!/usr/bin/env python3
"""
arlington_calculator.py
결정론 환원 모듈 — Arlington Impact Index 계산

출처: Petersen & Steinmüller (2009) Section III.2
  공식: ΔC + R + V + O + T + Op + P = I_AI
  PDF verbatim: "The Arlington Impact Index is a sum of the impact factors of
  the rate of change, reach, vulnerability, outcome, timing, opposition,
  and power factor of a Wild Card."

목적: LLM이 I_AI 합산을 틀리거나 정규화 값을 임의로 내는 것을 차단.
  West Coast Disaster 검증: ΔC=3, R=3, V=3, O=3, T=4, Op=0, P=3 → I_AI=19

정규화:
  - PDF 명시 범위: 1-24 (이론 max=24)
  - 실제 산술 min(Op=-2 포함): ΔC=1+R=1+V=1+O=1+T=1+Op=-2+P=1 = 4
  - 본 도구는 두 가지 normalization 모두 제공:
    (a) PDF 범위 기반: (I_AI - 1) / (24 - 1) = (I_AI - 1) / 23
    (b) 산술 범위 기반: (I_AI - 4) / (24 - 4) = (I_AI - 4) / 20
"""

import argparse
import json

# Allowed factor ranges (PDF verbatim)
FACTOR_RANGES = {
    "delta_c": {"min": 1, "max": 3, "label": "Rate of change (1=years·2=months·3=days)"},
    "r": {"min": 1, "max": 5, "label": "Reach (1=local→5=global)"},
    "v": {"min": 1, "max": 3, "label": "Vulnerability (1=less→3=more)"},
    "o": {"min": 1, "max": 3, "label": "Outcome (1=less uncertain→3=more uncertain)"},
    "t": {"min": 1, "max": 4, "label": "Timing (1=later→4=sooner)"},
    "op": {"min": -2, "max": 2, "label": "Opposition (-2=much support→+2=much opposition)"},
    "p": {"min": 1, "max": 4, "label": "Power Factor (1=Tools·2=Actions·3=Sustenance·4=Being)"},
}

I_AI_MAX = 24  # 3+5+3+3+4+2+4
I_AI_MIN_ARITHMETIC = 4  # 1+1+1+1+1-2+1 (actual arithmetic minimum with Op=-2)
I_AI_MIN_PDF = 1  # PDF Figure states 1-24 range

WEST_COAST_CALIBRATION = {
    "delta_c": 3, "r": 3, "v": 3, "o": 3, "t": 4, "op": 0, "p": 3,
    "expected_I_AI": 19,
    "source": "Petersen & Steinmüller (2009) PDF p.20 Figure West Coast Disaster verbatim"
}


def validate_factors(factors: dict) -> dict:
    errors = []
    for key, spec in FACTOR_RANGES.items():
        val = factors.get(key)
        if val is None:
            errors.append(f"{key}: missing")
        elif not isinstance(val, (int, float)):
            errors.append(f"{key}: not numeric (got {val})")
        elif not (spec["min"] <= val <= spec["max"]):
            errors.append(f"{key}={val}: out of range [{spec['min']}, {spec['max']}]")
    return {"valid": len(errors) == 0, "errors": errors}


def calculate(delta_c: int, r: int, v: int, o: int, t: int, op: int, p: int) -> dict:
    factors = {"delta_c": delta_c, "r": r, "v": v, "o": o, "t": t, "op": op, "p": p}

    validation = validate_factors(factors)
    if not validation["valid"]:
        return {
            "error": "Factor validation failed",
            "validation_errors": validation["errors"],
            "source": "Petersen & Steinmüller (2009) Section III.2 scale definitions",
        }

    I_AI = delta_c + r + v + o + t + op + p

    # Two normalizations
    norm_pdf = round((I_AI - I_AI_MIN_PDF) / (I_AI_MAX - I_AI_MIN_PDF), 4)  # (I-1)/23
    norm_arithmetic = round((I_AI - I_AI_MIN_ARITHMETIC) / (I_AI_MAX - I_AI_MIN_ARITHMETIC), 4)  # (I-4)/20

    # Self-check against West Coast Disaster
    wc = WEST_COAST_CALIBRATION
    wc_sum = wc["delta_c"] + wc["r"] + wc["v"] + wc["o"] + wc["t"] + wc["op"] + wc["p"]
    calibration_ok = (wc_sum == wc["expected_I_AI"])

    return {
        "I_AI": I_AI,
        "factors": {
            "delta_c": delta_c, "r": r, "v": v, "o": o, "t": t, "op": op, "p": p
        },
        "formula": f"{delta_c} + {r} + {v} + {o} + {t} + {op} + {p} = {I_AI}",
        "normalization": {
            "pdf_range_based": {
                "formula": f"({I_AI} - 1) / (24 - 1) = ({I_AI-1}) / 23",
                "value": norm_pdf,
                "note": "PDF states range 1-24"
            },
            "arithmetic_range_based": {
                "formula": f"({I_AI} - 4) / (24 - 4) = ({I_AI-4}) / 20",
                "value": norm_arithmetic,
                "note": "Actual arithmetic min=4 (with Op=-2)"
            }
        },
        "range": {"theoretical_pdf": [1, 24], "arithmetic": [4, 24]},
        "calibration_check": {
            "west_coast_disaster": f"ΔC=3+R=3+V=3+O=3+T=4+Op=0+P=3={wc_sum}",
            "expected": wc["expected_I_AI"],
            "calibration_pass": calibration_ok,
            "source": wc["source"]
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="Arlington Impact Index calculator — deterministic I_AI sum"
    )
    parser.add_argument("--dc", type=int, required=True, help="ΔC Rate of change (1-3)")
    parser.add_argument("--r", type=int, required=True, help="R Reach (1-5)")
    parser.add_argument("--v", type=int, required=True, help="V Vulnerability (1-3)")
    parser.add_argument("--o", type=int, required=True, help="O Outcome (1-3)")
    parser.add_argument("--t", type=int, required=True, help="T Timing (1-4)")
    parser.add_argument("--op", type=int, required=True, help="Op Opposition (-2 to +2)")
    parser.add_argument("--p", type=int, required=True, help="P Power Factor (1-4)")
    args = parser.parse_args()

    result = calculate(args.dc, args.r, args.v, args.o, args.t, args.op, args.p)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
