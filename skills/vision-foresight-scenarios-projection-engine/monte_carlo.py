#!/usr/bin/env python3
"""
vision-foresight-scenarios-projection-engine — Monte Carlo Engine
결정론적 Monte Carlo 시뮬레이션 엔진.

TFG V3.0 Ch19 Section III verbatim:
  "The historical data for each of the measures is projected using time-series methods.
   The events, expressed probabilistically, are combined with the extrapolation using
   Monte Carlo methods to produce a new median forecast and a range of uncertainty.
   Since events within a scenario impact several measures wherever they are used,
   they have the same probability; thus, internal consistency is promoted."

TIA V3.0 Ch08 verbatim:
  "TIA is a simple approach to forecasting in which a time series is modified to take
   into account perceptions about how future events may change extrapolations that
   would otherwise be surprise-free."

Usage:
  python3 monte_carlo.py --input projection_input.json
  python3 monte_carlo.py --input projection_input.json --output results.json
  python3 monte_carlo.py --demo
  python3 monte_carlo.py --table results.json

Exit codes: 0=success, 1=error
"""

import json
import sys
import argparse
import random
import math
from typing import Dict, List, Optional, Tuple, Any


# ── 1. Baseline curve fitting ─────────────────────────────────────────────────

def fit_linear(years: List[float], values: List[float]) -> Tuple[float, float, float]:
    """
    Linear regression: v = slope * year + intercept
    Returns (slope, intercept, r_squared).
    TIA V3.0 Ch08: "Linear v = m·t + b"
    """
    n = len(years)
    if n < 2:
        v0 = values[0] if values else 0.0
        return 0.0, v0, 0.0

    mean_y = sum(years) / n
    mean_v = sum(values) / n

    ss_xy = sum((y - mean_y) * (v - mean_v) for y, v in zip(years, values))
    ss_xx = sum((y - mean_y) ** 2 for y in years)

    if ss_xx == 0:
        return 0.0, mean_v, 0.0

    slope = ss_xy / ss_xx
    intercept = mean_v - slope * mean_y

    # R²
    ss_res = sum((v - (slope * y + intercept)) ** 2 for y, v in zip(years, values))
    ss_tot = sum((v - mean_v) ** 2 for v in values)
    r_sq = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0

    return slope, intercept, r_sq


def fit_polynomial2(years: List[float], values: List[float]) -> Tuple[Tuple, float]:
    """
    Quadratic fit: v = a*t² + b*t + c using normal equations.
    Returns ((a, b, c), r_squared).
    TIA V3.0 Ch08: "Power ln(v) = m·ln(t) + b" — approximated as quadratic for stability.
    """
    n = len(years)
    if n < 3:
        # Fall back to linear
        slope, intercept, r_sq = fit_linear(years, values)
        return (0.0, slope, intercept), r_sq

    # Normalize years for numerical stability
    y0 = years[0]
    ts = [y - y0 for y in years]

    # Normal equations for [a, b, c] in v = a*t² + b*t + c
    # Design matrix columns: t², t, 1
    def dot(u, v):
        return sum(ui * vi for ui, vi in zip(u, v))

    t2 = [t ** 2 for t in ts]
    t3 = [t ** 3 for t in ts]
    t4 = [t ** 4 for t in ts]

    # 3×3 normal equation matrix
    A = [
        [dot(t4, [1] * n), dot(t3, [1] * n), dot(t2, [1] * n)],
        [dot(t3, [1] * n), dot(t2, [1] * n), sum(ts)],
        [dot(t2, [1] * n), sum(ts), n]
    ]
    b_vec = [dot(t2, values), dot(ts, values), sum(values)]

    # Solve 3×3 via Gaussian elimination
    def gauss_solve(A, b):
        n = len(b)
        aug = [A[i][:] + [b[i]] for i in range(n)]
        for col in range(n):
            pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
            aug[col], aug[pivot] = aug[pivot], aug[col]
            if abs(aug[col][col]) < 1e-12:
                return None
            for row in range(col + 1, n):
                factor = aug[row][col] / aug[col][col]
                for k in range(col, n + 1):
                    aug[row][k] -= factor * aug[col][k]
        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            x[i] = aug[i][n]
            for j in range(i + 1, n):
                x[i] -= aug[i][j] * x[j]
            x[i] /= aug[i][i]
        return x

    coeffs = gauss_solve(A, b_vec)
    if coeffs is None:
        slope, intercept, r_sq = fit_linear(years, values)
        return (0.0, slope, intercept), r_sq

    a, b_coef, c = coeffs

    # Compute R² (using denormalized year)
    preds = [a * t ** 2 + b_coef * t + c for t in ts]
    mean_v = sum(values) / n
    ss_res = sum((v - p) ** 2 for v, p in zip(values, preds))
    ss_tot = sum((v - mean_v) ** 2 for v in values)
    r_sq = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0

    # Return coefficients adjusted for original year scale
    # v = a*(year-y0)² + b*(year-y0) + c
    # Store as (a, b, c, y0) for evaluation
    return (a, b_coef, c, y0), r_sq


