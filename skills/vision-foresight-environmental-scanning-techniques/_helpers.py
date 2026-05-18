#!/usr/bin/env python3
"""
vision-foresight-environmental-scanning-techniques: Deterministic helper functions.

Handles steps that LLMs could hallucinate if left to natural language inference:
- Date/year retrieval
- Boolean query building and validation
- Expert panel size recommendation
- Technique scoring / selection matrix

Sources:
  Gordon & Glenn (2009) Section III — 6 Environmental Scanning Techniques
  Panel size ranges and technique weights are operational definitions
  per SKILL.md and references/expert_panel_design_deep.md.

Usage (CLI):
  python3 _helpers.py --date                           → ISO 8601 UTC datetime
  python3 _helpers.py --year                           → current year (int)
  python3 _helpers.py --boolean-build '{"include":["AGI","alignment"],"exclude":["stock"],"exact":["korean fertility"]}'
                                                       → Boolean query string
  python3 _helpers.py --boolean-validate 'AGI AND (alignment OR safety) NOT stock'
                                                       → valid | invalid: reason
  python3 _helpers.py --panel-size CONTEXT_TYPE        → JSON size recommendation
  python3 _helpers.py --technique-score '{"context":"research","resources":"medium","horizon":"10y"}'
                                                       → JSON technique priority scores
  python3 _helpers.py --test                           → run self-tests
"""

import sys
import re
import json
import argparse
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Constants — operational definitions from SKILL.md + references
# ---------------------------------------------------------------------------

# Expert Panel size ranges per context type (Gordon-Glenn 2009 +박사님 컨텍스트)
PANEL_SIZES = {
    "unu_standard":      {"min": 50, "recommended": 75, "max": 100,
                          "note": "UNU/Millennium Project standard (Gordon-Glenn 2009)"},
    "research_institute": {"min": 30, "recommended": 40, "max": 50,
                           "note": "아시아미래인재연구소 1인+자문 — UNU 축소 버전"},
    "church":            {"min": 15, "recommended": 18, "max": 20,
                          "note": "교회 평신도+사역자 panel"},
    "investment":        {"min": 5,  "recommended": 7,  "max": 10,
                          "note": "금융투자 소수 정예 — 신뢰 동료"},
    "corporate":         {"min": 20, "recommended": 35, "max": 50,
                          "note": "일반 기업 issues management panel"},
}

# Technique weight matrix per context (0-10 scale)
# Derived from SKILL.md 6 기법 통합 운영 매트릭스
TECHNIQUE_WEIGHTS = {
    "research_institute": {
        "expert_panels": 9, "database_review": 6, "internet_searches": 9,
        "hard_copy": 3, "expert_essays": 6, "key_person_tracking": 9,
    },
    "church": {
        "expert_panels": 7, "database_review": 6, "internet_searches": 8,
        "hard_copy": 3, "expert_essays": 3, "key_person_tracking": 6,
    },
    "investment": {
        "expert_panels": 4, "database_review": 9, "internet_searches": 9,
        "hard_copy": 2, "expert_essays": 2, "key_person_tracking": 9,
    },
    "general": {
        "expert_panels": 7, "database_review": 7, "internet_searches": 7,
        "hard_copy": 4, "expert_essays": 5, "key_person_tracking": 7,
    },
}

VALID_BOOLEAN_OPS = {"AND", "OR", "NOT"}
TECHNIQUE_NAMES = list(TECHNIQUE_WEIGHTS["general"].keys())


# ---------------------------------------------------------------------------
# Core deterministic functions
# ---------------------------------------------------------------------------

