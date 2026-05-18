#!/usr/bin/env python3
"""
cone_engine.py — Deterministic engine for the
vision-foresight-scenarios-cone-of-plausibility sub-skill.

Primary source (verbatim):
  Glenn, J. C., & The Futures Group International. (2009).
  "Scenarios," Ch.19 in *Futures Research Methodology V3.0*,
  ed. J. C. Glenn & T. J. Gordon, The Millennium Project.
  Section V Frontiers — Charles W. Taylor "Cone of Plausibility."

Cross-cited (the Taylor primary source):
  Taylor, C. W. (1990). *Alternative World Scenarios for Strategic
  Planning.* U.S. Army War College, Strategic Studies Institute.
  Taylor, C. W. (1993). "Alternative Scenarios for the Future of
  Chemicals in Industrial Use," *Chemtech*, 23(7) July 1993.

This module performs every step that is deterministically reducible:
  - 4-theme inventory check         (Technology·Politics·Economics·Sociology)
  - 10 strategic elements / Top-4   (count·rank·duplicate checks)
  - wild card classification        (Catastrophic·Disruptive·Aberrant)
  - micro-scenario permutation      (delegates to cone_permutation.py logic)
  - mini-scenario word count        (target 500, accept 450-550)
  - causal-chain stage counter      (≥3 explicit stages for Plausibility)
  - internal-consistency cross-ref  (every scenario references Top-4 ids)
  - verbatim phrase coverage        (8 required Taylor/Glenn phrases)
  - time horizon format             (Nyr / N-Myr / N years)
  - integrated cone_validate

LLM may NOT regenerate any of these by natural-language inference.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
from typing import Dict, List, Tuple


# ─── 0. CITATION CONSTANT ────────────────────────────────────────────────────

SOURCE_PRIMARY = (
    "Glenn & TFG (2009) FRM V3.0 Ch.19 Section V Frontiers — "
    "Taylor 'Cone of Plausibility' (Chemtech 1993; "
    "Taylor 1990 *Alternative World Scenarios for Strategic Planning*, USAWC)"
)


# ─── 1. FROZEN CONSTANTS ─────────────────────────────────────────────────────

# Exhibit 3 verbatim themes — order matters (Taylor's column order).
CANONICAL_THEMES = ("Technology", "Politics", "Economics", "Sociology")

# Aliases (case-insensitive); also accepts adjectival forms from PDF Exhibit 3.
THEME_ALIASES: Dict[str, str] = {
    "technology": "Technology",
    "technological": "Technology",
    "tech": "Technology",
    "t": "Technology",
    "politics": "Politics",
    "political": "Politics",
    "p": "Politics",
    "economics": "Economics",
    "economic": "Economics",
    "economy": "Economics",
    "e": "Economics",
    "sociology": "Sociology",
    "sociological": "Sociology",
    "social": "Sociology",
    "society": "Sociology",
    "s": "Sociology",
}

# Wild card classification — 3 tiers (SKILL.md §3 Step 6 table).
WILD_CARD_TIERS = ("Catastrophic", "Disruptive", "Aberrant")

# Mini-scenario word count band — Taylor verbatim "about 500 words"
WORD_COUNT_TARGET = 500
WORD_COUNT_MIN = 450
WORD_COUNT_MAX = 550

# Strategic-element rules from Taylor verbatim.
N_STRATEGIC_ELEMENTS = 10
N_TOP_ELEMENTS = 4
N_MICRO_STATEMENTS = 8           # 4 positive + 4 opposing
N_MICRO_SELECTED = 4             # final ordered statements
N_PLANNING_SCENARIOS = 4         # one per theme

# Glenn 3-criteria minimum thresholds.
MIN_CAUSAL_STAGES = 3            # "logical progression of trends, events, and consequences"

# Eight required verbatim phrases — Taylor 1993 + Glenn TFG V3.0 19장.
VERBATIM_REQUIRED: Tuple[str, ...] = (
    # AIM verbatim
    "Cone of Plausibility",
    # Process verbatim
    "ten most important strategic elements",
    "four short statements that reflect positive attitudes",
    "process of permutation and sorting of the eight statements",
    "expanding micro-scenarios to mini-scenarios of about 500 words",
    # Outside-cone verbatim
    "Outside of the cone are wild-card scenarios",
    # Plausibility definition verbatim (Taylor)
    "logical progression of trends, events, and consequences",
    # Glenn 3-criteria verbatim (TFG V3.0 §III)
    "Plausible",
)


# ─── 2. THEME VALIDATION ─────────────────────────────────────────────────────

def canonicalize_theme(name: str) -> str:
    """Map a theme name (or alias) to its canonical Exhibit 3 form."""
    if not isinstance(name, str):
        return ""
    key = name.strip().lower()
    if key in THEME_ALIASES:
        return THEME_ALIASES[key]
    for t in CANONICAL_THEMES:
        if t.lower() == key:
            return t
    return ""


def validate_themes(themes: List[str], allow_extra: bool = True) -> dict:
    """Validate that themes include all 4 canonical Exhibit 3 themes.

    Args:
      themes: list of theme strings.
      allow_extra: if True, additional themes (e.g. Spiritual·Environmental)
                   may follow the 4 canonical ones; they are returned as
                   `extras`. If False, only the canonical four are allowed.
    """
    if not isinstance(themes, list) or len(themes) < N_PLANNING_SCENARIOS:
        return {
            "valid": False,
            "error": f"Need >= {N_PLANNING_SCENARIOS} themes, got {len(themes) if isinstance(themes, list) else 0}.",
        }
    canon = [canonicalize_theme(t) for t in themes]
    unknown = [orig for orig, c in zip(themes, canon) if not c]
    if unknown:
        return {
            "valid": False,
            "error": f"Unknown theme(s): {unknown}. Valid: {list(CANONICAL_THEMES)}.",
        }
    present = set(canon)
    missing_canon = [t for t in CANONICAL_THEMES if t not in present]
    if missing_canon:
        return {
            "valid": False,
            "error": f"Missing canonical theme(s): {missing_canon}. Exhibit 3 mandates all 4.",
        }
    extras = [c for c in canon if c not in CANONICAL_THEMES]
    if extras and not allow_extra:
        return {
            "valid": False,
            "error": f"Extra theme(s) not allowed: {extras}.",
        }
    seen = set()
    duplicates = []
    for c in canon:
        if c in seen:
            duplicates.append(c)
        seen.add(c)
    if duplicates:
        return {
            "valid": False,
            "error": f"Duplicate theme(s): {duplicates}.",
        }
    return {
        "valid": True,
        "canonical_themes": [c for c in canon if c in CANONICAL_THEMES],
        "extras": extras,
        "source": SOURCE_PRIMARY + " — Exhibit 3.",
    }


# ─── 3. STRATEGIC ELEMENTS & TOP-4 ───────────────────────────────────────────

def validate_strategic_elements(elements: List[dict]) -> dict:
    """Validate that there are exactly 10 ranked strategic elements,
    ranks 1..10 are present, and `name` fields are unique non-empty."""
    if not isinstance(elements, list):
        return {"valid": False, "error": "elements must be a list."}
    if len(elements) != N_STRATEGIC_ELEMENTS:
        return {"valid": False, "error": f"Need exactly {N_STRATEGIC_ELEMENTS} elements, got {len(elements)}."}
    seen_ranks = set()
    seen_names = set()
    for i, e in enumerate(elements):
        if not isinstance(e, dict):
            return {"valid": False, "error": f"Element #{i} is not an object."}
        rank = e.get("rank")
        name = e.get("name", "")
        if not isinstance(rank, int) or rank < 1 or rank > N_STRATEGIC_ELEMENTS:
            return {"valid": False, "error": f"Element #{i} rank={rank!r} must be 1..{N_STRATEGIC_ELEMENTS}."}
        if rank in seen_ranks:
            return {"valid": False, "error": f"Duplicate rank {rank}."}
        if not isinstance(name, str) or not name.strip():
            return {"valid": False, "error": f"Element rank={rank} has empty name."}
        n = name.strip().lower()
        if n in seen_names:
            return {"valid": False, "error": f"Duplicate element name: {name!r}."}
        seen_ranks.add(rank)
        seen_names.add(n)
    missing = set(range(1, N_STRATEGIC_ELEMENTS + 1)) - seen_ranks
    if missing:
        return {"valid": False, "error": f"Missing rank(s): {sorted(missing)}."}
    top4 = sorted(elements, key=lambda x: x["rank"])[:N_TOP_ELEMENTS]
    return {
        "valid": True,
        "count": len(elements),
        "top4": [{"rank": e["rank"], "name": e["name"]} for e in top4],
        "source": SOURCE_PRIMARY + " — 'ten most important strategic elements' (Taylor)",
    }


def validate_top4_consistency(scenarios: List[dict], top4_names: List[str]) -> dict:
    """For Glenn 'Internally consistent' criterion: every scenario must
    reference the Top-4 element names so cross-comparison is possible."""
    if not isinstance(scenarios, list) or len(scenarios) != N_PLANNING_SCENARIOS:
        return {"valid": False, "error": f"Need {N_PLANNING_SCENARIOS} scenarios, got {len(scenarios) if isinstance(scenarios, list) else 0}."}
    if not isinstance(top4_names, list) or len(top4_names) != N_TOP_ELEMENTS:
        return {"valid": False, "error": f"top4_names must have {N_TOP_ELEMENTS} entries."}
    top4_lower = [t.strip().lower() for t in top4_names]
    misses = []
    for sc in scenarios:
        name = sc.get("name", "?")
        text = (sc.get("mini_scenario", "") or "").lower()
        missing = [t for t in top4_lower if t not in text]
        if missing:
            misses.append({"scenario": name, "missing_top4_refs": missing})
    if misses:
        return {
            "valid": False,
            "error": "Internal consistency failure: some scenarios do not reference all Top-4 elements.",
            "details": misses,
        }
    return {
        "valid": True,
        "summary": "All 4 scenarios reference all Top-4 strategic elements (Internally Consistent).",
        "source": "Glenn TFG V3.0 §III — 'alternative scenarios should address similar issues'",
    }


# ─── 4. WILD CARD CLASSIFICATION ─────────────────────────────────────────────

def classify_wild_card(event: str, n_scenarios_affected: int) -> dict:
    """Tier a wild card by how many of the 4 planning scenarios it affects."""
    if not isinstance(event, str) or not event.strip():
        return {"valid": False, "error": "event must be a non-empty string."}
    try:
        n = int(n_scenarios_affected)
    except (TypeError, ValueError):
        return {"valid": False, "error": "n_scenarios_affected must be an integer 1..4."}
    if n < 1 or n > N_PLANNING_SCENARIOS:
        return {"valid": False, "error": f"n_scenarios_affected={n} out of [1,{N_PLANNING_SCENARIOS}]."}
    if n == N_PLANNING_SCENARIOS:
        tier = "Catastrophic"
    elif n >= 2:
        tier = "Disruptive"
    else:
        tier = "Aberrant"
    return {
        "valid": True,
        "event": event.strip(),
        "n_scenarios_affected": n,
        "tier": tier,
        "definition": {
            "Catastrophic": "neutralises all 4 planning scenarios",
            "Disruptive": "redirects >=2 planning scenarios",
            "Aberrant": "invalidates exactly 1 planning scenario",
        }[tier],
        "source": SOURCE_PRIMARY + " — Outside the cone are wild-card scenarios",
    }


# ─── 5. MICRO-SCENARIO PERMUTATION ───────────────────────────────────────────

def permute_micro(statements: List[str], seed=None) -> dict:
    """Select 4 statements at random from 8 (4 positive + 4 opposing).

    Mirrors cone_permutation.py logic but exposed as a function so the
    engine can call it without spawning a subprocess.
    """
    if not isinstance(statements, list):
        return {"valid": False, "error": "statements must be a list."}
    if len(statements) != N_MICRO_STATEMENTS:
        return {
            "valid": False,
            "error": f"Need exactly {N_MICRO_STATEMENTS} statements "
                     f"(4 positive + 4 opposing); got {len(statements)}.",
        }
    if any(not isinstance(s, str) or not s.strip() for s in statements):
        return {"valid": False, "error": "Empty or non-string statement found."}
    if len(set(s.strip() for s in statements)) != N_MICRO_STATEMENTS:
        return {"valid": False, "error": "Duplicate statements detected."}
    rng = random.Random(seed)
    selected = rng.sample(statements, N_MICRO_SELECTED)
    return {
        "valid": True,
        "input_count": N_MICRO_STATEMENTS,
        "selected_count": N_MICRO_SELECTED,
        "seed_used": seed,
        "selected_micro_scenario": selected,
        "source": SOURCE_PRIMARY + " — Taylor Step 8 permutation",
    }


# ─── 6. WORD-COUNT + CAUSAL CHAIN ────────────────────────────────────────────

def count_words(text: str) -> int:
    """Return whitespace-tokenized word count."""
    if not isinstance(text, str):
        return 0
    return len([w for w in re.split(r"\s+", text.strip()) if w])


def validate_word_count(text: str) -> dict:
    n = count_words(text)
    band_ok = WORD_COUNT_MIN <= n <= WORD_COUNT_MAX
    return {
        "valid": band_ok,
        "word_count": n,
        "target": WORD_COUNT_TARGET,
        "band": [WORD_COUNT_MIN, WORD_COUNT_MAX],
        "action": "OK" if band_ok else ("EXPAND" if n < WORD_COUNT_MIN else "COMPRESS"),
        "source": SOURCE_PRIMARY + " — 'mini-scenarios of about 500 words'",
    }


# Causal-chain markers — Korean and English connective tokens that signal
# explicit stage progression for the Plausibility criterion.
_CAUSAL_MARKERS = [
    "오늘", "현재", "이후", "그다음", "그 다음", "그러면", "결국", "마침내",
    "단계 1", "단계 2", "단계 3", "1단계", "2단계", "3단계",
    "phase 1", "phase 2", "phase 3", "stage 1", "stage 2", "stage 3",
    "today", "by 2030", "by 2035", "by 2040", "by 2050",
    "then", "subsequently", "next", "finally", "by year", "first,", "second,", "third,",
]


def count_causal_stages(text: str) -> int:
    if not isinstance(text, str) or not text.strip():
        return 0
    lower = text.lower()
    return sum(1 for m in _CAUSAL_MARKERS if m in lower)


def validate_plausibility(text: str) -> dict:
    n = count_causal_stages(text)
    ok = n >= MIN_CAUSAL_STAGES
    return {
        "valid": ok,
        "causal_stages_found": n,
        "required": MIN_CAUSAL_STAGES,
        "source": "Taylor 1993 — 'logical progression of trends, events, and consequences'",
    }


# ─── 7. VERBATIM COVERAGE ────────────────────────────────────────────────────

def _normalize(s: str) -> str:
    return (
        s.replace("‘", "'").replace("’", "'")
         .replace("“", '"').replace("”", '"')
         .replace("–", "-").replace("—", "-")
    )


def check_verbatim(output_text: str) -> dict:
    if not isinstance(output_text, str):
        return {"all_present": False, "error": "output_text must be a string."}
    norm = _normalize(output_text).lower()
    details = {}
    for phrase in VERBATIM_REQUIRED:
        details[phrase] = _normalize(phrase).lower() in norm
    present = sum(details.values())
    return {
        "all_present": present == len(VERBATIM_REQUIRED),
        "present_count": present,
        "total": len(VERBATIM_REQUIRED),
        "details": details,
        "source": SOURCE_PRIMARY,
    }


# ─── 8. TIME-HORIZON FORMAT ──────────────────────────────────────────────────

def validate_horizon(horizon: str) -> dict:
    if not isinstance(horizon, str) or not horizon.strip():
        return {"valid": False, "error": "horizon must be a non-empty string."}
    s = horizon.strip().lower().replace(" ", "")
    m = re.fullmatch(r"(\d{1,3})(?:-(\d{1,3}))?yr|(\d{1,3})years?", s)
    if not m:
        return {"valid": False, "error": f"Invalid horizon {horizon!r}. Use '15-25yr', '10yr', '20 years'."}
    if m.group(1) and m.group(2):
        lo, hi = int(m.group(1)), int(m.group(2))
        if lo >= hi:
            return {"valid": False, "error": f"horizon lower {lo}yr must be < upper {hi}yr."}
        if hi > 100:
            return {"valid": False, "error": f"horizon upper {hi}yr exceeds 100yr ceiling."}
        return {"valid": True, "lower_yr": lo, "upper_yr": hi}
    n = int(m.group(1) or m.group(3))
    if n < 1 or n > 100:
        return {"valid": False, "error": f"horizon {n}yr out of [1,100]."}
    return {"valid": True, "single_yr": n}


# ─── 9. INTEGRATED COMPLIANCE ────────────────────────────────────────────────

def cone_validate(payload: dict) -> dict:
    """Integrated Card-equivalent compliance pass.

    Expected payload keys: themes, elements, scenarios, wild_cards, horizon,
    output_text. Each is optional — only present keys are validated.
    """
    if not isinstance(payload, dict):
        return {"valid": False, "error": "payload must be a JSON object."}
    out = {}
    if "themes" in payload:
        out["themes"] = validate_themes(payload["themes"])
    if "elements" in payload:
        out["elements"] = validate_strategic_elements(payload["elements"])
        top4_names = [e["name"] for e in out["elements"].get("top4", [])]
        if "scenarios" in payload and top4_names:
            out["top4_consistency"] = validate_top4_consistency(payload["scenarios"], top4_names)
    if "wild_cards" in payload:
        out["wild_cards"] = [
            classify_wild_card(w.get("event", ""), w.get("n_scenarios_affected", 0))
            for w in payload["wild_cards"]
        ]
    if "horizon" in payload:
        out["horizon"] = validate_horizon(payload["horizon"])
    if "output_text" in payload:
        out["verbatim"] = check_verbatim(payload["output_text"])
    if "scenarios" in payload:
        wc = []
        plaus = []
        for s in payload["scenarios"]:
            text = s.get("mini_scenario", "")
            wc.append({"name": s.get("name", "?"), **validate_word_count(text)})
            plaus.append({"name": s.get("name", "?"), **validate_plausibility(text)})
        out["word_counts"] = wc
        out["plausibility"] = plaus
    # roll up
    flat = []
    def walk(v):
        if isinstance(v, dict):
            if "valid" in v or "all_present" in v:
                flat.append(v.get("valid", v.get("all_present", False)))
            else:
                for vv in v.values(): walk(vv)
        elif isinstance(v, list):
            for vv in v: walk(vv)
    walk(out)
    out["all_valid"] = all(flat) if flat else False
    out["source"] = SOURCE_PRIMARY
    return out


# ─── 10. CLI ─────────────────────────────────────────────────────────────────

COMMANDS = {
    "validate_themes": lambda d: validate_themes(d.get("themes", []), d.get("allow_extra", True)),
    "validate_strategic_elements": lambda d: validate_strategic_elements(d.get("elements", [])),
    "validate_top4_consistency": lambda d: validate_top4_consistency(d.get("scenarios", []), d.get("top4_names", [])),
    "classify_wild_card": lambda d: classify_wild_card(d.get("event", ""), d.get("n_scenarios_affected", 0)),
    "permute_micro": lambda d: permute_micro(d.get("statements", []), d.get("seed")),
    "validate_word_count": lambda d: validate_word_count(d.get("text", "")),
    "validate_plausibility": lambda d: validate_plausibility(d.get("text", "")),
    "check_verbatim": lambda d: check_verbatim(d.get("output_text", "")),
    "validate_horizon": lambda d: validate_horizon(d.get("horizon", "")),
    "cone_validate": lambda d: cone_validate(d),
    "list_canonical_themes": lambda d: {"themes": list(CANONICAL_THEMES), "source": SOURCE_PRIMARY},
    "list_wild_card_tiers": lambda d: {"tiers": list(WILD_CARD_TIERS), "source": SOURCE_PRIMARY},
    "list_verbatim_required": lambda d: {"verbatim": list(VERBATIM_REQUIRED), "count": len(VERBATIM_REQUIRED)},
}


def main():
    p = argparse.ArgumentParser(description="Cone of Plausibility deterministic engine")
    p.add_argument("--cmd", help="Command name (alternative to JSON stdin 'cmd' field)")
    args, _ = p.parse_known_args()
    try:
        raw = sys.stdin.read().strip()
        payload = json.loads(raw) if raw else {}
    except json.JSONDecodeError as e:
        sys.stdout.write(json.dumps({"error": f"JSON parse error: {e}"}) + "\n")
        sys.exit(1)
    cmd = args.cmd or payload.get("cmd", "")
    if cmd not in COMMANDS:
        sys.stdout.write(json.dumps({
            "error": f"Unknown command: {cmd!r}.",
            "available_commands": sorted(COMMANDS.keys()),
        }) + "\n")
        sys.exit(1)
    sys.stdout.write(json.dumps(COMMANDS[cmd](payload), ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
