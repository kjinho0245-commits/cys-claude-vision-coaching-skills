#!/usr/bin/env python3
"""
focal_issue_utils.py — 결정론 상수·검증 함수 (Focal Issue Definition 전용).

Sources (frozen):
  - Glenn, J.C. & TFG (2009). "Scenarios." In Glenn, J.C. (Ed.),
    Futures Research Methodology V3.0, Ch.19. The Millennium Project.
    (Section III — Schwartz 6-step Step 1 + Bishop SRI/Shell/GBN workshop
    + Section III Key Points verbatim.)
  - Schwartz, P. (1991). The Art of the Long View. Doubleday/Currency.
  - Schwartz, P. (1992) cited in Glenn & TFG V3.0 Ch.19.

결정론 환원 (LLM 자연어 재추론 금지):
  - PDF verbatim quotes (5 keys + aliases)
  - Schwartz 6+1 steps (Glenn extension flagged as Step 7)
  - Bishop 3 questions (verbatim, with [domain] and [T years] placeholders)
  - Schwartz planning questions (verbatim from Key Points)
  - Time-horizon enumeration (5yr / 10yr / 15-25yr DEFAULT / 30yr+)
  - Spatial-scope enumeration (Local / National / Regional / Global)
  - Stakeholder role taxonomy (affected · decides · acts)
  - 6 fixed personas for Bishop aggregation (P1..P6) + Devil's Advocate optional P7..P8
  - Sharpening test (5 deterministic checks)
  - Single-statement template structural validator
  - Bibliography (frozen)
  - Self-test (ALL_PASS)

Usage:
  python3 focal_issue_utils.py validate
  python3 focal_issue_utils.py verbatim KEY
  python3 focal_issue_utils.py verbatim_all
  python3 focal_issue_utils.py schwartz_step N
  python3 focal_issue_utils.py schwartz_all
  python3 focal_issue_utils.py bishop_questions [DOMAIN] [T]
  python3 focal_issue_utils.py schwartz_planning_questions
  python3 focal_issue_utils.py time_horizons
  python3 focal_issue_utils.py validate_horizon HORIZON
  python3 focal_issue_utils.py spatial_scopes
  python3 focal_issue_utils.py validate_scope SCOPE
  python3 focal_issue_utils.py stakeholder_roles
  python3 focal_issue_utils.py personas
  python3 focal_issue_utils.py sharpening_test "FOCAL ISSUE RAW"
  python3 focal_issue_utils.py validate_statement "STATEMENT"
  python3 focal_issue_utils.py bibliography
"""

from __future__ import annotations

import json
import re
import sys
from typing import Any

# ════════════════════════════════════════════════════════════════════════════
# PRIMARY SOURCES
# ════════════════════════════════════════════════════════════════════════════

PRIMARY_SOURCE = (
    "Glenn J.C. & TFG (2009). 'Scenarios.' In Glenn, J.C. (Ed.), "
    "Futures Research Methodology V3.0, Ch.19. The Millennium Project."
)

SCHWARTZ_1991 = (
    "Schwartz P. (1991). The Art of the Long View: Planning for the Future in "
    "an Uncertain World. Doubleday/Currency."
)

BISHOP_SOURCE = (
    "Peter Bishop — SRI/Shell/GBN workshop questions, "
    "as cited in Glenn & TFG (2009) V3.0 Ch.19 Section III."
)

# ════════════════════════════════════════════════════════════════════════════
# PDF VERBATIM QUOTES — Section III (Schwartz Step 1, Bishop, Key Points)
# ════════════════════════════════════════════════════════════════════════════

PDF_VERBATIM = {
    "schwartz_step1": (
        "identify the focal issue or decision"
    ),
    "schwartz_six_steps_list": (
        "These steps include: identify the focal issue or decision; "
        "identify the key forces and trends in the environment; rank the "
        "driving forces and trends by importance and uncertainty; select "
        "the scenario logics; fill out the scenarios; assess the implications; "
        "and select the leading indicators and signposts for monitoring purposes."
    ),
    "bishop_workshop": (
        "asking focused questions—such as, 'What is the most important issue "
        "concerning [domain] over the next 10 years?' 'What will stay the same "
        "about this issue that will limit its alternative futures?' 'What is "
        "changing about this issue that will alter its future?'—Bishop sets up "
        "the scenarios and develops the scenario logic."
    ),
    "key_points_sharply_focused": (
        "The most useful scenarios are sharply focused. They focus on critical "
        "issues facing the organization."
    ),
    "key_points_define_focus": (
        "Without a clear direction, the discussion of drivers is difficult to "
        "limit. The number of alternative worlds expands exponentially, and the "
        "list of variables can become unworkably long. The best defense is to "
        "define the focus from the outset."
    ),
    "key_points_planning_questions": (
        "Ask yourself: 'What planning questions need to be addressed? What "
        "variables are we most likely to forecast in order to address these "
        "concerns?'"
    ),
}

PDF_VERBATIM_SOURCES = {
    "schwartz_step1": (
        "Schwartz (1991) Step 1 — as cited in Glenn & TFG (2009) V3.0 Ch.19 "
        "Section III"
    ),
    "schwartz_six_steps_list": (
        "Glenn & TFG (2009) V3.0 Ch.19 Section III verbatim — Schwartz 6 steps "
        "+ Glenn extension (Step 7 indicators)"
    ),
    "bishop_workshop": (
        "Glenn & TFG (2009) V3.0 Ch.19 Section III — Bishop SRI/Shell/GBN "
        "workshop verbatim"
    ),
    "key_points_sharply_focused": (
        "Glenn & TFG (2009) V3.0 Ch.19 Section III Key Points verbatim"
    ),
    "key_points_define_focus": (
        "Glenn & TFG (2009) V3.0 Ch.19 Section III Key Points verbatim"
    ),
    "key_points_planning_questions": (
        "Glenn & TFG (2009) V3.0 Ch.19 Section III Key Points verbatim"
    ),
}