def fit_exponential(years: List[float], values: List[float]) -> Tuple[float, float, float]:
    """
    Exponential fit: ln(v) = m*t + b → v = exp(b) * exp(m*t)
    TIA V3.0 Ch08: "Exponential ln(v) = m·t + b"
    Only works for positive values.
    """
    if any(v <= 0 for v in values):
        return 0.0, 0.0, -1.0  # R²=-1 signals invalid fit

    log_values = [math.log(v) for v in values]
    slope, intercept, r_sq = fit_linear(years, log_values)
    return slope, math.exp(intercept), r_sq


def select_best_baseline(
    years: List[float], values: List[float]
) -> Tuple[str, Any]:
    """
    Fit linear, polynomial, and exponential; return best by R².
    TIA V3.0 Ch08: "7 curve types tried, best R² selected."
    Returns (method_name, params).
    """
    if len(years) < 2:
        v0 = values[0] if values else 0.0
        return "constant", {"value": v0, "r_squared": 0.0}

    candidates = {}

    # Linear
    slope, intercept, r_sq = fit_linear(years, values)
    candidates["linear"] = {"slope": slope, "intercept": intercept, "r_squared": r_sq}

    # Polynomial (only with ≥3 points)
    if len(years) >= 3:
        poly_coeffs, r_sq_poly = fit_polynomial2(years, values)
        candidates["polynomial2"] = {"coeffs": poly_coeffs, "r_squared": r_sq_poly}

    # Exponential (only for positive values)
    if all(v > 0 for v in values):
        exp_m, exp_a, r_sq_exp = fit_exponential(years, values)
        if r_sq_exp >= 0:
            candidates["exponential"] = {
                "m": exp_m, "a": exp_a, "r_squared": r_sq_exp
            }

    best_method = max(candidates, key=lambda k: candidates[k]["r_squared"])
    best_params = candidates[best_method]
    best_params["all_candidates"] = {
        k: round(v["r_squared"], 4) for k, v in candidates.items()
    }
    return best_method, best_params


def baseline_predict(method: str, params: Dict, year: float, base_year: float) -> float:
    """
    Predict baseline value for a given year using fitted parameters.
    If 'anchor_offset' is present in params, it is added to correct start-year anchoring.
    """
    if method == "constant":
        raw = params["value"]
    elif method == "linear":
        raw = params["slope"] * year + params["intercept"]
    elif method == "polynomial2":
        coeffs = params["coeffs"]
        if len(coeffs) == 4:
            a, b, c, y0 = coeffs
            t = year - y0
            raw = a * t ** 2 + b * t + c
        else:
            a, b, c = coeffs
            raw = a * year ** 2 + b * year + c
    elif method == "exponential":
        raw = params["a"] * math.exp(params["m"] * (year - base_year))
    else:
        raw = params.get("value", 0.0)

    return raw + params.get("anchor_offset", 0.0)


# ── 2. TIA event impact curve ─────────────────────────────────────────────────

