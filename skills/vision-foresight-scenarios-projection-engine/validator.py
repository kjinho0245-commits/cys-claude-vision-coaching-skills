#!/usr/bin/env python3
"""
vision-foresight-scenarios-projection-engine — Deterministic Validator
결정론적 검증기: LLM이 자연어로 재추론하지 못하는 항목을 Python으로 강제 검증.

Validates two types of input:
  1. Projection input (handoff from vision-foresight-scenarios-key-measures-events + TIA params)
  2. Monte Carlo output (from monte_carlo.py)

Usage:
  python3 validator.py --input projection_input.json
  python3 validator.py --output mc_output.json
  python3 validator.py --demo

Exit codes: 0=all valid, 1=errors found, 2=warnings only

References:
  TFG V3.0 Ch19 Section III: "events within a scenario impact several measures
  wherever they are used, they have the same probability; thus, internal
  consistency is promoted."
"""

import json
import sys
import argparse
import math
from typing import Any, Dict, List, Optional, Set, Tuple


# ── 1. Required field checks ──────────────────────────────────────────────────

REQUIRED_TOP_KEYS_INPUT = {
    "key_measures", "events", "probability_matrix", "scenarios",
    "time_horizon", "monte_carlo_runs"
}

REQUIRED_MEASURE_KEYS = {"id", "name", "unit", "current_value"}

REQUIRED_EVENT_KEYS = {"id", "name", "impacts", "impact_direction", "impact_magnitude_pct"}

REQUIRED_TIA_PARAM_KEYS = {
    "time_to_first_impact",
    "time_to_max_impact",
    "time_to_steady_state",
    "steady_state_magnitude_pct"
}

VALID_IMPACT_DIRECTIONS = {"+", "-", "+/-"}


def check_required_input_sections(data: Dict) -> List[str]:
    errors = []
    for key in REQUIRED_TOP_KEYS_INPUT:
        if key not in data:
            errors.append(f"MISSING_SECTION: top-level key '{key}' is absent")

    if "key_measures" in data:
        if not isinstance(data["key_measures"], list):
            errors.append("TYPE_ERROR: 'key_measures' must be a JSON array")
        else:
            for i, m in enumerate(data["key_measures"]):
                if not isinstance(m, dict):
                    errors.append(f"TYPE_ERROR: key_measures[{i}] must be a dict")
                    continue
                for k in REQUIRED_MEASURE_KEYS:
                    if k not in m:
                        errors.append(f"MISSING_FIELD: key_measures[{i}] missing '{k}'")

    if "events" in data:
        if not isinstance(data["events"], list):
            errors.append("TYPE_ERROR: 'events' must be a JSON array")
        else:
            for i, e in enumerate(data["events"]):
                if not isinstance(e, dict):
                    errors.append(f"TYPE_ERROR: events[{i}] must be a dict")
                    continue
                for k in REQUIRED_EVENT_KEYS:
                    if k not in e:
                        errors.append(f"MISSING_FIELD: events[{i}] missing '{k}'")

    if "probability_matrix" in data:
        if not isinstance(data["probability_matrix"], dict):
            errors.append("TYPE_ERROR: 'probability_matrix' must be a JSON object")

    if "scenarios" in data:
        if not isinstance(data["scenarios"], list) or len(data["scenarios"]) < 2:
            errors.append(
                "SCENARIO_COUNT_ERROR: 'scenarios' must be a list with ≥2 entries. "
                "TFG verbatim: 'The probabilities of the events are different in each scenario'"
            )

    if "time_horizon" in data:
        th = data["time_horizon"]
        if not isinstance(th, dict):
            errors.append("TYPE_ERROR: 'time_horizon' must be a dict with start_year and end_year")
        else:
            if "start_year" not in th:
                errors.append("MISSING_FIELD: time_horizon.start_year absent")
            if "end_year" not in th:
                errors.append("MISSING_FIELD: time_horizon.end_year absent")

    if "monte_carlo_runs" in data:
        n = data["monte_carlo_runs"]
        if not isinstance(n, int) or n < 1:
            errors.append("MC_RUNS_ERROR: monte_carlo_runs must be a positive integer")
        elif n < 100:
            errors.append(
                f"MC_RUNS_WARN: monte_carlo_runs={n} is below recommended minimum of 100. "
                "TFG Section III: '1000+ runs recommended for stable CI'"
            )

    return errors


