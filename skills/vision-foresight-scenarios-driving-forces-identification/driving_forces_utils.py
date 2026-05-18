#!/usr/bin/env python3
"""
driving_forces_utils.py — 결정론 상수·검증 함수 (Driving Forces Identification 전용)
출처: Glenn J.C. & TFG (2009). "Scenarios." In Futures Research Methodology V3.0,
      Ch.19. The Millennium Project. Section III Schwartz Step 2 + TFG Preparation.
      Schwartz P. (1991). The Art of the Long View. Doubleday.
      Coates J.F. & Jarratt J. (1989). What Futurists Believe. Lomond Publications.
      Mandel T. & Wilson I.H. (1993). How Companies Use Scenarios. SRI International.
결정론 환원:
  - PDF verbatim 인용 (Schwartz·TFG·MITRE·Coates·Mandel-Wilson)
  - STEEPS 6 domains 정의 (standard 5 + Spiritual 6th)
  - Millennium Futures Matrix 6 domains 정의
  - 변수 수 범위 검증 (6-30 raw → 6-20 winnowed → 6-12 final)
  - Predetermined vs Critical Uncertainty 분류 기준
  - 8 고정 페르소나 정의 + 집계 규칙
  - Schwartz Step 2 정의

Usage:
  python3 driving_forces_utils.py validate            — ALL_PASS 자체 검증
  python3 driving_forces_utils.py verbatim KEY        — PDF verbatim 인용
  python3 driving_forces_utils.py verbatim_all        — 전체 verbatim 출력
  python3 driving_forces_utils.py steeps              — STEEPS 6 domains
  python3 driving_forces_utils.py futures_matrix      — Millennium Futures Matrix
  python3 driving_forces_utils.py personas            — 8 고정 페르소나 + 집계 규칙
  python3 driving_forces_utils.py validate_count N STAGE — 변수 수 범위 검증
  python3 driving_forces_utils.py classify_type FORCE_TYPE — Predetermined vs Uncertainty
  python3 driving_forces_utils.py schwartz_step N     — Schwartz Step N 정의
  python3 driving_forces_utils.py winnowing_algorithm — Coates winnowing 알고리즘
"""

import sys
import json

# ════════════════════════════════════════════════════════════════════════════
# PRIMARY SOURCES
# ════════════════════════════════════════════════════════════════════════════

PRIMARY_SOURCE = (
    "Glenn J.C. & TFG (2009). 'Scenarios.' In Glenn, J.C. (Ed.), "
    "Futures Research Methodology V3.0, Ch.19. The Millennium Project."
)

SCHWARTZ_1991 = (
    "Schwartz P. (1991). The Art of the Long View: Planning for the Future in an "
    "Uncertain World. Doubleday/Currency."
)

COATES_JARRATT_1989 = (
    "Coates J.F. & Jarratt J. (1989). What Futurists Believe. "
    "Lomond Publications. (as cited in Glenn & TFG 2009 V3.0 Ch.19)"
)

MANDEL_WILSON_1993 = (
    "Mandel T. & Wilson I.H. (1993). How Companies Use Scenarios: Practices and Precedents. "
    "SRI International. (as cited in Glenn & TFG 2009 V3.0 Ch.19)"
)

MITRE_SOURCE = (
    "The Futures Group for MITRE Corporation. (as cited in Glenn & TFG 2009 V3.0 Ch.19 "
    "TFG Preparation section — social environment of crime study)"
)

MILLENNIUM_PROJECT_SOURCE = (
    "The Millennium Project. Futures Research Methodology V3.0, Ch.19 — "
    "Futures Matrix 6 domains."
)

# ════════════════════════════════════════════════════════════════════════════
# PDF VERBATIM QUOTES
# ════════════════════════════════════════════════════════════════════════════

PDF_VERBATIM = {
    "schwartz_step2": (
        "identify the key forces and trends in the environment"
    ),
    "building_blocks": (
        "Schwartz uses the driving forces as the building blocks of scenarios"
    ),
    "scriptwriters": (
        "As scriptwriters formulate an idea and develop characters, Schwartz uses the "
        "driving forces as the building blocks of scenarios."
    ),
    "tfg_define": (
        "Define the scenario space. A scenario study begins by defining the domain of "
        "interest. Given a clear statement of the domain, analysts list key driving forces "
        "thought to be important to the future of the domain."
    ),
    "mitre_case": (
        "In a study performed by The Futures Group for MITRE Corporation about the social "
        "environment of crime, driving forces of law enforcement funding and social attitudes "
        "toward crime were defined as ultimately important. To the degree possible, these "
        "driving forces should be independent 'axes' in a scenario space."
    ),
    "mandel_wilson": (
        "The team then analyzes forces that will shape the future business environment, both "
        "from within their own industry (competition) and outside of it (social, political, "
        "economic, etc.)"
    ),
    "coates_winnowing": (
        "some 6 to 30 variables affecting the future situation are nominated. This list is "
        "then winnowed down by eliminating redundancies, a process that usually results in "
        "6 to 20 variables."
    ),
}