VERBATIM_ALIASES = {
    "step1": "schwartz_step1",
    "step_1": "schwartz_step1",
    "schwartz_step_1": "schwartz_step1",
    "focal": "schwartz_step1",
    "focal_issue": "schwartz_step1",
    "schwartz": "schwartz_step1",
    "decision": "schwartz_step1",
    "six_steps": "schwartz_six_steps_list",
    "6_steps": "schwartz_six_steps_list",
    "seven_steps": "schwartz_six_steps_list",
    "7_steps": "schwartz_six_steps_list",
    "schwartz_list": "schwartz_six_steps_list",
    "all_steps": "schwartz_six_steps_list",
    "bishop": "bishop_workshop",
    "bishop_questions": "bishop_workshop",
    "workshop": "bishop_workshop",
    "sharply_focused": "key_points_sharply_focused",
    "sharp": "key_points_sharply_focused",
    "sharpness": "key_points_sharply_focused",
    "define_focus": "key_points_define_focus",
    "best_defense": "key_points_define_focus",
    "exponential": "key_points_define_focus",
    "planning": "key_points_planning_questions",
    "planning_questions": "key_points_planning_questions",
    "variables_to_forecast": "key_points_planning_questions",
}


def get_pdf_verbatim(key: str) -> dict:
    """Return PDF verbatim quote by key (with alias resolution)."""
    if not isinstance(key, str):
        return {"valid": False, "error": "key must be string."}
    norm = re.sub(r"[^a-z0-9_]+", "_", key.strip().lower()).strip("_")
    resolved = VERBATIM_ALIASES.get(norm, norm)
    if resolved in PDF_VERBATIM:
        return {
            "valid": True,
            "key": resolved,
            "verbatim": PDF_VERBATIM[resolved],
            "source": PDF_VERBATIM_SOURCES[resolved],
        }
    return {
        "valid": False,
        "error": f"Key '{key}' not found.",
        "valid_keys": list(PDF_VERBATIM.keys()),
        "alias_keys": list(VERBATIM_ALIASES.keys()),
    }


# ════════════════════════════════════════════════════════════════════════════
# SCHWARTZ 6 STEPS + GLENN EXTENSION (Step 7)
# ════════════════════════════════════════════════════════════════════════════

SCHWARTZ_STEPS = {
    1: {
        "description": "Identify the focal issue or decision",
        "source": "Schwartz (1991) Step 1",
        "current_skill_step": True,
    },
    2: {
        "description": "Identify the key forces and trends in the environment",
        "source": "Schwartz (1991) Step 2",
        "current_skill_step": False,
    },
    3: {
        "description": (
            "Rank the driving forces and trends by importance and uncertainty"
        ),
        "source": "Schwartz (1991) Step 3",
        "current_skill_step": False,
    },
    4: {
        "description": "Select the scenario logics",
        "source": "Schwartz (1991) Step 4",
        "current_skill_step": False,
    },
    5: {
        "description": "Fill out the scenarios",
        "source": "Schwartz (1991) Step 5",
        "current_skill_step": False,
    },
    6: {
        "description": "Assess the implications",
        "source": "Schwartz (1991) Step 6",
        "current_skill_step": False,
    },
    7: {
        "description": (
            "Select the leading indicators and signposts for monitoring purposes"
        ),
        "source": (
            "Glenn extension — added in Glenn & TFG (2009) V3.0 Ch.19. "
            "NOT in original Schwartz (1991) 6-step. Attribution must remain "
            "separate per parent SKILL.md §6."
        ),
        "current_skill_step": False,
        "glenn_extension": True,
    },
}

SCHWARTZ_STEPS_SOURCE = (
    "Schwartz P. (1991). The Art of the Long View. Doubleday/Currency. "
    "(Steps 1-6) + Glenn extension Step 7 (Glenn & TFG 2009 V3.0 Ch.19)"
)

CURRENT_SKILL_STEP_NUMBER = 1


def get_schwartz_step(n: int) -> dict:
    """Return Schwartz Step N definition (1-7)."""
    if not isinstance(n, int):
        return {"valid": False, "error": "step number must be int."}
    if n not in SCHWARTZ_STEPS:
        return {
            "valid": False,
            "error": f"Step {n} not found. Valid: 1-7.",
        }
    entry = dict(SCHWARTZ_STEPS[n])
    entry["step"] = n
    entry["valid"] = True
    return entry


# ════════════════════════════════════════════════════════════════════════════
# BISHOP 3 QUESTIONS — verbatim with [domain] and [T years] placeholders
# ════════════════════════════════════════════════════════════════════════════

BISHOP_QUESTIONS = {
    1: {
        "label": "Most important issue",
        "template": (
            "What is the most important issue concerning [domain] over the "
            "next [T] years?"
        ),
        "source": BISHOP_SOURCE,
    },
    2: {
        "label": "What stays the same (limits)",
        "template": (
            "What will stay the same about this issue that will limit its "
            "alternative futures?"
        ),
        "source": BISHOP_SOURCE,
    },
    3: {
        "label": "What is changing (alters)",
        "template": (
            "What is changing about this issue that will alter its future?"
        ),
        "source": BISHOP_SOURCE,
    },
}


def fill_bishop_questions(domain: str | None = None,
                          horizon: str | None = None) -> dict:
    """Return Bishop 3 questions with [domain] and [T] substituted (if given).

    Substitution is *literal*. The placeholders [domain] and [T] (with or
    without surrounding spaces) are the only tokens replaced.
    """
    out = {}
    domain_value = domain if (isinstance(domain, str) and domain.strip()) else "[domain]"
    horizon_value = horizon if (isinstance(horizon, str) and horizon.strip()) else "[T]"
    for n, entry in BISHOP_QUESTIONS.items():
        tpl = entry["template"]
        filled = tpl.replace("[domain]", domain_value).replace("[T]", horizon_value)
        out[n] = {
            "label": entry["label"],
            "question": filled,
            "template": tpl,
            "source": entry["source"],
        }
    return {"valid": True, "questions": out, "domain": domain_value, "horizon": horizon_value}


