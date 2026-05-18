#!/usr/bin/env python3
"""
Environmental Scanning Report Calculator — deterministic engine.

Handles:
  1. Issue ID generation (ISSUE-YYYY-MM-NNN format)
  2. Date calculations (current month/year, cross-month reference)
  3. Report structure validation (Items 1-8 completeness check)
  4. Sources count range check (5-10 per item)
  5. Implications domain coverage validation
  6. Issue tracking ID lookup

Source: Gordon, T.J. & Glenn, J.C. (2009). Environmental Scanning.
        Futures Research Methodology V3.0. Millennium Project. Chapter 02.
        Appendix B — Environmental Security Monthly Report (January 2009).

Usage:
    python3 report_calc.py --fn generate_issue_id '{"year":2026,"month":5,"sequence":1}'
    python3 report_calc.py --fn date_ref '{"year":2026,"month":5}'
    python3 report_calc.py --fn validate_structure '{"items":{"1":"text","2":"text",...}}'
    python3 report_calc.py --fn validate_sources '{"item_id":"1","source_count":6}'
    python3 report_calc.py --fn validate_implications '{"selected_domains":["Policy","Investment"],"item_implications":{"Policy":"text","Investment":"text"}}'
    python3 report_calc.py --fn next_id '{"existing_ids":["ISSUE-2026-05-001","ISSUE-2026-05-002"],"year":2026,"month":5}'
"""

import sys
import json
import re
from datetime import datetime
from typing import List, Dict, Optional

# ─── CONSTANTS ────────────────────────────────────────────────────────────────

REQUIRED_ITEMS = {1, 2, 3, 4, 5, 6, 7, 8}
ITEM_DESCRIPTIONS = {
    1: "Strategic issue 1 (newest/most impactful)",
    2: "Strategic issue 2",
    3: "Strategic issue 3",
    4: "Strategic issue 4",
    5: "Strategic issue 5",
    6: "Technological Advances (with sub-items 6.1-6.N)",
    7: "Updates on Previously Identified Issues (cross-month)",
    8: "Reports Suggested for Review",
}

SOURCES_MIN = 5
SOURCES_MAX = 10

# Gordon-Glenn Appendix B: report started 2002
REPORT_START_YEAR = 2002

MONTH_NAMES_EN = {
    1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",
    7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"
}
MONTH_NAMES_KO = {
    1:"1월",2:"2월",3:"3월",4:"4월",5:"5월",6:"6월",
    7:"7월",8:"8월",9:"9월",10:"10월",11:"11월",12:"12월"
}


# ─── FUNCTION 1: ISSUE ID GENERATOR ──────────────────────────────────────────

def generate_issue_id(year: int, month: int, sequence: int) -> dict:
    """
    Generate canonical Issue ID for cross-month tracking.
    Format: ISSUE-{YYYY}-{MM:02d}-{NNN:03d}

    Source: SKILL.md Issue tracking timeline convention.
    Example: ISSUE-2026-05-001 = first issue of May 2026.

    LLM must not invent or guess sequence numbers — use this function.
    """
    if not (2002 <= year <= 2100):
        return {"error": True, "message": f"year {year} out of [2002, 2100]"}
    if not (1 <= month <= 12):
        return {"error": True, "message": f"month {month} out of [1, 12]"}
    if not (1 <= sequence <= 999):
        return {"error": True, "message": f"sequence {sequence} out of [1, 999]"}

    issue_id = f"ISSUE-{year}-{month:02d}-{sequence:03d}"
    month_label = MONTH_NAMES_EN[month]

    return {
        "error": False,
        "issue_id": issue_id,
        "year": year,
        "month": month,
        "month_name_en": month_label,
        "month_name_ko": MONTH_NAMES_KO[month],
        "sequence": sequence,
        "format": "ISSUE-{YYYY}-{MM:02d}-{NNN:03d}"
    }