PDF_VERBATIM_SOURCES = {
    "schwartz_step2": (
        "Schwartz (1991) Step 2 — as cited in Glenn & TFG (2009) V3.0 Ch.19 Section III"
    ),
    "building_blocks": (
        "Glenn & TFG (2009) V3.0 Ch.19 Section III verbatim"
    ),
    "scriptwriters": (
        "Glenn & TFG (2009) V3.0 Ch.19 Section III verbatim"
    ),
    "tfg_define": (
        "Glenn & TFG (2009) V3.0 Ch.19 Section III TFG Preparation verbatim"
    ),
    "mitre_case": (
        "Glenn & TFG (2009) V3.0 Ch.19 Section III TFG Preparation — MITRE case verbatim"
    ),
    "mandel_wilson": (
        "Mandel & Wilson SRI (1993) — as cited in Glenn & TFG (2009) V3.0 Ch.19"
    ),
    "coates_winnowing": (
        "Coates & Jarratt (1989) — as cited in Glenn & TFG (2009) V3.0 Ch.19"
    ),
}

# ════════════════════════════════════════════════════════════════════════════
# SCHWARTZ STEPS (context for Step 2)
# ════════════════════════════════════════════════════════════════════════════

SCHWARTZ_STEPS = {
    1: "Identify the focal issue or decision (define the problem to be analyzed)",
    2: "Identify the key forces and trends in the environment (driving forces)",
    3: "Rank by importance and uncertainty",
    4: "Select scenario logics (structure the scenario space)",
    5: "Flesh out the scenarios (develop scenario content)",
    6: "Identify implications (assess strategic implications)",
    7: "Select leading indicators and signposts",
}

SCHWARTZ_STEPS_SOURCE = (
    "Schwartz P. (1991). The Art of the Long View. Doubleday/Currency. "
    "(as cited in Glenn & TFG 2009 V3.0 Ch.19 Section III)"
)

# ════════════════════════════════════════════════════════════════════════════
# STEEPS 6 DOMAINS (standard + Spiritual extension)
# ════════════════════════════════════════════════════════════════════════════

STEEPS_DOMAINS = {
    "Social": {
        "code": "S",
        "examples": ["Demographics", "values", "lifestyles", "culture", "education", "health"],
        "standard": True,
        "source": "Standard STEEPS/PESTLE framework",
    },
    "Technological": {
        "code": "T",
        "examples": ["Innovation", "diffusion", "obsolescence", "digitization", "AI", "biotech"],
        "standard": True,
        "source": "Standard STEEPS/PESTLE framework",
    },
    "Economic": {
        "code": "E",
        "examples": ["Markets", "resources", "trade", "inequality", "investment", "growth"],
        "standard": True,
        "source": "Standard STEEPS/PESTLE framework",
    },
    "Environmental": {
        "code": "E2",
        "examples": ["Climate", "biodiversity", "sustainability", "resources", "pollution"],
        "standard": True,
        "source": "Standard STEEPS/PESTLE framework",
    },
    "Political": {
        "code": "P",
        "examples": ["Governance", "regulation", "conflict", "alliances", "geopolitics"],
        "standard": True,
        "source": "Standard STEEPS/PESTLE framework",
    },
    "Spiritual": {
        "code": "Sp",
        "examples": ["Religious trends", "philosophical shifts", "identity", "meaning", "purpose"],
        "standard": False,
        "note": (
            "Non-standard 6th domain — added per domain-specialist vision. "
            "Standard STEEPS has 5 domains (S·T·E·E·P). "
            "Spiritual captures forces not adequately covered by Social or Political."
        ),
        "source": "User-specified extension to standard STEEPS framework",
    },
}

STEEPS_STANDARD_COUNT = 5
STEEPS_EXTENDED_COUNT = 6

# ════════════════════════════════════════════════════════════════════════════
# MILLENNIUM FUTURES MATRIX 6 DOMAINS
# ════════════════════════════════════════════════════════════════════════════

FUTURES_MATRIX_DOMAINS = {
    1: {
        "name": "Demographics and Human Resources",
        "abbreviation": "Demographics",
        "description": "Population trends, migration, aging, education, health, labor force",
    },
    2: {
        "name": "Environmental Change and Biodiversity",
        "abbreviation": "Environment",
        "description": "Climate change, ecosystems, biodiversity, natural resources, sustainability",
    },
    3: {
        "name": "Technological Capacity",
        "abbreviation": "Technology",
        "description": "R&D capacity, technology diffusion, digital infrastructure, biotech, AI",
    },
    4: {
        "name": "Governance and Conflict",
        "abbreviation": "Governance",
        "description": "Political institutions, rule of law, conflict, security, international relations",
    },
    5: {
        "name": "International Economics and Wealth",
        "abbreviation": "Economics",
        "description": "Global trade, investment, inequality, growth, financial systems",
    },
    6: {
        "name": "Integration or Whole Futures",
        "abbreviation": "Integration",
        "description": (
            "Cross-cutting integration of dimensions; emergence of new paradigms; "
            "sustainability transitions; systemic transformations not captured in other domains"
        ),
    },
}

FUTURES_MATRIX_SOURCE = MILLENNIUM_PROJECT_SOURCE

# ════════════════════════════════════════════════════════════════════════════
# VARIABLE COUNT RANGES (Coates + TFG convention)
# ════════════════════════════════════════════════════════════════════════════