# ── 2. Time horizon logic check ───────────────────────────────────────────────

def check_time_horizon(data: Dict) -> List[str]:
    """
    start_year < end_year, and projection span ≥1 year.
    """
    errors = []
    th = data.get("time_horizon", {})
    if not isinstance(th, dict):
        return errors

    start = th.get("start_year")
    end = th.get("end_year")

    if start is None or end is None:
        return errors

    if not isinstance(start, int) or not isinstance(end, int):
        errors.append("TYPE_ERROR: time_horizon.start_year and end_year must be integers")
        return errors

    if end <= start:
        errors.append(
            f"TIME_HORIZON_ERROR: end_year ({end}) must be strictly greater than start_year ({start})"
        )

    if end - start < 5:
        errors.append(
            f"TIME_HORIZON_WARN: projection span is only {end - start} years — "
            "TFG recommends ≥5 year horizon for meaningful scenario divergence"
        )

    return errors


# ── 3. Probability range check ────────────────────────────────────────────────

def check_probability(p: Any, label: str) -> Tuple[bool, str]:
    """P(event) MUST be in [0.0, 1.0]."""
    if not isinstance(p, (int, float)) or isinstance(p, bool):
        return False, (
            f"PROB_TYPE_ERROR: {label}={p!r} — must be numeric (int or float), "
            f"got {type(p).__name__}"
        )
    if p < 0.0 or p > 1.0:
        return False, f"PROB_RANGE_ERROR: {label}={p} — must be in [0.0, 1.0]"
    return True, ""


# ── 4. Probability variation check ────────────────────────────────────────────

def check_probability_variation(event_id: str, probs: Dict[str, float]) -> Tuple[bool, str]:
    """
    TFG V3.0 Ch19 verbatim: 'The probabilities of the events are different in each scenario
    and depend on their position in the scenario space.'
    At least one pair must differ by ≥0.05.
    """
    if len(probs) < 2:
        return True, ""

    values = list(probs.values())
    spread = max(values) - min(values)

    if spread < 0.05 - 1e-9:
        return False, (
            f"PROB_VARIATION_WARN: Event '{event_id}' spread={spread:.4f} < 0.05 across scenarios. "
            "TFG verbatim: 'probabilities of the events are different in each scenario'"
        )
    return True, ""


# ── 5. Event impact direction check ──────────────────────────────────────────

def check_impact_direction(event: Dict) -> Optional[str]:
    direction = event.get("impact_direction")
    if direction not in VALID_IMPACT_DIRECTIONS:
        return (
            f"DIRECTION_ERROR: events[{event.get('id')}].impact_direction={direction!r} — "
            f"must be one of {sorted(VALID_IMPACT_DIRECTIONS)}"
        )
    return None


# ── 6. Event magnitude check ──────────────────────────────────────────────────

def check_impact_magnitude(event: Dict) -> Optional[str]:
    """
    impact_magnitude_pct must be a positive number (% change at max impact).
    TIA verbatim: 'largest magnitude' is a required TIA event parameter.
    """
    mag = event.get("impact_magnitude_pct")
    if mag is None:
        return (
            f"MISSING_MAGNITUDE: events[{event.get('id')}] missing 'impact_magnitude_pct'. "
            "TIA V3.0 Ch08: event impact requires a 'largest magnitude' parameter. "
            "Use 1-100 (percent change); default 10 if truly unknown."
        )
    if not isinstance(mag, (int, float)) or isinstance(mag, bool):
        return (
            f"TYPE_ERROR: events[{event.get('id')}].impact_magnitude_pct must be numeric"
        )
    if mag <= 0:
        return (
            f"MAGNITUDE_ERROR: events[{event.get('id')}].impact_magnitude_pct={mag} must be > 0"
        )
    if mag > 200:
        return (
            f"MAGNITUDE_WARN: events[{event.get('id')}].impact_magnitude_pct={mag} > 200% — "
            "verify this is intentional"
        )
    return None


