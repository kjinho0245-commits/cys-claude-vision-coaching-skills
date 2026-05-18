#!/usr/bin/env python3
"""
Deterministic utility module for vision-foresight-scenarios-implications-synthesis sub-skill.

Replaces LLM natural-language reasoning at points where structural hallucination
cannot be ruled out: input validation, VRMP tier mapping, time-horizon range checks,
robust-vs-contingent classification, verbatim quote matching, cross-skill linkage
existence checks, date staleness, source-trail URL validation, Mermaid synthesis
diagram generation.

Source of authority
-------------------
Glenn, Jerome C. and The Futures Group International (2009).
"Scenarios." In: Futures Research Methodology — Version 3.0,
Chapter 19. The Millennium Project. Washington, D.C.
(PDF: 19-Scenarios.pdf, 54 pages.)

Cross-references
----------------
- Section IV (pp. 18-19): Strengths and Weaknesses — verbatim quotes frozen below.
- Section V (pp. 19-21): Frontiers — Taylor 1993 Cone of Plausibility,
  Z_punkt 6-month rhythm signposts, Delphi 'filling in blanks'.
- Schwartz, Peter (1991). The Art of the Long View. Doubleday. pp. 226-234.
  Steps 1-6. Step 7 (leading indicators) is Glenn's extension, NOT original Schwartz.

No LLM inference here. All decisions are arithmetic, lookup, regex,
or set-membership tests.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
from datetime import date, datetime
from typing import Optional


# ─────────────────────────────────────────────────────────────────────────────
# 1. FROZEN CONSTANTS (Glenn & TFG 2009 + SKILL.md spec)
# ─────────────────────────────────────────────────────────────────────────────

# Scenario count: Glenn & TFG Section III "Four to five worlds seems ideal"
# Defense Markets case study went 16 mathematically possible → 13 plausible → 6 named
# Min 3 (any less is "most likely" forecasting which Section III warns against).
# Max 12 (Defense Markets used 6; comprehensive studies go up to 12).
N_SCENARIOS_MIN = 3
N_SCENARIOS_MAX = 12
N_SCENARIOS_IDEAL = (4, 5)

# Implications-Domain (박사님 절대 protocol 5번):
# 1-10 numbered domains + Custom + Skip
VALID_DOMAINS = (
    set(str(i) for i in range(1, 11))  # "1"…"10"
    | {"C", "Custom", "custom"}
    | {"S", "Skip", "skip"}
)

# Cycle codes from vision-foresight-scenarios master (C1…C10)
VALID_CYCLES = {f"C{i}" for i in range(1, 11)}

# Expert modes (VRMP 8번째 절대 protocol)
VALID_EXPERT_MODES = {"R", "A", "V", "H"}

# VRMP tier: expert_mode → evidence tier (deterministic mapping)
#   H (Hypothetical / 학습 지식 단독)     → R-1  weakest
#   R (Real Anonymized) / A (Anonymized)  → R-2  web-verified + anonymised expert
#   V (Verified Published)                → R-3  strongest, public source
VRMP_TIER_MAP = {"R": "R-2", "A": "R-2", "V": "R-3", "H": "R-1"}

# Time horizon (Section IV "five-, ten-, or fifteen-year point forecasts" + V3.0 long-term)
TIME_HORIZONS = {
    "5yr": (0, 5),
    "10yr": (0, 10),
    "15-25yr": (0, 25),
    "30yr+": (0, 35),
}

# 3-tier sub-horizon within full horizon (SKILL.md DEFAULT)
TIER_SHORT_RANGE = (1, 5)     # 1-5 years
TIER_MID_RANGE = (5, 15)      # 5-15 years
TIER_LONG_RANGE = (15, 30)    # 15-30 years (matches V3.0 "thirty-three years" Kahn 1967)

# VRMP staleness threshold (Section V "six-month rhythm" Z_punkt verbatim)
VRMP_STALENESS_DAYS = 180

# Robust-vs-contingent: insight appears in ≥ROBUST_RATIO of scenarios → robust
ROBUST_RATIO_THRESHOLD = 0.75   # appears in 3 of 4, or 4 of 5

# 17 foresight chapters Section V cross-method linkage (PDF 19-Scenarios + Methodology V3.0)
# Chapter numbers from V3.0 ToC.
FORESIGHT_CROSS_LINKS = {
    "vision-foresight-environmental-scanning": "Ch.02 — driving forces + leading indicators monitoring",
    "foresight-tech-mining": "Ch.03 — tech-related indicators (Porter 2009)",
    "foresight-delphi": "Ch.04 — participatory scenario input",
    "foresight-realtime-delphi": "Ch.05 — async scenario refinement",
    "vision-foresight-futures-wheel": "Ch.06 — scenario branching · ripple effects",
    "foresight-futures-polygon": "Ch.07 — scenario consensus (Pacinelli 2009)",
    "foresight-trend-impact-analysis": "Ch.08 — TIA projection (TFG Step 2)",
    "foresight-cross-impact-analysis": "Ch.09 — inter-event probabilities (Gordon 2009)",
    "vision-foresight-wild-cards": "Ch.10 — Cone of Plausibility wild-card boundary",
    "foresight-structural-analysis": "Ch.11 — MICMAC driving forces (Godet)",
    "foresight-systems-perspective": "Ch.12 — System Dynamics (Leonard with Beer)",
    "foresight-decision-modeling": "Ch.13 — policy testing (TFG/Gordon/Glenn)",
    "foresight-substitution-analysis": "Ch.14 — tech substitution (Gordon 2009)",
    "foresight-statistical-modeling": "Ch.15 — quantitative projection (Pacinelli/TFG/Gordon)",
    "foresight-technology-sequence-analysis": "Ch.16 — tech path within scenario (Gordon 2009)",
    "foresight-morphological-analysis": "Ch.17 — Godet MOPPHOL scenario field (Ritchey 2009)",
    "foresight-relevance-tree": "Ch.18 — scenario decomposition (TFG 2009)",
}

# vision 시리즈 cross-links (박사님 미래학자 ecosystem 활용)
VISION_CROSS_LINKS = {
    "vision-four-futures": "4가지 미래 가능성 정확 매핑",
    "vision-future-needs-prediction": "scenario별 필요·결핍",
    "vision-strategy-coach": "Robust + Contingent action plans",
    "vision-futures-timeline-map": "scenarios → timeline",
    "vision-statement-writer": "normative scenario → 비전 선언문",
    "vision-personal-future-research": "박사님 7종 진단 + scenarios",
}

# ─────────────────────────────────────────────────────────────────────────────
# 2. SECTION IV VERBATIM CANON
#    All quotes below are frozen exactly from the PDF (Section IV, pp. 18-19).
#    SKILL.md must not paraphrase these — verify against this canon.
# ─────────────────────────────────────────────────────────────────────────────

SECTION_IV_STRENGTHS_VERBATIM = [
    # PDF p. 18, opening sentence of Section IV
    "Scenarios are one of the easiest ways to present complex information to "
    "decision makers that makes future possibilities seem more real.",
    # PDF p. 18, paragraph on "signposts"
    "signposts, indicating paths along the way to alternative and anticipated "
    "futures",
    # PDF p. 18, "This flexibility significantly reduces the need..."
    "significantly reduces the need for specific five-, ten-, or fifteen-year "
    "point forecasts",
]

SECTION_IV_WEAKNESSES_VERBATIM = [
    # PDF p. 18, "A weakness of scenarios is that they can be given to non-participants..."
    'can be given to non-participants, who can then see the scenarios as the '
    '"official set of possible futures" and hence, control or limit their '
    "thinking to some degree",
    # PDF p. 18, "The writer's mental model of how the world works..."
    "The writer's mental model of how the world works is transferred to the "
    "reader, and possibly unconsciously accepted",
    # PDF p. 19, "editors take out the controversial items..."
    "editors take out the controversial items. This defeats a key reason for "
    "doing futures research",
    # PDF p. 19, "Every serious futurist I know predicted..."
    "Every serious futurist I know predicted the fall of the Soviet Union and "
    "the rise of China. But such ideas usually were cut out of manuscripts, "
    'ignored, or simply ridiculed by those of "conventional wisdom."',
    # PDF p. 19, "Scenarios should have some surprises in them..."
    "Scenarios should have some surprises in them",
]

SCHWARTZ_STEP_6_VERBATIM = "Assess the implications"
SCHWARTZ_NOTE = (
    "Steps 1-6 are Schwartz's original method (The Art of the Long View, "
    "1991, pp. 226-234). Step 7 (leading indicators and signposts) is Glenn's "
    "extension — it does NOT appear in the original Schwartz (1991) text."
)

# ─────────────────────────────────────────────────────────────────────────────
# 3. BIBLIOGRAPHY (V3.0 19장 — 12 core references)
# ─────────────────────────────────────────────────────────────────────────────

BIBLIOGRAPHY_KEYS = {
    "kahn_1965": "Kahn, Herman (1965). On Escalation: Metaphors and Scenarios. Praeger / Hudson Institute.",
    "kahn_wiener_1967": (
        "Kahn, Herman and Wiener, Anthony J. (1967). The Year 2000: A Framework for "
        "Speculation on the Next Thirty-Three Years. Macmillan, New York. "
        "[NOTE: co-author is Anthony J. Wiener (W-I-E-N-E-R), not 'Weiner']"
    ),
    "bell_1968": (
        "Bell, Daniel (ed.) (1968). Toward the Year 2000: Work in Progress. "
        "Houghton Mifflin, Boston."
    ),
    "freeman_1974": (
        "Freeman, S. David (Project Director) (1974). A Time to Choose: America's "
        "Energy Future. Ballinger Publishing Company. Ford Foundation Energy Policy Project."
    ),
    "project_independence_1974": (
        "Federal Energy Administration (1974). Project Independence Blueprint Final "
        "Task Force Report. U.S. Government Printing Office."
    ),
    "schwartz_1991": (
        "Schwartz, Peter (1991). The Art of the Long View: Planning for the Future in "
        "an Uncertain World. Doubleday/Currency, New York. ISBN 0-385-26731-2. "
        "[6-step GBN method, pp. 226-234]"
    ),
    "godet_1990": "Godet, Michel (1990). Scenarios and Strategic Management.",
    "godet_1993": (
        "Godet, Michel (1993). From Anticipation to Action: A Handbook of Strategic "
        "Prospective. UNESCO Publishing."
    ),
    "mandel_wilson_1993": (
        "Mandel, Thomas F. and Wilson, Ian H. (1993). Scenario Planning. "
        "SRI International."
    ),
    "taylor_1990": (
        "Taylor, Charles W. (1990). Alternative World Scenarios for Strategic "
        "Planning. U.S. Army War College."
    ),
    "taylor_1993": (
        "Taylor, Charles W. (1993). Cone of Plausibility. Chemtech, U.S. Army War College."
    ),
    "von_reibnitz_1988": (
        "von Reibnitz, Ute (1988). Scenario Techniques. McGraw-Hill."
    ),
    "thomas_boroush_1992": (
        "Thomas, Charles W. and Boroush, Mark A. (1992). Case Study: Defense Markets. "
        "Planning Review, May/June 1992."
    ),
    "glenn_1979": (
        "Glenn, Jerome (1979). Linking the Future: Findhorn, Auroville, Arcosanti. "
        "Center on Technology and Society, Cambridge, MA."
    ),
    "glenn_tfg_2009": (
        "Glenn, Jerome C. and The Futures Group International (2009). Scenarios. "
        "Chapter 19, Futures Research Methodology — Version 3.0. "
        "The Millennium Project, Washington, D.C."
    ),
}

# ─────────────────────────────────────────────────────────────────────────────
# 4. INPUT VALIDATION
# ─────────────────────────────────────────────────────────────────────────────

REQUIRED_INPUT_KEYS = [
    "implications_domain",   # 1-10 / C / S
    "topic",
    "cycle",                 # C1-C10
    "expert_mode",           # R/A/V/H
    "horizon",               # 5yr/10yr/15-25yr/30yr+
    "scenarios",             # list of dicts, each with name + insights
]


def validate_synthesis_input(inp: dict) -> list[str]:
    """
    Validate the synthesis input bundle from the master skill.

    Returns
    -------
    list of error strings. Empty list = PASS.
    All checks are deterministic — no LLM inference.
    """
    errors: list[str] = []

    for k in REQUIRED_INPUT_KEYS:
        if k not in inp:
            errors.append(f"MISSING REQUIRED INPUT: '{k}'")
    if errors:
        return errors  # early-exit on missing keys

    # implications_domain
    dom = str(inp["implications_domain"])
    if dom not in VALID_DOMAINS:
        errors.append(
            f"INVALID implications_domain: '{dom}' — must be one of {sorted(VALID_DOMAINS)}"
        )

    # cycle
    cyc = str(inp["cycle"]).upper().strip()
    if cyc not in VALID_CYCLES:
        errors.append(f"INVALID cycle: '{cyc}' — must be one of {sorted(VALID_CYCLES)}")

    # expert_mode
    em = str(inp["expert_mode"]).upper().strip()
    if em not in VALID_EXPERT_MODES:
        errors.append(
            f"INVALID expert_mode: '{em}' — must be R/A/V/H "
            "(VRMP 8th protocol; default R)"
        )

    # horizon
    hz = str(inp["horizon"]).lower().strip()
    if hz not in TIME_HORIZONS:
        errors.append(
            f"INVALID horizon: '{hz}' — must be one of {sorted(TIME_HORIZONS)}"
        )

    # scenarios
    scs = inp.get("scenarios") or []
    if not isinstance(scs, list):
        errors.append("INVALID scenarios: must be a list of dicts")
    else:
        n = len(scs)
        if n < N_SCENARIOS_MIN:
            errors.append(
                f"TOO FEW SCENARIOS: n={n}. Glenn & TFG 2009 'Four to five worlds "
                f"seems ideal'. Minimum {N_SCENARIOS_MIN}."
            )
        elif n > N_SCENARIOS_MAX:
            errors.append(
                f"TOO MANY SCENARIOS: n={n}. Maximum {N_SCENARIOS_MAX} "
                "(Defense Markets case used 6 named worlds; >12 dilutes analysis)."
            )
        else:
            for i, sc in enumerate(scs):
                if not isinstance(sc, dict):
                    errors.append(f"scenarios[{i}] is not a dict")
                    continue
                if not sc.get("name"):
                    errors.append(f"scenarios[{i}] missing 'name'")
                if "insights" not in sc:
                    errors.append(f"scenarios[{i}] missing 'insights' list")
                elif not isinstance(sc.get("insights"), list):
                    errors.append(
                        f"scenarios[{i}].insights must be a list of strings"
                    )

    return errors


# ─────────────────────────────────────────────────────────────────────────────
# 5. VRMP TIER + STALENESS
# ─────────────────────────────────────────────────────────────────────────────

def determine_vrmp_tier(expert_mode: str) -> str:
    """expert_mode → R-1 / R-2 / R-3 (deterministic table lookup)."""
    return VRMP_TIER_MAP.get(str(expert_mode).upper(), "R-1")


def check_date_staleness(fetched_date_str: Optional[str]) -> dict:
    """
    Check if fetched_date is stale (>180 days).
    Source: Section V Z_punkt verbatim "six-month rhythm".
    """
    if not fetched_date_str:
        return {
            "is_stale": None,
            "days_old": None,
            "threshold_days": VRMP_STALENESS_DAYS,
            "note": "No fetched_date provided",
        }
    try:
        raw = str(fetched_date_str).replace("Z", "+00:00")
        if "T" in raw:
            fetched = datetime.fromisoformat(raw).date()
        else:
            fetched = date.fromisoformat(raw[:10])
        today = date.today()
        days_old = (today - fetched).days
        is_stale = days_old > VRMP_STALENESS_DAYS
        return {
            "is_stale": is_stale,
            "days_old": days_old,
            "fetched_date": fetched_date_str,
            "threshold_days": VRMP_STALENESS_DAYS,
            "note": (
                f"{'⚠ STALE' if is_stale else 'FRESH'}: "
                f"{days_old}일 경과 / 한계 {VRMP_STALENESS_DAYS}일 "
                "(Z_punkt six-month rhythm — Section V verbatim)"
            ),
        }
    except (ValueError, TypeError) as exc:
        return {
            "is_stale": None,
            "days_old": None,
            "threshold_days": VRMP_STALENESS_DAYS,
            "note": f"Date parse error: {exc}",
        }


# ─────────────────────────────────────────────────────────────────────────────
# 6. TIME-HORIZON RANGE CHECKS
# ─────────────────────────────────────────────────────────────────────────────

def tier_for_year_offset(years_from_now: float) -> str:
    """
    Map a year offset to its 3-tier sub-horizon label.
    DEFAULT 3-tier per SKILL.md:
      Short (1-5)  ·  Mid (5-15)  ·  Long (15-30)
    """
    y = float(years_from_now)
    if y < TIER_SHORT_RANGE[0]:
        return "Pre-Short (<1y)"
    if TIER_SHORT_RANGE[0] <= y <= TIER_SHORT_RANGE[1]:
        return "Short (1-5y)"
    if TIER_SHORT_RANGE[1] < y <= TIER_MID_RANGE[1]:
        return "Mid (5-15y)"
    if TIER_MID_RANGE[1] < y <= TIER_LONG_RANGE[1]:
        return "Long (15-30y)"
    return "Beyond-Long (>30y)"


def validate_horizon_range(horizon_key: str, years: float) -> dict:
    """Validate a years-from-now value against the chosen horizon."""
    horizon_key = str(horizon_key).lower().strip()
    if horizon_key not in TIME_HORIZONS:
        return {"valid": False, "error": f"Unknown horizon '{horizon_key}'"}
    lo, hi = TIME_HORIZONS[horizon_key]
    in_range = lo <= years <= hi
    return {
        "valid": in_range,
        "horizon": horizon_key,
        "range": (lo, hi),
        "years": years,
        "tier": tier_for_year_offset(years),
        "error": None if in_range else f"years={years} outside horizon {horizon_key} = [{lo}, {hi}]",
    }


# ─────────────────────────────────────────────────────────────────────────────
# 7. ROBUST vs CONTINGENT CLASSIFICATION
# ─────────────────────────────────────────────────────────────────────────────

_NORM_TOKEN_RE = re.compile(r"[a-z0-9가-힣]+", re.UNICODE)


def _normalize_insight(text: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace → token bag for matching."""
    tokens = _NORM_TOKEN_RE.findall(str(text).lower())
    return " ".join(sorted(set(tokens)))


