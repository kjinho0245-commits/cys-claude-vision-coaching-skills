#!/usr/bin/env python3
"""
options_action_catalog.py — Deterministic Catalog for Wild Cards Options-for-Action

Source: Petersen, J.L. & Steinmüller, K. (2009). "Wild Cards."
        In Glenn, J.C. & Gordon, T.J. (eds.), Futures Research Methodology V3.0,
        Chapter 10, Section III.4 "Options for Action: Is there anything we can
        do about them?". Millennium Project, World Federation of United Nations
        Associations, Washington DC.

Purpose: All factual lookups and number-to-name mappings used by the
vision-foresight-wild-cards-options-action sub-skill must come from this deterministic
catalogue. The LLM must NEVER guess segment names, rule numbers, step numbers,
nor outcome polarity — instead, call the appropriate CLI command here.

CLI:
  python3 options_action_catalog.py list_segments
  python3 options_action_catalog.py segment --id S5
  python3 options_action_catalog.py list_nonlinear_tools
  python3 options_action_catalog.py nonlinear_tool --name "Systems thinking"
  python3 options_action_catalog.py list_basic_rules
  python3 options_action_catalog.py basic_rule --num 1
  python3 options_action_catalog.py rule3_subrule --num 1
  python3 options_action_catalog.py list_institutional_steps
  python3 options_action_catalog.py institutional_step --num 5
  python3 options_action_catalog.py list_conceptual_redefinitions
  python3 options_action_catalog.py list_outcomes
  python3 options_action_catalog.py outcome_for_quality --quality "-"
  python3 options_action_catalog.py outcome_for_quality --quality "+"
  python3 options_action_catalog.py outcome_for_quality --quality "inevitable_negative"
  python3 options_action_catalog.py outcome_for_quality --quality "inevitable"
  python3 options_action_catalog.py list_vrmp_layers
  python3 options_action_catalog.py validate_output --json '<output JSON>'

All outputs are JSON.
"""

import sys
import json
import argparse


# ---------------------------------------------------------------------------
# Step 1 — 8 Segments (PDF Section III.4 verbatim)
# ---------------------------------------------------------------------------

SEGMENTS = {
    "S1": {
        "label": "must_be_addressed",
        "verbatim": "Those that must be addressed",
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 Step 1, segment 1"
    },
    "S2": {
        "label": "can_should_be_addressed",
        "verbatim": "Those that can or should be addressed",
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 Step 1, segment 2"
    },
    "S3": {
        "label": "only_prepared_for",
        "verbatim": (
            "Those events that can only be prepared for, not averted "
            "(usually revolve around individual natural events — those things "
            "for which humans are not the direct cause)"
        ),
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 Step 1, segment 3"
    },
    "S4": {
        "label": "no_warnings",
        "verbatim": "Those events for which there are likely to be no warnings",
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 Step 1, segment 4"
    },
    "S5": {
        "label": "too_big",
        "verbatim": "Those events that are potentially too big for the system to adjust to",
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 Step 1, segment 5"
    },
    "S6": {
        "label": "can_be_changed",
        "verbatim": "Those events that might be changed",
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 Step 1, segment 6"
    },
    "S7": {
        "label": "new_solution_invented",
        "verbatim": "Those for which a new solution must be invented",
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 Step 1, segment 7"
    },
    "S8": {
        "label": "existing_tools_used",
        "verbatim": "Those for which existing tools (education, stockpiling, etc.) can be used",
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 Step 1, segment 8"
    }
}


# ---------------------------------------------------------------------------
# 5 Nonlinear / Out-of-the-box Thinking Tools (PDF p.8 verbatim)
# ---------------------------------------------------------------------------

NONLINEAR_TOOLS = {
    "Systems thinking": {
        "tool_id": "NL1",
        "implementation": "System dynamics persona — feedback loops, delays, stocks, flows",
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4, PDF p.8 figure"
    },
    "Creativity training": {
        "tool_id": "NL2",
        "implementation": "De Bono 6-hat, SCAMPER, random word association",
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4, PDF p.8 figure"
    },
    "Intuition": {
        "tool_id": "NL3",
        "implementation": "AI gut-check persona — 'first instinct' probe",
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4, PDF p.8 figure"
    },
    "Associative thinking": {
        "tool_id": "NL4",
        "implementation": "Concept blending, metaphor mapping",
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4, PDF p.8 figure"
    },
    "Dreamwork": {
        "tool_id": "NL5",
        "implementation": "Image/narrative generation, archetypal scan",
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4, PDF p.8 figure"
    }
}