# ── 7. TIA parameter completeness check ──────────────────────────────────────

def check_tia_params(event: Dict) -> List[str]:
    """
    TIA V3.0 Ch08 verbatim: 5 impact parameters required.
    If tia_params is present, all sub-keys must be present and logically ordered.
    If absent: WARN (defaults will be used by monte_carlo.py).
    """
    warnings = []
    eid = event.get("id", "?")
    tia = event.get("tia_params")

    if tia is None:
        warnings.append(
            f"TIA_PARAMS_WARN: events[{eid}] has no 'tia_params' — "
            "monte_carlo.py will use defaults (T_F=1, T_M=3, T_S=10, M_S=50% of M_L). "
            "TIA V3.0 Ch08: 5 parameters (T_F, T_M, T_S, M_L, M_S) are expert-judged."
        )
        return warnings

    if not isinstance(tia, dict):
        warnings.append(f"TYPE_WARN: events[{eid}].tia_params must be a dict")
        return warnings

    for k in REQUIRED_TIA_PARAM_KEYS:
        if k not in tia:
            warnings.append(
                f"TIA_MISSING_PARAM: events[{eid}].tia_params missing '{k}'. "
                "Default will be used by monte_carlo.py."
            )

    # Logical ordering: T_F ≤ T_M ≤ T_S
    t_f = tia.get("time_to_first_impact", 1)
    t_m = tia.get("time_to_max_impact", 3)
    t_s = tia.get("time_to_steady_state", 10)

    if isinstance(t_f, (int, float)) and isinstance(t_m, (int, float)):
        if t_f > t_m:
            warnings.append(
                f"TIA_ORDER_WARN: events[{eid}]: time_to_first_impact ({t_f}) > "
                f"time_to_max_impact ({t_m}) — TIA requires T_F ≤ T_M"
            )

    if isinstance(t_m, (int, float)) and isinstance(t_s, (int, float)):
        if t_m > t_s:
            warnings.append(
                f"TIA_ORDER_WARN: events[{eid}]: time_to_max_impact ({t_m}) > "
                f"time_to_steady_state ({t_s}) — TIA requires T_M ≤ T_S"
            )

    return warnings


# ── 8. Event impact mapping check ────────────────────────────────────────────

def check_event_impact_mapping(event: Dict, known_measure_ids: Set[str]) -> List[str]:
    """Each event MUST reference ≥1 key measure."""
    errors = []
    eid = event.get("id", "?")
    impacts = event.get("impacts", [])

    if not impacts:
        errors.append(
            f"MISSING_IMPACT: events[{eid}] has no impact mapping. "
            "TFG verbatim: events must 'impact the key measures'"
        )
    else:
        for km_id in impacts:
            if known_measure_ids and km_id not in known_measure_ids:
                errors.append(
                    f"UNKNOWN_MEASURE_REF: events[{eid}] references measure '{km_id}' "
                    "not found in key_measures list"
                )
    return errors


# ── 9. Probability matrix completeness check ─────────────────────────────────

def check_matrix_completeness(data: Dict) -> List[str]:
    """
    Every event in the events list must appear in probability_matrix.
    Every matrix row must correspond to a known event.
    TFG verbatim: 'This list of events will also appear in each scenario.'
    """
    errors = []
    events = data.get("events", [])
    matrix = data.get("probability_matrix", {})

    if not isinstance(events, list) or not isinstance(matrix, dict):
        return errors

    event_ids = {e.get("id") for e in events if isinstance(e, dict) and "id" in e}
    matrix_ids = set(matrix.keys())

    for eid in sorted(event_ids - matrix_ids):
        errors.append(
            f"MATRIX_MISSING: Event '{eid}' not in probability_matrix. "
            "TFG verbatim: 'This list of events will also appear in each scenario'"
        )

    for eid in sorted(matrix_ids - event_ids):
        errors.append(
            f"MATRIX_UNKNOWN: probability_matrix has entry for '{eid}' "
            "but no matching event definition"
        )

    return errors