# ════════════════════════════════════════════════════════════════════════════
# SCHWARTZ PLANNING QUESTIONS — Section III Key Points verbatim + Q6 extension
# ════════════════════════════════════════════════════════════════════════════

SCHWARTZ_PLANNING_QUESTIONS = {
    4: {
        "label": "Planning questions to address",
        "question": "What planning questions need to be addressed?",
        "source": (
            "Glenn & TFG (2009) V3.0 Ch.19 Section III Key Points verbatim "
            "(Schwartz 1991)"
        ),
        "verbatim": True,
    },
    5: {
        "label": "Variables to forecast",
        "question": (
            "What variables are we most likely to forecast in order to "
            "address these concerns?"
        ),
        "source": (
            "Glenn & TFG (2009) V3.0 Ch.19 Section III Key Points verbatim "
            "(Schwartz 1991)"
        ),
        "verbatim": True,
    },
    6: {
        "label": "Decisions hinging on the answer",
        "question": "What decisions hinge on the answer?",
        "source": (
            "Operational extension of Schwartz Step 1 'identify the focal "
            "issue or decision' — added in current SKILL.md to make "
            "decision-relevance explicit. NOT a PDF verbatim quote."
        ),
        "verbatim": False,
    },
}


# ════════════════════════════════════════════════════════════════════════════
# TIME HORIZON ENUM (matches parent SKILL.md §3 Step 0)
# ════════════════════════════════════════════════════════════════════════════

TIME_HORIZONS = {
    "5yr": {
        "label": "5 years (short-term)",
        "years_min": 5,
        "years_max": 5,
        "default": False,
        "source": "Parent vision-foresight-scenarios SKILL.md §3 Step 0",
    },
    "10yr": {
        "label": "10 years",
        "years_min": 10,
        "years_max": 10,
        "default": False,
        "source": "Parent vision-foresight-scenarios SKILL.md §3 Step 0",
    },
    "15-25yr": {
        "label": "15-25 years (DEFAULT)",
        "years_min": 15,
        "years_max": 25,
        "default": True,
        "source": "Parent vision-foresight-scenarios SKILL.md §3 Step 0 DEFAULT",
    },
    "30yr+": {
        "label": "30+ years (long-term, Millennium 2050 양식)",
        "years_min": 30,
        "years_max": None,
        "default": False,
        "source": "Parent vision-foresight-scenarios SKILL.md §3 Step 0",
    },
}


def validate_time_horizon(value: str) -> dict:
    """Validate a horizon string against the canonical enum.

    Bucketing rule (deterministic):
      - canonical key match wins first
      - any positive integer N years → bucket by years:
          1-7  → '5yr'
          8-12 → '10yr'
          13-27 → '15-25yr' (DEFAULT bucket)
          28+ → '30yr+'
      - common text aliases ('default', 'long', 'short')
    Returns canonical bucket + the years extracted (if numeric).
    """
    if not isinstance(value, str):
        return {"valid": False, "error": "horizon must be string."}
    raw = value.strip()
    key = raw.lower().replace(" ", "")
    text_aliases = {
        "default": "15-25yr",
        "short": "5yr",
        "shortterm": "5yr",
        "short-term": "5yr",
        "medium": "10yr",
        "long": "30yr+",
        "longterm": "30yr+",
        "long-term": "30yr+",
    }
    if key in text_aliases:
        canon = text_aliases[key]
        return {"valid": True, "canonical": canon, "input": value,
                "years_extracted": None, **TIME_HORIZONS[canon]}
    if key in TIME_HORIZONS:
        return {"valid": True, "canonical": key, "input": value,
                "years_extracted": None, **TIME_HORIZONS[key]}
    # Extract integer years from forms like "17yr", "17 years", "17년", "by 2040".
    # Order: 'by 20XX' year-target form takes precedence (more specific) over
    # bare integer-years form.
    years = None
    m_by = re.search(r"(?:by)?20(\d{2})", key)
    if m_by:
        future_year = 2000 + int(m_by.group(1))
        delta = future_year - 2026
        if delta > 0:
            years = delta
    if years is None:
        m_yr = re.search(r"(\d{1,3})\s*(?:yr|year|years|년)\b", key)
        if m_yr:
            n = int(m_yr.group(1))
            if 1 <= n <= 200:
                years = n
        else:
            # bare leading-integer fallback ("17", "8")
            m_bare = re.match(r"^(\d{1,3})$", key)
            if m_bare:
                n = int(m_bare.group(1))
                if 1 <= n <= 200:
                    years = n
    if years is None:
        return {
            "valid": False,
            "input": value,
            "error": (
                f"Horizon '{value}' could not be parsed. "
                f"Canonical: {list(TIME_HORIZONS.keys())}; or specify an integer N years."
            ),
        }
    if 1 <= years <= 7:
        canon = "5yr"
    elif 8 <= years <= 12:
        canon = "10yr"
    elif 13 <= years <= 27:
        canon = "15-25yr"
    elif years >= 28:
        canon = "30yr+"
    else:
        return {
            "valid": False,
            "input": value,
            "error": f"Years value {years} out of supported range.",
        }
    return {
        "valid": True,
        "canonical": canon,
        "input": value,
        "years_extracted": years,
        "bucketing_rule": "1-7→5yr · 8-12→10yr · 13-27→15-25yr · 28+→30yr+",
        **TIME_HORIZONS[canon],
    }


