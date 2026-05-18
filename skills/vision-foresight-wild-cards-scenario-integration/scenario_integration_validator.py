#!/usr/bin/env python3
"""
scenario_integration_validator.py
Deterministic Steinmüller 1997 6-Rule Wild Card Selection Validator
Permanent component of vision-foresight-wild-cards-scenario-integration skill.

Source:
  Steinmüller K. (1997) The Future as Wild Card. SFZ-Werkstattbericht 20.
  Petersen & Steinmüller (2009) V3.0 Chapter 10, Section V "Use with Other Methods"

Deterministic rules (implemented here):
  R-4: count(WC_pool) >= 4  — "not limited to only two or three"
  R-5: negative WCs ordered first — "considered first" as stability test
  R-6: ≥1 contextual AND ≥1 peripheral WC present

Non-deterministic (LLM judgment required — NOT implemented here):
  R-1: topic appropriateness (semantic relevance)
  R-2: novelty and non-obvious consequences
  R-3: "barely possible" classification (NO numeric threshold in source)

Usage:
  python3 scenario_integration_validator.py rules
  python3 scenario_integration_validator.py r4 <count>
  python3 scenario_integration_validator.py validate '<json_array>'
  python3 scenario_integration_validator.py modes
"""

import sys
import json

# ─── VERBATIM RULES TABLE (Section V, Steinmüller 1997) ──────────────────────

STEINMULLER_RULES = {
    "R-1": {
        "verbatim": "Wild Cards have to be appropriate to the situation. Although they do not have to stem from the central area of the study they should be associated with it.",
        "deterministic": False,
        "reason": "Topic relevance/association requires semantic LLM judgment — no computable proxy in source.",
    },
    "R-2": {
        "verbatim": "Wild Cards should be as original and as new as possible. Their consequences should not be immediately apparent.",
        "deterministic": False,
        "reason": "Originality and non-obviousness of consequences require LLM judgment.",
    },
    "R-3": {
        "verbatim": "Wild Cards that are 'barely possible' according to conventional thinking should be used more.",
        "deterministic": False,
        "reason": (
            "'Barely possible' is a qualitative judgment — Steinmüller 1997 specifies NO numeric "
            "probability threshold. Any specific percentage (e.g., ≤5%) is an operational elaboration "
            "OUTSIDE the verbatim. LLM judgment required."
        ),
    },
    "R-4": {
        "verbatim": "The analysis should not be limited to only two or three Wild Cards.",
        "deterministic": True,
        "check": "len(wc_pool) >= 4",
        "reason": "'Not limited to 2-3' logically requires minimum 4.",
    },
    "R-5": {
        "verbatim": "'Negative' Wild Cards that undermine the constructed scenario should be considered first. They are usually a good test of the stability of the scenario.",
        "deterministic": True,
        "check": "all negative-quality WCs appear before positive-quality WCs in ordered list",
        "reason": "'Considered first' = processing order; deterministic once quality_factor is assigned.",
    },
    "R-6": {
        "verbatim": "Wild Cards with a strong contextual reference to the scenario should be combined with Wild Cards that primarily change peripheral conditions and environment of the scenario.",
        "deterministic": True,
        "check": "contextual_count >= 1 AND peripheral_count >= 1",
        "reason": "Presence of both types is structurally checkable.",
        "note": "Source says 'combined' not 'balanced'; equal counts not required.",
    },
}

# Section V 4 Usage Modes (PDF verbatim)
SECTION_V_MODES = {
    "Mode-1": {
        "name": "Susceptibility Test",
        "verbatim": "Wild Cards can be used in order to estimate the susceptibility of a scenario to external disruptions.",
    },
    "Mode-2": {
        "name": "Mental Map Compensation",
        "verbatim": "They can be used to compensate for potential weak points in the conceptual framework (mental map).",
    },
    "Mode-3": {
        "name": "New Alternatives",
        "verbatim": "They can help recognize new alternatives and be open-minded about the 'unexpected'.",
    },
    "Mode-4": {
        "name": "Anti-Wishful-Thinking",
        "verbatim": "Finally, they can be used to fight such common weaknesses as lack of imaginative capacity, wishful thinking or fixation on catastrophic scenarios ('hyper worst case thinking').",
    },
}


# ─── CORE VALIDATION FUNCTIONS ────────────────────────────────────────────────

def validate_r4(count: int) -> dict:
    """R-4: pool must contain >= 4 Wild Cards."""
    passed = count >= 4
    return {
        "rule": "R-4",
        "verbatim": STEINMULLER_RULES["R-4"]["verbatim"],
        "wc_count": count,
        "minimum_required": 4,
        "pass": passed,
        "verdict": "PASS" if passed else f"FAIL — {count} WCs; minimum 4 required (Steinmüller 1997)",
    }


