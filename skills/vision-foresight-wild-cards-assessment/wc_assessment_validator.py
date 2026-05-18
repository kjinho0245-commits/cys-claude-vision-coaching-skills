#!/usr/bin/env python3
"""
wc_assessment_validator.py — Deterministic validation and computation engine
for the Wild Cards Assessment sub-skill (vision-foresight-wild-cards-assessment).

ALL hallucination-prone numerical/classification computations are here.
LLM may NOT re-compute or re-reason about any function in this file.

Covers:
  1.  Sub-variable score validation ({0,1,2,3} range check per 14 vars)
  2.  Pyramid score computation (Being/Sustenance/Actions/Tools weighted means)
  3.  PPS total computation and dominant Power Factor determination
  4.  Affinity score normalization and range validation
  5.  Psychographic profile normalization (sum-to-1.0)
  6.  Adjusted PPS computation
  7.  Top-N validation ({5,10,15,20})
  8.  Top-N filter with sorted ranking
  9.  Domain (STEEP+S) diversity enforcement and exception handling
  10. 3-Surprise-Type diversity enforcement
  11. Positive/Negative quality diversity check
  12. Full assessment output completeness gate

Sources:
  Petersen, J.L., & Steinmüller, K. (2009). "Wild Cards."
    Futures Research Methodology V3.0, Ch.10.
    The Millennium Project.
  Petersen, J.L. (1997, 1999). Out of the Blue: How to Anticipate Big Future
    Surprises. Arlington Institute.
    [Pyramid 4-Factor Hierarchy, Power Factor 1-4, Arlington Impact Index]
"""

import json
import sys
from typing import Optional

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS (verbatim from Petersen & Steinmüller 2009 Ch.10 + Petersen 1997)
# ─────────────────────────────────────────────────────────────────────────────

# Sub-variable impact score range: 0=no impact, 1=minor, 2=significant, 3=decisive
IMPACT_SCORE_MIN = 0
IMPACT_SCORE_MAX = 3
VALID_IMPACT_SCORES = {0, 1, 2, 3}

# Power Factors (Petersen Pyramid hierarchy)
POWER_FACTORS = {
    "being":      4,   # HIGHEST — "closest to defining the essence of a person"
    "sustenance": 3,
    "actions":    2,
    "tools":      1,   # LOWEST — "upper" level, broader but less profound
}

# Sub-variables per category (verbatim Section III.2)
SUBVARIABLES = {
    "being": ["B-1", "B-2", "B-3", "B-4"],        # 4 variables
    "sustenance": ["S-1", "S-2", "S-3", "S-4"],   # 4 variables
    "actions": ["A-1", "A-2", "A-3"],              # 3 variables
    "tools": ["T-1", "T-2", "T-3"],               # 3 variables
}

# Theoretical PPS range: 0 to (max_mean × PF) summed
# max Being: 3 × 4 = 12, max Sustenance: 3 × 3 = 9, max Actions: 3 × 2 = 6, max Tools: 3 × 1 = 3
PPS_MAX = 30.0  # 12 + 9 + 6 + 3
PPS_MIN = 0.0

# Valid Top-N values (SKILL.md: "default 10·configurable 5/15/20")
VALID_TOP_N = {5, 10, 15, 20}
DEFAULT_TOP_N = 10

# STEEP+S domain definitions (verbatim extensions of standard foresight usage)
STEEP_S_DOMAINS = {
    "S":   "Social",
    "T":   "Technological",
    "E":   "Economic",
    "Env": "Environmental",
    "P":   "Political",
    "Spi": "Spiritual/Values",
}

# 3 Surprise Types (Petersen & Steinmüller 2009 p.4 verbatim)
VALID_SURPRISE_TYPES = {"type1", "type2", "type3"}

SURPRISE_TYPE_VERBATIM = {
    "type1": "known with uncertain timing — 'the next earthquake'",
    "type2": "unknown to public but discoverable by experts — 'impacts of climate change'",
    "type3": "intrinsically unknowable — 'unknown unknowns'",
}

# Quality Factor values
VALID_QUALITY_FACTORS = {"positive", "negative", "both"}

# Required fields in assessment output
REQUIRED_ASSESSMENT_FIELDS = [
    "meta",
    "ranked_candidates",
    "filter_summary",
]