def next_issue_id(existing_ids: List[str], year: int, month: int) -> dict:
    """
    Determine next available Issue ID for a given month by inspecting existing IDs.
    Prevents LLM from guessing sequence numbers.
    """
    if not (1 <= month <= 12):
        return {"error": True, "message": f"month {month} out of [1,12]"}

    prefix = f"ISSUE-{year}-{month:02d}-"
    month_ids = [id_ for id_ in existing_ids if id_.startswith(prefix)]

    # Extract sequence numbers
    sequences = []
    for id_ in month_ids:
        m = re.search(r'-(\d{3})$', id_)
        if m:
            sequences.append(int(m.group(1)))

    next_seq = max(sequences, default=0) + 1
    result = generate_issue_id(year, month, next_seq)
    result["existing_count"] = len(month_ids)
    result["next_sequence"] = next_seq
    return result


# ─── FUNCTION 2: DATE REFERENCE GENERATOR ────────────────────────────────────

def date_ref(year: int, month: int) -> dict:
    """
    Generate standardized date references for cross-month citations.
    Returns English and Korean month labels for use in Item 7 cross-references.

    Example output: "January 2026" / "2026년 1월"
    """
    if not (2002 <= year <= 2100):
        return {"error": True, "message": f"year {year} out of [2002, 2100]"}
    if not (1 <= month <= 12):
        return {"error": True, "message": f"month {month} out of [1, 12]"}

    # Previous month
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1

    # Next month
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    def label(y, m):
        return {
            "en": f"{MONTH_NAMES_EN[m]} {y}",
            "ko": f"{y}년 {MONTH_NAMES_KO[m]}"
        }

    return {
        "error": False,
        "current": label(year, month),
        "previous": label(prev_year, prev_month),
        "next": label(next_year, next_month),
        "years_since_2002": year - REPORT_START_YEAR,
        "item7_cross_ref_template": (
            f"[See also {MONTH_NAMES_EN[prev_month]} {prev_year} Item N]"
        ),
        "reference": (
            "Gordon-Glenn (2009) Appendix B — 'All reports since 2002 are available at "
            "http://www.millennium-project.org/millennium/env-scanning.html'"
        )
    }


# ─── FUNCTION 3: REPORT STRUCTURE VALIDATOR ───────────────────────────────────

def validate_structure(items: Dict[str, str]) -> dict:
    """
    Validate that report contains all 8 required items.
    Items should be keyed by "1"-"8" (string).

    PDF Appendix B structure: Items 1-5 (strategic) + 6 (tech) + 7 (updates) + 8 (reports).
    """
    if not items:
        return {"error": True, "message": "items dict is empty"}

    present = set()
    for k in items.keys():
        try:
            n = int(k)
            if 1 <= n <= 8:
                present.add(n)
        except ValueError:
            pass

    missing = REQUIRED_ITEMS - present
    extra = present - REQUIRED_ITEMS

    all_present = len(missing) == 0

    return {
        "error": False,
        "present_items": sorted(present),
        "missing_items": sorted(missing),
        "extra_items": sorted(extra),
        "all_8_present": all_present,
        "status": "PASS" if all_present else f"FAIL — missing items: {sorted(missing)}",
        "item_descriptions": {str(k): v for k, v in ITEM_DESCRIPTIONS.items() if k in missing},
        "reference": (
            "Gordon-Glenn (2009) Appendix B — 8-item structure: "
            "Items 1-5 (strategic), 6 (technological), 7 (updates), 8 (reports)."
        )
    }


# ─── FUNCTION 4: SOURCES COUNT VALIDATOR ─────────────────────────────────────

def validate_sources(item_id: str, source_count: int) -> dict:
    """
    Validate source count for a given item is within [5, 10] range.

    PDF Appendix B standard: "Sources: (additional sources in the Appendix)"
    with 5-10 primary sources per item.
    """
    try:
        item_num = int(item_id)
    except ValueError:
        return {"error": True, "message": f"Invalid item_id '{item_id}' — must be 1-8"}

    if not (1 <= item_num <= 8):
        return {"error": True, "message": f"item_id {item_id} out of [1,8]"}
    if source_count < 0:
        return {"error": True, "message": f"source_count {source_count} cannot be negative"}

    in_range = SOURCES_MIN <= source_count <= SOURCES_MAX
    status = "PASS" if in_range else (
        "FAIL — too few sources" if source_count < SOURCES_MIN
        else "FAIL — too many body sources (move extras to Appendix)"
    )

    return {
        "error": False,
        "item_id": item_id,
        "source_count": source_count,
        "required_range": [SOURCES_MIN, SOURCES_MAX],
        "in_range": in_range,
        "status": status,
        "action": None if in_range else (
            f"Add {SOURCES_MIN - source_count} more source(s)"
            if source_count < SOURCES_MIN
            else f"Move {source_count - SOURCES_MAX} excess source(s) to Appendix"
        ),
        "reference": (
            "Gordon-Glenn (2009) Appendix B — each item has 5-10 primary sources in Body, "
            "comprehensive list in Appendix."
        )
    }