VARIABLE_COUNT_RANGES = {
    "raw": {
        "min": 6,
        "max": 30,
        "description": "Raw nominated variables (Coates: '6 to 30 variables')",
        "source": "Coates & Jarratt (1989) as cited in TFG V3.0 Ch.19",
    },
    "winnowed": {
        "min": 6,
        "max": 20,
        "description": "After eliminating redundancies (Coates: 'results in 6 to 20 variables')",
        "source": "Coates & Jarratt (1989) verbatim — 'usually results in 6 to 20'",
    },
    "final": {
        "min": 6,
        "max": 12,
        "description": "Final curated driving forces for scenario building (TFG convention + MITRE axes)",
        "source": (
            "TFG convention + Schwartz (1991) scenario axes framework — "
            "6-12 provides enough richness without overcomplication"
        ),
    },
}


def validate_variable_count(n: int, stage: str) -> dict:
    """
    Validate variable count for a given stage.
    Stages: 'raw' | 'winnowed' | 'final'
    """
    stage_lower = stage.strip().lower()
    if stage_lower not in VARIABLE_COUNT_RANGES:
        return {
            "valid": False,
            "error": f"Unknown stage '{stage}'. Valid: {list(VARIABLE_COUNT_RANGES.keys())}",
        }
    r = VARIABLE_COUNT_RANGES[stage_lower]
    in_range = r["min"] <= n <= r["max"]
    return {
        "valid": in_range,
        "n": n,
        "stage": stage_lower,
        "range": f"[{r['min']}, {r['max']}]",
        "description": r["description"],
        "source": r["source"],
        "warning": (
            None if in_range else
            f"Count {n} outside recommended range [{r['min']}, {r['max']}] for stage '{stage_lower}'"
        ),
    }


# ════════════════════════════════════════════════════════════════════════════
# PREDETERMINED vs CRITICAL UNCERTAINTY CLASSIFICATION
# ════════════════════════════════════════════════════════════════════════════

FORCE_TYPES = {
    "Predetermined": {
        "definition": (
            "Driving forces whose outcomes are relatively certain regardless of scenario — "
            "trends already set in motion that will play out predictably."
        ),
        "criteria": [
            "Demographic trends (populations already born — aging, generational shift)",
            "Physical/geological processes",
            "Long lead-time infrastructure already under construction",
            "Technological changes already in diffusion stage",
            "Historical momentum with no plausible reversal",
        ],
        "examples": ["Population aging", "Climate inertia", "Internet infrastructure diffusion"],
        "role_in_scenarios": (
            "Provide shared background for all scenarios — constant across scenario variants"
        ),
        "source": "Schwartz (1991) — predetermined elements concept as cited in TFG V3.0 Ch.19",
    },
    "Critical Uncertainty": {
        "definition": (
            "Driving forces that are both important AND highly uncertain — "
            "these become the axes of the scenario space (MITRE verbatim: 'independent axes')."
        ),
        "criteria": [
            "Political decisions not yet made",
            "Technology adoption rate (direction uncertain)",
            "Cultural and values shifts",
            "Economic policy choices",
            "Wild card events with significant impact probability",
            "Geopolitical alignments",
        ],
        "examples": [
            "AI regulatory direction", "Social cohesion trajectory",
            "Energy transition pace", "Geopolitical alignment"
        ],
        "role_in_scenarios": (
            "Become the primary scenario-differentiating axes — vary across scenarios. "
            "MITRE verbatim: 'driving forces should be independent axes in a scenario space'"
        ),
        "source": "Schwartz (1991) + TFG MITRE case verbatim (TFG V3.0 Ch.19)",
    },
}

FORCE_TYPE_CLASSIFICATION_RULE = {
    "method": (
        "Classify based on two dimensions: "
        "(1) Outcome certainty: Certain vs Uncertain; "
        "(2) Impact importance: Low vs High. "
        "Predetermined = High importance + High certainty (outcome already set). "
        "Critical Uncertainty = High importance + Low certainty (key fork in the road). "
        "Low importance forces are filtered out in Step 5 (winnowing)."
    ),
    "source": (
        "Schwartz (1991) importance-uncertainty matrix concept as cited in "
        "Glenn & TFG (2009) V3.0 Ch.19 Section III"
    ),
}

# ════════════════════════════════════════════════════════════════════════════
# 8 FIXED PERSONAS (Driving Forces Identification)
# ════════════════════════════════════════════════════════════════════════════

PERSONAS = [
    {
        "id": "P1",
        "name": "Industry Insider",
        "role": "Internal forces from within the focal domain",
        "focus": "Competition, industry dynamics, sector-specific trends, internal constraints",
        "source_link": "Mandel-Wilson SRI: 'forces from within their own industry (competition)'",
    },
    {
        "id": "P2",
        "name": "Scenario Specialist",
        "role": "External environmental forces beyond the focal domain",
        "focus": "Macro-environmental trends, cross-domain forces, scenario driving forces methodology",
        "source_link": "Schwartz (1991) Step 2 — building blocks approach",
    },
    {
        "id": "P3",
        "name": "Policy Analyst",
        "role": "Political·regulatory·governance forces",
        "focus": "STEEPS Political domain, international agreements, regulatory trends",
        "source_link": "Mandel-Wilson SRI: 'outside of it (social, political, economic, etc.)'",
    },
    {
        "id": "P4",
        "name": "Technology Expert",
        "role": "Technological driving forces, innovation trajectories",
        "focus": "STEEPS Technological domain, Futures Matrix: Technological Capacity",
        "source_link": "Standard STEEPS framework",
    },
    {
        "id": "P5",
        "name": "Sociologist/Anthropologist",
        "role": "Social·cultural·demographic forces",
        "focus": "STEEPS Social + Spiritual domains, Futures Matrix: Demographics",
        "source_link": "Standard STEEPS Social domain",
    },
    {
        "id": "P6",
        "name": "Economist",
        "role": "Economic forces, markets, trade, inequality",
        "focus": "STEEPS Economic domain, Futures Matrix: International Economics and Wealth",
        "source_link": "Mandel-Wilson SRI: 'economic' forces",
    },
    {
        "id": "P7",
        "name": "Environmental Scientist",
        "role": "Environmental·ecological forces",
        "focus": "STEEPS Environmental domain, Futures Matrix: Environmental Change and Biodiversity",
        "source_link": "Standard STEEPS Environmental domain",
    },
    {
        "id": "P8",
        "name": "Devil's Advocate / Wild Card Thinker",
        "role": "Challenges assumptions, surfaces overlooked forces, identifies wild cards",
        "focus": (
            "Edge cases, non-linear forces, Black Swan candidates, "
            "Futures Matrix: Integration / Whole Futures"
        ),
        "source_link": "Standard scenario planning wild card methodology",
    },
]