# ════════════════════════════════════════════════════════════════════════════
# SPATIAL SCOPE ENUM
# ════════════════════════════════════════════════════════════════════════════

SPATIAL_SCOPES = {
    "Local": {
        "label": "Local — city·county·district level",
        "source": "TFG scenario space convention; Glenn & TFG (2009) V3.0 Ch.19",
    },
    "National": {
        "label": "National — single country",
        "source": "TFG scenario space convention; Glenn & TFG (2009) V3.0 Ch.19",
    },
    "Regional": {
        "label": "Regional — multi-country (e.g., East Asia, EU)",
        "source": "TFG scenario space convention; Glenn & TFG (2009) V3.0 Ch.19",
    },
    "Global": {
        "label": "Global — worldwide (Millennium Project 양식)",
        "source": (
            "Millennium Project Futures Matrix global scope; "
            "Glenn & TFG (2009) V3.0 Ch.19"
        ),
    },
}


def validate_spatial_scope(value: str) -> dict:
    if not isinstance(value, str):
        return {"valid": False, "error": "scope must be string."}
    key = value.strip().title()
    aliases = {
        "City": "Local",
        "Municipal": "Local",
        "County": "Local",
        "District": "Local",
        "Country": "National",
        "Nation": "National",
        "Continental": "Regional",
        "Multi-Country": "Regional",
        "Multinational": "Regional",
        "Worldwide": "Global",
        "World": "Global",
        "International": "Global",
    }
    canon = aliases.get(key, key)
    if canon in SPATIAL_SCOPES:
        return {
            "valid": True,
            "canonical": canon,
            "input": value,
            **SPATIAL_SCOPES[canon],
        }
    return {
        "valid": False,
        "input": value,
        "error": (
            f"Scope '{value}' not in enum. "
            f"Valid: {list(SPATIAL_SCOPES.keys())}"
        ),
    }


# ════════════════════════════════════════════════════════════════════════════
# STAKEHOLDER ROLE TAXONOMY
# ════════════════════════════════════════════════════════════════════════════

STAKEHOLDER_ROLES = {
    "affected": {
        "label": "Those affected by the outcome",
        "description": (
            "Stakeholders whose well-being, livelihood, or interests are "
            "materially affected by how the focal issue resolves."
        ),
        "examples": [
            "Citizens", "End users", "Local communities", "Future generations",
        ],
    },
    "decides": {
        "label": "Those who make the decision(s)",
        "description": (
            "Stakeholders who hold formal authority over the policy, "
            "investment, or strategic choice in scope."
        ),
        "examples": [
            "Policymakers", "Board / executive leadership", "Regulators",
            "Standards bodies",
        ],
    },
    "acts": {
        "label": "Those who execute / implement",
        "description": (
            "Stakeholders whose actions translate the decision into outcomes "
            "(may differ from those who decide)."
        ),
        "examples": [
            "Operators", "Frontline staff", "Suppliers / contractors",
            "Civil society", "Researchers",
        ],
    },
}


def validate_stakeholders(stakeholders: Any) -> dict:
    """Verify a stakeholder list provides at least one entry per role.

    Accepts a dict {role: [name, ...]} OR a list of dicts
    [{"name": ..., "role": "affected"|"decides"|"acts"}].
    """
    valid_roles = set(STAKEHOLDER_ROLES.keys())
    role_index: dict[str, list[str]] = {r: [] for r in valid_roles}
    if isinstance(stakeholders, dict):
        for role, items in stakeholders.items():
            r = role.strip().lower()
            if r not in valid_roles:
                return {
                    "valid": False,
                    "error": f"Unknown role '{role}'. Valid: {sorted(valid_roles)}",
                }
            if not isinstance(items, list):
                return {"valid": False, "error": f"Role '{role}' value must be list."}
            for it in items:
                if isinstance(it, str) and it.strip():
                    role_index[r].append(it.strip())
    elif isinstance(stakeholders, list):
        for entry in stakeholders:
            if not isinstance(entry, dict):
                return {"valid": False, "error": f"List entry not dict: {entry!r}"}
            name = entry.get("name", "")
            role = str(entry.get("role", "")).strip().lower()
            if role not in valid_roles:
                return {
                    "valid": False,
                    "error": f"Entry '{name}' role '{role}' invalid. Valid: {sorted(valid_roles)}",
                }
            if isinstance(name, str) and name.strip():
                role_index[role].append(name.strip())
    else:
        return {
            "valid": False,
            "error": "stakeholders must be dict or list.",
        }
    missing = [r for r, lst in role_index.items() if not lst]
    return {
        "valid": not missing,
        "missing_roles": missing,
        "by_role": role_index,
        "note": (
            "All three roles (affected · decides · acts) should have at least "
            "one stakeholder to fully scope the focal issue."
        ),
    }


# ════════════════════════════════════════════════════════════════════════════
# 8 FIXED PERSONAS for Bishop aggregation
# ════════════════════════════════════════════════════════════════════════════
# Six core domain personas + Devil's Advocate + Scenario Specialist.
# Parent SKILL.md text mentioned "6-8 personas" without listing — frozen here.