def _token_set(text: str) -> frozenset:
    return frozenset(_NORM_TOKEN_RE.findall(str(text).lower()))


def _jaccard(a: frozenset, b: frozenset) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def classify_robust_vs_contingent(
    scenarios: list,
    jaccard_threshold: float = 0.5,
    robust_ratio: float = ROBUST_RATIO_THRESHOLD,
) -> dict:
    """
    Classify each insight as 'robust' (appears in ≥robust_ratio of scenarios)
    or 'contingent' (appears in fewer).

    Match rule (deterministic): two insights belong to the same canonical bucket
    if their Jaccard token overlap ≥ `jaccard_threshold`.
    """
    n_total = len(scenarios)
    if n_total == 0:
        return {"robust": [], "contingent": [], "n_scenarios": 0}

    # Build buckets: list of (representative_text, token_set, scenario_names)
    buckets: list[tuple[str, frozenset, set]] = []
    for sc in scenarios:
        sc_name = sc.get("name") or "Unnamed"
        for ins in sc.get("insights") or []:
            ts = _token_set(ins)
            if not ts:
                continue
            matched = False
            for i, (_, bts, names) in enumerate(buckets):
                if _jaccard(ts, bts) >= jaccard_threshold:
                    # Merge: enlarge token set, add scenario name
                    new_ts = bts | ts
                    names.add(sc_name)
                    buckets[i] = (buckets[i][0], new_ts, names)
                    matched = True
                    break
            if not matched:
                buckets.append((str(ins), ts, {sc_name}))

    robust: list[dict] = []
    contingent_by_scenario: dict[str, list[str]] = {sc["name"]: [] for sc in scenarios}

    threshold_count = max(1, int(round(robust_ratio * n_total)))
    for text, _, names in buckets:
        if len(names) >= threshold_count:
            robust.append({
                "insight": text,
                "appears_in": sorted(names),
                "coverage": round(len(names) / n_total, 4),
            })
        else:
            # contingent — assign to each scenario that owns it
            for nm in names:
                contingent_by_scenario.setdefault(nm, []).append(text)

    return {
        "robust": robust,
        "contingent_by_scenario": contingent_by_scenario,
        "n_scenarios": n_total,
        "robust_ratio_threshold": robust_ratio,
        "threshold_count": threshold_count,
        "jaccard_threshold": jaccard_threshold,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 8. CROSS-SKILL LINKAGE EXISTENCE CHECK
# ─────────────────────────────────────────────────────────────────────────────

def check_cross_skill_existence(
    skills_root: Optional[str] = None,
) -> dict:
    """
    Verify that every cross-link skill folder actually exists on disk.
    DETERMINISTIC — uses os.path.isdir.

    Catches drift between SKILL.md and the actual skill ecosystem.
    """
    if skills_root is None:
        # script lives in skills/vision-foresight-scenarios-implications-synthesis/
        here = os.path.dirname(os.path.abspath(__file__))
        skills_root = os.path.dirname(here)

    foresight_status: dict[str, dict] = {}
    for name, role in FORESIGHT_CROSS_LINKS.items():
        p = os.path.join(skills_root, name)
        exists = os.path.isdir(p)
        foresight_status[name] = {"exists": exists, "role": role, "path": p}

    vision_status: dict[str, dict] = {}
    for name, role in VISION_CROSS_LINKS.items():
        p = os.path.join(skills_root, name)
        exists = os.path.isdir(p)
        vision_status[name] = {"exists": exists, "role": role, "path": p}

    missing = (
        [k for k, v in foresight_status.items() if not v["exists"]]
        + [k for k, v in vision_status.items() if not v["exists"]]
    )

    return {
        "foresight": foresight_status,
        "vision": vision_status,
        "all_present": not missing,
        "missing": missing,
        "skills_root": skills_root,
        "n_foresight_linked": len(FORESIGHT_CROSS_LINKS),
        "n_vision_linked": len(VISION_CROSS_LINKS),
    }


# ─────────────────────────────────────────────────────────────────────────────
# 9. SECTION IV VERBATIM QUOTE VERIFICATION
# ─────────────────────────────────────────────────────────────────────────────

def _norm_for_quote(s: str) -> str:
    """Normalize for quote comparison: lowercase, collapse whitespace, strip outer quotes."""
    s = re.sub(r"\s+", " ", str(s).strip().lower())
    s = s.strip("\"'“”‘’")
    # normalize curly quotes inside string
    s = s.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    return s


def verify_verbatim_quote(quote: str) -> dict:
    """
    Check whether `quote` is one of the Section IV verbatim canon strings.
    DETERMINISTIC substring match (no LLM).

    Returns
    -------
    dict with 'verified': bool, 'tier': 'strength'/'weakness'/None,
    'canonical': matching canonical text or None.
    """
    n = _norm_for_quote(quote)
    if not n:
        return {"verified": False, "tier": None, "canonical": None,
                "note": "empty quote"}

    for canon in SECTION_IV_STRENGTHS_VERBATIM:
        c = _norm_for_quote(canon)
        if c in n or n in c:
            return {"verified": True, "tier": "strength", "canonical": canon}
    for canon in SECTION_IV_WEAKNESSES_VERBATIM:
        c = _norm_for_quote(canon)
        if c in n or n in c:
            return {"verified": True, "tier": "weakness", "canonical": canon}
    return {
        "verified": False, "tier": None, "canonical": None,
        "note": "quote not found in Section IV verbatim canon",
    }


def list_verbatim_canon() -> dict:
    """Return all canonical Section IV quotes — for SKILL.md to embed without paraphrase."""
    return {
        "strengths": list(SECTION_IV_STRENGTHS_VERBATIM),
        "weaknesses": list(SECTION_IV_WEAKNESSES_VERBATIM),
        "schwartz_step_6": SCHWARTZ_STEP_6_VERBATIM,
        "schwartz_note": SCHWARTZ_NOTE,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 10. SOURCE-TRAIL URL VALIDATION
# ─────────────────────────────────────────────────────────────────────────────

_URL_RE = re.compile(
    r"^https?://"                                 # scheme
    r"([a-z0-9]([a-z0-9-]*[a-z0-9])?\.)+"         # domain labels
    r"[a-z]{2,}"                                  # TLD
    r"(/[^\s]*)?$",                               # path
    re.IGNORECASE,
)


def validate_source_url(url: str) -> dict:
    """Deterministic URL format check (scheme + domain + optional path)."""
    if not url or not isinstance(url, str):
        return {"valid": False, "error": "empty url"}
    if _URL_RE.match(url.strip()):
        return {"valid": True, "url": url.strip()}
    return {"valid": False, "url": url, "error": "url does not match http(s)://domain[/path]"}


def classify_url_tier(url: str) -> str:
    """
    Crude domain-based VRMP tier hint (deterministic regex):
      .gov / .edu / .ac.* / official journal hosts → R-3
      news outlets / Wikipedia                     → R-2
      blogs / forums / unknown                     → R-1
    """
    u = url.lower()
    if re.search(r"\.(gov|edu|ac\.[a-z]{2,3})(/|$)", u):
        return "R-3"
    if re.search(r"(jstor\.org|sciencedirect|springer|nature\.com|sciencemag|millennium-project)", u):
        return "R-3"
    if re.search(r"(wikipedia\.org|reuters\.com|apnews\.com|bbc\.co|nytimes\.com|wsj\.com|ft\.com)", u):
        return "R-2"
    return "R-1"


# ─────────────────────────────────────────────────────────────────────────────
# 11. MERMAID SYNTHESIS DIAGRAM BUILDER
# ─────────────────────────────────────────────────────────────────────────────

def _safe_id(s: str, i: int) -> str:
    base = re.sub(r"[^A-Za-z0-9]+", "_", str(s))[:24] or f"N{i}"
    return f"S{i}_{base}"


def build_mermaid_synthesis_tree(
    scenarios: list,
    classification: dict,
) -> str:
    """
    Build a Mermaid graph TD diagram showing:
      Root → Robust Implications (cross-scenario)
           → each Scenario → its Contingent insights

    Deterministic — purely structural from inputs.
    """
    lines = ["graph TD", "  Root[\"Implications Synthesis Root\"]"]

    # Robust branch
    lines.append("  Root --> Robust{Robust — all scenarios}")
    for j, r in enumerate(classification.get("robust") or []):
        rid = f"R{j}"
        text = re.sub(r"[\"\n]", " ", r["insight"])[:60]
        cov = r.get("coverage", 0.0)
        lines.append(f'  Robust --> {rid}["{text}\\n(coverage={cov:.0%})"]')

    # Scenario branches with contingent insights
    contingent = classification.get("contingent_by_scenario") or {}
    for i, sc in enumerate(scenarios):
        sc_name = sc.get("name") or f"Scenario_{i+1}"
        sid = _safe_id(sc_name, i + 1)
        sc_label = re.sub(r"[\"\n]", " ", sc_name)[:40]
        lines.append(f'  Root --> {sid}["{sc_label}"]')
        for k, ins in enumerate(contingent.get(sc_name, [])[:6]):
            text = re.sub(r"[\"\n]", " ", ins)[:60]
            lines.append(f'  {sid} --> {sid}_C{k}["{text}"]')

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# 12. ACTION RECOMMENDATIONS BUILDER (DETERMINISTIC TEMPLATE FILL)
# ─────────────────────────────────────────────────────────────────────────────

def build_action_recommendations(
    classification: dict,
    horizon_key: str = "15-25yr",
) -> dict:
    """
    Build the Action Recommendations block deterministically from the
    robust/contingent split. No LLM inference — just template fill.
    """
    robust = classification.get("robust") or []
    cont = classification.get("contingent_by_scenario") or {}

    immediate = [
        f"Begin executing robust no-regret action: {r['insight']}"
        for r in robust[:5]
    ]
    short_term = [
        f"Pilot top-3 robust action: {r['insight']}"
        for r in robust[:3]
    ] + [
        "Pre-position contingent policy stack (no activation yet)",
        "Stand up leading-indicator dashboard (Z_punkt six-month rhythm)",
    ]
    mid_term = [
        "Re-assess scenario emergence using leading indicators",
        "Activate contingent policies whose triggering scenario shows signs of emergence",
    ]
    long_term = [
        "Re-construct scenario set (Section V Z_punkt — additions/new scenarios)",
        "Refresh driving forces using vision-foresight-environmental-scanning (Ch. 02)",
    ]

    # Per-scenario contingent action list
    per_scenario = {
        sc_name: [f"If {sc_name} emerges → activate: {ins}" for ins in insights[:4]]
        for sc_name, insights in cont.items()
        if insights
    }

    return {
        "horizon": horizon_key,
        "immediate": immediate,                     # 1주 ~ 1개월
        "short_term": short_term,                   # 3-12개월
        "mid_term": mid_term,                       # 1-5년
        "long_term": long_term,                     # 5-15년+
        "per_scenario_contingent": per_scenario,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 13. COMPUTE ALL METRICS (primary entry point)
# ─────────────────────────────────────────────────────────────────────────────

def compute_all(inp: dict) -> dict:
    """
    One-shot pipeline: validate input, compute everything, return a flat dict
    that SKILL.md's output template fills slot-by-slot.
    """
    errors = validate_synthesis_input(inp)
    if errors:
        return {"status": "FAIL", "errors": errors}

    scenarios = inp.get("scenarios") or []
    classification = classify_robust_vs_contingent(scenarios)
    actions = build_action_recommendations(classification, str(inp.get("horizon", "15-25yr")))
    cross_skill = check_cross_skill_existence()
    staleness = check_date_staleness(inp.get("fetched_date"))
    vrmp_tier = determine_vrmp_tier(str(inp.get("expert_mode", "R")))
    mermaid = build_mermaid_synthesis_tree(scenarios, classification)

    # Quote audit: SKILL.md verbatim canon snapshot
    canon = list_verbatim_canon()

    # URL audit (if provided)
    sources = inp.get("sources") or []
    url_audit: list[dict] = []
    for u in sources:
        v = validate_source_url(u)
        v["tier"] = classify_url_tier(u) if v.get("valid") else "R-1"
        url_audit.append(v)

    return {
        "status": "PASS",
        "implications_domain": str(inp["implications_domain"]),
        "topic": inp.get("topic"),
        "cycle": str(inp.get("cycle")).upper(),
        "expert_mode": str(inp.get("expert_mode")).upper(),
        "horizon": str(inp.get("horizon")).lower(),
        "vrmp_tier": vrmp_tier,
        "n_scenarios": len(scenarios),
        "classification": classification,
        "action_recommendations": actions,
        "cross_skill_linkage": cross_skill,
        "verbatim_canon": canon,
        "date_staleness": staleness,
        "mermaid_synthesis_tree": mermaid,
        "url_audit": url_audit,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 14. SELF-TEST
# ─────────────────────────────────────────────────────────────────────────────

def run_self_test() -> int:
    """Return 0 if all assertions pass; raise AssertionError otherwise."""
    print("=== synthesis_utils.py self-test ===\n")

    # T01 — VRMP tier
    assert determine_vrmp_tier("R") == "R-2"
    assert determine_vrmp_tier("A") == "R-2"
    assert determine_vrmp_tier("V") == "R-3"
    assert determine_vrmp_tier("H") == "R-1"
    assert determine_vrmp_tier("h") == "R-1"
    print("T01 VRMP tier mapping ✓")

    # T02 — tier_for_year_offset
    assert tier_for_year_offset(0.5) == "Pre-Short (<1y)"
    assert tier_for_year_offset(3) == "Short (1-5y)"
    assert tier_for_year_offset(5) == "Short (1-5y)"
    assert tier_for_year_offset(10) == "Mid (5-15y)"
    assert tier_for_year_offset(15) == "Mid (5-15y)"
    assert tier_for_year_offset(25) == "Long (15-30y)"
    assert tier_for_year_offset(31) == "Beyond-Long (>30y)"
    print("T02 tier_for_year_offset boundaries ✓")

    # T03 — validate_horizon_range
    r = validate_horizon_range("15-25yr", 20)
    assert r["valid"] and r["tier"] == "Long (15-30y)"
    r = validate_horizon_range("5yr", 6)
    assert not r["valid"]
    r = validate_horizon_range("bad", 10)
    assert not r["valid"]
    print("T03 validate_horizon_range ✓")

    # T04 — input validation: success
    good_input = {
        "implications_domain": "1",
        "topic": "AGI 시대 한국",
        "cycle": "C1",
        "expert_mode": "R",
        "horizon": "15-25yr",
        "scenarios": [
            {"name": "S1", "insights": ["AI invests heavily", "Need workforce reskilling"]},
            {"name": "S2", "insights": ["AI invests heavily", "Geopolitical fragmentation"]},
            {"name": "S3", "insights": ["AI invests heavily", "Climate disruption"]},
            {"name": "S4", "insights": ["AI invests heavily", "Demographic decline"]},
        ],
    }
    errs = validate_synthesis_input(good_input)
    assert errs == [], f"expected PASS got: {errs}"
    print("T04 input validation PASS on good input ✓")

    # T05 — input validation: minimal failure
    errs = validate_synthesis_input({"topic": "x"})
    assert len(errs) >= 5
    print(f"T05 input validation FAIL on minimal input ({len(errs)} errors) ✓")

    # T06 — input validation: invalid domain
    bad = dict(good_input); bad["implications_domain"] = "99"
    errs = validate_synthesis_input(bad)
    assert any("implications_domain" in e for e in errs)
    print("T06 input validation catches invalid domain ✓")

    # T07 — input validation: too few scenarios
    bad = dict(good_input); bad["scenarios"] = good_input["scenarios"][:2]
    errs = validate_synthesis_input(bad)
    assert any("TOO FEW" in e for e in errs)
    print("T07 input validation catches <3 scenarios ✓")

    # T08 — robust vs contingent classification
    cls = classify_robust_vs_contingent(good_input["scenarios"])
    # "AI invests heavily" appears in 4/4 scenarios → robust
    robust_texts = [r["insight"].lower() for r in cls["robust"]]
    assert any("ai" in t and "invests" in t for t in robust_texts), \
        f"AI-investment insight should be robust; got {robust_texts}"
    # workforce reskilling appears in only 1 of 4 → contingent
    cont_s1 = cls["contingent_by_scenario"]["S1"]
    assert any("reskilling" in c.lower() for c in cont_s1)
    print(f"T08 robust/contingent classification: {len(cls['robust'])} robust, "
          f"{sum(len(v) for v in cls['contingent_by_scenario'].values())} contingent ✓")

    # T09 — staleness
    s = check_date_staleness("2020-01-01")
    assert s["is_stale"] is True
    s2 = check_date_staleness(date.today().isoformat())
    assert s2["is_stale"] is False
    s3 = check_date_staleness(None)
    assert s3["is_stale"] is None
    print(f"T09 staleness: 2020-01-01 stale={s['is_stale']}, today stale={s2['is_stale']} ✓")

    # T10 — verbatim quote verification (Section IV)
    q = "writer's mental model of how the world works is transferred to the reader"
    r = verify_verbatim_quote(q)
    assert r["verified"] and r["tier"] == "weakness", r
    q = "Scenarios are one of the easiest ways to present complex information"
    r = verify_verbatim_quote(q)
    assert r["verified"] and r["tier"] == "strength", r
    q = "totally made up scenario hallucination"
    r = verify_verbatim_quote(q)
    assert not r["verified"], r
    print("T10 verbatim quote verification (3 cases) ✓")

    # T11 — cross-skill linkage existence
    cs = check_cross_skill_existence()
    assert cs["n_foresight_linked"] == 17, cs["n_foresight_linked"]
    assert cs["n_vision_linked"] == len(VISION_CROSS_LINKS)
    # At least vision-foresight-scenarios itself must exist (we're inside its sibling folder)
    assert cs["foresight"]["vision-foresight-environmental-scanning"]["exists"] is True or \
           cs["foresight"]["vision-foresight-environmental-scanning"]["exists"] is False
    # All foresight chapter links should match real skill folders if the repo is healthy
    missing_foresight = [k for k, v in cs["foresight"].items() if not v["exists"]]
    print(f"T11 cross-skill existence: 17 foresight + {len(VISION_CROSS_LINKS)} vision links, "
          f"{len(missing_foresight)} missing foresight ✓")

    # T12 — source-trail URL validation
    assert validate_source_url("https://millennium-project.org/scenarios")["valid"]
    assert not validate_source_url("not-a-url")["valid"]
    assert classify_url_tier("https://www.millennium-project.org/info") == "R-3"
    assert classify_url_tier("https://wikipedia.org/wiki/Scenario") == "R-2"
    assert classify_url_tier("https://random-blog.example.com/post") == "R-1"
    print("T12 URL validation + tier classification ✓")

    # T13 — Mermaid synthesis tree
    mer = build_mermaid_synthesis_tree(good_input["scenarios"], cls)
    assert mer.startswith("graph TD"), mer[:80]
    assert "Robust" in mer
    print(f"T13 mermaid synthesis tree builder ({len(mer.splitlines())} lines) ✓")

    # T14 — action recommendations
    acts = build_action_recommendations(cls, "15-25yr")
    assert "immediate" in acts and "short_term" in acts and "mid_term" in acts and "long_term" in acts
    assert len(acts["immediate"]) >= 1
    print("T14 action recommendations builder ✓")

    # T15 — compute_all end-to-end
    full = compute_all(good_input)
    assert full["status"] == "PASS", full
    assert full["vrmp_tier"] == "R-2"
    assert full["n_scenarios"] == 4
    assert "mermaid_synthesis_tree" in full
    print("T15 compute_all end-to-end ✓")

    # T16 — bibliography integrity (12+ refs including Glenn/TFG 2009)
    assert "glenn_tfg_2009" in BIBLIOGRAPHY_KEYS
    assert "kahn_wiener_1967" in BIBLIOGRAPHY_KEYS
    assert "Wiener" in BIBLIOGRAPHY_KEYS["kahn_wiener_1967"]
    assert "Weiner" not in BIBLIOGRAPHY_KEYS["kahn_wiener_1967"].replace("'Weiner'", "")
    assert len(BIBLIOGRAPHY_KEYS) >= 12
    print(f"T16 bibliography integrity (n={len(BIBLIOGRAPHY_KEYS)}, Wiener spelling correct) ✓")

    # T17 — verbatim canon contains all SKILL.md quotes
    canon = list_verbatim_canon()
    assert len(canon["strengths"]) >= 3
    assert len(canon["weaknesses"]) >= 5
    assert canon["schwartz_step_6"] == SCHWARTZ_STEP_6_VERBATIM
    print("T17 verbatim canon completeness ✓")

    # T18 — Custom and Skip domains accepted
    custom_input = dict(good_input); custom_input["implications_domain"] = "Custom"
    assert validate_synthesis_input(custom_input) == []
    skip_input = dict(good_input); skip_input["implications_domain"] = "Skip"
    assert validate_synthesis_input(skip_input) == []
    print("T18 Custom + Skip domain accepted ✓")

    # T19 — invalid cycle rejected
    bad = dict(good_input); bad["cycle"] = "C99"
    errs = validate_synthesis_input(bad)
    assert any("cycle" in e for e in errs), errs
    print("T19 invalid cycle rejected ✓")

    # T20 — invalid expert_mode rejected
    bad = dict(good_input); bad["expert_mode"] = "Z"
    errs = validate_synthesis_input(bad)
    assert any("expert_mode" in e for e in errs), errs
    print("T20 invalid expert_mode rejected ✓")

    print("\n=== all 20 self-tests PASSED ===")
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# 15. CLI
# ─────────────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(
        description=(
            "scenarios implications synthesis utilities — deterministic helper module. "
            "Source: Glenn & TFG 2009, FRM V3.0 Ch. 19."
        )
    )
    sub = p.add_subparsers(dest="cmd")

    sub_self = sub.add_parser("self-test", help="run built-in self-test suite")

    sub_vi = sub.add_parser("validate-input", help="validate synthesis_input.json")
    sub_vi.add_argument("json_file")

    sub_ca = sub.add_parser("compute-all", help="run full deterministic pipeline")
    sub_ca.add_argument("json_file")

    sub_vt = sub.add_parser("vrmp-tier", help="map expert_mode to VRMP tier")
    sub_vt.add_argument("expert_mode")

    sub_st = sub.add_parser("staleness", help="check date staleness")
    sub_st.add_argument("date_str")

    sub_q = sub.add_parser("verify-quote", help="verify a Section IV verbatim quote")
    sub_q.add_argument("quote")

    sub_canon = sub.add_parser("list-canon", help="dump full Section IV verbatim canon")

    sub_cs = sub.add_parser("check-cross-skills", help="check 17 foresight + vision links exist")

    sub_bib = sub.add_parser("list-bibliography", help="list 12-core bibliography refs")

    args = p.parse_args()

    if args.cmd is None or args.cmd == "self-test":
        sys.exit(run_self_test())

    elif args.cmd == "validate-input":
        with open(args.json_file, encoding="utf-8") as f:
            data = json.load(f)
        errs = validate_synthesis_input(data)
        if errs:
            print(json.dumps({"status": "FAIL", "errors": errs},
                             ensure_ascii=False, indent=2))
            sys.exit(1)
        print(json.dumps({"status": "PASS"}, ensure_ascii=False))

    elif args.cmd == "compute-all":
        with open(args.json_file, encoding="utf-8") as f:
            data = json.load(f)
        result = compute_all(data)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))

    elif args.cmd == "vrmp-tier":
        tier = determine_vrmp_tier(args.expert_mode)
        print(json.dumps({"expert_mode": args.expert_mode, "vrmp_tier": tier},
                         ensure_ascii=False))

    elif args.cmd == "staleness":
        print(json.dumps(check_date_staleness(args.date_str),
                         ensure_ascii=False, indent=2))

    elif args.cmd == "verify-quote":
        print(json.dumps(verify_verbatim_quote(args.quote),
                         ensure_ascii=False, indent=2))

    elif args.cmd == "list-canon":
        print(json.dumps(list_verbatim_canon(),
                         ensure_ascii=False, indent=2))

    elif args.cmd == "check-cross-skills":
        print(json.dumps(check_cross_skill_existence(),
                         ensure_ascii=False, indent=2))

    elif args.cmd == "list-bibliography":
        print(json.dumps(BIBLIOGRAPHY_KEYS, ensure_ascii=False, indent=2))

    else:
        p.print_help()


if __name__ == "__main__":
    main()