PERSONA_AGGREGATION_RULE = {
    "step1": "8 persona proposals의 합집합 (Union) — all suggested driving forces",
    "step2": "중복 제거 — 동일·유사 개념 병합 (exact or near-synonym)",
    "step3": "STEEPS domain 분류 — 각 force를 S·T·E·E·P·Sp 중 하나 이상에 배정",
    "step4": "Futures Matrix 매핑 — 각 force를 6개 domain 중 하나에 매핑",
    "step5": (
        "Coates winnowing — redundancies 제거 → 6-20 remaining; "
        "Check: python3 driving_forces_utils.py validate_count N winnowed"
    ),
    "step6": (
        "Final curation → 6-12 key driving forces; "
        "Check: python3 driving_forces_utils.py validate_count N final"
    ),
    "step7": "Predetermined vs Critical Uncertainty 분류",
    "note": (
        "Steps 1-2 are set operations (deterministic). "
        "Steps 3-7 require LLM semantic judgment with Python validation of counts."
    ),
}

# ════════════════════════════════════════════════════════════════════════════
# WINNOWING ALGORITHM
# ════════════════════════════════════════════════════════════════════════════

WINNOWING_ALGORITHM = {
    "verbatim": PDF_VERBATIM["coates_winnowing"],
    "source": PDF_VERBATIM_SOURCES["coates_winnowing"],
    "steps": [
        {
            "step": 1,
            "action": "List all proposed forces from 8 personas (union)",
            "output": "Raw list (6-30)",
            "check": "validate_count N raw",
        },
        {
            "step": 2,
            "action": (
                "Identify redundant or overlapping forces — "
                "merge if two forces describe the same phenomenon from different angles"
            ),
            "output": "Merged list",
            "rule": "Merge criterion: identical or >80% conceptual overlap",
        },
        {
            "step": 3,
            "action": (
                "Remove forces with low relevance to focal issue — "
                "keep only forces that materially affect the focal domain"
            ),
            "output": "Winnowed list (6-20)",
            "check": "validate_count N winnowed",
        },
        {
            "step": 4,
            "action": (
                "Final curation for scenario building: "
                "select the most important + most uncertain forces"
            ),
            "output": "Final list (6-12)",
            "check": "validate_count N final",
        },
    ],
    "independence_rule": (
        "MITRE verbatim: 'to the degree possible, these driving forces should be independent "
        "axes in a scenario space' — Final forces should have minimal overlap in their causal domain"
    ),
}

# ════════════════════════════════════════════════════════════════════════════
# DETERMINISTIC FUNCTIONS
# ════════════════════════════════════════════════════════════════════════════

def get_pdf_verbatim(key: str) -> dict:
    """Return PDF verbatim quote by key."""
    key_lower = key.strip().lower().replace("-", "_").replace(" ", "_")
    aliases = {
        "step2": "schwartz_step2",
        "schwartz": "schwartz_step2",
        "key_forces": "schwartz_step2",
        "building": "building_blocks",
        "blocks": "building_blocks",
        "scriptwriter": "scriptwriters",
        "tfg": "tfg_define",
        "define": "tfg_define",
        "scenario_space": "tfg_define",
        "mitre": "mitre_case",
        "crime": "mitre_case",
        "axes": "mitre_case",
        "mandel": "mandel_wilson",
        "wilson": "mandel_wilson",
        "sri": "mandel_wilson",
        "coates": "coates_winnowing",
        "winnow": "coates_winnowing",
        "jarratt": "coates_winnowing",
        "variables": "coates_winnowing",
    }
    resolved = aliases.get(key_lower, key_lower)
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
    }


def get_schwartz_step(n: int) -> dict:
    """Return Schwartz Step N definition."""
    if n not in SCHWARTZ_STEPS:
        return {"error": f"Step {n} not found. Valid: 1-7"}
    return {
        "step": n,
        "description": SCHWARTZ_STEPS[n],
        "current_skill_step": n == 2,
        "note": "Step 2 = identify key driving forces" if n == 2 else "",
        "source": SCHWARTZ_STEPS_SOURCE,
    }