REQUIRED_META_FIELDS = [
    "target_group",
    "target_group_profile",
    "top_n",
    "n_total_candidates",
]

# ─────────────────────────────────────────────────────────────────────────────
# 1. SUB-VARIABLE SCORE VALIDATION
# ─────────────────────────────────────────────────────────────────────────────

def validate_subvar_scores(candidate: dict) -> dict:
    """
    Validate that all 14 sub-variable impact scores are in {0, 1, 2, 3}.

    Expects candidate dict with 'scores' key containing all 14 sub-variables:
      B-1..B-4, S-1..S-4, A-1..A-3, T-1..T-3

    Source: Petersen & Steinmüller (2009) Ch.10 Section III.2 assessment rubric.
    Impact scale: 0=no impact, 1=minor, 2=significant, 3=decisive
    """
    violations: list[str] = []
    present: list[str] = []
    scores = candidate.get("scores", {})

    all_vars = []
    for cat, vars_ in SUBVARIABLES.items():
        all_vars.extend(vars_)

    for var in all_vars:
        val = scores.get(var)
        if val is None:
            violations.append(f"MISSING_SUBVAR: '{var}' — required score in {VALID_IMPACT_SCORES}")
        else:
            try:
                ival = int(val)
                if ival not in VALID_IMPACT_SCORES:
                    violations.append(
                        f"INVALID_SCORE: '{var}' = {ival} not in {VALID_IMPACT_SCORES}. "
                        "Scale: 0=no impact, 1=minor, 2=significant, 3=decisive. "
                        "Source: Petersen & Steinmüller (2009) Ch.10 Section III.2."
                    )
                else:
                    present.append(var)
            except (TypeError, ValueError):
                violations.append(f"NON_INTEGER_SCORE: '{var}' = {val!r}")

    passed = len(violations) == 0
    return {
        "passed": passed,
        "present": present,
        "violations": violations,
        "total_required": len(all_vars),
        "total_present": len(present),
        "summary": "PASS — all 14 sub-variable scores valid" if passed
                   else f"FAIL — {len(violations)} violation(s)",
        "source": "Petersen & Steinmüller (2009) Ch.10 Section III.2",
    }


# ─────────────────────────────────────────────────────────────────────────────
# 2. PYRAMID SCORE COMPUTATION
# ─────────────────────────────────────────────────────────────────────────────

def compute_pyramid_scores(scores: dict) -> dict:
    """
    Compute category-level weighted Pyramid scores for a Wild Card candidate.

    Formula (Section III.2):
      category_score = mean(sub-variable scores) × Power_Factor
      where Power_Factor: Being=4, Sustenance=3, Actions=2, Tools=1

    Returns scores for each category + raw means + validation.

    Source: Petersen (1997) Out of the Blue + Petersen & Steinmüller (2009) Ch.10.
    """
    result: dict = {}
    violations: list[str] = []

    for cat, vars_ in SUBVARIABLES.items():
        pf = POWER_FACTORS[cat]
        vals = []
        for v in vars_:
            val = scores.get(v)
            if val is None:
                violations.append(f"MISSING '{v}' in scores — needed for {cat} computation")
            else:
                try:
                    ival = int(val)
                    if ival not in VALID_IMPACT_SCORES:
                        violations.append(f"INVALID_SCORE '{v}'={ival} not in {VALID_IMPACT_SCORES}")
                    else:
                        vals.append(float(ival))
                except (TypeError, ValueError):
                    violations.append(f"NON_INTEGER '{v}'={val!r}")

        if vals:
            mean_val = sum(vals) / len(vals)
            weighted = mean_val * pf
        else:
            mean_val = 0.0
            weighted = 0.0

        result[cat] = {
            "subvars": {v: scores.get(v) for v in vars_},
            "mean": round(mean_val, 4),
            "power_factor": pf,
            "weighted_score": round(weighted, 4),
        }

    return {
        "passed": len(violations) == 0,
        "violations": violations,
        "pyramid_scores": result,
        "formula": "category_score = mean(sub-vars) × Power_Factor",
        "source": "Petersen & Steinmüller (2009) Ch.10 Section III.2 verbatim",
    }


# ─────────────────────────────────────────────────────────────────────────────
# 3. PPS TOTAL + DOMINANT POWER FACTOR
# ─────────────────────────────────────────────────────────────────────────────