def compute_event_impact_fraction(
    event: Dict, event_occurrence_year: int, target_year: int
) -> float:
    """
    TIA V3.0 Ch08 impact curve: 0 → M_L at T_M → M_S at T_S.
    Returns fractional change to apply to baseline (positive or negative).

    Parameters:
      T_F: time_to_first_impact (years after event_occurrence_year)
      T_M: time_to_max_impact
      T_S: time_to_steady_state
      M_L: impact_magnitude_pct / 100 (largest magnitude, fraction)
      M_S: steady_state_magnitude_pct / 100
    """
    if target_year < event_occurrence_year:
        return 0.0

    tia = event.get("tia_params", {})
    t_f = float(tia.get("time_to_first_impact", 1))
    t_m = float(tia.get("time_to_max_impact", 3))
    t_s = float(tia.get("time_to_steady_state", 10))

    m_l = float(event.get("impact_magnitude_pct", 10.0)) / 100.0
    m_s_pct = tia.get("steady_state_magnitude_pct", event.get("impact_magnitude_pct", 10.0) * 0.5)
    m_s = float(m_s_pct) / 100.0

    dt = float(target_year - event_occurrence_year)

    if dt < t_f:
        return 0.0
    elif t_m <= t_f:
        # Degenerate: first impact = max impact
        if dt >= t_s:
            return m_s
        elif dt >= t_m:
            frac = (dt - t_m) / max(t_s - t_m, 0.001)
            return m_l + (m_s - m_l) * frac
        else:
            return m_l
    elif dt < t_m:
        frac = (dt - t_f) / max(t_m - t_f, 0.001)
        return m_l * frac
    elif t_s <= t_m:
        return m_s
    elif dt < t_s:
        frac = (dt - t_m) / max(t_s - t_m, 0.001)
        return m_l + (m_s - m_l) * frac
    else:
        return m_s


def stable_char_hash(s: str) -> int:
    """
    Deterministic hash using sum of character codes (stable across Python sessions).
    Python's built-in hash() for strings is randomized (PYTHONHASHSEED) in Python 3.3+
    and cannot be used for reproducible determinism.
    """
    return sum(ord(c) for c in s) % 2


def apply_direction(base_fraction: float, event: Dict, scenario_name: str) -> float:
    """
    Apply impact_direction to the magnitude fraction.
    "+/-" uses a stable character-sum hash for consistent direction within scenario.
    This is deterministic across Python sessions (no PYTHONHASHSEED dependency).
    """
    direction = event.get("impact_direction", "+")
    if direction == "+":
        return base_fraction
    elif direction == "-":
        return -base_fraction
    elif direction == "+/-":
        # Deterministic sign: same scenario+event always gets same direction
        # Satisfies TFG internal consistency: same P(E|S) used for all measures
        sign = stable_char_hash(scenario_name + event.get("id", ""))
        return base_fraction if sign == 0 else -base_fraction
    return base_fraction


# ── 3. Single Monte Carlo run ─────────────────────────────────────────────────

def run_single_trial(
    events: List[Dict],
    probability_matrix: Dict[str, Dict[str, float]],
    scenario_name: str,
    measures: List[Dict],
    baseline_fits: Dict[str, Tuple[str, Dict]],
    years: List[int],
    rng: random.Random
) -> Dict[str, List[float]]:
    """
    One Monte Carlo trial for one scenario.
    TFG verbatim: "Since events within a scenario impact several measures wherever
    they are used, they have the same probability; thus, internal consistency is promoted."

    Internal consistency enforcement:
      - All events are sampled ONCE per trial
      - The same event occurrence decision is applied to ALL measures it impacts
      - This is the structural guarantee of internal consistency
    """
    # Step 1: Sample event occurrences for this trial (once per event, once per year)
    # An event can occur at most once, at the first year it's sampled as "occurring"
    event_occurrence_years: Dict[str, Optional[int]] = {}
    for event in events:
        eid = event["id"]
        p_scenario = probability_matrix.get(eid, {}).get(scenario_name, 0.0)
        # Sample: does this event occur in the projection window?
        # Model: event occurs in some year with annual probability p_scenario.
        # First year it occurs (geometric distribution).
        occurred = False
        for yr in years:
            if rng.random() < p_scenario:
                event_occurrence_years[eid] = yr
                occurred = True
                break
        if not occurred:
            event_occurrence_years[eid] = None

    # Step 2: For each measure, compute adjusted trajectory
    trajectories: Dict[str, List[float]] = {}

    for measure in measures:
        km_id = measure["id"]
        method, params = baseline_fits.get(km_id, ("constant", {"value": 0.0}))
        base_year = years[0] if years else 2026

        traj = []
        for yr in years:
            # Baseline prediction
            baseline = baseline_predict(method, params, float(yr), float(base_year))

            # Accumulate event impacts (TIA impact curve per event)
            cumulative_impact = 0.0
            for event in events:
                eid = event["id"]
                if km_id not in event.get("impacts", []):
                    continue
                occ_year = event_occurrence_years.get(eid)
                if occ_year is None:
                    continue

                frac = compute_event_impact_fraction(event, occ_year, yr)
                directed_frac = apply_direction(frac, event, scenario_name)
                cumulative_impact += directed_frac

            # Adjusted value: baseline × (1 + cumulative_impact)
            adjusted = baseline * (1.0 + cumulative_impact)
            traj.append(adjusted)

        trajectories[km_id] = traj

    return trajectories