def aggregate_persona_proposals(persona_proposals: dict) -> dict:
    """Deterministic union + near-duplicate folding of 8-persona proposals.

    Args:
      persona_proposals: dict like {"P1": ["force-a", "force b"], "P2": [...], ...}
                         Keys must subset of {"P1".."P8"}.

    Returns:
      {
        "valid": bool, "raw_count": int, "deduped_count": int,
        "merged": [{"force": str, "personas": [..]}],
        "unknown_personas": [..],
        "error": str (only when valid is False)
      }

    De-duplication is case-insensitive on a normalised token form:
    whitespace-stripped, punctuation-stripped, lower-cased. This catches
    "AI adoption" vs "ai adoption" / "AI  adoption." but does NOT attempt
    to merge semantically distinct forces — that requires LLM judgment.
    """
    if not isinstance(persona_proposals, dict):
        return {"valid": False, "error": "persona_proposals must be a dict."}
    valid_ids = {p["id"] for p in PERSONAS}
    unknown = [k for k in persona_proposals.keys() if k not in valid_ids]

    import re

    def norm(s):
        return re.sub(r"[^a-z0-9가-힣]+", " ", s.strip().lower()).strip()

    bucket = {}
    raw_count = 0
    for pid, items in persona_proposals.items():
        if pid not in valid_ids:
            continue
        if not isinstance(items, list):
            return {"valid": False, "error": f"{pid} proposals must be a list."}
        for it in items:
            if not isinstance(it, str) or not it.strip():
                continue
            raw_count += 1
            key = norm(it)
            if not key:
                continue
            if key not in bucket:
                bucket[key] = {"force": it.strip(), "personas": []}
            if pid not in bucket[key]["personas"]:
                bucket[key]["personas"].append(pid)
    merged = sorted(bucket.values(), key=lambda x: x["force"].lower())
    out = {
        "valid": True,
        "raw_count": raw_count,
        "deduped_count": len(merged),
        "merged": merged,
        "unknown_personas": unknown,
    }
    if unknown:
        out["warning"] = f"Unknown persona ids ignored: {unknown}"
    return out


def validate_steeps_coverage(forces: list) -> dict:
    """Ensure every STEEPS domain has at least one force.

    Args:
      forces: list of {"name": str, "steeps_code": "S"|"T"|"E"|"E2"|"P"|"Sp"}
    """
    if not isinstance(forces, list):
        return {"valid": False, "error": "forces must be a list."}
    valid_codes = {info["code"] for info in STEEPS_DOMAINS.values()}
    seen = set()
    for f in forces:
        if not isinstance(f, dict):
            return {"valid": False, "error": f"force entry not dict: {f!r}"}
        code = f.get("steeps_code", "")
        if code not in valid_codes:
            return {
                "valid": False,
                "error": f"Force {f.get('name','?')!r} has unknown STEEPS code {code!r}.",
                "valid_codes": sorted(valid_codes),
            }
        seen.add(code)
    # Standard 5 + Spiritual extension. Standard 5 must all be covered.
    standard_codes = {info["code"] for info in STEEPS_DOMAINS.values() if info["standard"]}
    missing_standard = sorted(standard_codes - seen)
    return {
        "valid": not missing_standard,
        "covered": sorted(seen),
        "missing_standard": missing_standard,
        "spiritual_used": "Sp" in seen,
        "note": "Standard 5 STEEPS domains must all be covered; Spiritual optional.",
    }


def validate_futures_matrix_coverage(forces: list, require_full: bool = False) -> dict:
    """Map each force to a Futures Matrix domain id (1-6) and report coverage.

    Args:
      forces: list of {"name": str, "matrix_id": 1..6}
      require_full: when True, all 6 domains must be touched at least once.
    """
    if not isinstance(forces, list):
        return {"valid": False, "error": "forces must be a list."}
    valid_ids = set(FUTURES_MATRIX_DOMAINS.keys())
    seen = set()
    for f in forces:
        mid = f.get("matrix_id")
        if mid not in valid_ids:
            return {
                "valid": False,
                "error": f"Force {f.get('name','?')!r} has matrix_id={mid!r}; must be 1..6.",
            }
        seen.add(mid)
    missing = sorted(valid_ids - seen)
    valid = (not missing) if require_full else True
    return {
        "valid": valid,
        "covered": sorted(seen),
        "missing": missing,
        "require_full": require_full,
        "source": FUTURES_MATRIX_SOURCE,
    }


def classify_by_scores(importance: float, certainty: float,
                       importance_threshold: float = 0.5,
                       certainty_threshold: float = 0.5) -> dict:
    """Deterministic Predetermined / Critical Uncertainty / Filtered classification.

    Importance and certainty must be in [0, 1].
      - importance < threshold              -> "Filtered" (drop in winnowing)
      - importance >= threshold, certainty high  -> "Predetermined"
      - importance >= threshold, certainty low   -> "Critical Uncertainty"
    """
    for nm, v in [("importance", importance), ("certainty", certainty)]:
        if not isinstance(v, (int, float)):
            return {"valid": False, "error": f"{nm} must be numeric, got {type(v).__name__}."}
        if v < 0 or v > 1:
            return {"valid": False, "error": f"{nm}={v} out of [0,1]."}
    for nm, v in [("importance_threshold", importance_threshold),
                  ("certainty_threshold", certainty_threshold)]:
        if not isinstance(v, (int, float)) or v < 0 or v > 1:
            return {"valid": False, "error": f"{nm}={v} must be in [0,1]."}
    if importance < importance_threshold:
        cls = "Filtered"
    elif certainty >= certainty_threshold:
        cls = "Predetermined"
    else:
        cls = "Critical Uncertainty"
    return {
        "valid": True,
        "classification": cls,
        "importance": importance,
        "certainty": certainty,
        "thresholds": {
            "importance": importance_threshold,
            "certainty": certainty_threshold,
        },
        "source": FORCE_TYPE_CLASSIFICATION_RULE["source"],
    }