PERSONAS = [
    {
        "id": "P1",
        "name": "Domain Insider",
        "role": (
            "Names the most important *internal* issue inside the focal domain "
            "(industry, sector, organization)."
        ),
        "source_link": (
            "Bishop SRI/Shell/GBN — 'most important issue concerning [domain]'; "
            "internal axis"
        ),
    },
    {
        "id": "P2",
        "name": "Policy Analyst",
        "role": (
            "Names political/regulatory/governance dimensions of the focal "
            "issue."
        ),
        "source_link": "STEEPS Political domain",
    },
    {
        "id": "P3",
        "name": "Technology Forecaster",
        "role": (
            "Names technological dimensions that will reshape the focal issue."
        ),
        "source_link": "STEEPS Technological domain",
    },
    {
        "id": "P4",
        "name": "Economist",
        "role": (
            "Names macro/sectoral economic dimensions of the focal issue."
        ),
        "source_link": "STEEPS Economic domain",
    },
    {
        "id": "P5",
        "name": "Sociologist / Anthropologist",
        "role": (
            "Names social, cultural, demographic dimensions of the focal "
            "issue."
        ),
        "source_link": "STEEPS Social domain",
    },
    {
        "id": "P6",
        "name": "Environmental Scientist",
        "role": (
            "Names environmental, ecological, climate dimensions of the focal "
            "issue."
        ),
        "source_link": "STEEPS Environmental domain",
    },
    {
        "id": "P7",
        "name": "Scenario Specialist",
        "role": (
            "Cross-cuts the other personas; applies Schwartz Step 1 "
            "discipline (sharply focused, decision-relevant)."
        ),
        "source_link": "Schwartz (1991) The Art of the Long View Step 1",
    },
    {
        "id": "P8",
        "name": "Devil's Advocate",
        "role": (
            "Challenges scope assumptions; surfaces overlooked stakeholders, "
            "horizons, or framings."
        ),
        "source_link": "Standard scenario planning wild-card persona",
    },
]

PERSONA_AGGREGATION_RULE = {
    "min_personas": 6,
    "max_personas": 8,
    "default_personas": 6,
    "step1": "Each persona answers Bishop Q1, Q2, Q3 with one sentence per Q.",
    "step2": "Union of answers per Q, then de-duplicate (case-insensitive normalized).",
    "step3": "Group near-synonyms; surface dissent as separate items (do NOT silently average).",
    "step4": "Final aggregated answer per Q = 1-3 sentences capturing dominant themes + dissent.",
    "note": (
        "Aggregation must NOT erase divergent views. Devil's Advocate dissent "
        "is preserved verbatim if present."
    ),
}


def validate_persona_count(n: int) -> dict:
    if not isinstance(n, int):
        return {"valid": False, "error": "n must be int."}
    in_range = (
        PERSONA_AGGREGATION_RULE["min_personas"]
        <= n
        <= PERSONA_AGGREGATION_RULE["max_personas"]
    )
    return {
        "valid": in_range,
        "n": n,
        "min": PERSONA_AGGREGATION_RULE["min_personas"],
        "max": PERSONA_AGGREGATION_RULE["max_personas"],
        "default": PERSONA_AGGREGATION_RULE["default_personas"],
        "warning": (
            None if in_range else
            f"Persona count {n} outside [{PERSONA_AGGREGATION_RULE['min_personas']}, "
            f"{PERSONA_AGGREGATION_RULE['max_personas']}]"
        ),
    }


# ════════════════════════════════════════════════════════════════════════════
# SHARPENING TEST — 5 deterministic checks
# ════════════════════════════════════════════════════════════════════════════

SHARPENING_RULES = {
    "min_words": 3,
    "max_words": 60,
    "min_chars": 12,
    "max_chars": 400,
    "banned_vague_tokens": [
        # English vague openers / fillers that signal an unfocused issue.
        "everything", "anything", "stuff", "things in general",
        "the future", "future in general",
        # Korean equivalents commonly used in non-focused issues.
        "모든 것", "모든것", "전반적으로", "막연한", "잘 모르겠",
    ],
    "must_have_domain_signal": True,
    "note": (
        "Sharpness criteria operationalized for Section III Key Points: "
        "'The most useful scenarios are sharply focused' + "
        "'define the focus from the outset'."
    ),
    "source": "Glenn & TFG (2009) V3.0 Ch.19 Section III Key Points",
}


def _count_words(text: str) -> int:
    return len([w for w in re.split(r"\s+", text.strip()) if w])


def sharpening_test(raw_focal_issue: str) -> dict:
    """Deterministic sharpening checks on raw focal issue text.

    Returns pass/fail per rule and an overall verdict. LLM does NOT
    re-judge these rules with natural language.
    """
    if not isinstance(raw_focal_issue, str):
        return {"valid": False, "error": "raw_focal_issue must be string."}
    txt = raw_focal_issue.strip()
    if not txt:
        return {
            "valid": False,
            "error": "Empty focal issue.",
            "overall_pass": False,
        }
    words = _count_words(txt)
    chars = len(txt)
    lower = txt.lower()
    banned_hits = [
        tok for tok in SHARPENING_RULES["banned_vague_tokens"]
        if tok in lower
    ]
    word_pass = (
        SHARPENING_RULES["min_words"] <= words <= SHARPENING_RULES["max_words"]
    )
    char_pass = (
        SHARPENING_RULES["min_chars"] <= chars <= SHARPENING_RULES["max_chars"]
    )
    vague_pass = not banned_hits
    # Domain signal: must contain at least one capitalized proper noun OR
    # a domain word longer than 4 chars. This is a structural check, not a
    # semantic one — LLM does the semantic refinement downstream.
    has_proper = bool(re.search(r"\b[A-Z][a-zA-Z0-9가-힣]{2,}", txt))
    has_long_token = any(len(w) >= 4 for w in re.split(r"\s+", txt))
    domain_pass = has_proper or has_long_token

    # Decision relevance signal: presence of decision/policy/horizon vocab.
    decision_tokens = [
        "decision", "policy", "strategy", "choose", "should",
        "how will", "what if", "by 20", "by 21",
        "결정", "정책", "전략", "선택", "어떻게", "2030", "2040", "2050",
        "year", "years", "년", "horizon",
    ]
    decision_pass = any(tok in lower for tok in decision_tokens)

    rules = {
        "word_count_range": {
            "pass": word_pass,
            "value": words,
            "expected": f"[{SHARPENING_RULES['min_words']}, {SHARPENING_RULES['max_words']}]",
        },
        "char_count_range": {
            "pass": char_pass,
            "value": chars,
            "expected": f"[{SHARPENING_RULES['min_chars']}, {SHARPENING_RULES['max_chars']}]",
        },
        "no_banned_vague_tokens": {
            "pass": vague_pass,
            "hits": banned_hits,
        },
        "domain_signal_present": {
            "pass": domain_pass,
            "has_proper_noun": has_proper,
            "has_long_token": has_long_token,
        },
        "decision_relevance_signal": {
            "pass": decision_pass,
            "tokens_searched": decision_tokens,
        },
    }
    overall_pass = all(r["pass"] for r in rules.values())
    return {
        "valid": True,
        "input": txt,
        "rules": rules,
        "overall_pass": overall_pass,
        "source": SHARPENING_RULES["source"],
        "recommendation": (
            "If overall_pass is False, ask the user to narrow/broaden the "
            "focal issue per the failing rules — do NOT auto-rewrite."
        ),
    }