# ── 10. Internal consistency check (TFG verbatim enforcement) ─────────────────

def check_internal_consistency(data: Dict) -> List[str]:
    """
    TFG V3.0 Ch19 Section III verbatim:
    'events within a scenario impact several measures wherever they are used,
     they have the same probability; thus, internal consistency is promoted.'

    Enforcement:
    For each event E that impacts multiple measures within the same scenario:
      → The probability P(E|scenario) in the matrix must be IDENTICAL for all
        measure calculations within that scenario.

    Since the probability matrix already stores exactly ONE P(E|scenario) per
    event-scenario pair, internal consistency is structurally guaranteed IF:
      a) The matrix is complete (all events × all scenarios covered)
      b) Monte Carlo uses the matrix as the single source of truth
      c) The same event ID is not duplicated with different probabilities

    This function verifies (a) and (c).
    """
    errors = []
    matrix = data.get("probability_matrix", {})
    declared_scenarios = data.get("scenarios", [])

    if not isinstance(matrix, dict) or not declared_scenarios:
        return errors

    # Check: every event in matrix covers ALL declared scenarios
    for event_id, probs in matrix.items():
        if not isinstance(probs, dict):
            continue
        covered = set(probs.keys())
        declared_set = set(declared_scenarios)

        missing = declared_set - covered
        extra = covered - declared_set

        if missing:
            errors.append(
                f"CONSISTENCY_ERROR: Event '{event_id}' missing from scenarios "
                f"{sorted(missing)} in probability_matrix. "
                "TFG verbatim: 'events within a scenario impact several measures wherever "
                "they are used, they have the same probability' — matrix must be complete."
            )

        if extra:
            errors.append(
                f"CONSISTENCY_ERROR: Event '{event_id}' has probability entries for "
                f"undeclared scenarios {sorted(extra)}. "
                "All matrix entries must correspond to declared scenarios."
            )

    # Check: all declared scenarios have the same set of events
    scenario_event_sets = {}
    for event_id, probs in matrix.items():
        if not isinstance(probs, dict):
            continue
        for scenario_name in probs.keys():
            if scenario_name not in scenario_event_sets:
                scenario_event_sets[scenario_name] = set()
            scenario_event_sets[scenario_name].add(event_id)

    if len(scenario_event_sets) >= 2:
        all_scenarios = list(scenario_event_sets.keys())
        ref_set = scenario_event_sets[all_scenarios[0]]
        for sc in all_scenarios[1:]:
            if scenario_event_sets[sc] != ref_set:
                diff = ref_set.symmetric_difference(scenario_event_sets[sc])
                errors.append(
                    f"CONSISTENCY_ERROR: Scenario '{sc}' has different event coverage "
                    f"from '{all_scenarios[0]}' — differing events: {sorted(diff)}. "
                    "TFG verbatim requires identical event sets across scenarios."
                )

    return errors


# ── 11. MC output validation ──────────────────────────────────────────────────

REQUIRED_MC_OUTPUT_KEYS = {"scenarios", "projections", "internal_consistency_audit"}