NONLINEAR_TOOLS_RATIONALE = (
    "All are technologies for shaking up old assumptions and allowing new ideas to emerge"
)


# ---------------------------------------------------------------------------
# 3 Basic Rules (PDF Section III.4 verbatim)
# ---------------------------------------------------------------------------

BASIC_RULES = {
    1: {
        "title": "Think Now",
        "verbatim": (
            "If you don't think about Wild Cards before they happen, "
            "all of the value in thinking about them is lost."
        ),
        "extended_verbatim": (
            "If one accepts that there will be an increasing number of Wild Cards "
            "in the future, then the only defense is to begin to systematically think "
            "about them now. The more that is known about a potential future event, "
            "the less threatening it becomes; this is because the solutions to it "
            "eventually become obvious."
        ),
        "application": "preparedness_checklist 'What if it happened tomorrow?'",
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 Rule I (PDF p.9)"
    },
    2: {
        "title": "Information is Key",
        "verbatim": "Accessing and understanding information is key.",
        "extended_verbatim": (
            "Whether identifying early warning signs of a Wild Card, understanding "
            "its structure, or developing a response, a sophisticated, effective "
            "information gathering and analysis process is needed. This process "
            "requires input from experts in systems behavior, the Internet, "
            "complexity theory, and other 'new sciences', as well as from many "
            "traditional disciplines. Access to a robust network of resources is "
            "necessary. Constant outreach through conferences, conventions, and "
            "other professional meetings provides links to other individuals and "
            "ideas that would otherwise escape one's point of view."
        ),
        "application": "info_gathering_plan with disciplinary experts, conferences, networks",
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 Rule II (PDF p.9)"
    },
    3: {
        "title": "Extraordinary Approaches",
        "verbatim": "Extraordinary events may require extraordinary approaches.",
        "extended_verbatim": "See rule3_subrule[1..5] for the 5 verbatim sub-rules.",
        "application": "unconventional approach pool — fringe scan, heterodox sources, 'unleash from past'",
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 Rule III (PDF p.9)"
    }
}

RULE3_SUBRULES = {
    1: {
        "verbatim": (
            "Some of these potential events look so big, strange, and scary because "
            "typical methods of problem solving are incongruent with events of this "
            "magnitude and character. If we are to deal with them before they occur, "
            "we will need a new mindset that will allow us to look at potential "
            "problems in a new light."
        ),
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 Rule III sub-rule 1"
    },
    2: {
        "verbatim": (
            "Often, the most commonly used tools — including political, economic, "
            "and military approaches — will not be equal to the task."
        ),
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 Rule III sub-rule 2"
    },
    3: {
        "verbatim": (
            "This era of global transition will result in the redesign of the "
            "fundamentals of human activity. People and organizations that look "
            "for ways to deal with unprecedented events will be better prepared "
            "to survive and prosper. Those who are willing to unleash themselves "
            "from the past, take risks, and objectively search for novel tools "
            "and perspectives will come out ahead."
        ),
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 Rule III sub-rule 3"
    },
    4: {
        "verbatim": (
            "Many of the solutions we seek will come from unconventional sources "
            "that are outside of the mainstream."
        ),
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 Rule III sub-rule 4"
    },
    5: {
        "verbatim": (
            "It will require good judgment to identify the potential jewels within "
            "the unconventional sources that are being used. The 'fringe' is "
            "typically the domain of more than the usual number of charlatans and "
            "misguided individuals, but the discoveries are worth the explanations. "
            "History has shown that significant breakthroughs, from those of "
            "Copernicus to those of Einstein, initially seem strange and somewhat "
            "unbelievable."
        ),
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 Rule III sub-rule 5"
    }
}


# ---------------------------------------------------------------------------
# 9-Step Institutional Process (PDF Section III.4 verbatim)
# ---------------------------------------------------------------------------