# ── 4. Aggregate Monte Carlo runs ─────────────────────────────────────────────

def percentile(sorted_values: List[float], pct: float) -> float:
    """
    Compute percentile using linear interpolation (same as numpy.percentile default).
    """
    n = len(sorted_values)
    if n == 0:
        return 0.0
    if n == 1:
        return sorted_values[0]

    idx = (pct / 100.0) * (n - 1)
    lo = int(idx)
    hi = lo + 1
    frac = idx - lo

    if hi >= n:
        return sorted_values[-1]
    return sorted_values[lo] + frac * (sorted_values[hi] - sorted_values[lo])


def aggregate_trials(trials: List[Dict[str, List[float]]], years: List[int]) -> Dict:
    """
    Aggregate N Monte Carlo trials into median + P10 + P90 per year per measure.
    TFG verbatim: "produce a new median forecast and a range of uncertainty."
    CI: P10–P90 (80% interval) + P5–P95 (90% interval).
    """
    if not trials:
        return {}

    measure_ids = list(trials[0].keys())
    result = {}

    for km_id in measure_ids:
        year_points = []
        for i, yr in enumerate(years):
            values_at_year = sorted([trial[km_id][i] for trial in trials if km_id in trial])
            med = percentile(values_at_year, 50)
            p10 = percentile(values_at_year, 10)
            p90 = percentile(values_at_year, 90)
            p5 = percentile(values_at_year, 5)
            p95 = percentile(values_at_year, 95)
            year_points.append({
                "year": yr,
                "median": round(med, 4),
                "p10": round(p10, 4),
                "p90": round(p90, 4),
                "p5": round(p5, 4),
                "p95": round(p95, 4)
            })
        result[km_id] = year_points

    return result


# ── 5. Fit baselines for all measures ────────────────────────────────────────

def fit_all_baselines(key_measures: List[Dict], start_year: int) -> Dict:
    """
    Fit best baseline curve for each key measure.
    Uses historical_data if provided, else uses current_value (constant).

    Anchoring rule (TIA best practice):
      After selecting best fit, compute predicted value at start_year.
      If |predicted - current_value| / |current_value| > 0.20 (20% deviation)
      AND R² < 0.80 (poor fit quality):
        → apply anchor_offset = current_value - predicted_at_start
        → this shifts the entire projection curve to start at current_value
        → the growth RATE is still from the historical fit (not zeroed)
      This prevents poor polynomial fits (e.g., COVID-distorted GDP data)
      from projecting wildly unrealistic start values.
    """
    fits = {}
    fit_reports = {}

    for measure in key_measures:
        km_id = measure["id"]
        current_value = float(measure.get("current_value", 0.0))
        historical = measure.get("historical_data", [])

        if historical and len(historical) >= 2:
            hist_years = [float(d["year"]) for d in historical]
            hist_values = [float(d["value"]) for d in historical]
            method, params = select_best_baseline(hist_years, hist_values)
        else:
            method = "constant"
            params = {"value": current_value, "r_squared": 0.0, "all_candidates": {}}

        # Anchor check
        anchor_offset = 0.0
        anchored = False
        r_sq = params.get("r_squared", 0.0)
        if method != "constant":
            predicted_at_start = baseline_predict(method, params, float(start_year), float(start_year))
            if abs(current_value) > 1e-9:
                rel_dev = abs(predicted_at_start - current_value) / abs(current_value)
            else:
                rel_dev = abs(predicted_at_start - current_value)
            if rel_dev > 0.20 and r_sq < 0.80:
                anchor_offset = current_value - predicted_at_start
                params["anchor_offset"] = anchor_offset
                anchored = True

        fits[km_id] = (method, params)
        fit_reports[km_id] = {
            "method": method,
            "r_squared": round(r_sq, 4),
            "data_points": len(historical),
            "anchored": anchored,
            "anchor_offset": round(anchor_offset, 6) if anchored else 0.0,
            "note": (
                f"anchored at current_value={current_value} (fit deviation >{20}%, R²<0.80)"
                if anchored
                else "historical data provided" if historical
                else "no historical data — constant baseline at current_value"
            )
        }

    return fits, fit_reports