def validate_r5(wc_list: list) -> dict:
    """
    R-5: negative-quality (quality='-') WCs must appear before positive-quality (quality='+') WCs.
    ±(mixed) WCs are treated as NEUTRAL — they may appear anywhere without constraint.
    Policy: Steinmüller 1997 verbatim specifies only "negative first"; ± placement is
    an operational elaboration NOT in the source text.
    Each WC dict must have 'quality': '+' | '-' | '±'
    """
    if not wc_list:
        return {
            "rule": "R-5",
            "verbatim": STEINMULLER_RULES["R-5"]["verbatim"],
            "pass": False,
            "verdict": "FAIL — empty WC list",
        }

    negative_idx = [i for i, w in enumerate(wc_list) if w.get("quality") == "-"]
    positive_idx = [i for i, w in enumerate(wc_list) if w.get("quality") == "+"]
    mixed_idx    = [i for i, w in enumerate(wc_list) if w.get("quality") == "±"]

    if not negative_idx:
        return {
            "rule": "R-5",
            "verbatim": STEINMULLER_RULES["R-5"]["verbatim"],
            "pass": False,
            "verdict": "FAIL — no negative WCs present; stability test requires ≥1 negative WC",
        }

    if positive_idx:
        max_neg = max(negative_idx)
        min_pos = min(positive_idx)
        ordered = max_neg < min_pos
    else:
        ordered = True  # no pure positives → negative-first trivially satisfied

    return {
        "rule": "R-5",
        "verbatim": STEINMULLER_RULES["R-5"]["verbatim"],
        "negative_positions": negative_idx,
        "positive_positions": positive_idx,
        "mixed_positions": mixed_idx,
        "negative_first_satisfied": ordered,
        "pass": ordered,
        "verdict": "PASS" if ordered else "FAIL — negative WCs not listed before positive WCs",
    }


def validate_r6(wc_list: list) -> dict:
    """R-6: must have ≥1 contextual AND ≥1 peripheral WC."""
    contextual = [w for w in wc_list if w.get("wc_type") == "contextual"]
    peripheral = [w for w in wc_list if w.get("wc_type") == "peripheral"]
    has_both = len(contextual) >= 1 and len(peripheral) >= 1

    return {
        "rule": "R-6",
        "verbatim": STEINMULLER_RULES["R-6"]["verbatim"],
        "contextual_count": len(contextual),
        "peripheral_count": len(peripheral),
        "pass": has_both,
        "verdict": "PASS" if has_both else (
            "FAIL — no contextual WCs" if not contextual else
            "FAIL — no peripheral WCs"
        ),
        "note": STEINMULLER_RULES["R-6"]["note"],
    }


def validate_all(wc_list: list) -> dict:
    """Run all 3 deterministic rules on a WC pool."""
    r4 = validate_r4(len(wc_list))
    r5 = validate_r5(wc_list)
    r6 = validate_r6(wc_list)

    return {
        "deterministic_rules": {
            "R-4": r4,
            "R-5": r5,
            "R-6": r6,
        },
        "non_deterministic_rules": {
            "R-1": "LLM judgment — topic appropriateness",
            "R-2": "LLM judgment — originality and non-obvious consequences",
            "R-3": "LLM judgment — 'barely possible' (no numeric threshold in Steinmüller 1997)",
        },
        "all_deterministic_pass": r4["pass"] and r5["pass"] and r6["pass"],
        "source": "Steinmüller K. (1997) SFZ-Werkstattbericht 20; Petersen & Steinmüller (2009) V3.0 §V",
    }


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "commands": {
                "rules":             "Show all 6 rules: verbatim + determinism status",
                "modes":             "Show Section V 4 scenario-WC usage modes (verbatim)",
                "r4 <count>":        "Quick R-4 check: is count >= 4?",
                "validate '<json>'": "Full R-4/R-5/R-6 deterministic validation of WC pool JSON array",
            },
            "wc_schema": {
                "title": "string",
                "quality": "'+' | '-' | '±'",
                "wc_type": "'contextual' | 'peripheral'",
            },
        }, ensure_ascii=False, indent=2))
        sys.exit(0)

    cmd = sys.argv[1].lower()

    try:
        if cmd == "rules":
            print(json.dumps(STEINMULLER_RULES, ensure_ascii=False, indent=2))

        elif cmd == "modes":
            print(json.dumps(SECTION_V_MODES, ensure_ascii=False, indent=2))

        elif cmd == "r4":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "r4: requires count argument (integer)"}, ensure_ascii=False))
                sys.exit(1)
            count = int(sys.argv[2])
            print(json.dumps(validate_r4(count), ensure_ascii=False, indent=2))

        elif cmd == "validate":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "validate: requires JSON array of WC objects"}, ensure_ascii=False))
                sys.exit(1)
            wc_list = json.loads(sys.argv[2])
            if not isinstance(wc_list, list):
                raise ValueError("Input must be a JSON array")
            print(json.dumps(validate_all(wc_list), ensure_ascii=False, indent=2))

        else:
            print(json.dumps({"error": f"Unknown command '{cmd}'"}, ensure_ascii=False))
            sys.exit(1)

    except (ValueError, json.JSONDecodeError) as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