def check_independence(force_names: list, overlap_threshold: float = 0.8) -> dict:
    """MITRE 'independent axes' rule: pair-wise token-overlap check.

    Uses Jaccard similarity on whitespace-tokenised normalised names.
    Pairs with similarity > overlap_threshold are flagged.
    """
    import re
    if not isinstance(force_names, list) or len(force_names) < 2:
        return {"valid": True, "n": len(force_names) if isinstance(force_names, list) else 0,
                "flagged_pairs": [], "note": "fewer than 2 forces — independence vacuous."}
    def tokens(s):
        return set(t for t in re.split(r"[^a-z0-9가-힣]+", s.lower()) if t)
    toks = [tokens(n) for n in force_names]
    flagged = []
    for i in range(len(force_names)):
        for j in range(i + 1, len(force_names)):
            a, b = toks[i], toks[j]
            if not a or not b:
                continue
            inter = len(a & b)
            union = len(a | b)
            sim = inter / union if union else 0
            if sim > overlap_threshold:
                flagged.append({
                    "force_a": force_names[i],
                    "force_b": force_names[j],
                    "jaccard": round(sim, 3),
                })
    return {
        "valid": not flagged,
        "n": len(force_names),
        "threshold": overlap_threshold,
        "flagged_pairs": flagged,
        "source": (
            "MITRE verbatim: 'driving forces should be independent axes in a scenario space' — "
            "as cited in Glenn & TFG (2009) V3.0 Ch.19"
        ),
    }


def bibliography() -> dict:
    """Return the full bibliography frozen in this module."""
    return {
        "primary": PRIMARY_SOURCE,
        "schwartz": SCHWARTZ_1991,
        "coates_jarratt": COATES_JARRATT_1989,
        "mandel_wilson": MANDEL_WILSON_1993,
        "mitre": MITRE_SOURCE,
        "millennium": MILLENNIUM_PROJECT_SOURCE,
    }


def classify_force_type(force_description: str) -> dict:
    """
    Returns classification guidance for LLM.
    NOT deterministic (requires semantic judgment), but provides structured prompt.
    """
    return {
        "note": (
            "Force type classification requires LLM semantic judgment. "
            "Use criteria below as evaluation framework."
        ),
        "force_description": force_description,
        "predetermined_criteria": FORCE_TYPES["Predetermined"]["criteria"],
        "critical_uncertainty_criteria": FORCE_TYPES["Critical Uncertainty"]["criteria"],
        "classification_rule": FORCE_TYPE_CLASSIFICATION_RULE["method"],
        "source": FORCE_TYPE_CLASSIFICATION_RULE["source"],
        "prompt": (
            f"For force: '{force_description}'\n"
            f"Q1: Is the outcome of this force relatively certain (locked-in)?\n"
            f"Q2: Is this force important to the focal issue?\n"
            f"→ If Q1=Yes and Q2=Yes → Predetermined\n"
            f"→ If Q1=No and Q2=Yes → Critical Uncertainty\n"
            f"→ If Q2=No → Consider filtering in winnowing step"
        ),
    }


# ════════════════════════════════════════════════════════════════════════════
# SELF-VALIDATION
# ════════════════════════════════════════════════════════════════════════════