# ════════════════════════════════════════════════════════════════════════════
# SINGLE-STATEMENT TEMPLATE VALIDATOR
# ════════════════════════════════════════════════════════════════════════════

STATEMENT_TEMPLATE = (
    "How will [stakeholders] navigate [issue] under [conditions] by "
    "[horizon] in [scope]?"
)

STATEMENT_TEMPLATE_PARTS = [
    "[stakeholders]", "[issue]", "[conditions]", "[horizon]", "[scope]",
]


def validate_statement(statement: str) -> dict:
    """Verify the final 1-2 sentence focal-issue statement covers the 5 slots.

    The statement does NOT need to literally contain '[stakeholders]' etc.
    It needs to communicate each of the 5 dimensions. We approximate by
    requiring (a) it ends with '?' or '.', (b) it is 1-2 sentences,
    (c) it is within length bounds, (d) it contains horizon and scope signals.
    """
    if not isinstance(statement, str):
        return {"valid": False, "error": "statement must be string."}
    txt = statement.strip()
    if not txt:
        return {"valid": False, "error": "Empty statement.", "overall_pass": False}
    sentences = [s for s in re.split(r"(?<=[.?!])\s+", txt) if s.strip()]
    sentence_pass = 1 <= len(sentences) <= 2
    length_pass = 12 <= len(txt) <= 600
    end_pass = txt.endswith(("?", ".", "!"))
    lower = txt.lower()
    horizon_pass = bool(
        re.search(r"\b20\d{2}\b", txt)
        or re.search(r"\b(by|within|next)\s+\d+\s*(year|yr|years)\b", lower)
        or "년" in txt
        or "20" in txt
    )
    scope_tokens = [
        "global", "national", "regional", "local",
        "global ly".replace(" ", ""), "worldwide",
        "한국", "korea", "korean", "asia", "world",
        "지역", "국가", "글로벌", "전 세계",
    ]
    scope_pass = any(t in lower or t in txt for t in scope_tokens)
    rules = {
        "sentence_count_1_to_2": {"pass": sentence_pass, "value": len(sentences)},
        "length_12_to_600_chars": {"pass": length_pass, "value": len(txt)},
        "ends_with_punctuation": {"pass": end_pass},
        "horizon_signal": {"pass": horizon_pass},
        "scope_signal": {"pass": scope_pass},
    }
    overall_pass = all(r["pass"] for r in rules.values())
    return {
        "valid": True,
        "input": txt,
        "rules": rules,
        "overall_pass": overall_pass,
        "template": STATEMENT_TEMPLATE,
        "template_parts": STATEMENT_TEMPLATE_PARTS,
        "source": (
            "Glenn & TFG (2009) V3.0 Ch.19 Section III — sharply focused "
            "focal issue + Schwartz planning-question discipline"
        ),
    }


# ════════════════════════════════════════════════════════════════════════════
# BIBLIOGRAPHY
# ════════════════════════════════════════════════════════════════════════════

def bibliography() -> dict:
    return {
        "primary": PRIMARY_SOURCE,
        "schwartz_1991": SCHWARTZ_1991,
        "bishop": BISHOP_SOURCE,
        "millennium_project": (
            "The Millennium Project. Futures Research Methodology V3.0, Ch.19."
        ),
    }


# ════════════════════════════════════════════════════════════════════════════
# SELF-VALIDATION
# ════════════════════════════════════════════════════════════════════════════