def compute_pps(pyramid_scores: dict) -> dict:
    """
    Compute Total Pyramid Score (PPS) and dominant Power Factor.

    PPS = Being_weighted + Sustenance_weighted + Actions_weighted + Tools_weighted
    Theoretical range: 0.0 – 30.0
    Dominant Power Factor = argmax of category weighted scores → P value (1-4)

    Source: Petersen (1997) + Petersen & Steinmüller (2009) Ch.10 Section III.2.
    """
    violations: list[str] = []
    weighted_scores: dict = {}

    for cat in POWER_FACTORS:
        cat_data = pyramid_scores.get(cat)
        if cat_data is None:
            violations.append(f"MISSING_CATEGORY: '{cat}' in pyramid_scores")
            weighted_scores[cat] = 0.0
        elif isinstance(cat_data, dict):
            ws = cat_data.get("weighted_score", 0.0)
            weighted_scores[cat] = float(ws)
        else:
            violations.append(f"INVALID_CATEGORY_FORMAT: '{cat}'")
            weighted_scores[cat] = 0.0

    total_pps = sum(weighted_scores.values())

    # Dominant category = highest weighted score
    dominant_cat = max(weighted_scores, key=lambda k: weighted_scores[k])
    dominant_pf = POWER_FACTORS[dominant_cat]

    # Validate range
    range_violations = []
    if not (PPS_MIN <= total_pps <= PPS_MAX + 0.001):
        range_violations.append(
            f"PPS_OUT_OF_RANGE: total_pps={total_pps:.4f} not in "
            f"[{PPS_MIN}, {PPS_MAX}]. Theoretical max = {PPS_MAX}."
        )

    all_violations = violations + range_violations
    return {
        "passed": len(all_violations) == 0,
        "violations": all_violations,
        "total_pps": round(total_pps, 4),
        "pps_range": [PPS_MIN, PPS_MAX],
        "category_weighted_scores": weighted_scores,
        "dominant_category": dominant_cat,
        "dominant_power_factor": dominant_pf,
        "summary": f"PPS={total_pps:.4f}, dominant={dominant_cat}(PF={dominant_pf})",
        "source": "Petersen & Steinmüller (2009) Ch.10 Section III.2",
    }


# ─────────────────────────────────────────────────────────────────────────────
# 4. AFFINITY SCORE VALIDATION
# ─────────────────────────────────────────────────────────────────────────────

def validate_affinity_score(score: float) -> dict:
    """
    Validate affinity score is in [0.0, 1.0].

    Affinity score must be bounded [0, 1] to ensure Adjusted_PPS ≤ PPS.
    Values > 1.0 would inflate Adjusted_PPS beyond the PPS theoretical max.

    Source: Petersen & Steinmüller (2009) Ch.10 Section III.2 p.3
    'close to home' variation — affinity modulates impact, cannot amplify beyond max.
    """
    try:
        s = float(score)
    except (TypeError, ValueError):
        return {"valid": False, "error": f"Non-numeric affinity score: {score!r}"}

    valid = 0.0 <= s <= 1.0
    return {
        "valid": valid,
        "score": s,
        "error": (
            f"affinity_score={s} out of [0.0, 1.0]. "
            "Must be bounded to prevent Adjusted_PPS exceeding PPS max."
        ) if not valid else None,
        "note": "Score < 0.5 indicates low target group relevance. Score = 1.0 = perfect alignment.",
        "source": "Petersen & Steinmüller (2009) Ch.10 Section III.2 p.3 'close to home'",
    }


# ─────────────────────────────────────────────────────────────────────────────
# 5. PSYCHOGRAPHIC PROFILE NORMALIZATION
# ─────────────────────────────────────────────────────────────────────────────