def run_all_validations() -> dict:
    """Run all deterministic self-checks. ALL_PASS must be True."""
    results = {}

    def chk(name, condition):
        results[name] = {"pass": bool(condition)}

    # PDF verbatim count
    results["pdf_verbatim_count"] = {
        "expected": 7,
        "got": len(PDF_VERBATIM),
        "pass": len(PDF_VERBATIM) == 7,
    }

    # Schwartz steps count
    results["schwartz_steps_count"] = {
        "expected": 7,
        "got": len(SCHWARTZ_STEPS),
        "pass": len(SCHWARTZ_STEPS) == 7,
    }

    # Step 2 is driving forces
    s2 = get_schwartz_step(2)
    chk("schwartz_step2_driving_forces",
        "forces" in s2["description"].lower() or "trends" in s2["description"].lower())
    chk("schwartz_step2_current_skill", s2["current_skill_step"])

    # STEEPS domains
    results["steeps_standard_count"] = {
        "expected": 5,
        "got": STEEPS_STANDARD_COUNT,
        "pass": STEEPS_STANDARD_COUNT == 5,
    }
    results["steeps_extended_count"] = {
        "expected": 6,
        "got": STEEPS_EXTENDED_COUNT,
        "pass": STEEPS_EXTENDED_COUNT == 6,
    }
    chk("steeps_all_6_domains_present", len(STEEPS_DOMAINS) == 6)
    chk("steeps_spiritual_non_standard", not STEEPS_DOMAINS["Spiritual"]["standard"])
    chk("steeps_social_standard", STEEPS_DOMAINS["Social"]["standard"])

    # Futures Matrix
    results["futures_matrix_count"] = {
        "expected": 6,
        "got": len(FUTURES_MATRIX_DOMAINS),
        "pass": len(FUTURES_MATRIX_DOMAINS) == 6,
    }
    chk("futures_matrix_domain1_demographics",
        "Demographics" in FUTURES_MATRIX_DOMAINS[1]["name"])
    chk("futures_matrix_domain6_integration",
        "Integration" in FUTURES_MATRIX_DOMAINS[6]["name"])

    # Variable count ranges
    results["raw_range_min"] = {
        "expected": 6,
        "got": VARIABLE_COUNT_RANGES["raw"]["min"],
        "pass": VARIABLE_COUNT_RANGES["raw"]["min"] == 6,
    }
    results["raw_range_max"] = {
        "expected": 30,
        "got": VARIABLE_COUNT_RANGES["raw"]["max"],
        "pass": VARIABLE_COUNT_RANGES["raw"]["max"] == 30,
    }
    results["winnowed_range_min"] = {
        "expected": 6,
        "got": VARIABLE_COUNT_RANGES["winnowed"]["min"],
        "pass": VARIABLE_COUNT_RANGES["winnowed"]["min"] == 6,
    }
    results["winnowed_range_max"] = {
        "expected": 20,
        "got": VARIABLE_COUNT_RANGES["winnowed"]["max"],
        "pass": VARIABLE_COUNT_RANGES["winnowed"]["max"] == 20,
    }
    results["final_range_min"] = {
        "expected": 6,
        "got": VARIABLE_COUNT_RANGES["final"]["min"],
        "pass": VARIABLE_COUNT_RANGES["final"]["min"] == 6,
    }
    results["final_range_max"] = {
        "expected": 12,
        "got": VARIABLE_COUNT_RANGES["final"]["max"],
        "pass": VARIABLE_COUNT_RANGES["final"]["max"] == 12,
    }

    # validate_count function
    vc_raw_valid = validate_variable_count(15, "raw")
    chk("validate_count_15_raw_valid", vc_raw_valid["valid"])

    vc_raw_too_many = validate_variable_count(35, "raw")
    chk("validate_count_35_raw_invalid", not vc_raw_too_many["valid"])

    vc_winnowed_valid = validate_variable_count(12, "winnowed")
    chk("validate_count_12_winnowed_valid", vc_winnowed_valid["valid"])

    vc_winnowed_invalid = validate_variable_count(25, "winnowed")
    chk("validate_count_25_winnowed_invalid", not vc_winnowed_invalid["valid"])

    vc_final_valid = validate_variable_count(8, "final")
    chk("validate_count_8_final_valid", vc_final_valid["valid"])

    vc_final_invalid = validate_variable_count(15, "final")
    chk("validate_count_15_final_invalid", not vc_final_invalid["valid"])

    vc_bad_stage = validate_variable_count(10, "unknown_stage")
    chk("validate_count_bad_stage_invalid", not vc_bad_stage["valid"])

    # Personas
    results["personas_count"] = {
        "expected": 8,
        "got": len(PERSONAS),
        "pass": len(PERSONAS) == 8,
    }
    chk("personas_P1_industry", PERSONAS[0]["id"] == "P1")
    chk("personas_P8_devil", "Devil" in PERSONAS[7]["name"])
    # PERSONA_AGGREGATION_RULE has step1..step7 + a "note" — total 8 entries.
    chk("persona_aggregation_step1_to_step7_present",
        all(f"step{i}" in PERSONA_AGGREGATION_RULE for i in range(1, 8)))
    chk("persona_aggregation_total_8", len(PERSONA_AGGREGATION_RULE) == 8)

    # Force types
    chk("force_types_predetermined", "Predetermined" in FORCE_TYPES)
    chk("force_types_critical_uncertainty", "Critical Uncertainty" in FORCE_TYPES)

    # Winnowing algorithm steps
    chk("winnowing_4_steps", len(WINNOWING_ALGORITHM["steps"]) == 4)

    # PDF verbatim content checks
    chk("verbatim_schwartz_step2_forces",
        "forces" in PDF_VERBATIM["schwartz_step2"].lower())
    chk("verbatim_coates_6_to_30",
        "6 to 30" in PDF_VERBATIM["coates_winnowing"])
    chk("verbatim_coates_6_to_20",
        "6 to 20" in PDF_VERBATIM["coates_winnowing"])
    chk("verbatim_mitre_axes",
        "axes" in PDF_VERBATIM["mitre_case"])
    chk("verbatim_building_blocks",
        "building blocks" in PDF_VERBATIM["building_blocks"])

    # Verbatim lookup
    vr = get_pdf_verbatim("schwartz_step2")
    chk("verbatim_lookup_schwartz_valid", vr.get("valid"))
    vr2 = get_pdf_verbatim("coates")
    chk("verbatim_lookup_coates_valid", vr2.get("valid"))
    vr3 = get_pdf_verbatim("nonexistent_key_xyz")
    chk("verbatim_bad_key_invalid", not vr3.get("valid"))

    # Overall
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

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "validate":
        print(json.dumps(run_all_validations(), ensure_ascii=False, indent=2))

    elif args[0] == "verbatim" and len(args) > 1:
        result = get_pdf_verbatim(" ".join(args[1:]))
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args[0] == "verbatim_all":
        print(json.dumps(
            {
                k: {"verbatim": v,
                    "source": PDF_VERBATIM_SOURCES.get(k, PRIMARY_SOURCE)}
                for k, v in PDF_VERBATIM.items()
            },
            ensure_ascii=False, indent=2,
        ))

    elif args[0] == "steeps":
        print(json.dumps({
            "standard_count": STEEPS_STANDARD_COUNT,
            "extended_count": STEEPS_EXTENDED_COUNT,
            "domains": STEEPS_DOMAINS,
            "note": "Standard STEEPS = 5 domains. Spiritual is a 6th non-standard domain.",
        }, ensure_ascii=False, indent=2))

    elif args[0] == "futures_matrix":
        print(json.dumps({
            "domain_count": len(FUTURES_MATRIX_DOMAINS),
            "domains": FUTURES_MATRIX_DOMAINS,
            "source": FUTURES_MATRIX_SOURCE,
        }, ensure_ascii=False, indent=2))

    elif args[0] == "personas":
        print("=== 8 Fixed Personas (Driving Forces Identification) ===\n")
        for p in PERSONAS:
            print(f"  {p['id']}. {p['name']} [{p['role']}]")
            print(f"     Focus: {p['focus']}")
        print("\n=== Aggregation Rule ===\n")
        for k, v in PERSONA_AGGREGATION_RULE.items():
            print(f"  {k}: {v}")

    elif args[0] == "validate_count" and len(args) >= 3:
        try:
            n = int(args[1])
            stage = args[2]
            result = validate_variable_count(n, stage)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        except ValueError:
            print(json.dumps({"error": "N must be an integer"}))

    elif args[0] == "classify_type" and len(args) > 1:
        force_desc = " ".join(args[1:])
        result = classify_force_type(force_desc)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args[0] == "schwartz_step" and len(args) > 1:
        try:
            n = int(args[1])
            result = get_schwartz_step(n)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        except ValueError:
            print(json.dumps({"error": "Step must be integer 1-7"}))

    elif args[0] == "schwartz_all":
        for n, desc in SCHWARTZ_STEPS.items():
            print(f"Step {n}: {desc}")

    elif args[0] == "winnowing_algorithm":
        print(json.dumps(WINNOWING_ALGORITHM, ensure_ascii=False, indent=2))

    elif args[0] == "force_types":
        print(json.dumps({
            "types": FORCE_TYPES,
            "classification_rule": FORCE_TYPE_CLASSIFICATION_RULE,
        }, ensure_ascii=False, indent=2))

    elif args[0] == "bibliography":
        print(json.dumps(bibliography(), ensure_ascii=False, indent=2))

    elif args[0] == "aggregate" and len(args) > 1:
        # Single arg is a JSON dict of persona proposals.
        try:
            payload = json.loads(args[1])
            print(json.dumps(aggregate_persona_proposals(payload),
                             ensure_ascii=False, indent=2))
        except json.JSONDecodeError as e:
            print(json.dumps({"valid": False, "error": f"JSON parse error: {e}"}))

    elif args[0] == "steeps_coverage" and len(args) > 1:
        try:
            payload = json.loads(args[1])
            print(json.dumps(validate_steeps_coverage(payload),
                             ensure_ascii=False, indent=2))
        except json.JSONDecodeError as e:
            print(json.dumps({"valid": False, "error": f"JSON parse error: {e}"}))

    elif args[0] == "matrix_coverage" and len(args) > 1:
        try:
            payload = json.loads(args[1])
            require_full = "--full" in args[2:]
            print(json.dumps(validate_futures_matrix_coverage(payload, require_full),
                             ensure_ascii=False, indent=2))
        except json.JSONDecodeError as e:
            print(json.dumps({"valid": False, "error": f"JSON parse error: {e}"}))

    elif args[0] == "classify_scores" and len(args) >= 3:
        try:
            imp = float(args[1])
            cert = float(args[2])
            print(json.dumps(classify_by_scores(imp, cert),
                             ensure_ascii=False, indent=2))
        except ValueError as e:
            print(json.dumps({"valid": False, "error": f"value error: {e}"}))

    elif args[0] == "independence" and len(args) > 1:
        try:
            payload = json.loads(args[1])
            print(json.dumps(check_independence(payload),
                             ensure_ascii=False, indent=2))
        except json.JSONDecodeError as e:
            print(json.dumps({"valid": False, "error": f"JSON parse error: {e}"}))

    else:
        print(
            "Usage: driving_forces_utils.py [\n"
            "  validate                              — ALL_PASS 자체 검증\n"
            "  verbatim KEY                          — PDF verbatim 인용\n"
            "  verbatim_all                          — 전체 verbatim 출력\n"
            "  steeps                                — STEEPS 6 domains\n"
            "  futures_matrix                        — Millennium Futures Matrix\n"
            "  personas                              — 8 고정 페르소나 + 집계 규칙\n"
            "  validate_count N STAGE                — 변수 수 검증 (raw/winnowed/final)\n"
            "  classify_type FORCE_DESCRIPTION       — Predetermined vs Uncertainty 분류 가이드\n"
            "  schwartz_step N                       — Schwartz Step N (1-7)\n"
            "  schwartz_all                          — Schwartz Steps 전체\n"
            "  winnowing_algorithm                   — Coates winnowing 알고리즘\n"
            "  force_types                           — Predetermined vs Critical Uncertainty 정의\n"
            "]"
        )