def run_all_validations() -> dict:
    results: dict[str, Any] = {}

    def chk(name: str, cond: bool, **extra: Any) -> None:
        entry = {"pass": bool(cond)}
        entry.update(extra)
        results[name] = entry

    # PDF verbatim count
    chk("pdf_verbatim_count_6", len(PDF_VERBATIM) == 6, got=len(PDF_VERBATIM))
    chk("verbatim_sources_match_keys",
        set(PDF_VERBATIM.keys()) == set(PDF_VERBATIM_SOURCES.keys()))
    chk("verbatim_schwartz_step1",
        PDF_VERBATIM["schwartz_step1"] == "identify the focal issue or decision")
    chk("verbatim_bishop_workshop_has_three_qs",
        PDF_VERBATIM["bishop_workshop"].count("?") == 3)
    chk("verbatim_key_points_sharply_focused",
        "sharply focused" in PDF_VERBATIM["key_points_sharply_focused"])
    chk("verbatim_key_points_define_focus",
        "define the focus from the outset" in PDF_VERBATIM["key_points_define_focus"])
    chk("verbatim_key_points_planning",
        "planning questions" in PDF_VERBATIM["key_points_planning_questions"])

    # Verbatim lookup
    vr = get_pdf_verbatim("schwartz_step1")
    chk("lookup_schwartz_step1_valid", vr.get("valid"))
    vr2 = get_pdf_verbatim("bishop")
    chk("lookup_bishop_alias_valid", vr2.get("valid"))
    vr3 = get_pdf_verbatim("nonexistent_xyz")
    chk("lookup_bad_key_invalid", not vr3.get("valid"))

    # Schwartz steps
    chk("schwartz_steps_count_7", len(SCHWARTZ_STEPS) == 7)
    chk("schwartz_step1_focal",
        "focal issue" in SCHWARTZ_STEPS[1]["description"].lower())
    chk("schwartz_step1_current_skill",
        SCHWARTZ_STEPS[1]["current_skill_step"] is True)
    chk("schwartz_step7_glenn_extension",
        SCHWARTZ_STEPS[7].get("glenn_extension") is True)
    chk("schwartz_step2_not_current",
        SCHWARTZ_STEPS[2]["current_skill_step"] is False)
    chk("get_schwartz_step_valid", get_schwartz_step(1)["valid"])
    chk("get_schwartz_step_bad", not get_schwartz_step(99).get("valid", False))

    # Bishop questions
    chk("bishop_three_questions", len(BISHOP_QUESTIONS) == 3)
    chk("bishop_q1_has_domain_placeholder",
        "[domain]" in BISHOP_QUESTIONS[1]["template"])
    chk("bishop_q1_has_T_placeholder",
        "[T]" in BISHOP_QUESTIONS[1]["template"])
    chk("bishop_q2_stay_same",
        "stay the same" in BISHOP_QUESTIONS[2]["template"])
    chk("bishop_q3_changing",
        "changing" in BISHOP_QUESTIONS[3]["template"])
    filled = fill_bishop_questions("AGI", "10")
    chk("fill_bishop_substitutes_domain",
        "AGI" in filled["questions"][1]["question"])
    chk("fill_bishop_substitutes_horizon",
        " 10 " in filled["questions"][1]["question"] or
        " 10 years" in filled["questions"][1]["question"])

    # Schwartz planning questions
    chk("planning_questions_count_3", len(SCHWARTZ_PLANNING_QUESTIONS) == 3)
    chk("planning_q4_verbatim",
        SCHWARTZ_PLANNING_QUESTIONS[4]["verbatim"] is True)
    chk("planning_q5_verbatim",
        SCHWARTZ_PLANNING_QUESTIONS[5]["verbatim"] is True)
    chk("planning_q6_extension",
        SCHWARTZ_PLANNING_QUESTIONS[6]["verbatim"] is False)

    # Time horizons
    chk("time_horizon_count_4", len(TIME_HORIZONS) == 4)
    chk("time_horizon_default_is_15_25",
        TIME_HORIZONS["15-25yr"]["default"] is True)
    chk("time_horizon_only_one_default",
        sum(1 for v in TIME_HORIZONS.values() if v["default"]) == 1)
    vh1 = validate_time_horizon("15-25yr")
    chk("validate_horizon_15_25_valid", vh1["valid"])
    vh2 = validate_time_horizon("default")
    chk("validate_horizon_default_alias", vh2["valid"] and vh2["canonical"] == "15-25yr")
    vh3 = validate_time_horizon("42yr")
    chk("validate_horizon_42_buckets_to_30plus",
        vh3["valid"] and vh3["canonical"] == "30yr+")
    vh4 = validate_time_horizon("not a horizon")
    chk("validate_horizon_garbage_invalid", not vh4["valid"])
    vh5 = validate_time_horizon("17yr")
    chk("validate_horizon_17_buckets_to_15_25",
        vh5["valid"] and vh5["canonical"] == "15-25yr")
    vh6 = validate_time_horizon("by 2040")
    chk("validate_horizon_by_2040_valid", vh6["valid"])

    # Spatial scopes
    chk("spatial_scope_count_4", len(SPATIAL_SCOPES) == 4)
    chk("validate_scope_global", validate_spatial_scope("Global")["valid"])
    chk("validate_scope_worldwide_alias",
        validate_spatial_scope("worldwide")["valid"] and
        validate_spatial_scope("worldwide")["canonical"] == "Global")
    chk("validate_scope_bad", not validate_spatial_scope("Galactic")["valid"])

    # Stakeholder roles
    chk("stakeholder_roles_count_3", len(STAKEHOLDER_ROLES) == 3)
    chk("stakeholder_role_affected", "affected" in STAKEHOLDER_ROLES)
    chk("stakeholder_role_decides", "decides" in STAKEHOLDER_ROLES)
    chk("stakeholder_role_acts", "acts" in STAKEHOLDER_ROLES)
    sk = validate_stakeholders({
        "affected": ["citizens"],
        "decides": ["regulators"],
        "acts": ["operators"],
    })
    chk("validate_stakeholders_all_three", sk["valid"])
    sk2 = validate_stakeholders({"affected": ["citizens"]})
    chk("validate_stakeholders_missing_roles", not sk2["valid"])

    # Personas
    chk("personas_8_total", len(PERSONAS) == 8)
    chk("persona_aggregation_min_6",
        PERSONA_AGGREGATION_RULE["min_personas"] == 6)
    chk("persona_aggregation_max_8",
        PERSONA_AGGREGATION_RULE["max_personas"] == 8)
    chk("validate_persona_count_6_ok", validate_persona_count(6)["valid"])
    chk("validate_persona_count_8_ok", validate_persona_count(8)["valid"])
    chk("validate_persona_count_5_fail", not validate_persona_count(5)["valid"])
    chk("validate_persona_count_9_fail", not validate_persona_count(9)["valid"])

    # Sharpening test
    st_good = sharpening_test(
        "How will Korean policymakers govern AGI safety by 2035 nationally?"
    )
    chk("sharpening_good_overall_pass", st_good["overall_pass"])
    st_bad_empty = sharpening_test("")
    chk("sharpening_empty_fail", not st_bad_empty.get("overall_pass", True))
    st_bad_vague = sharpening_test("everything about the future")
    chk("sharpening_vague_fail", not st_bad_vague["overall_pass"])
    st_bad_short = sharpening_test("xy")
    chk("sharpening_too_short_fail", not st_bad_short["overall_pass"])

    # Statement validator
    sv_good = validate_statement(
        "How will Korean policymakers navigate AGI safety under "
        "regulatory uncertainty by 2035 nationally?"
    )
    chk("statement_good_overall_pass", sv_good["overall_pass"])
    sv_bad = validate_statement("AGI?")
    chk("statement_too_short_fail", not sv_bad["overall_pass"])
    sv_no_horizon = validate_statement(
        "How will policymakers regulate AGI globally?"
    )
    chk("statement_missing_horizon_fail", not sv_no_horizon["overall_pass"])

    # Bibliography
    bib = bibliography()
    chk("bibliography_has_primary", "primary" in bib)
    chk("bibliography_has_schwartz", "schwartz_1991" in bib)
    chk("bibliography_has_bishop", "bishop" in bib)

    all_pass = all(
        v.get("pass", True)
        for v in results.values()
        if isinstance(v, dict) and "pass" in v
    )
    results["ALL_PASS"] = all_pass
    return results