def validate_mc_output(output: Dict) -> Dict:
    """
    Validate the output of monte_carlo.py.
    Checks: structure, CI logical ordering (P10 ≤ median ≤ P90),
            scenario/measure completeness, internal consistency audit presence.
    """
    errors = []
    warnings = []

    for k in REQUIRED_MC_OUTPUT_KEYS:
        if k not in output:
            errors.append(f"MC_OUTPUT_MISSING: '{k}' absent in monte_carlo.py output")

    projections = output.get("projections", {})
    if not isinstance(projections, dict):
        errors.append("MC_OUTPUT_TYPE_ERROR: 'projections' must be a dict")
        return {"valid": False, "errors": errors, "warnings": warnings}

    for scenario_name, measures in projections.items():
        if not isinstance(measures, dict):
            errors.append(f"MC_OUTPUT_TYPE_ERROR: projections['{scenario_name}'] must be a dict")
            continue

        for measure_id, trajectory in measures.items():
            if not isinstance(trajectory, list):
                errors.append(
                    f"MC_OUTPUT_TYPE_ERROR: projections['{scenario_name}']['{measure_id}'] "
                    "must be a list of year entries"
                )
                continue

            for i, point in enumerate(trajectory):
                if not isinstance(point, dict):
                    errors.append(
                        f"MC_OUTPUT_TYPE_ERROR: projections['{scenario_name}']['{measure_id}']"
                        f"[{i}] must be a dict with keys: year, median, p10, p90"
                    )
                    continue

                for k in ("year", "median", "p10", "p90"):
                    if k not in point:
                        errors.append(
                            f"MC_OUTPUT_MISSING_FIELD: [{scenario_name}][{measure_id}][{i}] "
                            f"missing '{k}'"
                        )

                p10 = point.get("p10")
                median = point.get("median")
                p90 = point.get("p90")

                if all(isinstance(x, (int, float)) for x in [p10, median, p90]):
                    if not (p10 <= median <= p90):
                        errors.append(
                            f"CI_ORDER_ERROR: [{scenario_name}][{measure_id}][year={point.get('year')}] "
                            f"violates p10 ({p10}) ≤ median ({median}) ≤ p90 ({p90})"
                        )

    audit = output.get("internal_consistency_audit")
    if audit is None:
        errors.append(
            "MC_OUTPUT_MISSING: 'internal_consistency_audit' absent. "
            "TFG verbatim: 'events within a scenario impact several measures wherever "
            "they are used, they have the same probability'"
        )

    return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}


# ── 12. Main input validation orchestrator ────────────────────────────────────

def validate_projection_input(data: Dict) -> Dict:
    """Run all deterministic checks on the projection engine input JSON."""
    errors: List[str] = []
    warnings: List[str] = []

    # 1. Required sections
    errors.extend(check_required_input_sections(data))

    # 2. Time horizon logic
    errors.extend(check_time_horizon(data))

    # 3. Event-level checks
    events = data.get("events", [])
    measures = data.get("key_measures", [])
    known_measure_ids: Set[str] = set()
    if isinstance(measures, list):
        known_measure_ids = {m.get("id") for m in measures if isinstance(m, dict) and "id" in m}

    if isinstance(events, list):
        for e in events:
            if not isinstance(e, dict):
                continue

            # Impact mapping
            errors.extend(check_event_impact_mapping(e, known_measure_ids))

            # Impact direction
            direction_err = check_impact_direction(e)
            if direction_err:
                errors.append(direction_err)

            # Impact magnitude
            magnitude_err = check_impact_magnitude(e)
            if magnitude_err:
                if "WARN" in magnitude_err or "default" in magnitude_err.lower():
                    warnings.append(magnitude_err)
                else:
                    errors.append(magnitude_err)

            # TIA parameters
            warnings.extend(check_tia_params(e))

    # 4. Probability matrix checks
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

            valid_probs = {
                k: v for k, v in probs.items()
                if isinstance(v, (int, float)) and not isinstance(v, bool)
            }
            ok, msg = check_probability_variation(event_id, valid_probs)
            if not ok:
                warnings.append(msg)

        errors.extend(check_matrix_completeness(data))

    # 5. Internal consistency (TFG verbatim enforcement)
    errors.extend(check_internal_consistency(data))

    # 6. MC runs
    n_runs = data.get("monte_carlo_runs", 0)
    if isinstance(n_runs, int) and n_runs < 100:
        warnings.append(
            f"MC_RUNS_WARN: monte_carlo_runs={n_runs} < recommended 100. "
            "TFG Monte Carlo requires sufficient runs for stable CI."
        )

    return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}


# ── 13. Demo / self-test ──────────────────────────────────────────────────────