# ── 6. Internal consistency audit ────────────────────────────────────────────

def audit_internal_consistency(
    events: List[Dict],
    probability_matrix: Dict,
    scenarios: List[str]
) -> Dict:
    """
    TFG V3.0 Ch19 Section III verbatim:
    'events within a scenario impact several measures wherever they are used,
     they have the same probability; thus, internal consistency is promoted.'

    Verification:
    For each event E that impacts multiple measures within the same scenario:
      P(E|scenario) is structurally IDENTICAL for all measures (single matrix entry).
    This audit reports events impacting multiple measures and confirms consistency.
    """
    multi_impact_events = [
        e for e in events if len(e.get("impacts", [])) > 1
    ]

    audit_rows = []
    all_consistent = True

    for event in multi_impact_events:
        eid = event["id"]
        ename = event["name"]
        impacted_measures = event.get("impacts", [])

        for scenario in scenarios:
            p = probability_matrix.get(eid, {}).get(scenario)
            consistent = (p is not None)
            if not consistent:
                all_consistent = False
            audit_rows.append({
                "event_id": eid,
                "event_name": ename,
                "scenario": scenario,
                "impacted_measures": impacted_measures,
                "probability_used": p,
                "consistent": consistent,
                "note": (
                    "CONSISTENT — single P(E|S) applied uniformly to all measures" if consistent
                    else "INCONSISTENT — probability missing from matrix"
                )
            })

    return {
        "overall_consistent": all_consistent,
        "multi_impact_events_checked": len(multi_impact_events),
        "tfg_verbatim": (
            "'events within a scenario impact several measures wherever they are used, "
            "they have the same probability; thus, internal consistency is promoted.'"
        ),
        "mechanism": (
            "Structural guarantee: the probability matrix stores exactly ONE P(E|S) per "
            "event-scenario pair. Monte Carlo samples each event ONCE per trial and applies "
            "the same occurrence decision to all measures it impacts."
        ),
        "audit_rows": audit_rows
    }


# ── 7. ASCII table formatter ──────────────────────────────────────────────────

def format_ascii_table(
    result: Dict, measures: List[Dict], scenarios: List[str], sample_years: List[int]
) -> str:
    """
    Format projection results as an ASCII table for LLM output.
    Shows median (P10–P90) per measure × scenario × selected years.
    """
    lines = []
    measure_map = {m["id"]: m["name"] for m in measures}

    for km_id in [m["id"] for m in measures]:
        km_name = measure_map.get(km_id, km_id)
        lines.append(f"\n### {km_id}: {km_name}")
        lines.append(f"{'Year':<8} " + " ".join(f"{s[:15]:<25}" for s in scenarios))
        lines.append("-" * (8 + 26 * len(scenarios)))

        for yr in sample_years:
            row = f"{yr:<8} "
            for sc in scenarios:
                traj = result.get("projections", {}).get(sc, {}).get(km_id, [])
                point = next((p for p in traj if p["year"] == yr), None)
                if point:
                    cell = f"{point['median']:.2f} ({point['p10']:.1f}–{point['p90']:.1f})"
                else:
                    cell = "N/A"
                row += f"{cell:<25} "
            lines.append(row)

    return "\n".join(lines)