INSTITUTIONAL_STEPS = {
    1: {
        "title": "Identify high-interest Wild Cards and segment them according to options",
        "verbatim": (
            "Identify high-interest Wild Cards and segment them according to options"
        ),
        "ai_implementation": "8-segment multi-tag assignment via segment lookup",
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 Step 1"
    },
    2: {
        "title": "Determine lesser events that point to coming Wild Card",
        "verbatim": (
            "Determine what kinds of lesser events would point to the coming of a Wild Card."
        ),
        "ai_implementation": "Cross-link with vision-foresight-wild-cards-monitoring sub-skill output",
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 Step 2"
    },
    3: {
        "title": "Dedicated scouting group (traveling, probing, reaching)",
        "verbatim": (
            "Put in place a dedicated scouting group that looks for early "
            "indicators (traveling, probing, reaching)."
        ),
        "ai_implementation": "AI Scouting Group persona — traveling, probing, reaching personas",
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 Step 3"
    },
    4: {
        "title": "All organizational units aware; central clearing house",
        "verbatim": (
            "Ensure that all organizational units are aware of general concerns "
            "and interests: Make the whole system an information-gathering device. "
            "Have a central clearing house where all of the information is received "
            "(probably electronically, perhaps a Web site)."
        ),
        "ai_implementation": "AI Clearing House persona — central repository design",
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 Step 4"
    },
    5: {
        "title": "Structure incoming information",
        "verbatim": (
            "Structure incoming information: early indicators, linkages, new events, "
            "unknowns, and confirmations."
        ),
        "ai_implementation": "Taxonomy + ingestion pipeline spec",
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 Step 5"
    },
    6: {
        "title": "Spatial display of information",
        "verbatim": (
            "Develop an ability to display information spatially in sophisticated "
            "ways that quickly suggest what might be happening. Show systems, "
            "relationships, early indicators, and potential effects."
        ),
        "ai_implementation": "Spatial visualization spec — network graph, heatmap, sankey, timeline",
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 Step 6"
    },
    7: {
        "title": "Understand high-interest Wild Cards and decide what to do",
        "verbatim": (
            "Understand the high-interest Wild Cards and decide what can or must "
            "be done about them."
        ),
        "ai_implementation": "Decision matrix",
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 Step 7"
    },
    8: {
        "title": "Create action plan to influence selected events",
        "verbatim": (
            "Create an action plan to influence those selected potential events "
            "that can be influenced."
        ),
        "ai_implementation": "Action plan template per WC (short/mid/long-term)",
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 Step 8"
    },
    9: {
        "title": "Set gates or trip wires",
        "verbatim": (
            "Set gates or trip wires that generate increased attention to a "
            "particular event, as it appears more likely."
        ),
        "ai_implementation": "Trip-wire spec linked to vision-foresight-wild-cards-monitoring sub-skill",
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 Step 9"
    }
}


# ---------------------------------------------------------------------------
# 7 Conceptual Redefinitions (PDF p.10 verbatim)
# ---------------------------------------------------------------------------

CONCEPTUAL_REDEFINITIONS = [
    "self-interest",
    "national security",
    "standard of living",
    "work",
    "education",  # "reinvent all or most of our educational system"
    "governance",  # "government"
    "economy",
    "family",  # "families"
    "military"
]

CONCEPTUAL_REDEFINITION_VERBATIM = (
    "If we are to respond effectively to certain Wild Cards, we will also have "
    "to redefine basic concepts such as: self-interest, national security, "
    "standard of living, work, etc. We will almost certainly have to reinvent "
    "all or most of our educational system, government, economy, families, "
    "and military."
)


# ---------------------------------------------------------------------------
# 4 Outcome Strategies (PDF Section III.4)
# ---------------------------------------------------------------------------
# Per PDF p.8: 3 outcomes (diffuse, mitigate, adjust) + positive case "provoke"

OUTCOMES = {
    "diffuse": {
        "trigger": "quality == '-' AND avoidable",
        "verbatim_from_pdf": (
            "Help diffuse the Wild Card before it erupts "
            "(or help provoke it if it promises to be beneficial)"
        ),
        "description": "Pre-emptive prevention/mitigation actions to defuse a negative WC",
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 outcome (1a)"
    },
    "provoke": {
        "trigger": "quality == '+' (beneficial)",
        "verbatim_from_pdf": (
            "(or help provoke it if it promises to be beneficial)"
        ),
        "description": "Acceleration/realization actions for a positive WC",
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 outcome (1b)"
    },
    "mitigate": {
        "trigger": "quality == '-' AND inevitable",
        "verbatim_from_pdf": (
            "Help mitigate and alleviate negative impacts of a Wild Card"
        ),
        "description": "Minimize impact / resilience strengthening for unavoidable negative WC",
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 outcome (2)"
    },
    "adjust": {
        "trigger": "inevitable (any polarity)",
        "verbatim_from_pdf": (
            "Give one a head start on adjusting for the changes that a Wild Card may bring"
        ),
        "description": "Head-start adjustment preparation",
        "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 outcome (3)"
    }
}


