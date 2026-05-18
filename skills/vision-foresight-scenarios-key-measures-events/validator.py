#!/usr/bin/env python3
"""
vision-foresight-scenarios-key-measures-events — Deterministic Validator
결정론적 검증기: LLM이 자연어로 재추론하지 못하는 항목을 Python으로 강제 검증.

Usage:
  python3 validator.py --input kme_data.json
  python3 validator.py --demo

Exit codes: 0=all valid, 1=errors found, 2=warnings only
"""

import json
import sys
import argparse
from typing import Any, Dict, List, Tuple

# ── 1. Count range checks ─────────────────────────────────────────────────────

def check_measure_count(n: int) -> Tuple[str, str]:
    """
    TFG V3.0 Ch19 Section III: key measures 6-12 (DEFAULT).
    n < 6 → WARN (may be under-specified)
    n > 12 → WARN (may be over-complex for projection engine)
    """
    if n < 1:
        return "ERROR", "No key measures provided"
    if n < 6:
        return "WARN", f"n_measures={n}: SKILL.md requires 6-12 key measures (TFG Development Step 2)"
    if n > 12:
        return "WARN", f"n_measures={n}: exceeds recommended 12 max — projection complexity increases"
    return "OK", f"n_measures={n}: within required range [6,12]"


def check_event_count(n: int) -> Tuple[str, str]:
    """
    TFG V3.0 Ch19 Section III: events 10-30 (DEFAULT).
    """
    if n < 1:
        return "ERROR", "No events provided"
    if n < 10:
        return "WARN", f"n_events={n}: SKILL.md requires 10-30 events (TFG Development Step 2)"
    if n > 30:
        return "WARN", f"n_events={n}: exceeds recommended 30 max"
    return "OK", f"n_events={n}: within required range [10,30]"


# ── 2. Probability range check ────────────────────────────────────────────────

def check_probability(p: Any, label: str) -> Tuple[bool, str]:
    """
    P(event) MUST be a float or int in [0.0, 1.0].
    No negative values, no values > 1.
    """
    if not isinstance(p, (int, float)) or isinstance(p, bool):
        return False, f"PROB_TYPE_ERROR: {label}={p!r} — must be numeric (int or float), got {type(p).__name__}"
    if p < 0.0 or p > 1.0:
        return False, f"PROB_RANGE_ERROR: {label}={p} — must be in [0.0, 1.0]"
    return True, ""


# ── 3. Probability variation check ────────────────────────────────────────────

def check_probability_variation(event_id: str, probs: Dict[str, float]) -> Tuple[bool, str]:
    """
    TFG V3.0 Ch19 verbatim: 'The probabilities of the events are different in each scenario
    and depend on their position in the scenario space.'
    → At least one pair of scenarios must differ by ≥ 0.05 for each event.

    Exception: If all scenarios truly have the same P (e.g., fixed constant), flag as WARNING not ERROR.
    """
    if len(probs) < 2:
        return True, ""  # can't check variation with <2 scenarios

    values = list(probs.values())
    min_p = min(values)
    max_p = max(values)
    spread = max_p - min_p

    if spread < 0.05:
        return False, (
            f"PROB_VARIATION_WARN: Event '{event_id}' has identical or near-identical probabilities "
            f"across all scenarios (spread={spread:.3f} < 0.05). "
            f"TFG V3.0 verbatim: 'probabilities of the events are different in each scenario'"
        )
    return True, ""


# ── 4. Impact mapping check ───────────────────────────────────────────────────

def check_event_impact_mapping(event: Dict, known_measure_ids: set, label: str) -> List[str]:
    """
    TFG verbatim: events 'can impact the key measures, change the chains of causality'.
    Each event MUST reference ≥1 key measure impact.
    """
    errors = []
    impacts = event.get("impacts", [])

    if not impacts:
        errors.append(
            f"MISSING_IMPACT: {label} has no impact mapping to any key measure. "
            f"TFG verbatim: events must 'impact the key measures'"
        )
    else:
        for km_id in impacts:
            if known_measure_ids and km_id not in known_measure_ids:
                errors.append(
                    f"UNKNOWN_MEASURE_REF: {label} references measure '{km_id}' not in key_measures list"
                )
    return errors


