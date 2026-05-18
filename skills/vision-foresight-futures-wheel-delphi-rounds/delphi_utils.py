#!/usr/bin/env python3
"""
Deterministic utility functions for vision-foresight-futures-wheel-delphi-rounds.
Replaces LLM reasoning for all computable steps to eliminate hallucination.

Glenn (2009) V3.0 Ch.6 §VI anchor: frequency-weighted oval mapping,
panel diversity scoring, rating aggregation, divergence flagging.
"""

from __future__ import annotations
import json
import math
import sys
from datetime import datetime, timezone
from typing import Any

# ─── 1. Frequency → Oval Size Mapping (Glenn Round 4/5) ──────────────────────
# Glenn: "the size of the oval around each primary impact could represent
# the frequency with which the panel identified it" (§VI Round 4)
OVAL_THRESHOLDS: list[tuple[float, str]] = [
    (0.90, "XL"),
    (0.70, "L"),
    (0.50, "M"),
    (0.30, "S"),
    (0.00, "XS"),
]


def frequency_to_oval(frequency: float) -> str:
    """Map panel agreement ratio (0.0–1.0) to oval size label. Deterministic."""
    if not 0.0 <= frequency <= 1.0:
        raise ValueError(f"frequency must be in [0, 1], got {frequency}")
    for threshold, label in OVAL_THRESHOLDS:
        if frequency >= threshold:
            return label
    return "XS"


# ─── 2. Impact Frequency Counter (Aggregator + Frequency Counter agents) ──────
def count_impact_frequencies(
    panel_responses: list[list[str]],
    panel_size: int,
) -> dict[str, dict]:
    """
    Count unique impact mentions per panelist and return sorted frequency dict.
    panel_responses: list of lists, each inner list is one panelist's impacts.
    Returns: {impact_label: {count, frequency, frequency_pct, oval_size}}
    """
    validate_panel_size(panel_size)
    counts: dict[str, int] = {}
    for panelist_impacts in panel_responses:
        seen: set[str] = set()
        for impact in panelist_impacts:
            key = impact.strip()
            if key and key not in seen:
                counts[key] = counts.get(key, 0) + 1
                seen.add(key)
    result: dict[str, dict] = {}
    for impact, count in sorted(counts.items(), key=lambda x: -x[1]):
        freq = count / panel_size
        result[impact] = {
            "count": count,
            "frequency": round(freq, 4),
            "frequency_pct": f"{freq * 100:.1f}%",
            "oval_size": frequency_to_oval(freq),
        }
    return result


# ─── 3. Panel Diversity Score ─────────────────────────────────────────────────
# Glenn: "An international panel could assemble asynchronously" — diversity is
# structurally required. Minimum thresholds per SKILL.md Phase 1 spec.
DIVERSITY_DIMENSIONS: dict[str, list[str]] = {
    "domain": [
        "Technologist", "Economist", "Sociologist", "Policy Maker",
        "Industry Practitioner", "Academia", "Civic Society",
    ],
    "geography": ["North America", "Europe", "East Asia", "Global South"],
    "perspective": ["Optimist", "Pessimist", "Pragmatist", "Critic"],
    "age_cohort": ["Boomer", "Gen X", "Millennial", "Gen Z"],
}

DIVERSITY_MINIMUMS: dict[str, int] = {
    "domain": 4,
    "geography": 3,
    "perspective": 3,
}


def calculate_panel_diversity_score(panelists: list[dict]) -> dict:
    """
    Score panel diversity 0–1 across 4 dimensions. Returns per-dimension detail.
    panelists: list of {domain, geography, perspective, age_cohort}
    """
    if not panelists:
        return {
            "score": 0.0,
            "dimensions": {},
            "minimums_met": False,
            "minimums_required": DIVERSITY_MINIMUMS,
        }
    dimension_scores: dict[str, dict] = {}
    for dim, all_values in DIVERSITY_DIMENSIONS.items():
        present: set[str] = set()
        for p in panelists:
            val = p.get(dim, "")
            if val in all_values:
                present.add(val)
        coverage = len(present) / len(all_values)
        dimension_scores[dim] = {
            "unique_values": sorted(present),
            "count": len(present),
            "max": len(all_values),
            "coverage": round(coverage, 4),
        }
    overall = sum(d["coverage"] for d in dimension_scores.values()) / len(dimension_scores)
    minimums_met = all(
        dimension_scores.get(dim, {}).get("count", 0) >= min_count
        for dim, min_count in DIVERSITY_MINIMUMS.items()
    )
    return {
        "score": round(overall, 4),
        "dimensions": dimension_scores,
        "minimums_met": minimums_met,
        "minimums_required": DIVERSITY_MINIMUMS,
    }


# ─── 4. Rating Aggregation (mean + std dev + ranking) ────────────────────────
def aggregate_ratings(ratings_by_item: dict[str, list[float]]) -> list[dict]:
    """
    Compute mean, std dev, and composite score per rated item.
    composite_score = mean (used for ranking); std dev for divergence flag.
    Returns list sorted by mean descending.
    """
    results: list[dict] = []
    for item, scores in ratings_by_item.items():
        n = len(scores)
        if n == 0:
            continue
        mean = sum(scores) / n
        variance = sum((s - mean) ** 2 for s in scores) / n if n > 1 else 0.0
        std = math.sqrt(variance)
        results.append({
            "item": item,
            "mean": round(mean, 4),
            "std_dev": round(std, 4),
            "n": n,
            "divergence_flag": _classify_divergence(std),
        })
    return sorted(results, key=lambda x: -x["mean"])