def outcome_for_quality(quality: str) -> dict:
    """
    Deterministic outcome strategy mapping.

    Inputs:
      quality: one of
        '+'                  → positive, beneficial → provoke + adjust
        '-'                  → negative, avoidable → diffuse + adjust
        'inevitable_negative'→ negative, unavoidable → mitigate + adjust
        'inevitable'         → no polarity, just inevitable → adjust

    Returns: dict with primary_outcome, secondary_outcomes, rationale, source.
    """
    quality = quality.strip().lower()
    mapping = {
        "+": {
            "primary_outcome": "provoke",
            "secondary_outcomes": ["adjust"],
            "rationale": "Beneficial WC: accelerate realization (provoke) and prepare adjustments"
        },
        "positive": {
            "primary_outcome": "provoke",
            "secondary_outcomes": ["adjust"],
            "rationale": "Beneficial WC: accelerate realization (provoke) and prepare adjustments"
        },
        "-": {
            "primary_outcome": "diffuse",
            "secondary_outcomes": ["adjust"],
            "rationale": "Negative avoidable WC: pre-emptive defusing (diffuse) + adjust"
        },
        "negative": {
            "primary_outcome": "diffuse",
            "secondary_outcomes": ["adjust"],
            "rationale": "Negative avoidable WC: pre-emptive defusing (diffuse) + adjust"
        },
        "inevitable_negative": {
            "primary_outcome": "mitigate",
            "secondary_outcomes": ["adjust"],
            "rationale": "Unavoidable negative: minimize impact (mitigate) + adjust"
        },
        "inevitable": {
            "primary_outcome": "adjust",
            "secondary_outcomes": [],
            "rationale": "Inevitable regardless of polarity: head-start adjustment"
        }
    }
    if quality not in mapping:
        raise ValueError(
            f"quality={quality!r} not recognized. "
            f"Valid: {sorted(set(mapping.keys()))}"
        )
    result = dict(mapping[quality])
    result["source"] = "Petersen & Steinmüller 2009, Ch.10 Section III.4 outcomes"
    return result


# ---------------------------------------------------------------------------
# VRMP 6-Layer Cascade
# ---------------------------------------------------------------------------

VRMP_LAYERS = {
    "L1": {
        "name": "WebSearch (primary)",
        "queries": [
            "wild card action plan",
            "wild card response strategy [domain]"
        ]
    },
    "L2": {
        "name": "WebSearch (saturation)",
        "queries": [
            "9 step institutional process Wild Card",
            "trip wire futures",
            "preparedness checklist [WC]"
        ]
    },
    "L3": {
        "name": "Reverse / contrarian search",
        "queries": [
            "wild card overreaction critique",
            "preparedness paradox"
        ]
    },
    "L4": {
        "name": "WebFetch (canonical sources)",
        "targets": [
            "Out of the Blue (Petersen 1997) Chapter 5-6 — Options",
            "Arlington Institute methodology",
            "iKnow EU options inventory"
        ]
    },
    "L5": {
        "name": "Expert pool",
        "experts": [
            "John L. Petersen",
            "Pierre Wack",
            "Mika Aaltonen",
            "Strategic foresight practitioners"
        ]
    },
    "L6": {
        "name": "Synthesis with source trail",
        "deliverable": "Cross-source synthesis with provenance per claim"
    }
}


# ---------------------------------------------------------------------------
# Output Validator
# ---------------------------------------------------------------------------

REQUIRED_OUTPUT_KEYS = {
    "meta", "per_wild_card", "segment_summary", "outcome_strategy_summary"
}

REQUIRED_META_KEYS = {
    "n_wild_cards_planned", "rule_applied",
    "institutional_steps_executed", "conceptual_redefinition_proposed"
}

REQUIRED_RULE_KEYS = {
    "rule_1_think_now", "rule_2_information_key", "rule_3_extraordinary"
}