# ── 8. Main Monte Carlo orchestrator ─────────────────────────────────────────

def run_projection(data: Dict, seed: int = 42) -> Dict:
    """
    Full Monte Carlo projection pipeline.
    """
    key_measures = data["key_measures"]
    events = data["events"]
    probability_matrix = data["probability_matrix"]
    scenarios = data["scenarios"]
    th = data["time_horizon"]
    start_year = th["start_year"]
    end_year = th["end_year"]
    n_runs = data.get("monte_carlo_runs", 1000)

    years = list(range(start_year, end_year + 1))

    # Step 1: Fit baselines
    baseline_fits, fit_reports = fit_all_baselines(key_measures, start_year)

    # Step 2: Monte Carlo per scenario
    projections = {}
    scenario_run_summaries = {}

    rng = random.Random(seed)

    for scenario in scenarios:
        trials = []
        for _ in range(n_runs):
            trial = run_single_trial(
                events, probability_matrix, scenario,
                key_measures, baseline_fits, years, rng
            )
            trials.append(trial)

        agg = aggregate_trials(trials, years)
        projections[scenario] = agg
        scenario_run_summaries[scenario] = {
            "n_runs_completed": n_runs,
            "years_projected": len(years),
            "measures_projected": len(key_measures)
        }

    # Step 3: Internal consistency audit
    ica = audit_internal_consistency(events, probability_matrix, scenarios)

    return {
        "scenarios": scenarios,
        "meta": {
            "method": "TIA-integrated Monte Carlo",
            "n_runs": n_runs,
            "start_year": start_year,
            "end_year": end_year,
            "scenarios": scenarios,
            "ci_definition": "P10–P90 (80% interval), P5–P95 (90% interval)",
            "random_seed": seed,
            "tfg_reference": "TFG V3.0 Ch19 Section III + TIA Ch08",
            "cross_skill": "foresight-trend-impact-analysis"
        },
        "baseline_fit_report": fit_reports,
        "scenario_run_summaries": scenario_run_summaries,
        "projections": projections,
        "internal_consistency_audit": ica
    }


# ── 9. Demo / self-test ───────────────────────────────────────────────────────

DEMO_INPUT = {
    "key_measures": [
        {
            "id": "KM01", "name": "GDP Growth Rate", "unit": "%/year",
            "current_value": 2.3,
            "historical_data": [
                {"year": 2005, "value": 3.1}, {"year": 2010, "value": 2.5},
                {"year": 2015, "value": 2.9}, {"year": 2020, "value": -3.4},
                {"year": 2025, "value": 2.3}
            ]
        },
        {
            "id": "KM02", "name": "AI R&D Spend (USD bn)", "unit": "USD billion/year",
            "current_value": 150,
            "historical_data": [
                {"year": 2015, "value": 20}, {"year": 2020, "value": 60},
                {"year": 2023, "value": 110}, {"year": 2025, "value": 150}
            ]
        },
        {
            "id": "KM03", "name": "Regulatory Stringency Index", "unit": "0-100 scale",
            "current_value": 35,
            "historical_data": [
                {"year": 2010, "value": 20}, {"year": 2015, "value": 25},
                {"year": 2020, "value": 30}, {"year": 2025, "value": 35}
            ]
        }
    ],
    "events": [
        {
            "id": "E01", "name": "AGI Announced", "impacts": ["KM01", "KM02"],
            "impact_direction": "+", "impact_magnitude_pct": 20.0,
            "tia_params": {
                "time_to_first_impact": 1, "time_to_max_impact": 3,
                "time_to_steady_state": 8, "steady_state_magnitude_pct": 10.0
            }
        },
        {
            "id": "E02", "name": "Global AI Regulation Treaty", "impacts": ["KM03"],
            "impact_direction": "-", "impact_magnitude_pct": 15.0,
            "tia_params": {
                "time_to_first_impact": 1, "time_to_max_impact": 2,
                "time_to_steady_state": 5, "steady_state_magnitude_pct": 8.0
            }
        },
        {
            "id": "E03", "name": "AI Financial Crash", "impacts": ["KM01"],
            "impact_direction": "-", "impact_magnitude_pct": 25.0,
            "tia_params": {
                "time_to_first_impact": 0, "time_to_max_impact": 1,
                "time_to_steady_state": 5, "steady_state_magnitude_pct": 5.0
            }
        }
    ],
    "probability_matrix": {
        "E01": {"Optimist": 0.8, "Baseline": 0.5, "Pessimist": 0.2},
        "E02": {"Optimist": 0.1, "Baseline": 0.4, "Pessimist": 0.8},
        "E03": {"Optimist": 0.05, "Baseline": 0.2, "Pessimist": 0.6}
    },
    "scenarios": ["Optimist", "Baseline", "Pessimist"],
    "time_horizon": {"start_year": 2026, "end_year": 2040},
    "monte_carlo_runs": 200
}