def normalize_psychographic_profile(profile: dict) -> dict:
    """
    Normalize psychographic profile so weights sum to 1.0.

    PDF p.3 defines 3 psychographic types: inner-directed, outer-directed,
    sustenance-driven. Raw weights may not sum to 1.0 and must be normalized.

    Source: Petersen & Steinmüller (2009) Ch.10 Section III.2 p.3 verbatim:
    "One might think of a group in psychological terms: is it inner-directed,
     outer-directed, or sustenance-driven?"
    """
    valid_keys = {"inner-directed", "outer-directed", "sustenance-driven"}
    violations: list[str] = []
    values: dict = {}

    for k in valid_keys:
        val = profile.get(k)
        if val is None:
            violations.append(f"MISSING_PSYCHOGRAPHIC_KEY: '{k}'")
        else:
            try:
                fval = float(val)
                if fval < 0.0:
                    violations.append(f"NEGATIVE_WEIGHT: '{k}'={fval} — weights must be >= 0")
                else:
                    values[k] = fval
            except (TypeError, ValueError):
                violations.append(f"NON_NUMERIC: '{k}'={val!r}")

    if violations:
        return {
            "passed": False,
            "violations": violations,
            "normalized": {},
            "source": "Petersen & Steinmüller (2009) Ch.10 Section III.2 p.3",
        }

    total = sum(values.values())
    if total == 0.0:
        violations.append("ZERO_SUM: all psychographic weights are 0 — cannot normalize")
        return {
            "passed": False,
            "violations": violations,
            "normalized": {},
            "source": "Petersen & Steinmüller (2009) Ch.10 Section III.2 p.3",
        }

    normalized = {k: round(v / total, 6) for k, v in values.items()}
    normalized_sum = sum(normalized.values())

    return {
        "passed": True,
        "violations": [],
        "original": {k: profile.get(k) for k in valid_keys},
        "original_sum": round(total, 6),
        "normalized": normalized,
        "normalized_sum": round(normalized_sum, 6),
        "note": (
            "Profile normalized to sum=1.0. "
            "Verbatim: inner-directed·outer-directed·sustenance-driven "
            "(Petersen & Steinmüller 2009 Ch.10 p.3)."
        ),
        "source": "Petersen & Steinmüller (2009) Ch.10 Section III.2 p.3",
    }


# ─────────────────────────────────────────────────────────────────────────────
# 6. ADJUSTED PPS COMPUTATION
# ─────────────────────────────────────────────────────────────────────────────

def compute_adjusted_pps(pps: float, affinity_score: float) -> dict:
    """
    Compute Adjusted PPS = PPS × affinity_score.

    Constraints:
      - pps must be in [0, 30]
      - affinity_score must be in [0, 1]
      - Adjusted_PPS is therefore in [0, 30]

    Source: Petersen & Steinmüller (2009) Ch.10 Section III.2.
    """
    violations: list[str] = []

    try:
        pps_f = float(pps)
    except (TypeError, ValueError):
        return {"passed": False, "violations": [f"NON_NUMERIC pps: {pps!r}"]}

    if not (PPS_MIN <= pps_f <= PPS_MAX + 0.001):
        violations.append(f"PPS_OUT_OF_RANGE: pps={pps_f} not in [{PPS_MIN}, {PPS_MAX}]")

    aff_result = validate_affinity_score(affinity_score)
    if not aff_result["valid"]:
        violations.append(f"AFFINITY_INVALID: {aff_result['error']}")
        aff_f = 0.0
    else:
        aff_f = float(affinity_score)

    adjusted = pps_f * aff_f
    passed = len(violations) == 0

    return {
        "passed": passed,
        "violations": violations,
        "pps": round(pps_f, 4),
        "affinity_score": round(aff_f, 4),
        "adjusted_pps": round(adjusted, 4),
        "formula": "Adjusted_PPS = PPS × affinity_score",
        "adjusted_range": [0.0, PPS_MAX],
        "source": "Petersen & Steinmüller (2009) Ch.10 Section III.2",
    }


# ─────────────────────────────────────────────────────────────────────────────
# 7. TOP-N VALIDATION
# ─────────────────────────────────────────────────────────────────────────────

def validate_top_n(n: int) -> dict:
    """
    Validate Top-N selection count against valid options {5, 10, 15, 20}.

    Source: vision-foresight-wild-cards-assessment SKILL.md:
    "Top N filter (default 10·configurable 5/15/20)"
    """
    try:
        n_int = int(n)
    except (TypeError, ValueError):
        return {"valid": False, "error": f"Non-integer n: {n!r}"}

    valid = n_int in VALID_TOP_N
    return {
        "valid": valid,
        "n": n_int,
        "default": DEFAULT_TOP_N,
        "valid_options": sorted(VALID_TOP_N),
        "error": (
            f"n={n_int} not in valid options {sorted(VALID_TOP_N)}."
        ) if not valid else None,
        "source": "vision-foresight-wild-cards-assessment SKILL.md",
    }