REQUIRED_PER_WC_KEYS = {
    "wild_card_id", "title", "segments", "outcome_strategy",
    "nonlinear_thinking_options", "rule_1_preparedness_checklist",
    "rule_2_information_plan", "rule_3_unconventional_approaches",
    "conceptual_redefinitions", "action_plan", "trip_wires_linked"
}

VALID_SEGMENT_IDS = set(SEGMENTS.keys())
VALID_OUTCOMES = set(OUTCOMES.keys())


def validate_output(output_dict: dict) -> dict:
    """
    Validate an options_action_output structure against the required schema.
    Returns dict with 'valid', 'errors', 'warnings'.
    """
    errors = []
    warnings = []

    if not isinstance(output_dict, dict):
        return {"valid": False, "errors": ["output must be a JSON object"],
                "warnings": []}

    root = output_dict.get("options_action_output", output_dict)
    if not isinstance(root, dict):
        return {"valid": False,
                "errors": ["options_action_output must be a JSON object"],
                "warnings": []}

    missing_root = REQUIRED_OUTPUT_KEYS - set(root.keys())
    if missing_root:
        errors.append(f"Missing root keys: {sorted(missing_root)}")

    meta = root.get("meta", {})
    if not isinstance(meta, dict):
        errors.append("meta must be a JSON object")
    else:
        missing_meta = REQUIRED_META_KEYS - set(meta.keys())
        if missing_meta:
            errors.append(f"Missing meta keys: {sorted(missing_meta)}")
        rules = meta.get("rule_applied", {})
        if isinstance(rules, dict):
            missing_rules = REQUIRED_RULE_KEYS - set(rules.keys())
            if missing_rules:
                errors.append(f"Missing rule_applied keys: {sorted(missing_rules)}")
        steps = meta.get("institutional_steps_executed")
        if steps is not None and steps != 9:
            warnings.append(
                f"institutional_steps_executed={steps} (expected 9 per PDF Section III.4)"
            )

    per_wc = root.get("per_wild_card", [])
    if not isinstance(per_wc, list):
        errors.append("per_wild_card must be a list")
    else:
        for i, wc in enumerate(per_wc):
            if not isinstance(wc, dict):
                errors.append(f"per_wild_card[{i}] must be a JSON object")
                continue
            missing_wc = REQUIRED_PER_WC_KEYS - set(wc.keys())
            if missing_wc:
                errors.append(f"per_wild_card[{i}] missing keys: {sorted(missing_wc)}")
            segs = wc.get("segments", [])
            if isinstance(segs, list):
                bad_segs = [s for s in segs if s not in VALID_SEGMENT_IDS]
                if bad_segs:
                    errors.append(
                        f"per_wild_card[{i}] has invalid segment IDs {bad_segs}. "
                        f"Valid: {sorted(VALID_SEGMENT_IDS)}"
                    )
            out_strat = wc.get("outcome_strategy")
            if out_strat is not None:
                strat_str = str(out_strat).lower()
                primary = strat_str.split("/")[0].strip() if "/" in strat_str else strat_str.split()[0] if strat_str else ""
                if primary and primary not in VALID_OUTCOMES:
                    bare = primary.replace(",", "").replace(";", "").strip()
                    if bare not in VALID_OUTCOMES:
                        warnings.append(
                            f"per_wild_card[{i}] outcome_strategy={out_strat!r}; "
                            f"could not validate primary outcome — valid set: {sorted(VALID_OUTCOMES)}"
                        )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "schema_source": "options_action_catalog.py REQUIRED_*_KEYS"
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(
        description="Options for Action Catalog (Petersen & Steinmüller 2009 Ch.10 §III.4)"
    )
    sub = p.add_subparsers(dest="command")

    sub.add_parser("list_segments", help="List all 8 segments")
    s1 = sub.add_parser("segment", help="Look up one segment by ID (S1..S8)")
    s1.add_argument("--id", required=True)

    sub.add_parser("list_nonlinear_tools", help="List 5 nonlinear thinking tools")
    s2 = sub.add_parser("nonlinear_tool", help="Look up one nonlinear tool by name")
    s2.add_argument("--name", required=True)

    sub.add_parser("list_basic_rules", help="List 3 basic rules")
    s3 = sub.add_parser("basic_rule", help="Look up one basic rule by number 1..3")
    s3.add_argument("--num", type=int, required=True)

    s4 = sub.add_parser("rule3_subrule", help="Look up Rule III sub-rule 1..5")
    s4.add_argument("--num", type=int, required=True)

    sub.add_parser("list_institutional_steps", help="List 9 institutional steps")
    s5 = sub.add_parser("institutional_step", help="Look up one step by number 1..9")
    s5.add_argument("--num", type=int, required=True)

    sub.add_parser("list_conceptual_redefinitions", help="List conceptual redefinitions (verbatim PDF p.10)")

    sub.add_parser("list_outcomes", help="List 4 outcome strategies")
    s6 = sub.add_parser("outcome_for_quality", help="Map quality polarity to outcome strategy")
    s6.add_argument("--quality", required=True,
                    help="One of '+', '-', 'inevitable_negative', 'inevitable'")

    sub.add_parser("list_vrmp_layers", help="List VRMP L1-L6 cascade")

    s7 = sub.add_parser("validate_output", help="Validate an options_action_output JSON structure")
    s7.add_argument("--json", required=True, help="JSON string of the output object")

    args = p.parse_args()

    if args.command == "list_segments":
        result = SEGMENTS
    elif args.command == "segment":
        key = args.id.strip().upper()
        if key not in SEGMENTS:
            raise KeyError(f"Segment '{args.id}' not found. Valid: {sorted(SEGMENTS.keys())}")
        result = {"id": key, **SEGMENTS[key]}
    elif args.command == "list_nonlinear_tools":
        result = {"rationale_verbatim": NONLINEAR_TOOLS_RATIONALE, "tools": NONLINEAR_TOOLS}
    elif args.command == "nonlinear_tool":
        # case-insensitive lookup
        target = args.name.strip().lower()
        match = None
        for k in NONLINEAR_TOOLS:
            if k.lower() == target:
                match = k
                break
        if not match:
            raise KeyError(
                f"Nonlinear tool '{args.name}' not found. "
                f"Valid: {sorted(NONLINEAR_TOOLS.keys())}"
            )
        result = {"name": match, **NONLINEAR_TOOLS[match]}
    elif args.command == "list_basic_rules":
        result = BASIC_RULES
    elif args.command == "basic_rule":
        if args.num not in BASIC_RULES:
            raise KeyError(
                f"Basic rule {args.num} not found. Valid: {sorted(BASIC_RULES.keys())}"
            )
        result = {"num": args.num, **BASIC_RULES[args.num]}
    elif args.command == "rule3_subrule":
        if args.num not in RULE3_SUBRULES:
            raise KeyError(
                f"Rule III sub-rule {args.num} not found. Valid: {sorted(RULE3_SUBRULES.keys())}"
            )
        result = {"num": args.num, **RULE3_SUBRULES[args.num]}
    elif args.command == "list_institutional_steps":
        result = INSTITUTIONAL_STEPS
    elif args.command == "institutional_step":
        if args.num not in INSTITUTIONAL_STEPS:
            raise KeyError(
                f"Institutional step {args.num} not found. Valid: {sorted(INSTITUTIONAL_STEPS.keys())}"
            )
        result = {"num": args.num, **INSTITUTIONAL_STEPS[args.num]}
    elif args.command == "list_conceptual_redefinitions":
        result = {
            "verbatim_source": CONCEPTUAL_REDEFINITION_VERBATIM,
            "concepts": CONCEPTUAL_REDEFINITIONS,
            "n_concepts": len(CONCEPTUAL_REDEFINITIONS),
            "source": "Petersen & Steinmüller 2009, Ch.10 Section III.4 (PDF p.10)"
        }
    elif args.command == "list_outcomes":
        result = OUTCOMES
    elif args.command == "outcome_for_quality":
        result = outcome_for_quality(args.quality)
    elif args.command == "list_vrmp_layers":
        result = VRMP_LAYERS
    elif args.command == "validate_output":
        try:
            parsed = json.loads(args.json)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON for --json: {e}") from e
        result = validate_output(parsed)
    else:
        p.print_help()
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


def _safe_main():
    try:
        main()
    except SystemExit:
        raise
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as e:
        print(json.dumps({"error": str(e), "type": type(e).__name__}, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e), "type": type(e).__name__}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    _safe_main()