DEMO_VALID_INPUT = {
    "key_measures": [
        {"id": "KM01", "name": "GDP Growth Rate", "unit": "%/year", "current_value": 2.3,
         "historical_data": [{"year": 2005, "value": 3.1}, {"year": 2010, "value": 2.5},
                              {"year": 2015, "value": 2.9}, {"year": 2020, "value": -3.4},
                              {"year": 2025, "value": 2.3}]},
        {"id": "KM02", "name": "AI R&D Spend", "unit": "USD billion/year", "current_value": 150,
         "historical_data": [{"year": 2015, "value": 20}, {"year": 2020, "value": 60},
                              {"year": 2025, "value": 150}]},
        {"id": "KM03", "name": "Regulatory Stringency Index", "unit": "0-100 scale", "current_value": 35,
         "historical_data": [{"year": 2010, "value": 20}, {"year": 2015, "value": 25},
                              {"year": 2020, "value": 30}, {"year": 2025, "value": 35}]},
        {"id": "KM04", "name": "Tech Diffusion Rate", "unit": "% firms/year", "current_value": 12,
         "historical_data": [{"year": 2015, "value": 3}, {"year": 2020, "value": 7},
                              {"year": 2025, "value": 12}]},
        {"id": "KM05", "name": "Labor Displacement Rate", "unit": "% jobs/year", "current_value": 1.5,
         "historical_data": [{"year": 2015, "value": 0.5}, {"year": 2020, "value": 1.0},
                              {"year": 2025, "value": 1.5}]},
        {"id": "KM06", "name": "Global Trade Volume", "unit": "USD trillion", "current_value": 24,
         "historical_data": [{"year": 2005, "value": 12}, {"year": 2010, "value": 16},
                              {"year": 2015, "value": 19}, {"year": 2020, "value": 17},
                              {"year": 2025, "value": 24}]}
    ],
    "events": [
        {"id": "E01", "name": "AGI Announced by Major Lab", "impacts": ["KM01", "KM02", "KM04"],
         "impact_direction": "+", "impact_magnitude_pct": 20.0,
         "tia_params": {"time_to_first_impact": 1, "time_to_max_impact": 3,
                         "time_to_steady_state": 8, "steady_state_magnitude_pct": 10.0}},
        {"id": "E02", "name": "Global AI Regulation Treaty", "impacts": ["KM03", "KM04"],
         "impact_direction": "-", "impact_magnitude_pct": 15.0,
         "tia_params": {"time_to_first_impact": 1, "time_to_max_impact": 2,
                         "time_to_steady_state": 5, "steady_state_magnitude_pct": 8.0}},
        {"id": "E03", "name": "AI-Induced Financial Crash", "impacts": ["KM01", "KM06"],
         "impact_direction": "-", "impact_magnitude_pct": 25.0,
         "tia_params": {"time_to_first_impact": 0, "time_to_max_impact": 1,
                         "time_to_steady_state": 6, "steady_state_magnitude_pct": 5.0}},
        {"id": "E04", "name": "Energy Price Collapse", "impacts": ["KM01", "KM02"],
         "impact_direction": "+", "impact_magnitude_pct": 10.0,
         "tia_params": {"time_to_first_impact": 2, "time_to_max_impact": 5,
                         "time_to_steady_state": 12, "steady_state_magnitude_pct": 7.0}},
        {"id": "E05", "name": "Pandemic AI Response", "impacts": ["KM05", "KM04"],
         "impact_direction": "+", "impact_magnitude_pct": 12.0,
         "tia_params": {"time_to_first_impact": 0, "time_to_max_impact": 2,
                         "time_to_steady_state": 5, "steady_state_magnitude_pct": 6.0}},
        {"id": "E06", "name": "China AI Chip Breakthrough", "impacts": ["KM02", "KM06"],
         "impact_direction": "+/-", "impact_magnitude_pct": 18.0,
         "tia_params": {"time_to_first_impact": 1, "time_to_max_impact": 3,
                         "time_to_steady_state": 7, "steady_state_magnitude_pct": 9.0}},
        {"id": "E07", "name": "Mass AI Labor Protest", "impacts": ["KM03", "KM05"],
         "impact_direction": "-", "impact_magnitude_pct": 8.0,
         "tia_params": {"time_to_first_impact": 0, "time_to_max_impact": 1,
                         "time_to_steady_state": 4, "steady_state_magnitude_pct": 4.0}},
        {"id": "E08", "name": "Open Source AI Dominance", "impacts": ["KM04", "KM02"],
         "impact_direction": "+", "impact_magnitude_pct": 22.0,
         "tia_params": {"time_to_first_impact": 1, "time_to_max_impact": 4,
                         "time_to_steady_state": 9, "steady_state_magnitude_pct": 11.0}},
        {"id": "E09", "name": "AI Tax Legislation", "impacts": ["KM01", "KM03"],
         "impact_direction": "-", "impact_magnitude_pct": 6.0,
         "tia_params": {"time_to_first_impact": 1, "time_to_max_impact": 2,
                         "time_to_steady_state": 6, "steady_state_magnitude_pct": 3.0}},
        {"id": "E10", "name": "AI-Human Brain Interface", "impacts": ["KM04", "KM05"],
         "impact_direction": "+", "impact_magnitude_pct": 30.0,
         "tia_params": {"time_to_first_impact": 2, "time_to_max_impact": 6,
                         "time_to_steady_state": 15, "steady_state_magnitude_pct": 15.0}}
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
    },
    "scenarios": ["Scenario A", "Scenario B", "Scenario C", "Scenario D"],
    "time_horizon": {"start_year": 2026, "end_year": 2040},
    "monte_carlo_runs": 1000
}