# ─────────────────────────────────────────────────────────────────────────────
# 8. TOP-N FILTER (sort and select)
# ─────────────────────────────────────────────────────────────────────────────

def apply_top_n_filter(candidates: list, n: int) -> dict:
    """
    Apply process of elimination: sort by adjusted_pps descending, select top N.

    Input candidates list: each item must have:
      id, adjusted_pps, surprise_type ('type1'/'type2'/'type3'),
      domain (one of STEEP+S keys), quality_factor ('positive'/'negative'/'both')

    Source: Petersen & Steinmüller (2009) Ch.10 Section III.2 verbatim:
    "we need a simple process of elimination" — relative ranking, biases consistent.
    """
    violations: list[str] = []

    # Validate n
    n_result = validate_top_n(n)
    if not n_result["valid"]:
        violations.append(f"INVALID_TOP_N: {n_result['error']}")
        n = DEFAULT_TOP_N

    if not isinstance(candidates, list) or len(candidates) == 0:
        return {
            "passed": False,
            "violations": ["EMPTY_CANDIDATES: candidate list is empty"],
            "selected": [],
        }

    # Validate and sort candidates by adjusted_pps
    valid_candidates = []
    for i, c in enumerate(candidates):
        if not isinstance(c, dict):
            violations.append(f"INVALID_CANDIDATE[{i}]: not a dict")
            continue
        cid = c.get("id", f"unknown-{i}")
        adj_pps = c.get("adjusted_pps")
        if adj_pps is None:
            violations.append(f"MISSING_ADJUSTED_PPS: candidate '{cid}'")
            continue
        try:
            adj_f = float(adj_pps)
            valid_candidates.append({**c, "_adj_pps_float": adj_f})
        except (TypeError, ValueError):
            violations.append(f"NON_NUMERIC_ADJUSTED_PPS: candidate '{cid}' = {adj_pps!r}")

    sorted_candidates = sorted(valid_candidates, key=lambda x: x["_adj_pps_float"], reverse=True)
    top_n = sorted_candidates[:n]

    # Assign ranks
    for rank_i, c in enumerate(top_n, 1):
        c["rank"] = rank_i
        c["eliminated"] = False

    eliminated = sorted_candidates[n:]
    for c in eliminated:
        c["eliminated"] = True
        c.get("elimination_reason")  # preserve if set

    passed = len(violations) == 0
    return {
        "passed": passed,
        "violations": violations,
        "n_requested": n,
        "n_total_candidates": len(candidates),
        "n_valid_candidates": len(valid_candidates),
        "selected": [{k: v for k, v in c.items() if not k.startswith("_")} for c in top_n],
        "eliminated_count": len(eliminated),
        "sort_basis": "adjusted_pps descending (relative ranking)",
        "source": (
            "Petersen & Steinmüller (2009) Ch.10 Section III.2 verbatim: "
            "'Although this process is relative, the conclusions are valuable nonetheless, "
            "for biases will be consistent across the spectrum of all considered Wild Cards.'"
        ),
    }


# ─────────────────────────────────────────────────────────────────────────────
# 9. DOMAIN DIVERSITY ENFORCEMENT (STEEP+S)
# ─────────────────────────────────────────────────────────────────────────────