def run_demo():
    print("=== vision-foresight-scenarios-projection-engine — Monte Carlo Demo ===")
    print(f"Scenarios: {DEMO_INPUT['scenarios']}")
    print(f"Measures: {[m['id'] for m in DEMO_INPUT['key_measures']]}")
    print(f"Events: {[e['id'] for e in DEMO_INPUT['events']]}")
    print(f"MC runs: {DEMO_INPUT['monte_carlo_runs']}")
    print()

    result = run_projection(DEMO_INPUT, seed=42)

    # Print baseline fits
    print("=== Baseline Fit Report ===")
    for km_id, report in result["baseline_fit_report"].items():
        print(f"  {km_id}: {report['method']} (R²={report['r_squared']}, n={report['data_points']})")
    print()

    # Print sample projections (every 5 years)
    sample_years = [2026, 2030, 2035, 2040]
    print("=== Projection Results (median, P10–P90) ===")
    measures = DEMO_INPUT["key_measures"]
    scenarios = DEMO_INPUT["scenarios"]

    for m in measures:
        km_id = m["id"]
        print(f"\n{km_id}: {m['name']} ({m['unit']})")
        header = f"{'Year':<6} " + " ".join(f"{s:<30}" for s in scenarios)
        print(header)
        print("-" * (6 + 31 * len(scenarios)))
        for yr in sample_years:
            row = f"{yr:<6} "
            for sc in scenarios:
                traj = result["projections"].get(sc, {}).get(km_id, [])
                pt = next((p for p in traj if p["year"] == yr), None)
                if pt:
                    row += f"{pt['median']:.2f} ({pt['p10']:.1f}–{pt['p90']:.1f})     "
                else:
                    row += "N/A                           "
            print(row)

    # Print internal consistency audit summary
    ica = result["internal_consistency_audit"]
    print(f"\n=== Internal Consistency Audit ===")
    print(f"Overall consistent: {ica['overall_consistent']}")
    print(f"Multi-impact events checked: {ica['multi_impact_events_checked']}")
    print(f"Mechanism: {ica['mechanism']}")

    return result


# ── 10. CLI entry point ───────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Monte Carlo projection engine for vision-foresight-scenarios-projection-engine"
    )
    parser.add_argument("--input", help="Path to projection input JSON file")
    parser.add_argument("--output", help="Path to write results JSON (optional)")
    parser.add_argument("--table", help="Path to existing results JSON to render as ASCII table")
    parser.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")
    parser.add_argument("--demo", action="store_true", help="Run demo with built-in sample data")
    args = parser.parse_args()

    if args.demo:
        result = run_demo()
        sys.exit(0)

    if args.table:
        with open(args.table, encoding="utf-8") as f:
            result = json.load(f)
        input_path = args.table.replace("_results.json", "_input.json").replace(".json", "_input.json")
        # Minimal rendering from results only
        print(json.dumps(result["baseline_fit_report"], ensure_ascii=False, indent=2))
        sys.exit(0)

    if not args.input:
        parser.print_help()
        sys.exit(2)

    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)

    result = run_projection(data, seed=args.seed)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Results written to {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

    sys.exit(0)
