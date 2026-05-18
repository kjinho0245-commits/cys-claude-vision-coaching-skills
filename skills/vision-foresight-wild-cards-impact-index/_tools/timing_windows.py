#!/usr/bin/env python3
"""
timing_windows.py
결정론 환원 모듈 — T Timing Factor 연도 창 (2026 기준)

출처: Petersen & Steinmüller (2009) Section III.2 Timing 원칙 verbatim
  "We assume that humanity gains depths and the ability to deal with shocks
   the longer we are around."
  → 더 일찍 일어날수록 = T 높음 = I_AI 높음

PDF 원본 창 (2009 기준): T=4 = 2005-2010 (sooner at time of writing)
본 도구: 2026 현재 시점 기준 재계산

⚠️ 원본 SKILL.md의 T=4 = 2020-2023은 2026년 시점에서 이미 과거 — 수정됨.

원칙: sooner = T높음 = I_AI 높음 (default)
예외: "internet collapse 류" — later=worse. AI Calculator case-by-case 판정.
"""
import argparse
import json
from datetime import datetime

CURRENT_YEAR = 2026

# Updated 2026-based timing windows
# Original PDF (2009): T=4 = 2005-2010 (within ~5 years)
# Adapted for 2026: same relative structure
TIMING_WINDOWS_2026 = {
    4: {"label": "imminent", "range": f"{CURRENT_YEAR}-{CURRENT_YEAR+2}", "description": "2026-2028 (within 2 years)"},
    3: {"label": "soon",     "range": f"{CURRENT_YEAR+3}-{CURRENT_YEAR+6}", "description": "2029-2032"},
    2: {"label": "medium",   "range": f"{CURRENT_YEAR+7}-{CURRENT_YEAR+12}", "description": "2033-2038"},
    1: {"label": "later",    "range": f"{CURRENT_YEAR+13}+", "description": "2039+ (far future)"},
}

# Original SKILL.md (incorrect) windows for reference
TIMING_WINDOWS_OLD = {
    4: "2020-2023 (PAST — invalid for 2026 evaluation)",
    3: "2024-2025 (PAST/expired — invalid for 2026 evaluation)",
    2: "2026-2030",
    1: "2031-2035",
}

# PDF original context (2009)
TIMING_WINDOWS_PDF_2009 = {
    4: "2005-2010 (sooner — PDF original context)",
    3: "2010-2015",
    2: "2015-2020",
    1: "2020-2025 (later — PDF original context)",
}


def get_window(t_value: int) -> dict:
    if t_value not in TIMING_WINDOWS_2026:
        return {
            "error": f"T={t_value} not valid. Must be 1, 2, 3, or 4.",
            "valid_range": list(TIMING_WINDOWS_2026.keys())
        }
    w = TIMING_WINDOWS_2026[t_value]
    return {
        "t_value": t_value,
        "window_2026": w,
        "meaning": f"T={t_value} → {w['description']} → {'higher' if t_value >= 3 else 'lower'} relative impact",
        "principle": "sooner = T higher = I_AI higher (default; except internet-collapse-type events)",
        "source": "Petersen & Steinmüller (2009) Section III.2 verbatim + 2026 reframe",
        "old_window_was": TIMING_WINDOWS_OLD.get(t_value, "N/A"),
        "correction_note": (
            "Original SKILL.md had T=4=2020-2023 and T=3=2024-2025 which are PAST dates in 2026. "
            "Updated to 2026-based windows."
        ) if t_value in (3, 4) else None
    }


def get_t_for_year(year: int) -> dict:
    """Given an expected year, return the appropriate T value."""
    years_from_now = year - CURRENT_YEAR
    if years_from_now <= 2:
        t = 4
    elif years_from_now <= 6:
        t = 3
    elif years_from_now <= 12:
        t = 2
    else:
        t = 1
    w = TIMING_WINDOWS_2026[t]
    return {
        "input_year": year,
        "years_from_now": years_from_now,
        "t_value": t,
        "window": w,
        "source": "Petersen & Steinmüller (2009) Section III.2 Timing factor + 2026 reframe"
    }


def list_all() -> dict:
    return {
        "current_year": CURRENT_YEAR,
        "windows_2026": TIMING_WINDOWS_2026,
        "pdf_original_2009": TIMING_WINDOWS_PDF_2009,
        "old_incorrect_windows": TIMING_WINDOWS_OLD,
        "correction_note": (
            "T=4=2020-2023 and T=3=2024-2025 from original SKILL.md are PAST dates. "
            "Use the 2026-based windows above."
        )
    }


def main():
    parser = argparse.ArgumentParser(description="Timing windows — 2026 based T factor lookup")
    parser.add_argument("--t", type=int, help="T value (1-4)")
    parser.add_argument("--year", type=int, help="Expected year → T value")
    parser.add_argument("--all", action="store_true", help="List all windows")
    args = parser.parse_args()

    if args.t:
        print(json.dumps(get_window(args.t), ensure_ascii=False, indent=2))
    elif args.year:
        print(json.dumps(get_t_for_year(args.year), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(list_all(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