def validate_domain_diversity(selected: list, n: int) -> dict:
    """
    Check STEEP+S domain diversity in selected Wild Cards.
    Rule: try to include at least 1 from each of 6 domains (when n >= 6).
    Exception: if n < 6 or fewer than 6 domains available in pool, do best-effort.

    Domains: S(Social), T(Technological), E(Economic), Env(Environmental),
             P(Political), Spi(Spiritual/Values)

    Source: vision-foresight-wild-cards-assessment SKILL.md Section 5.
    """
    violations: list[str] = []
    warnings: list[str] = []
    domain_counts: dict = {d: 0 for d in STEEP_S_DOMAINS}
    unknown_domains: list[str] = []

    for c in selected:
        d = c.get("domain", "")
        if d in STEEP_S_DOMAINS:
            domain_counts[d] += 1
        else:
            unknown_domains.append(f"id={c.get('id', '?')} domain='{d}'")

    if unknown_domains:
        warnings.append(
            f"UNKNOWN_DOMAINS: {unknown_domains} — must be one of {list(STEEP_S_DOMAINS.keys())}"
        )

    covered = [d for d, count in domain_counts.items() if count > 0]
    uncovered = [d for d in STEEP_S_DOMAINS if domain_counts[d] == 0]

    # Exception: if n < 6, full 6-domain coverage is structurally impossible
    if n < len(STEEP_S_DOMAINS) and uncovered:
        warnings.append(
            f"DOMAIN_COVERAGE_IMPOSSIBLE: n={n} < 6 domains — cannot cover all {len(STEEP_S_DOMAINS)} domains. "
            f"Best-effort: covered={covered}, uncovered={uncovered}."
        )
    elif uncovered:
        violations.append(
            f"DOMAIN_DIVERSITY_INCOMPLETE: uncovered domains {uncovered}. "
            "SKILL.md Section 5: 'STEEP+S 도메인 다양성 보장 — 모든 6 도메인에서 최소 1개 (가능 시)'."
        )

    # Build total (deterministic)
    total_covered = sum(domain_counts.values())

    passed = len(violations) == 0
    return {
        "passed": passed,
        "violations": violations,
        "warnings": warnings,
        "domain_counts": domain_counts,
        "domain_coverage_count": domain_counts,
        "total_in_selected": total_covered,
        "covered_domains": covered,
        "uncovered_domains": uncovered,
        "n_domains_required": min(n, len(STEEP_S_DOMAINS)),
        "domains_defined": STEEP_S_DOMAINS,
        "source": "vision-foresight-wild-cards-assessment SKILL.md Section 5",
    }


# ─────────────────────────────────────────────────────────────────────────────
# 10. SURPRISE TYPE DIVERSITY
# ─────────────────────────────────────────────────────────────────────────────

def validate_surprise_type_diversity(selected: list) -> dict:
    """
    Check that selected Wild Cards include all 3 Surprise Types when possible.
    Rule: try to include Type 1, Type 2, Type 3 (when pool allows).

    Source: Petersen & Steinmüller (2009) Ch.10 p.4 — 3 types verbatim.
    SKILL.md Section 5: "3 Surprise Type 다양성 보장 — Type 1·2·3 모두 포함 (가능 시)"
    """
    violations: list[str] = []
    warnings: list[str] = []
    type_counts: dict = {t: 0 for t in VALID_SURPRISE_TYPES}
    invalid_types: list[str] = []

    for c in selected:
        st = str(c.get("surprise_type", "")).lower().strip()
        if st in VALID_SURPRISE_TYPES:
            type_counts[st] += 1
        else:
            invalid_types.append(f"id={c.get('id', '?')} type='{st}'")

    if invalid_types:
        warnings.append(
            f"UNKNOWN_SURPRISE_TYPES: {invalid_types} — must be one of {sorted(VALID_SURPRISE_TYPES)}"
        )

    missing_types = [t for t in VALID_SURPRISE_TYPES if type_counts[t] == 0]
    if missing_types:
        warnings.append(
            f"SURPRISE_TYPE_GAP: types {missing_types} not represented. "
            "SKILL.md Section 5: 'Type 1·2·3 모두 포함 (가능 시)'. "
            "If pool lacks these types, note as best-effort."
        )

    return {
        "passed": True,  # diversity is best-effort, not hard requirement
        "violations": violations,
        "warnings": warnings,
        "type_counts": type_counts,
        "missing_types": missing_types,
        "type_verbatim": SURPRISE_TYPE_VERBATIM,
        "source": "Petersen & Steinmüller (2009) Ch.10 p.4 — 3 Surprise Types verbatim",
    }


# ─────────────────────────────────────────────────────────────────────────────
# 11. QUALITY FACTOR DIVERSITY
# ─────────────────────────────────────────────────────────────────────────────