# ── 5. Required sections check ────────────────────────────────────────────────

REQUIRED_TOP_KEYS = {"key_measures", "events", "probability_matrix"}

REQUIRED_MEASURE_KEYS = {"id", "name", "unit", "impact_rationale"}

REQUIRED_EVENT_KEYS = {"id", "name", "impacts", "impact_direction"}


def check_required_sections(data: Dict) -> List[str]:
    errors = []
    for key in REQUIRED_TOP_KEYS:
        if key not in data:
            errors.append(f"MISSING_SECTION: top-level key '{key}' absent")

    if "key_measures" in data:
        if not isinstance(data["key_measures"], list):
            errors.append("TYPE_ERROR: 'key_measures' must be a JSON array")
        else:
            for i, m in enumerate(data["key_measures"]):
                for k in REQUIRED_MEASURE_KEYS:
                    if k not in m:
                        errors.append(f"MISSING_FIELD: key_measures[{i}] missing '{k}'")

    if "events" in data:
        if not isinstance(data["events"], list):
            errors.append("TYPE_ERROR: 'events' must be a JSON array")
        else:
            for i, e in enumerate(data["events"]):
                for k in REQUIRED_EVENT_KEYS:
                    if k not in e:
                        errors.append(f"MISSING_FIELD: events[{i}] missing '{k}'")

    if "probability_matrix" in data:
        if not isinstance(data["probability_matrix"], dict):
            errors.append("TYPE_ERROR: 'probability_matrix' must be a JSON object")

    return errors


# ── 6. Matrix completeness check ──────────────────────────────────────────────

def check_matrix_completeness(data: Dict) -> List[str]:
    """
    Every event in the events list must appear in the probability matrix,
    and every matrix row must correspond to a known event.
    TFG verbatim: 'This list of events will also appear in each scenario.'
    """
    errors = []
    events = data.get("events", [])
    matrix = data.get("probability_matrix", {})

    if not isinstance(events, list) or not isinstance(matrix, dict):
        return errors

    event_ids = {e.get("id") for e in events if isinstance(e, dict) and "id" in e}
    matrix_ids = set(matrix.keys())

    # Events missing from matrix
    missing_from_matrix = event_ids - matrix_ids
    for eid in sorted(missing_from_matrix):
        errors.append(
            f"MATRIX_MISSING: Event '{eid}' not found in probability_matrix. "
            f"TFG verbatim: 'This list of events will also appear in each scenario'"
        )

    # Matrix entries referencing unknown events
    unknown_in_matrix = matrix_ids - event_ids
    for eid in sorted(unknown_in_matrix):
        errors.append(
            f"MATRIX_UNKNOWN: probability_matrix has entry for '{eid}' but no matching event definition"
        )

    return errors


# ── 7. Scenario consistency check ─────────────────────────────────────────────

def check_scenario_consistency(matrix: Dict) -> List[str]:
    """
    All events must have probability values for the SAME set of scenarios.
    """
    errors = []
    if not matrix:
        return errors

    scenario_sets = {}
    for event_id, probs in matrix.items():
        if not isinstance(probs, dict):
            errors.append(f"TYPE_ERROR: matrix['{event_id}'] must be a dict of scenario→probability")
            continue
        scenario_sets[event_id] = set(probs.keys())

    if len(scenario_sets) < 2:
        return errors

    reference_scenarios = list(scenario_sets.values())[0]
    for event_id, scenarios in scenario_sets.items():
        if scenarios != reference_scenarios:
            missing = reference_scenarios - scenarios
            extra = scenarios - reference_scenarios
            if missing:
                errors.append(f"SCENARIO_MISSING: Event '{event_id}' missing scenarios: {sorted(missing)}")
            if extra:
                errors.append(f"SCENARIO_EXTRA: Event '{event_id}' has extra scenarios: {sorted(extra)}")

    return errors


# ── 8. Main validation orchestrator ──────────────────────────────────────────