# ─── FUNCTION 5: IMPLICATIONS DOMAIN COVERAGE VALIDATOR ──────────────────────

def validate_implications(
    selected_domains: List[str],
    item_implications: Dict[str, str]
) -> dict:
    """
    Validate that all user-selected N domains have implications written for an item.

    selected_domains: list of domain names selected at Step 1-A (e.g., ["Policy","Investment"])
    item_implications: dict of {domain_name: implications_text} for this item

    Prevents LLM from missing a domain or hardcoding wrong domains.
    """
    if not selected_domains:
        return {
            "error": False,
            "all_covered": True,
            "status": "PASS — generic mode (no specific domains selected)",
            "mode": "generic",
            "note": "No domains selected → Generic Universal Implications mode, no coverage check needed."
        }

    missing = [d for d in selected_domains if d not in item_implications]
    present = [d for d in selected_domains if d in item_implications]

    # Check for non-empty implications
    empty = [d for d in present if not item_implications.get(d, "").strip()]

    all_covered = len(missing) == 0 and len(empty) == 0

    return {
        "error": False,
        "selected_domains": selected_domains,
        "n_required": len(selected_domains),
        "present_domains": present,
        "missing_domains": missing,
        "empty_implications": empty,
        "all_covered": all_covered,
        "status": "PASS" if all_covered else (
            f"FAIL — missing implications for: {missing + empty}"
        ),
        "note": (
            "Implications must cover ALL user-selected N domains. "
            "Never hardcode 'Futurology·Pastoral·Investment' — use actual user selection."
        )
    }


# ─── FUNCTION 6: BATCH VALIDATE REPORT ───────────────────────────────────────

def validate_full_report(data: dict) -> dict:
    """
    Run all validators on a complete report specification.

    Input:
        items: dict {item_id: {"source_count": int, "implications": {domain: text}}}
        selected_domains: list[str]
        year: int
        month: int
    """
    year = data.get("year", datetime.now().year)
    month = data.get("month", datetime.now().month)
    items = data.get("items", {})
    selected_domains = data.get("selected_domains", [])

    results = {}

    # Structure check
    results["structure"] = validate_structure(items)

    # Sources and implications per item
    item_results = {}
    for item_id, item_data in items.items():
        source_count = item_data.get("source_count", 0)
        implications = item_data.get("implications", {})

        item_results[item_id] = {
            "sources": validate_sources(item_id, source_count),
            "implications": validate_implications(selected_domains, implications)
        }
    results["items"] = item_results

    # Date reference
    results["date_ref"] = date_ref(year, month)

    # Overall pass/fail
    all_pass = (
        results["structure"]["all_8_present"] and
        all(
            v["sources"]["in_range"] and v["implications"]["all_covered"]
            for v in item_results.values()
            if isinstance(v, dict)
        )
    )
    results["all_pass"] = all_pass
    results["status"] = "PASS" if all_pass else "FAIL — see individual checks above"

    return results


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
        "generate_issue_id": lambda d: generate_issue_id(d["year"], d["month"], d["sequence"]),
        "next_id":           lambda d: next_issue_id(d["existing_ids"], d["year"], d["month"]),
        "date_ref":          lambda d: date_ref(d["year"], d["month"]),
        "validate_structure":lambda d: validate_structure(d["items"]),
        "validate_sources":  lambda d: validate_sources(d["item_id"], d["source_count"]),
        "validate_implications": lambda d: validate_implications(d["selected_domains"], d["item_implications"]),
        "validate_full_report":  lambda d: validate_full_report(d),
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