def validate_quality_diversity(selected: list) -> dict:
    """
    Check that selected Wild Cards include at least 1 positive Quality Factor.
    Rule: minimum 1 positive (+) in top-N selection.

    Source: vision-foresight-wild-cards-assessment SKILL.md Section 5:
    "Positive/Negative Quality 다양성 — 최소 1 positive 포함"
    """
    violations: list[str] = []
    warnings: list[str] = []
    quality_counts: dict = {q: 0 for q in VALID_QUALITY_FACTORS}
    invalid_quality: list[str] = []

    for c in selected:
        q = str(c.get("quality_factor", "")).lower().strip()
        if q in VALID_QUALITY_FACTORS:
            quality_counts[q] += 1
        else:
            invalid_quality.append(f"id={c.get('id', '?')} quality='{q}'")

    if invalid_quality:
        warnings.append(
            f"UNKNOWN_QUALITY_FACTORS: {invalid_quality} — must be one of "
            f"{sorted(VALID_QUALITY_FACTORS)}"
        )

    positive_count = quality_counts.get("positive", 0) + quality_counts.get("both", 0)
    if positive_count == 0:
        violations.append(
            "MISSING_POSITIVE_QUALITY: at least 1 Wild Card with positive Quality Factor required. "
            "SKILL.md Section 5: 'Positive/Negative Quality 다양성 — 최소 1 positive 포함'."
        )

    passed = len(violations) == 0
    return {
        "passed": passed,
        "violations": violations,
        "warnings": warnings,
        "quality_counts": quality_counts,
        "positive_count": positive_count,
        "required_minimum_positive": 1,
        "source": "vision-foresight-wild-cards-assessment SKILL.md Section 5",
    }


# ─────────────────────────────────────────────────────────────────────────────
# 12. FULL ASSESSMENT OUTPUT COMPLETENESS GATE
# ─────────────────────────────────────────────────────────────────────────────

def validate_assessment_output(output: dict) -> dict:
    """
    Full output completeness gate for the Wild Cards Assessment sub-skill.

    Validates:
      - Required sections present (meta, ranked_candidates, filter_summary)
      - meta fields present (target_group, target_group_profile, top_n, n_total_candidates)
      - top_n is valid {5,10,15,20}
      - psychographic profile normalizes (sum > 0)
      - ranked_candidates non-empty
      - domain_coverage total matches sum of individual counts
      - quality diversity (at least 1 positive)
      - next_skill pointer present

    Source: Petersen & Steinmüller (2009) Ch.10 Section III.2 full spec.
    """
    violations: list[str] = []
    warnings: list[str] = []

    # Required sections
    for field in REQUIRED_ASSESSMENT_FIELDS:
        if field not in output or not output[field]:
            violations.append(f"MISSING_SECTION: '{field}'")

    if violations:
        return {
            "passed": False,
            "violations": violations,
            "warnings": warnings,
            "summary": f"FAIL — {len(violations)} missing section(s)",
        }

    meta = output.get("meta", {})
    for mf in REQUIRED_META_FIELDS:
        if mf not in meta or meta[mf] is None:
            violations.append(f"MISSING_META_FIELD: '{mf}'")

    # Top-N validation
    top_n = meta.get("top_n")
    if top_n is not None:
        n_result = validate_top_n(top_n)
        if not n_result["valid"]:
            violations.append(f"INVALID_TOP_N: {n_result['error']}")
        n_int = top_n
    else:
        n_int = DEFAULT_TOP_N

    # Psychographic profile normalization check
    profile = meta.get("target_group_profile", {})
    psych_keys = {"inner-directed", "outer-directed", "sustenance-driven"}
    if any(k in profile for k in psych_keys):
        norm_result = normalize_psychographic_profile(profile)
        if not norm_result["passed"]:
            violations.extend(norm_result["violations"])

    # Ranked candidates
    ranked = output.get("ranked_candidates", [])
    if not isinstance(ranked, list) or len(ranked) == 0:
        violations.append("EMPTY_RANKED_CANDIDATES: must be non-empty list")
    else:
        # Quality diversity check
        qd_result = validate_quality_diversity(ranked)
        if not qd_result["passed"]:
            violations.extend(qd_result["violations"])
        if qd_result.get("warnings"):
            warnings.extend(qd_result["warnings"])

        # Surprise type diversity
        st_result = validate_surprise_type_diversity(ranked)
        if st_result.get("warnings"):
            warnings.extend(st_result["warnings"])

        # Domain diversity
        dd_result = validate_domain_diversity(ranked, n_int)
        if not dd_result["passed"]:
            violations.extend(dd_result["violations"])
        if dd_result.get("warnings"):
            warnings.extend(dd_result["warnings"])

    # filter_summary total consistency check
    fs = output.get("filter_summary", {})
    if isinstance(fs, dict):
        dc = fs.get("domain_coverage", {})
        if isinstance(dc, dict):
            declared_total = dc.get("total")
            computed_total = sum(v for k, v in dc.items() if k != "total" and isinstance(v, (int, float)))
            if declared_total is not None and int(declared_total) != int(computed_total):
                violations.append(
                    f"DOMAIN_COVERAGE_TOTAL_MISMATCH: declared total={declared_total}, "
                    f"computed total={computed_total}. All domain counts must sum to declared total."
                )

    # next_skill pointer
    if "next_skill" not in output and "return" not in output:
        warnings.append(
            "MISSING_NEXT_SKILL: output should include 'next_skill' pointer to "
            "'vision-foresight-wild-cards-impact-index' (SKILL.md Section 8)."
        )

    passed = len(violations) == 0
    return {
        "passed": passed,
        "violations": violations,
        "warnings": warnings,
        "summary": "PASS" if passed else f"FAIL — {len(violations)} violation(s)",
        "source": "Petersen & Steinmüller (2009) Ch.10 Section III.2",
    }


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