# ════════════════════════════════════════════════════════════════════════════
# CLI
# ════════════════════════════════════════════════════════════════════════════

def _print_json(obj: Any) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def _usage() -> str:
    return (
        "Usage: focal_issue_utils.py [\n"
        "  validate                                — ALL_PASS 자체 검증\n"
        "  verbatim KEY                            — PDF verbatim 인용\n"
        "  verbatim_all                            — 전체 verbatim 출력\n"
        "  schwartz_step N                         — Schwartz Step N (1-7)\n"
        "  schwartz_all                            — Schwartz 전체 7 step\n"
        "  bishop_questions [DOMAIN] [T]           — Bishop 3 questions (치환)\n"
        "  schwartz_planning_questions             — Schwartz planning Qs\n"
        "  time_horizons                           — Time horizon enum\n"
        "  validate_horizon HORIZON                — Horizon 검증\n"
        "  spatial_scopes                          — Spatial scope enum\n"
        "  validate_scope SCOPE                    — Scope 검증\n"
        "  stakeholder_roles                       — Stakeholder taxonomy\n"
        "  validate_stakeholders JSON              — Stakeholder 검증\n"
        "  personas                                — 8 고정 페르소나 + 규칙\n"
        "  validate_persona_count N                — Persona 수 검증 (6-8)\n"
        "  sharpening_test 'TEXT'                  — Sharpening 5 규칙 검증\n"
        "  validate_statement 'TEXT'               — Final statement 검증\n"
        "  bibliography                            — Frozen 출처 목록\n"
        "]"
    )


def main(argv: list[str]) -> int:
    args = argv[1:]
    if not args or args[0] == "validate":
        _print_json(run_all_validations())
        return 0
    cmd = args[0]
    rest = args[1:]
    if cmd == "verbatim" and rest:
        _print_json(get_pdf_verbatim(" ".join(rest)))
        return 0
    if cmd == "verbatim_all":
        _print_json({
            k: {"verbatim": v, "source": PDF_VERBATIM_SOURCES[k]}
            for k, v in PDF_VERBATIM.items()
        })
        return 0
    if cmd == "schwartz_step" and rest:
        try:
            _print_json(get_schwartz_step(int(rest[0])))
        except ValueError:
            _print_json({"valid": False, "error": "step must be integer 1-7"})
        return 0
    if cmd == "schwartz_all":
        out = {
            n: {
                **{k: v for k, v in entry.items()},
                "step": n,
            }
            for n, entry in SCHWARTZ_STEPS.items()
        }
        _print_json({"steps": out, "source": SCHWARTZ_STEPS_SOURCE,
                     "current_skill_step": CURRENT_SKILL_STEP_NUMBER})
        return 0
    if cmd == "bishop_questions":
        domain = rest[0] if len(rest) >= 1 else None
        horizon = rest[1] if len(rest) >= 2 else None
        _print_json(fill_bishop_questions(domain, horizon))
        return 0
    if cmd == "schwartz_planning_questions":
        _print_json({
            "questions": SCHWARTZ_PLANNING_QUESTIONS,
            "note": "Q4 and Q5 are PDF verbatim (Key Points). Q6 is operational extension.",
        })
        return 0
    if cmd == "time_horizons":
        _print_json(TIME_HORIZONS)
        return 0
    if cmd == "validate_horizon" and rest:
        _print_json(validate_time_horizon(" ".join(rest)))
        return 0
    if cmd == "spatial_scopes":
        _print_json(SPATIAL_SCOPES)
        return 0
    if cmd == "validate_scope" and rest:
        _print_json(validate_spatial_scope(" ".join(rest)))
        return 0
    if cmd == "stakeholder_roles":
        _print_json(STAKEHOLDER_ROLES)
        return 0
    if cmd == "validate_stakeholders" and rest:
        try:
            payload = json.loads(" ".join(rest))
            _print_json(validate_stakeholders(payload))
        except json.JSONDecodeError as e:
            _print_json({"valid": False, "error": f"JSON parse error: {e}"})
        return 0
    if cmd == "personas":
        _print_json({
            "personas": PERSONAS,
            "aggregation_rule": PERSONA_AGGREGATION_RULE,
        })
        return 0
    if cmd == "validate_persona_count" and rest:
        try:
            _print_json(validate_persona_count(int(rest[0])))
        except ValueError:
            _print_json({"valid": False, "error": "n must be integer"})
        return 0
    if cmd == "sharpening_test" and rest:
        _print_json(sharpening_test(" ".join(rest)))
        return 0
    if cmd == "validate_statement" and rest:
        _print_json(validate_statement(" ".join(rest)))
        return 0
    if cmd == "bibliography":
        _print_json(bibliography())
        return 0
    print(_usage())
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