def validate_kme_output(data: Dict) -> Dict:
    """
    Run all deterministic checks on the LLM-generated KME JSON.
    """
    errors: List[str] = []
    warnings: List[str] = []

    # 1. Required sections
    errors.extend(check_required_sections(data))

    # 2. Measure count
    measures = data.get("key_measures", [])
    if isinstance(measures, list):
        n_m = len(measures)
        status, msg = check_measure_count(n_m)
        if status == "ERROR":
            errors.append(f"COUNT_ERROR: {msg}")
        elif status == "WARN":
            warnings.append(f"COUNT_WARN: {msg}")

    # 3. Event count
    events = data.get("events", [])
    if isinstance(events, list):
        n_e = len(events)
        status, msg = check_event_count(n_e)
        if status == "ERROR":
            errors.append(f"COUNT_ERROR: {msg}")
        elif status == "WARN":
            warnings.append(f"COUNT_WARN: {msg}")

    # 4. Event impact mapping
    known_measure_ids = set()
    if isinstance(measures, list):
        known_measure_ids = {m.get("id") for m in measures if isinstance(m, dict) and "id" in m}

    if isinstance(events, list):
        for i, e in enumerate(events):
            if isinstance(e, dict):
                label = f"Event[{e.get('id', i)}]"
                errors.extend(check_event_impact_mapping(e, known_measure_ids, label))

                # impact_direction must be "+" or "-" or "+/-"
                direction = e.get("impact_direction")
                if direction not in ("+", "-", "+/-", None):
                    errors.append(
                        f"DIRECTION_ERROR: {label}.impact_direction={direction!r} — must be '+', '-', or '+/-'"
                    )

    # 5. Probability matrix checks
    matrix = data.get("probability_matrix", {})
    if isinstance(matrix, dict):
        for event_id, probs in matrix.items():
            if not isinstance(probs, dict):
                errors.append(f"TYPE_ERROR: matrix['{event_id}'] must be a dict")
                continue
            for scenario_name, p in probs.items():
                label = f"matrix['{event_id}']['{scenario_name}']"
                ok, msg = check_probability(p, label)
                if not ok:
                    errors.append(msg)

            # Variation check
            valid_probs = {k: v for k, v in probs.items() if isinstance(v, (int, float)) and not isinstance(v, bool)}
            ok, msg = check_probability_variation(event_id, valid_probs)
            if not ok:
                warnings.append(msg)

        # 5b. Matrix completeness
        errors.extend(check_matrix_completeness(data))

        # 5c. Scenario consistency
        errors.extend(check_scenario_consistency(matrix))

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }


# ── 9. Demo / self-test ───────────────────────────────────────────────────────