COMMANDS = {
    "validate_subvar_scores":        "Validate all 14 sub-variable impact scores are in {0,1,2,3}",
    "compute_pyramid_scores":        "Compute Being/Sustenance/Actions/Tools weighted scores from raw scores",
    "compute_pps":                   "Compute Total PPS + dominant Power Factor from pyramid_scores dict",
    "validate_affinity_score":       "Validate affinity score is in [0.0, 1.0]",
    "normalize_psychographic_profile":"Normalize inner-directed/outer-directed/sustenance-driven to sum=1.0",
    "compute_adjusted_pps":          "Compute Adjusted_PPS = PPS × affinity_score with range validation",
    "validate_top_n":                "Validate Top-N selection count {5,10,15,20}",
    "apply_top_n_filter":            "Sort candidates by adjusted_pps and select top N",
    "validate_domain_diversity":     "Check STEEP+S domain diversity in selected Wild Cards",
    "validate_surprise_type_diversity":"Check Type 1/2/3 diversity in selected Wild Cards",
    "validate_quality_diversity":    "Check at least 1 positive Quality Factor in selected Wild Cards",
    "validate_assessment_output":    "Full assessment output completeness gate",
    "list_commands":                 "List all available commands",
}


def cli() -> None:
    if len(sys.argv) < 2 or sys.argv[1] == "list_commands":
        print(json.dumps({"commands": COMMANDS}, ensure_ascii=False, indent=2))
        return

    cmd = sys.argv[1]
    args: dict = {}
    if len(sys.argv) > 2:
        try:
            args = json.loads(sys.argv[2])
        except json.JSONDecodeError as exc:
            print(json.dumps({"error": f"Invalid JSON: {exc}"}))
            sys.exit(1)

    result: dict = {}

    if cmd == "validate_subvar_scores":
        result = validate_subvar_scores(args.get("candidate", {}))
    elif cmd == "compute_pyramid_scores":
        result = compute_pyramid_scores(args.get("scores", {}))
    elif cmd == "compute_pps":
        result = compute_pps(args.get("pyramid_scores", {}))
    elif cmd == "validate_affinity_score":
        result = validate_affinity_score(args.get("score", 0))
    elif cmd == "normalize_psychographic_profile":
        result = normalize_psychographic_profile(args.get("profile", {}))
    elif cmd == "compute_adjusted_pps":
        result = compute_adjusted_pps(args.get("pps", 0), args.get("affinity_score", 0))
    elif cmd == "validate_top_n":
        result = validate_top_n(args.get("n", 0))
    elif cmd == "apply_top_n_filter":
        result = apply_top_n_filter(args.get("candidates", []), args.get("n", DEFAULT_TOP_N))
    elif cmd == "validate_domain_diversity":
        result = validate_domain_diversity(args.get("selected", []), args.get("n", DEFAULT_TOP_N))
    elif cmd == "validate_surprise_type_diversity":
        result = validate_surprise_type_diversity(args.get("selected", []))
    elif cmd == "validate_quality_diversity":
        result = validate_quality_diversity(args.get("selected", []))
    elif cmd == "validate_assessment_output":
        result = validate_assessment_output(args.get("output", {}))
    else:
        print(json.dumps({
            "error": f"Unknown command '{cmd}'",
            "available": list(COMMANDS.keys()),
        }))
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    cli()