DEMO_INVALID_INPUT = {
    "key_measures": [
        {"id": "KM01", "name": "GDP", "unit": "%", "current_value": 2.0}
    ],
    "events": [
        {"id": "E01", "name": "AGI", "impacts": [],
         "impact_direction": "up", "impact_magnitude_pct": -5},
        {"id": "E02", "name": "Crash", "impacts": ["KM99"],
         "impact_direction": "-", "impact_magnitude_pct": 10}
    ],
    "probability_matrix": {
        "E01": {"Scenario A": 1.5, "Scenario B": -0.1},
        "E03": {"Scenario A": 0.5, "Scenario B": 0.5}
    },
    "scenarios": ["Scenario A"],
    "time_horizon": {"start_year": 2040, "end_year": 2026},
    "monte_carlo_runs": 10
}


def run_demo():
    print("=== DEMO: Valid projection input (10 events, 6 measures, 4 scenarios) ===")
    r = validate_projection_input(DEMO_VALID_INPUT)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    print()
    print("=== DEMO: Invalid projection input (bad direction, magnitude, time horizon) ===")
    r2 = validate_projection_input(DEMO_INVALID_INPUT)
    print(json.dumps(r2, ensure_ascii=False, indent=2))


# ── 14. CLI entry point ───────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Deterministic validator for vision-foresight-scenarios-projection-engine"
    )
    parser.add_argument("--input", help="Path to projection input JSON file")
    parser.add_argument("--output", help="Path to monte_carlo.py output JSON (MC output validation)")
    parser.add_argument("--demo", action="store_true", help="Run self-test with demo data")
    args = parser.parse_args()

    if args.demo:
        run_demo()
        sys.exit(0)

    if args.input:
        with open(args.input, encoding="utf-8") as f:
            data = json.load(f)
        result = validate_projection_input(data)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if not result["valid"]:
            sys.exit(1)
        elif result["warnings"]:
            sys.exit(2)
        else:
            sys.exit(0)

    if args.output:
        with open(args.output, encoding="utf-8") as f:
            output = json.load(f)
        result = validate_mc_output(output)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if not result["valid"]:
            sys.exit(1)
        elif result["warnings"]:
            sys.exit(2)
        else:
            sys.exit(0)

    parser.print_help()
    sys.exit(2)