def aggregate_composite_ratings(
    ratings_by_item: dict[str, dict[str, list[float]]],
) -> list[dict]:
    """
    Aggregate multi-dimension ratings (importance, impact, certainty).
    Returns items ranked by composite mean = avg(importance, impact, certainty).
    ratings_by_item: {item: {importance: [...], impact: [...], certainty: [...]}}
    """
    results: list[dict] = []
    for item, dims in ratings_by_item.items():
        dim_means: dict[str, float] = {}
        for dim, scores in dims.items():
            n = len(scores)
            if n == 0:
                dim_means[dim] = 0.0
                continue
            dim_means[dim] = sum(scores) / n
        composite = sum(dim_means.values()) / len(dim_means) if dim_means else 0.0
        all_scores = [s for scores in dims.values() for s in scores]
        mean_all = sum(all_scores) / len(all_scores) if all_scores else 0.0
        variance = sum((s - mean_all) ** 2 for s in all_scores) / len(all_scores) if all_scores else 0.0
        std = math.sqrt(variance)
        top_flag = composite >= 4.0
        results.append({
            "item": item,
            "composite_mean": round(composite, 4),
            "dim_means": {k: round(v, 4) for k, v in dim_means.items()},
            "std_dev_pooled": round(std, 4),
            "divergence_flag": _classify_divergence(std),
            "top_candidate": top_flag,
        })
    return sorted(results, key=lambda x: -x["composite_mean"])


def _classify_divergence(std: float) -> str:
    """Classify divergence by std deviation threshold."""
    if std < 0.6:
        return "✓ consensus"
    elif std < 1.2:
        return "⚠️ moderate divergence"
    else:
        return "🚨 high divergence"


# ─── 5. Panel Size Validator ──────────────────────────────────────────────────
def validate_panel_size(n: int) -> None:
    """Enforce Glenn 5–30 panel size constraint. Raises ValueError if violated."""
    if not isinstance(n, int) or not 5 <= n <= 30:
        raise ValueError(
            f"panel_size must be integer 5–30 per Glenn (2009) §VI spec, got {n!r}"
        )


# ─── 6. Frequency Threshold Validator ────────────────────────────────────────
def validate_frequency_thresholds(thresholds: dict) -> None:
    """Ensure XL > L > M > S > XS=0 (strictly decreasing)."""
    required = ["XL", "L", "M", "S"]
    for key in required:
        if key not in thresholds:
            raise ValueError(f"Missing frequency threshold key: {key}")
    vals = [thresholds["XL"], thresholds["L"], thresholds["M"], thresholds["S"]]
    if not all(vals[i] > vals[i + 1] for i in range(len(vals) - 1)):
        raise ValueError(f"Thresholds must be strictly decreasing XL>L>M>S, got {thresholds}")
    if not all(0.0 <= v <= 1.0 for v in vals):
        raise ValueError("All threshold values must be in [0, 1]")


# ─── 7. Current UTC Timestamp (for Wiki) ─────────────────────────────────────
def now_utc_str() -> str:
    """Return current UTC datetime as 'YYYY-MM-DD HH:MM UTC'."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


# ─── 8. Minority Opinion Extractor ───────────────────────────────────────────
def extract_minority_opinions(
    aggregated: list[dict],
    divergence_threshold: str = "🚨 high divergence",
) -> list[dict]:
    """Extract items whose divergence_flag matches threshold for minority archive."""
    return [item for item in aggregated if item.get("divergence_flag") == divergence_threshold]


# ─── CLI Entrypoint ───────────────────────────────────────────────────────────
USAGE = """
delphi_utils.py — deterministic Delphi wheel computations

Commands:
  frequency_to_oval <ratio>
      Map 0.0–1.0 frequency ratio → oval size label (XL/L/M/S/XS)

  count_frequencies '<json_list_of_lists>' <panel_size>
      Count impact mentions across panelists

  diversity_score '<json_list_of_panelists>'
      Score panel diversity 0–1 across 4 dimensions

  aggregate_ratings '<json_dict_item_to_scores>'
      Mean+stddev+ranking for single-dimension ratings

  aggregate_composite '<json_dict_item_to_dim_scores>'
      Composite ranking for multi-dimension ratings (importance/impact/certainty)

  validate_panel_size <n>
      Check n is in [5, 30]

  now_utc
      Print current UTC datetime string for Wiki timestamps
"""

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"

    try:
        if cmd == "frequency_to_oval":
            freq = float(sys.argv[2])
            print(json.dumps({"frequency": freq, "oval_size": frequency_to_oval(freq)}))

        elif cmd == "count_frequencies":
            data = json.loads(sys.argv[2])
            panel_size = int(sys.argv[3])
            print(json.dumps(count_impact_frequencies(data, panel_size), indent=2))

        elif cmd == "diversity_score":
            panelists = json.loads(sys.argv[2])
            print(json.dumps(calculate_panel_diversity_score(panelists), indent=2))

        elif cmd == "aggregate_ratings":
            data = json.loads(sys.argv[2])
            print(json.dumps(aggregate_ratings(data), indent=2))

        elif cmd == "aggregate_composite":
            data = json.loads(sys.argv[2])
            print(json.dumps(aggregate_composite_ratings(data), indent=2))

        elif cmd == "validate_panel_size":
            n = int(sys.argv[2])
            validate_panel_size(n)
            print(json.dumps({"valid": True, "panel_size": n}))

        elif cmd == "now_utc":
            print(now_utc_str())

        else:
            print(USAGE)

    except (ValueError, IndexError) as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)