DEMO_VALID = {
    "key_measures": [
        {"id": "KM01", "name": "GDP Growth Rate", "unit": "%/year", "current_value": "2.3", "impact_rationale": "Core economic driver affecting all scenario outcomes"},
        {"id": "KM02", "name": "AI R&D Spend", "unit": "USD billion/year", "current_value": "150", "impact_rationale": "Directly determines AI capability trajectory"},
        {"id": "KM03", "name": "Regulatory Stringency Index", "unit": "0-100 scale", "current_value": "35", "impact_rationale": "Legislative environment shapes market access"},
        {"id": "KM04", "name": "Tech Diffusion Rate", "unit": "% of firms adopting/year", "current_value": "12", "impact_rationale": "Determines speed of transformation"},
        {"id": "KM05", "name": "Labor Displacement Rate", "unit": "% of jobs affected/year", "current_value": "1.5", "impact_rationale": "Social stability driver"},
        {"id": "KM06", "name": "Global Trade Volume", "unit": "USD trillion", "current_value": "24", "impact_rationale": "Competitive capability proxy"}
    ],
    "events": [
        {"id": "E01", "name": "AGI Announced by Major Lab", "trigger": "A major lab publicly claims AGI capability", "impacts": ["KM01", "KM02", "KM04"], "impact_direction": "+"},
        {"id": "E02", "name": "Global AI Regulation Treaty", "trigger": "UN-level binding AI treaty signed", "impacts": ["KM03", "KM04"], "impact_direction": "-"},
        {"id": "E03", "name": "AI-Induced Financial Crash", "trigger": "Algorithmic cascade in markets", "impacts": ["KM01", "KM06"], "impact_direction": "-"},
        {"id": "E04", "name": "Energy Price Collapse", "trigger": "Fusion energy commercialization", "impacts": ["KM01", "KM02"], "impact_direction": "+"},
        {"id": "E05", "name": "Pandemic AI Response", "trigger": "New pandemic managed by AI systems", "impacts": ["KM05", "KM04"], "impact_direction": "+"},
        {"id": "E06", "name": "China AI Chip Breakthrough", "trigger": "SMIC achieves 5nm parity", "impacts": ["KM02", "KM06"], "impact_direction": "+/-"},
        {"id": "E07", "name": "Mass AI Labor Protest", "trigger": "General strike by AI-displaced workers", "impacts": ["KM03", "KM05"], "impact_direction": "-"},
        {"id": "E08", "name": "Open Source AI Dominance", "trigger": "Open models overtake closed in capability", "impacts": ["KM04", "KM02"], "impact_direction": "+"},
        {"id": "E09", "name": "AI Tax Legislation", "trigger": "Robot tax enacted by G7", "impacts": ["KM01", "KM03"], "impact_direction": "-"},
        {"id": "E10", "name": "AI-Human Brain Interface", "trigger": "BCIs enable direct AI-human communication", "impacts": ["KM04", "KM05"], "impact_direction": "+"}
    ],
    "probability_matrix": {
        "E01": {"Scenario A": 0.7, "Scenario B": 0.2, "Scenario C": 0.9, "Scenario D": 0.4},
        "E02": {"Scenario A": 0.2, "Scenario B": 0.8, "Scenario C": 0.1, "Scenario D": 0.6},
        "E03": {"Scenario A": 0.1, "Scenario B": 0.3, "Scenario C": 0.05, "Scenario D": 0.4},
        "E04": {"Scenario A": 0.4, "Scenario B": 0.1, "Scenario C": 0.6, "Scenario D": 0.2},
        "E05": {"Scenario A": 0.3, "Scenario B": 0.3, "Scenario C": 0.5, "Scenario D": 0.3},
        "E06": {"Scenario A": 0.5, "Scenario B": 0.4, "Scenario C": 0.3, "Scenario D": 0.7},
        "E07": {"Scenario A": 0.2, "Scenario B": 0.7, "Scenario C": 0.1, "Scenario D": 0.5},
        "E08": {"Scenario A": 0.6, "Scenario B": 0.2, "Scenario C": 0.8, "Scenario D": 0.3},
        "E09": {"Scenario A": 0.1, "Scenario B": 0.6, "Scenario C": 0.05, "Scenario D": 0.4},
        "E10": {"Scenario A": 0.3, "Scenario B": 0.1, "Scenario C": 0.5, "Scenario D": 0.2}
    }
}

DEMO_INVALID = {
    "key_measures": [
        {"id": "KM01", "name": "GDP", "unit": "%", "impact_rationale": "important"},
        {"id": "KM02", "name": "Tech", "unit": "index"}
    ],
    "events": [
        {"id": "E01", "name": "AGI", "impacts": [], "impact_direction": "up"},
        {"id": "E02", "name": "Crash", "impacts": ["KM99"], "impact_direction": "-"}
    ],
    "probability_matrix": {
        "E01": {"Scenario A": 1.5, "Scenario B": -0.1},
        "E03": {"Scenario A": 0.5, "Scenario B": 0.5}
    }
}


def run_demo():
    print("=== DEMO: Valid KME output (10 events, 6 measures) ===")
    r = validate_kme_output(DEMO_VALID)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    print()
    print("=== DEMO: Invalid KME (short counts, bad probs, missing fields) ===")
    r2 = validate_kme_output(DEMO_INVALID)
    print(json.dumps(r2, ensure_ascii=False, indent=2))


# ── 10. CLI entry point ───────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Deterministic validator for vision-foresight-scenarios-key-measures-events JSON"
    )
    parser.add_argument("--input", help="Path to KME JSON file")
    parser.add_argument("--demo", action="store_true", help="Run self-test with demo data")
    args = parser.parse_args()

    if args.demo:
        run_demo()
        sys.exit(0)

    if not args.input:
        parser.print_help()
        sys.exit(2)

    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)

    result = validate_kme_output(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result["valid"]:
        sys.exit(1)
    elif result["warnings"]:
        sys.exit(2)
    else:
        sys.exit(0)