def get_current_utc_datetime() -> str:
    """Current UTC datetime in ISO 8601. Never hallucinated."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def get_current_year() -> int:
    """Current calendar year. Never hallucinated."""
    return datetime.now(timezone.utc).year


def build_boolean_query(
    include_terms: list,
    exclude_terms: list = None,
    exact_phrases: list = None,
) -> str:
    """
    Build a well-formed Boolean search query.
    Deterministic — prevents LLM from generating malformed queries.

    Rules (per Gordon-Glenn 2009 Database Lit Review guidance):
    - Include terms joined with AND
    - Exclude terms prefixed with NOT
    - Exact phrases wrapped in double quotes
    - Multiple includes produce: (term1 OR term2)
    - Combined: (include group) AND NOT (exclude group)

    Args:
        include_terms: list of keywords to include (OR logic within group)
        exclude_terms: list of keywords to exclude (NOT logic)
        exact_phrases: list of exact phrase strings (wrapped in quotes)

    Returns:
        Well-formed Boolean query string.
    """
    if not include_terms and not exact_phrases:
        raise ValueError("At least one include term or exact phrase required")

    parts = []

    # Exact phrases
    if exact_phrases:
        quoted = [f'"{p}"' for p in exact_phrases]
        if len(quoted) == 1:
            parts.append(quoted[0])
        else:
            parts.append("(" + " OR ".join(quoted) + ")")

    # Include terms
    if include_terms:
        if len(include_terms) == 1:
            parts.append(include_terms[0])
        else:
            parts.append("(" + " OR ".join(include_terms) + ")")

    query = " AND ".join(parts)

    # Exclude terms
    if exclude_terms:
        if len(exclude_terms) == 1:
            query += f" NOT {exclude_terms[0]}"
        else:
            query += " NOT (" + " OR ".join(exclude_terms) + ")"

    return query


def validate_boolean_query(query: str) -> tuple:
    """
    Validate Boolean query syntax.
    Returns (is_valid: bool, message: str).

    Checks:
    1. Balanced parentheses
    2. Balanced double quotes
    3. No adjacent operators (AND AND, OR OR)
    4. Not starting/ending with operator
    5. Minimum 1 search term
    """
    if not query or not query.strip():
        return False, "Empty query"

    q = query.strip()

    # Check balanced parentheses
    depth = 0
    for ch in q:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if depth < 0:
            return False, "Unbalanced parentheses: extra ')'"
    if depth != 0:
        return False, f"Unbalanced parentheses: {depth} unclosed '('"

    # Check balanced double quotes
    quote_count = q.count('"')
    if quote_count % 2 != 0:
        return False, f"Unbalanced double quotes: {quote_count} quote(s)"

    # Check for adjacent boolean operators
    for op1 in VALID_BOOLEAN_OPS:
        for op2 in VALID_BOOLEAN_OPS:
            pattern = rf'\b{op1}\s+{op2}\b'
            if re.search(pattern, q, re.IGNORECASE):
                return False, f"Adjacent operators: {op1} {op2}"

    # Check does not start with AND/OR (at query start or after opening paren)
    for op in ("AND", "OR"):
        if re.match(rf'^\s*{op}\b', q, re.IGNORECASE):
            return False, f"Query cannot start with {op}"
        if re.search(rf'\(\s*{op}\b', q, re.IGNORECASE):
            return False, f"Operator {op} cannot appear at start of parenthetical group"

    # Check does not end with operator
    for op in VALID_BOOLEAN_OPS:
        if re.search(rf'\b{op}\s*$', q, re.IGNORECASE):
            return False, f"Query cannot end with {op}"

    # Must have at least one non-operator word
    stripped = re.sub(r'\b(AND|OR|NOT)\b', '', q, flags=re.IGNORECASE)
    stripped = re.sub(r'[()"\s]', '', stripped)
    if not stripped:
        return False, "No search terms found (only operators)"

    return True, "valid"


def recommend_panel_size(context_type: str) -> dict:
    """
    Return recommended Expert Panel size for a given context.
    Deterministic mapping — LLM must not infer sizes from scratch.

    context_type options: unu_standard, research_institute, church, investment, corporate
    Falls back to general if unknown.
    """
    key = context_type.lower().replace(" ", "_").replace("-", "_")
    if key not in PANEL_SIZES:
        return {
            "context": context_type,
            "min": 20, "recommended": 30, "max": 50,
            "note": f"Unknown context '{context_type}' — using general defaults",
            "fallback": True,
        }
    rec = dict(PANEL_SIZES[key])
    rec["context"] = context_type
    return rec


def score_technique_fit(context: str, resources: str = "medium", horizon: str = "10y") -> dict:
    """
    Score all 6 techniques by fit for a given scanning context.
    Deterministic priority scoring — LLM must not rank techniques manually.

    Args:
        context: 'research_institute' | 'church' | 'investment' | 'general'
        resources: 'low' | 'medium' | 'high' (affects technique feasibility)
        horizon: '1y' | '5y' | '10y' | '20y' (affects technique emphasis)

    Returns:
        dict with technique names → adjusted score + rank + rationale.
    """
    key = context.lower().replace(" ", "_").replace("-", "_")
    weights = TECHNIQUE_WEIGHTS.get(key, TECHNIQUE_WEIGHTS["general"])

    # Resource modifier: low resources penalize high-burden techniques
    resource_penalty = {
        "expert_panels": {"low": -3, "medium": 0, "high": 1},
        "database_review": {"low": -1, "medium": 0, "high": 1},
        "internet_searches": {"low": 0, "medium": 0, "high": 0},
        "hard_copy": {"low": -2, "medium": -1, "high": 0},
        "expert_essays": {"low": -4, "medium": -1, "high": 1},
        "key_person_tracking": {"low": 0, "medium": 0, "high": 1},
    }

    # Horizon modifier: long horizon benefits essays + panels
    horizon_bonus = {
        "expert_panels": {"1y": -1, "5y": 0, "10y": 1, "20y": 2},
        "database_review": {"1y": 0, "5y": 0, "10y": 0, "20y": 0},
        "internet_searches": {"1y": 2, "5y": 1, "10y": 0, "20y": -1},
        "hard_copy": {"1y": -1, "5y": 0, "10y": 1, "20y": 1},
        "expert_essays": {"1y": -2, "5y": 0, "10y": 1, "20y": 2},
        "key_person_tracking": {"1y": 1, "5y": 1, "10y": 0, "20y": 0},
    }

    res_key = resources.lower()
    hor_key = horizon.lower()

    scores = {}
    for tech in TECHNIQUE_NAMES:
        base = weights[tech]
        rmod = resource_penalty.get(tech, {}).get(res_key, 0)
        hmod = horizon_bonus.get(tech, {}).get(hor_key, 0)
        adjusted = max(0, min(10, base + rmod + hmod))
        scores[tech] = adjusted

    # Rank by score
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    result = {
        "context": context,
        "resources": resources,
        "horizon": horizon,
        "scores": {},
    }
    for rank_i, (tech, score) in enumerate(ranked, 1):
        result["scores"][tech] = {"score": score, "rank": rank_i}

    return result


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

def self_test() -> None:
    print("=== vision-foresight-environmental-scanning-techniques _helpers.py self-test ===\n")

    dt = get_current_utc_datetime()
    yr = get_current_year()
    assert len(dt) == 20 and dt.endswith("Z"), f"Datetime wrong: {dt}"
    assert 2025 <= yr <= 2035
    print(f"[PASS] get_current_utc_datetime → {dt}")
    print(f"[PASS] get_current_year → {yr}")

    # Boolean query builder
    q1 = build_boolean_query(["AGI", "alignment"], ["stock"], ["korean fertility rate"])
    assert '"korean fertility rate"' in q1
    assert "AGI" in q1 and "alignment" in q1
    assert "NOT" in q1 and "stock" in q1
    print(f"[PASS] build_boolean_query → {q1}")

    q2 = build_boolean_query(["AI safety"])
    assert q2 == "AI safety"
    print(f"[PASS] build_boolean_query (single term) → {q2}")

    q3 = build_boolean_query([], exact_phrases=["synthetic biology"])
    assert q3 == '"synthetic biology"'
    print(f"[PASS] build_boolean_query (exact phrase only) → {q3}")

    # Boolean query validator
    valid_cases = [
        'AGI AND (alignment OR safety) NOT stock',
        '"korean fertility rate" AND population',
        'AI NOT "blockchain"',
        'AGI',
    ]
    for q in valid_cases:
        ok, msg = validate_boolean_query(q)
        assert ok, f"Should be valid: {q!r} → {msg}"
    print(f"[PASS] validate_boolean_query — {len(valid_cases)} valid cases")

    invalid_cases = [
        ('AGI AND AND safety', "adjacent operators"),
        ('AND AGI', "starts with AND"),
        ('AGI OR', "ends with OR"),
        ('AGI (AND safety)', "operator at start of group"),
        ('(AGI', "unbalanced parentheses"),
        ('"unclosed phrase', "unbalanced quotes"),
    ]
    for q, desc in invalid_cases:
        ok, msg = validate_boolean_query(q)
        assert not ok, f"Should be invalid ({desc}): {q!r}"
    print(f"[PASS] validate_boolean_query — {len(invalid_cases)} invalid cases")

    # Panel size recommendation
    unu = recommend_panel_size("unu_standard")
    assert unu["recommended"] == 75
    church = recommend_panel_size("church")
    assert church["min"] == 15 and church["max"] == 20
    invest = recommend_panel_size("investment")
    assert invest["min"] == 5 and invest["max"] == 10
    unknown = recommend_panel_size("unknown_org")
    assert unknown["fallback"] is True
    print("[PASS] recommend_panel_size — unu(75), church(15-20), investment(5-10), fallback")

    # Technique scoring
    scores_research = score_technique_fit("research_institute", "medium", "10y")
    assert "scores" in scores_research
    assert all(t in scores_research["scores"] for t in TECHNIQUE_NAMES)
    # For research_institute, expert_panels + internet_searches + key_person_tracking should be top
    top3 = [t for t, v in sorted(scores_research["scores"].items(),
                                   key=lambda x: x[1]["score"], reverse=True)][:3]
    print(f"[PASS] score_technique_fit research_institute top3: {top3}")

    scores_invest = score_technique_fit("investment", "low", "5y")
    # internet_searches and key_person_tracking should rank high for investment/low resources
    print(f"[PASS] score_technique_fit investment/low/5y: {scores_invest['scores']}")

    print("\n=== ALL SELF-TESTS PASSED ===")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Deterministic helpers for vision-foresight-environmental-scanning-techniques"
    )
    parser.add_argument("--date", action="store_true", help="Print current UTC datetime")
    parser.add_argument("--year", action="store_true", help="Print current year")
    parser.add_argument("--boolean-build", metavar="JSON",
                        help='Build Boolean query from JSON: {"include":[],"exclude":[],"exact":[]}')
    parser.add_argument("--boolean-validate", metavar="QUERY",
                        help="Validate Boolean query syntax")
    parser.add_argument("--panel-size", metavar="CONTEXT_TYPE",
                        help="Recommend Expert Panel size for context type")
    parser.add_argument("--technique-score", metavar="JSON",
                        help='Score techniques: {"context":"...","resources":"...","horizon":"..."}')
    parser.add_argument("--test", action="store_true", help="Run self-tests")

    args = parser.parse_args()

    if args.test:
        self_test()
    elif args.date:
        print(get_current_utc_datetime())
    elif args.year:
        print(get_current_year())
    elif args.boolean_build:
        params = json.loads(args.boolean_build)
        q = build_boolean_query(
            include_terms=params.get("include", []),
            exclude_terms=params.get("exclude"),
            exact_phrases=params.get("exact"),
        )
        print(q)
    elif args.boolean_validate:
        ok, msg = validate_boolean_query(args.boolean_validate)
        if ok:
            print("valid")
        else:
            print(f"invalid: {msg}")
    elif args.panel_size:
        result = recommend_panel_size(args.panel_size)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.technique_score:
        params = json.loads(args.technique_score)
        result = score_technique_fit(
            context=params.get("context", "general"),
            resources=params.get("resources", "medium"),
            horizon=params.get("horizon", "10y"),
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
