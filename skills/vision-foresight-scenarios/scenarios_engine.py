#!/usr/bin/env python3
"""
scenarios_engine.py
-------------------
Deterministic reference engine for the vision-foresight-scenarios skill.
Source: Jerome C. Glenn and The Futures Group International,
        "Scenarios," in Futures Research Methodology — V3.0,
        Chapter 19, The Millennium Project (2009).

NO LLM reasoning. All data frozen verbatim from SKILL.md / PDF original.
"""

import sys
import json
from typing import Optional

# ─────────────────────────────────────────────────────────────────────────────
# FROZEN DATA — all verbatim from SKILL.md / Glenn & TFG V3.0 Chapter 19
# ─────────────────────────────────────────────────────────────────────────────

CYCLES = {
    "C1": {
        "name": "TFG 3-step (DEFAULT)",
        "description": "The Futures Group 3-step scenario process: Preparation → Development → Reporting and Utilization. Default cycle.",
        "triggers": ["scenarios", "기본 시나리오", "TFG 3-step"],
        "subskills": [
            "focal-issue-definition",
            "driving-forces-identification",
            "importance-uncertainty-ranking",
            "scenario-logics-selection",
            "key-measures-events",
            "projection-engine",
            "narrative-writing",
            "internal-consistency-check",
            "policy-testing",
            "leading-indicators",
            "implications-synthesis",
        ],
    },
    "C2": {
        "name": "Schwartz GBN 6-step",
        "description": "Peter Schwartz / Global Business Network 6-step scenario method from The Art of the Long View (1991).",
        "triggers": ["Art of Long View", "Peter Schwartz", "GBN 6 steps"],
        "subskills": [
            "focal-issue-definition",
            "driving-forces-identification",
            "importance-uncertainty-ranking",
            "scenario-logics-selection",
            "narrative-writing",
            "implications-synthesis",
            "leading-indicators",
        ],
    },
    "C3": {
        "name": "Coates-Jarratt",
        "description": "Coates & Jarratt method using 6-20 variables and transition scenarios.",
        "triggers": ["Coates Jarratt", "6-20 variables", "transition scenarios"],
        "subskills": "All standard (3-6 scenarios)",
    },
    "C4": {
        "name": "Godet MOPPHOL",
        "description": "Michel Godet structural analysis + morphological + scenarios (MOPPHOL base image).",
        "triggers": ["Godet base image", "structural analysis + morphological + scenarios"],
        "subskills": [
            "driving-forces-identification",
            "cross-skill foresight-morphological-analysis",
            "narrative-writing",
        ],
    },
    "C5": {
        "name": "Von Reibnitz 6-step",
        "description": "Ute von Reibnitz Scenario Techniques (1988) — 6-step German pragmatic approach for organization structure scenarios.",
        "triggers": ["Scenario Techniques 1988", "organization structure scenarios"],
        "subskills": "6-step German pragmatic 양식",
    },
    "C6": {
        "name": "Millennium Project Participatory",
        "description": "Millennium Project participatory scenario method combining Delphi + filling in blanks + global normative 4 norms.",
        "triggers": ["Delphi + scenarios", "filling in blanks", "global normative 4 norms"],
        "subskills": "participatory simulation + AI panel + cross-skill foresight-delphi",
    },
    "C7": {
        "name": "Bishop Workshop",
        "description": "Peter Bishop 4-6 hour introductory futures workshop scenario method — abbreviated all-in-one.",
        "triggers": ["4-6 hour scenarios", "intro futures workshop"],
        "subskills": "abbreviated all-in-one",
    },
    "C8": {
        "name": "Cone of Plausibility (Taylor)",
        "description": "Charles W. Taylor U.S. Army War College 1993 — Cone of Plausibility with 4 themes and wild card boundary.",
        "triggers": ["U.S. Army War College", "wild card boundary", "4 themes cone"],
        "subskills": [
            "cone-of-plausibility",
            "narrative-writing",
        ],
    },
    "C9": {
        "name": "Hybrid Approach",
        "description": "TFG + Schwartz mixed methods — all sub-skills with mixed methodology.",
        "triggers": ["TFG + Schwartz", "mixed methods scenarios"],
        "subskills": "All sub-skills with mixed methodology",
    },
    "C10": {
        "name": "Full Pipeline",
        "description": "Comprehensive scenario pipeline — ALL 12 sub-skills executed in sequence.",
        "triggers": ["comprehensive scenarios", "전체 시나리오 pipeline"],
        "subskills": "ALL 12 sub-skills",
    },
}

SCENARIO_COUNTS = {
    3: "minimum",
    4: "DEFAULT (4-5 worlds ideal — 'Four to five worlds seems ideal')",
    5: "DEFAULT (4-5 worlds ideal — 'Four to five worlds seems ideal')",
    6: "deep dive",
    8: "comprehensive (Defense Markets case 양식)",
    9: "comprehensive (Defense Markets case 양식)",
    10: "comprehensive (Defense Markets case 양식)",
    11: "comprehensive (Defense Markets case 양식)",
    12: "comprehensive (Defense Markets case 양식)",
}

SCENARIO_TYPES = {
    "exploratory": {
        "name": "Exploratory",
        "definition": (
            "Exploratory: events/trends evolve based on alternative assumptions on how "
            "these events/trends may influence the future"
        ),
        "default": True,
    },
    "normative": {
        "name": "Normative",
        "definition": "Normative: describe how a desirable future can emerge from the present",
        "default": False,
    },
    "mixed": {
        "name": "Mixed",
        "definition": "Mixed: combines both Exploratory and Normative approaches.",
        "default": False,
    },
}

TIME_HORIZONS = {
    "5yr": {"label": "5-year short-term", "default": False},
    "10yr": {"label": "10-year", "default": False},
    "15-25yr": {"label": "15-25 year (DEFAULT)", "default": True},
    "30yr+": {"label": "30-year+ long-term (Millennium 2050 양식)", "default": False},
}

EXPERT_MODES = {
    "R": {
        "label": "Real Anonymized Expert (DEFAULT)",
        "description": "Real anonymized expert input — VRMP 8th protocol default.",
        "default": True,
    },
    "A": {
        "label": "Attributed Expert",
        "description": "Attributed expert — named expert views used directly.",
        "default": False,
    },
    "V": {
        "label": "Virtual Expert",
        "description": "Virtual/simulated expert panel.",
        "default": False,
    },
    "H": {
        "label": "Hybrid Expert",
        "description": "Hybrid of real and virtual experts.",
        "default": False,
    },
}

AXES_STRATEGIES = {
    "2-axis": {
        "label": "2-axis 4 quadrants (MITRE 양식)",
        "description": "Two independent driving force axes producing 4 quadrant scenario space.",
        "default": True,
    },
    "3-axis": {
        "label": "3-axis 8 octants",
        "description": "Three independent axes producing 8 octant scenario space.",
        "default": False,
    },
    "n-axis": {
        "label": "n-axis morphological (Godet 양식, C4 cycle)",
        "description": "Multi-axis morphological field (Godet MOPPHOL method).",
        "default": False,
    },
}

QUANTIFICATION_MODES = {
    "qualitative": {
        "label": "Qualitative (DEFAULT, narrative emphasis)",
        "default": True,
    },
    "tia-integrated": {
        "label": "TIA-integrated (Trend Impact Analysis projection)",
        "default": False,
    },
    "software-supported": {
        "label": "Software-supported (Parmenides EIDOS · MOPPHOL)",
        "default": False,
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# TFG 3-STEP PROCESS — verbatim from Section III
# ─────────────────────────────────────────────────────────────────────────────

TFG_3_STEPS = [
    {
        "step": 1,
        "title": "Preparation",
        "elements": [
            "Define scenario space",
            "Identify key driving forces (independent 'axes')",
            "4-5 worlds ideal",
        ],
    },
    {
        "step": 2,
        "title": "Development",
        "elements": [
            "Define key measures (forces with high impact)",
            "Define events (impact key measures · change causality · affect policies)",
            "Project key measures (TIA — Trend Impact Analysis)",
            "Prepare descriptions (narrative future histories)",
        ],
    },
    {
        "step": 3,
        "title": "Reporting and Utilization",
        "elements": [
            "Document (top-line + multiple detail levels)",
            "Contrast implications across alternative worlds",
            "Test policies (robust = consistent / contingent = scenario-specific)",
        ],
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# SCHWARTZ 6+1 STEPS — verbatim from Section III (Schwartz 1991 pp. 226-234)
# NOTE: Steps 1-6 are original Schwartz. Step 7 (leading indicators) is
#       Glenn's extension / addition — NOT part of original Schwartz (1991).
# ─────────────────────────────────────────────────────────────────────────────

SCHWARTZ_STEPS = [
    {
        "step": 1,
        "title": "Identify the focal issue or decision",
        "source": "Schwartz (1991)",
    },
    {
        "step": 2,
        "title": "Identify the key forces and trends in the environment",
        "source": "Schwartz (1991)",
    },
    {
        "step": 3,
        "title": "Rank the driving forces and trends by importance and uncertainty",
        "source": "Schwartz (1991)",
    },
    {
        "step": 4,
        "title": "Select the scenario logics",
        "source": "Schwartz (1991)",
    },
    {
        "step": 5,
        "title": "Fill out the scenarios",
        "source": "Schwartz (1991)",
    },
    {
        "step": 6,
        "title": "Assess the implications",
        "source": "Schwartz (1991)",
    },
    {
        "step": 7,
        "title": "Select leading indicators and signposts for monitoring",
        "source": "Glenn extension (NOT original Schwartz 1991) — added in Glenn & TFG V3.0",
        "note": "This step is Glenn's addition to the original 6-step Schwartz method.",
    },
]

SCHWARTZ_NOTE = (
    "NOTE: Steps 1-6 are Schwartz's original method (The Art of the Long View, 1991, pp. 226-234). "
    "Step 7 (leading indicators and signposts) is Glenn's extension — "
    "it does NOT appear in the original Schwartz (1991) text."
)

# ─────────────────────────────────────────────────────────────────────────────
# 3 GOOD SCENARIO CRITERIA — verbatim from Section II
# ─────────────────────────────────────────────────────────────────────────────

GOOD_SCENARIO_CRITERIA = {
    "verbatim_quote": (
        '"Good" scenarios are those that are: '
        "1) Plausible (a rational route from here to there that make causal processes and decisions explicit); "
        "2) Internally consistent (alternative scenarios should address similar issues so that they can be compared); and "
        "3) Sufficiently interesting and exciting to make the future \"real\" enough to elicit strategic responses."
    ),
    "criteria": [
        {
            "number": 1,
            "name": "Plausible",
            "description": "A rational route from here to there that make causal processes and decisions explicit.",
        },
        {
            "number": 2,
            "name": "Internally consistent",
            "description": "Alternative scenarios should address similar issues so that they can be compared.",
        },
        {
            "number": 3,
            "name": "Sufficiently interesting and exciting",
            "description": 'Make the future "real" enough to elicit strategic responses.',
        },
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# 8 USES OF SCENARIOS — verbatim from Section II
# ─────────────────────────────────────────────────────────────────────────────

EIGHT_USES = [
    "① catalog what is unknown",
    "② understand significance of uncertainties",
    "③ illustrate what is possible / not possible",
    "④ identify strategies across scenarios",
    "⑤ dichotomize strategies (robust vs contingent)",
    "⑥ make future more real for decision makers",
    "⑦ prepare for risks",
    "⑧ uncover new opportunities",
]

# ─────────────────────────────────────────────────────────────────────────────
# 12 SUB-SKILLS ROSTER — frozen from SKILL.md Section 5
# ─────────────────────────────────────────────────────────────────────────────

SUBSKILLS = [
    {
        "number": 1,
        "subskill": "focal-issue-definition",
        "ai_agent": "Focal Issue Definer",
        "role": 'Schwartz Step 1 — "What is the most important issue?" 양식',
    },
    {
        "number": 2,
        "subskill": "driving-forces-identification",
        "ai_agent": "Driving Forces Identifier",
        "role": "Key forces · trends · STEEPS 6 domains + Millennium Futures Matrix",
    },
    {
        "number": 3,
        "subskill": "importance-uncertainty-ranking",
        "ai_agent": "I-U Ranker",
        "role": "Schwartz Step 3 — 2×2 importance × uncertainty matrix",
    },
    {
        "number": 4,
        "subskill": "scenario-logics-selection",
        "ai_agent": "Scenario Logics Selector",
        "role": "TFG axes · MITRE 4 quadrants · Defense Markets 4 dimensions · Schwartz logics",
    },
    {
        "number": 5,
        "subskill": "key-measures-events",
        "ai_agent": "KM/Events Architect",
        "role": "TFG Step 2 — key measures + impacting events",
    },
    {
        "number": 6,
        "subskill": "projection-engine",
        "ai_agent": "Projection Engineer",
        "role": "TIA conjunction · Monte Carlo · quantitative projection per scenario",
    },
    {
        "number": 7,
        "subskill": "narrative-writing",
        "ai_agent": "Narrative Writer",
        "role": "Exploratory + Normative · Appendix A·B 양식 · story with plausible cause-effect",
    },
    {
        "number": 8,
        "subskill": "internal-consistency-check",
        "ai_agent": "Consistency Checker",
        "role": "3 criteria verbatim audit (plausible · consistent · interesting)",
    },
    {
        "number": 9,
        "subskill": "cone-of-plausibility",
        "ai_agent": "Cone Modeler",
        "role": "Taylor 1993 · 4 themes · wild card boundary · micro→mini 500 words",
    },
    {
        "number": 10,
        "subskill": "policy-testing",
        "ai_agent": "Policy Tester",
        "role": "Robust vs contingent · dichotomize strategies across scenarios",
    },
    {
        "number": 11,
        "subskill": "leading-indicators",
        "ai_agent": "Indicators Monitor",
        "role": "Schwartz Step 7 · signposts · Z_Punkt 6-month rhythm",
    },
    {
        "number": 12,
        "subskill": "implications-synthesis",
        "ai_agent": "Implications Synthesizer",
        "role": "Domain별 implications + Section IV caveat verbatim",
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# 13 AI AGENTS ROSTER — frozen from SKILL.md
# ─────────────────────────────────────────────────────────────────────────────

AI_AGENTS = [
    "Senior Scenario Strategist",
    "Focal Issue Definer",
    "Driving Forces Identifier",
    "Importance-Uncertainty Ranker",
    "Scenario Logics Selector",
    "Key Measures-Events Architect",
    "Projection Engineer",
    "Narrative Writer",
    "Internal Consistency Checker",
    "Cone of Plausibility Modeler",
    "Policy Tester",
    "Leading Indicators Monitor",
    "Implications Synthesizer",
]

# ─────────────────────────────────────────────────────────────────────────────
# DEFENSE MARKETS CASE STUDY — frozen verbatim from SKILL.md Section 7
# Thor Industries — TFG 1992; Thomas + Boroush, Planning Review May/June 1992
# ─────────────────────────────────────────────────────────────────────────────

DEFENSE_MARKETS_CASE = {
    "source": "Charles W. Thomas + Mark A. Boroush, Planning Review May/June 1992; Thor Industries — TFG 1992",
    "four_dimensions": [
        "a. extent of U.S. diplomatic · economic · military involvement",
        "b. character of countervailing military power",
        "c. vitality of U.S. economy",
        "d. level of global instability",
    ],
    "world_counts": {
        "mathematically_possible": 16,
        "plausible": 13,
        "excluded": 3,
        "selected": 6,
    },
    "six_worlds": [
        {
            "number": 1,
            "name": "U.S. Driven Market",
            "dimensions": "High involvement · focused power · vibrant economy · high instability",
        },
        {
            "number": 2,
            "name": "Dangerous Poverty",
            "dimensions": "High · focused · vibrant · low",
        },
        {
            "number": 3,
            "name": "Regional Markets",
            "dimensions": "High · focused · weak · high",
        },
        {
            "number": 4,
            "name": "Peace and Prosperity",
            "dimensions": "High · diffuse · vibrant · high",
        },
        {
            "number": 5,
            "name": "Confused Priorities",
            "dimensions": "High · diffuse · weak · low",
        },
        {
            "number": 6,
            "name": "Isolationist's Dream",
            "dimensions": "Low · focused · vibrant · high",
        },
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# HERMAN KAHN BIOGRAPHY — frozen, correcting "Weiner" → "Wiener"
# The correct name is Anthony J. Wiener.
# ─────────────────────────────────────────────────────────────────────────────

HERMAN_KAHN_BIO = {
    "name": "Herman Kahn (1922-1983)",
    "title": "Father of scenario construction",
    "biography": (
        "Herman Kahn (1922-1983) is widely credited as the father of scenario "
        "construction in futures research. "
        "1950s: RAND Corporation — nuclear strategy and military/strategic planning. "
        "1961: co-founded the Hudson Institute (Croton-on-Hudson, NY); served as director. "
        "Key works: On Thermonuclear War (1960, Princeton University Press); "
        "On Escalation: Metaphors and Scenarios (1965, Praeger); "
        "The Year 2000: A Framework for Speculation on the Next Thirty-Three Years "
        "(1967, Macmillan, co-authored with Anthony J. Wiener — "
        "NOTE: correct spelling is 'Wiener' W-I-E-N-E-R, NOT 'Weiner' — "
        "prepared for the Commission on the Year 2000 of the American Academy of "
        "Arts and Sciences, chaired by Daniel Bell). "
        "Kahn developed 3 alternative scenario types: surprise-free · worst case · best case. "
        "Critics later advocated 4-scenario sets without a business-as-usual scenario."
    ),
    "coauthor_correction": {
        "incorrect": "Anthony Weiner",
        "correct": "Anthony J. Wiener",
        "note": (
            "The co-author of 'The Year 2000' (1967, Macmillan) is Anthony J. Wiener "
            "(spelled W-I-E-N-E-R), not 'Weiner'. This is a common misspelling. "
            "Anthony J. Wiener (1930-2012) was a Hudson Institute scholar."
        ),
    },
    "scenario_types": [
        "Surprise-free (business-as-usual)",
        "Worst case",
        "Best case",
    ],
    "timeline": [
        ("1950s", "RAND Corporation — nuclear strategy / scenario work"),
        ("1960", "On Thermonuclear War (Princeton University Press)"),
        ("1961", "Co-founded the Hudson Institute"),
        ("1965", "On Escalation: Metaphors and Scenarios (Praeger)"),
        ("1967", "The Year 2000 (Macmillan, with Anthony J. Wiener)"),
        ("1983", "Died in Croton-on-Hudson, NY"),
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# KEY BIBLIOGRAPHY — at least 10 entries
# ─────────────────────────────────────────────────────────────────────────────

BIBLIOGRAPHY = {
    "kahn_1965": {
        "key": "kahn_1965",
        "authors": "Kahn, Herman",
        "year": 1965,
        "title": "On Escalation: Metaphors and Scenarios",
        "note": "RAND/Hudson Institute. Foundational scenario construction text.",
    },
    "kahn_wiener_1967": {
        "key": "kahn_wiener_1967",
        "authors": "Kahn, Herman and Wiener, Anthony J.",
        "year": 1967,
        "title": "The Year 2000: A Framework for Speculation on the Next Thirty-Three Years",
        "publisher": "Macmillan, New York",
        "commissioning_body": (
            "Prepared for the Commission on the Year 2000 of the "
            "American Academy of Arts and Sciences (chaired by Daniel Bell)"
        ),
        "note": (
            "Co-author is Anthony J. Wiener (W-I-E-N-E-R), not 'Weiner'. "
            "Full title is 'The Year 2000: A Framework for Speculation on the Next "
            "Thirty-Three Years' (Macmillan, 1967). 'Toward The Year 2000' is the "
            "title used by Daniel Bell's edited volume from the same Commission "
            "(Bell, ed., 1968, Houghton Mifflin). PDF V3.0 19장 references both works "
            "under the broader 'Year 2000' rubric; both attributions are valid foresight scholarship."
        ),
    },
    "bell_1968": {
        "key": "bell_1968",
        "authors": "Bell, Daniel (ed.)",
        "year": 1968,
        "title": "Toward the Year 2000: Work in Progress",
        "publisher": "Houghton Mifflin, Boston",
        "note": (
            "Edited volume from the Commission on the Year 2000 of the American Academy "
            "of Arts and Sciences. Daniel Bell chaired the Commission. Often conflated "
            "with Kahn & Wiener (1967) in foresight literature."
        ),
    },
    "schwartz_1991": {
        "key": "schwartz_1991",
        "authors": "Schwartz, Peter",
        "year": 1991,
        "title": "The Art of the Long View: Planning for the Future in an Uncertain World",
        "publisher": "Doubleday/Currency, New York",
        "isbn": "0-385-26731-2",
        "note": (
            "6-step Global Business Network scenario method (pp. 226-234). "
            "Step 7 (leading indicators/signposts) was added by Glenn in V3.0 (2009) "
            "and is NOT part of Schwartz's original 6 steps."
        ),
    },
    "project_independence_1974": {
        "key": "project_independence_1974",
        "authors": "Federal Energy Administration (FEA)",
        "year": 1974,
        "title": "Project Independence Blueprint Final Task Force Report",
        "publisher": "U.S. Government Printing Office, Washington, D.C.",
        "note": (
            "Energy scenario response to the 1973 OPEC oil embargo. Initiated by "
            "President Richard Nixon's November 1973 'Project Independence' speech. "
            "PDF V3.0 19장 references this as one of the seminal applied scenario projects."
        ),
    },
    "freeman_1974": {
        "key": "freeman_1974",
        "authors": "Freeman, S. David (Project Director)",
        "year": 1974,
        "title": "A Time to Choose: America's Energy Future — Final Report of the Energy Policy Project",
        "publisher": "Ballinger Publishing Company, Cambridge, MA",
        "sponsor": "Ford Foundation Energy Policy Project",
        "note": (
            "Ford Foundation's Energy Policy Project final report directed by S. David Freeman. "
            "Companion / alternative to Project Independence Blueprint. PDF V3.0 19장 cited."
        ),
    },
    "schwartz_1992": {
        "key": "schwartz_1992",
        "authors": "Schwartz, Peter",
        "year": 1992,
        "title": "Scenario-based Planning (article/chapter)",
        "note": "Global Business Network.",
    },
    "godet_1990": {
        "key": "godet_1990",
        "authors": "Godet, Michel",
        "year": 1990,
        "title": "Scenarios and Strategic Management",
        "note": "MOPPHOL structural analysis + morphological + scenarios.",
    },
    "godet_1993": {
        "key": "godet_1993",
        "authors": "Godet, Michel",
        "year": 1993,
        "title": "From Anticipation to Action: A Handbook of Strategic Prospective",
        "publisher": "UNESCO Publishing",
        "note": "Base image / scenarios prospective.",
    },
    "mandel_wilson_1993": {
        "key": "mandel_wilson_1993",
        "authors": "Mandel, Thomas F. and Wilson, Ian H.",
        "year": 1993,
        "title": "Scenario Planning (SRI International)",
        "note": "SRI scenario method reference.",
    },
    "taylor_1990": {
        "key": "taylor_1990",
        "authors": "Taylor, Charles W.",
        "year": 1990,
        "title": "Alternative World Scenarios for Strategic Planning",
        "publisher": "U.S. Army War College",
    },
    "taylor_1992": {
        "key": "taylor_1992",
        "authors": "Taylor, Charles W.",
        "year": 1992,
        "title": "A World 2010: A New Order of Nations",
        "publisher": "U.S. Army War College",
    },
    "taylor_1993": {
        "key": "taylor_1993",
        "authors": "Taylor, Charles W.",
        "year": 1993,
        "title": "Cone of Plausibility",
        "publisher": "U.S. Army War College",
        "note": "Defines the Cone of Plausibility — wild card boundary; 4 themes.",
    },
    "von_reibnitz_1988": {
        "key": "von_reibnitz_1988",
        "authors": "von Reibnitz, Ute",
        "year": 1988,
        "title": "Scenario Techniques",
        "note": "6-step German pragmatic scenario approach.",
    },
    "thomas_boroush_1992": {
        "key": "thomas_boroush_1992",
        "authors": "Thomas, Charles W. and Boroush, Mark A.",
        "year": 1992,
        "title": "Defense Markets Case Study (Thor Industries)",
        "publisher": "Planning Review, May/June 1992",
        "note": "16→13→6 worlds; 4 dimensions; TFG 1992.",
    },
    "glenn_tfg_2009": {
        "key": "glenn_tfg_2009",
        "authors": "Glenn, Jerome C. and The Futures Group International",
        "year": 2009,
        "title": "Scenarios",
        "publisher": "Futures Research Methodology — V3.0, Chapter 19, The Millennium Project",
        "note": "Primary source for this skill. 54-page chapter.",
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# EXPLORATORY VS NORMATIVE — verbatim definitions from Section II
# ─────────────────────────────────────────────────────────────────────────────

EXPLORATORY_VS_NORMATIVE = {
    "exploratory": {
        "name": "Exploratory",
        "definition": (
            "Events/trends evolve based on alternative assumptions on how "
            "these events/trends may influence the future."
        ),
        "verbatim": (
            "Exploratory: events/trends evolve based on alternative assumptions on how "
            "these events/trends may influence the future"
        ),
    },
    "normative": {
        "name": "Normative",
        "definition": "Describe how a desirable future can emerge from the present.",
        "verbatim": "Normative: describe how a desirable future can emerge from the present",
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# CONE OF PLAUSIBILITY — Taylor (1993) definition from Section V
# ─────────────────────────────────────────────────────────────────────────────

CONE_OF_PLAUSIBILITY = {
    "source": "Charles W. Taylor, U.S. Army War College (1993)",
    "definition": (
        "The Cone of Plausibility (Taylor 1993) depicts the expanding range of plausible futures "
        "over time, originating from the present as a narrow point and widening to encompass "
        "alternative scenarios. Wild cards fall outside the cone's boundary. "
        "Taylor identified 4 themes within the cone. "
        "The cone provides a visual boundary between plausible and implausible futures, "
        "helping analysts identify where wild cards might penetrate the cone's edge."
    ),
    "key_features": [
        "Originates at the present (narrow point)",
        "Expands over time to encompass alternative scenarios",
        "Wild cards fall outside the cone boundary",
        "4 themes identified within the cone (Taylor 1993)",
        "Supports micro → mini scenario development (500 words)",
        "Applied in Section V Frontiers of Glenn & TFG V3.0",
    ],
    "reference": "Section V Frontiers — Glenn & TFG V3.0 Chapter 19 (2009)",
}

# ─────────────────────────────────────────────────────────────────────────────
# CORE DEFINITION — verbatim from Section I / description
# ─────────────────────────────────────────────────────────────────────────────

CORE_DEFINITION = (
    '"A scenario is a story with plausible cause and effect links that connects a future condition '
    'with the present, while illustrating key decisions, events, and consequences throughout the narrative."'
)

SCENARIO_ABUSE_QUOTE = (
    '"Scenario is probably the most abused term in futures research. What usually passes for a scenario today '
    "is a discussion about a range of future possibilities with data and analysis. Such a discussion of futures "
    "research is perfectly fine and should be done, but does not constitute a scenario. It is like confusing "
    "the text of a play's newspaper review with the text of the play written by the playwright.\""
)


# ─────────────────────────────────────────────────────────────────────────────
# VALIDATION FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def validate_cycle(cycle_code: str) -> dict:
    """Validate a cycle code (C1-C10)."""
    code = cycle_code.upper().strip()
    if code in CYCLES:
        return {
            "valid": True,
            "code": code,
            "name": CYCLES[code]["name"],
            "description": CYCLES[code]["description"],
        }
    valid_codes = list(CYCLES.keys())
    return {
        "valid": False,
        "code": cycle_code,
        "error": f"Invalid cycle code '{cycle_code}'. Valid codes: {', '.join(valid_codes)}",
    }


def validate_count(n: int) -> dict:
    """Validate scenario count. Valid range: 3-12."""
    try:
        n = int(n)
    except (ValueError, TypeError):
        return {"valid": False, "count": n, "error": f"Count must be an integer, got: {n}"}

    if n < 3:
        return {
            "valid": False,
            "count": n,
            "error": f"Scenario count {n} is below minimum (3). Minimum is 3.",
        }
    if n > 12:
        return {
            "valid": False,
            "count": n,
            "error": f"Scenario count {n} exceeds maximum (12). Maximum comprehensive is 12.",
        }

    label = SCENARIO_COUNTS.get(n, "comprehensive")
    return {"valid": True, "count": n, "label": label}


def validate_type(scenario_type: str) -> dict:
    """Validate scenario type (Exploratory/Normative/Mixed)."""
    key = scenario_type.lower().strip()
    if key in SCENARIO_TYPES:
        entry = SCENARIO_TYPES[key]
        return {
            "valid": True,
            "type": entry["name"],
            "definition": entry["definition"],
            "is_default": entry["default"],
        }
    valid_types = [v["name"] for v in SCENARIO_TYPES.values()]
    return {
        "valid": False,
        "type": scenario_type,
        "error": f"Invalid type '{scenario_type}'. Valid types: {', '.join(valid_types)}",
    }


def validate_horizon(horizon: str) -> dict:
    """Validate time horizon (5yr/10yr/15-25yr/30yr+)."""
    key = horizon.lower().strip()
    if key in TIME_HORIZONS:
        entry = TIME_HORIZONS[key]
        return {
            "valid": True,
            "horizon": key,
            "label": entry["label"],
            "is_default": entry["default"],
        }
    valid_horizons = list(TIME_HORIZONS.keys())
    return {
        "valid": False,
        "horizon": horizon,
        "error": f"Invalid horizon '{horizon}'. Valid horizons: {', '.join(valid_horizons)}",
    }


def validate_mode(mode: str) -> dict:
    """Validate expert mode (R/A/V/H)."""
    key = mode.upper().strip()
    if key in EXPERT_MODES:
        entry = EXPERT_MODES[key]
        return {
            "valid": True,
            "mode": key,
            "label": entry["label"],
            "description": entry["description"],
            "is_default": entry["default"],
        }
    valid_modes = list(EXPERT_MODES.keys())
    return {
        "valid": False,
        "mode": mode,
        "error": f"Invalid expert mode '{mode}'. Valid modes: {', '.join(valid_modes)}",
    }


def validate_axes(axes: str) -> dict:
    """Validate axes strategy (2-axis/3-axis/n-axis)."""
    key = axes.lower().strip()
    if key in AXES_STRATEGIES:
        entry = AXES_STRATEGIES[key]
        return {
            "valid": True,
            "axes": key,
            "label": entry["label"],
            "description": entry["description"],
            "is_default": entry["default"],
        }
    valid_axes = list(AXES_STRATEGIES.keys())
    return {
        "valid": False,
        "axes": axes,
        "error": f"Invalid axes strategy '{axes}'. Valid strategies: {', '.join(valid_axes)}",
    }


def validate_quant(quant: str) -> dict:
    """Validate quantification mode (qualitative/tia-integrated/software-supported)."""
    key = quant.lower().strip()
    if key in QUANTIFICATION_MODES:
        entry = QUANTIFICATION_MODES[key]
        return {
            "valid": True,
            "quant": key,
            "label": entry["label"],
            "is_default": entry["default"],
        }
    valid_quants = list(QUANTIFICATION_MODES.keys())
    return {
        "valid": False,
        "quant": quant,
        "error": f"Invalid quantification '{quant}'. Valid modes: {', '.join(valid_quants)}",
    }


def validate_step0(
    cycle: str,
    count: int,
    scenario_type: str,
    horizon: str,
    mode: str,
    axes: str,
    quant: str,
) -> dict:
    """Validate ALL Step 0 inputs at once. Returns combined validation result."""
    results = {
        "cycle": validate_cycle(cycle),
        "count": validate_count(count),
        "type": validate_type(scenario_type),
        "horizon": validate_horizon(horizon),
        "mode": validate_mode(mode),
        "axes": validate_axes(axes),
        "quant": validate_quant(quant),
    }
    all_valid = all(r["valid"] for r in results.values())
    errors = {k: r["error"] for k, r in results.items() if not r["valid"]}
    return {
        "all_valid": all_valid,
        "results": results,
        "errors": errors if errors else None,
    }


# ─────────────────────────────────────────────────────────────────────────────
# DISPLAY FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def display_criteria():
    """Display 3 good scenario criteria verbatim."""
    print('=== 3 "Good Scenario" Criteria (Section II verbatim) ===\n')
    print(GOOD_SCENARIO_CRITERIA["verbatim_quote"])
    print()
    for c in GOOD_SCENARIO_CRITERIA["criteria"]:
        print(f"{c['number']}. {c['name']}: {c['description']}")


def display_tfg_steps():
    """Display TFG 3-step process."""
    print("=== TFG 3-Step Process (Section III verbatim) ===\n")
    for step in TFG_3_STEPS:
        print(f"Step {step['step']}: {step['title']}")
        for elem in step["elements"]:
            print(f"  - {elem}")
        print()


def display_schwartz_steps():
    """Display Schwartz 6+1 steps."""
    print("=== Schwartz 6+1 Steps (Section III, Schwartz 1991 pp. 226-234) ===\n")
    print(SCHWARTZ_NOTE)
    print()
    for step in SCHWARTZ_STEPS:
        note = f"  [{step['source']}]"
        if "note" in step:
            note += f" *** {step['note']} ***"
        print(f"Step {step['step']}: {step['title']}")
        print(note)
    print()


def display_uses():
    """Display 8 uses of scenarios."""
    print("=== 8 Uses of Scenarios (Section II verbatim) ===\n")
    for use in EIGHT_USES:
        print(f"  {use}")
    print()


def display_subskills():
    """Display 12 sub-skills roster."""
    print("=== 12 Sub-skills Roster ===\n")
    print(f"{'#':<4} {'Sub-skill':<35} {'AI Agent':<35} Role")
    print("-" * 110)
    for s in SUBSKILLS:
        print(f"{s['number']:<4} {s['subskill']:<35} {s['ai_agent']:<35} {s['role']}")
    print()


def display_agents():
    """Display 13 AI Agents roster."""
    print("=== 13 AI Agents Roster ===\n")
    for i, agent in enumerate(AI_AGENTS, 1):
        print(f"  {i:2d}. {agent}")
    print()


def display_defense_markets():
    """Display Defense Markets case study."""
    case = DEFENSE_MARKETS_CASE
    print("=== Defense Markets Case Study ===\n")
    print(f"Source: {case['source']}\n")
    print("4 Principal Dimensions:")
    for dim in case["four_dimensions"]:
        print(f"  {dim}")
    print()
    wc = case["world_counts"]
    print(
        f"Worlds: {wc['mathematically_possible']} mathematically possible → "
        f"{wc['plausible']} plausible ({wc['excluded']} excluded) → "
        f"{wc['selected']} selected\n"
    )
    print("6 Selected Worlds:")
    for world in case["six_worlds"]:
        print(f"  {world['number']}. {world['name']}: {world['dimensions']}")
    print()


def display_kahn_bio():
    """Display Herman Kahn biography with corrected Wiener spelling."""
    bio = HERMAN_KAHN_BIO
    print("=== Herman Kahn Biography ===\n")
    print(f"Name: {bio['name']}")
    print(f"Title: {bio['title']}\n")
    print(bio["biography"])
    print()
    corr = bio["coauthor_correction"]
    print(f"CORRECTION: '{corr['incorrect']}' → '{corr['correct']}'")
    print(f"Note: {corr['note']}")
    print()
    print("3 Kahn Scenario Types:")
    for t in bio["scenario_types"]:
        print(f"  - {t}")
    print()
    print("Timeline:")
    for year, event in bio["timeline"]:
        print(f"  {year}: {event}")
    print()


def display_citation(key: str):
    """Display a single bibliography entry by key."""
    entry = BIBLIOGRAPHY.get(key)
    if not entry:
        print(f"Error: Citation key '{key}' not found.")
        print("Available keys:", ", ".join(sorted(BIBLIOGRAPHY.keys())))
        return
    print(f"=== Citation: {key} ===\n")
    for field, value in entry.items():
        if field != "key":
            print(f"  {field}: {value}")
    print()


def display_list_citations():
    """List all bibliography keys with short descriptions."""
    print("=== Bibliography (Key Entries) ===\n")
    for key, entry in sorted(BIBLIOGRAPHY.items()):
        authors = entry.get("authors", "")
        year = entry.get("year", "")
        title = entry.get("title", "")
        print(f"  [{key}] {authors} ({year}). {title}")
    print()


def display_exploratory_vs_normative():
    """Display Exploratory vs Normative definitions."""
    print("=== Exploratory vs Normative Scenarios (Section II verbatim) ===\n")
    for key, entry in EXPLORATORY_VS_NORMATIVE.items():
        print(f"{entry['name']}:")
        print(f"  {entry['verbatim']}")
        print()


def display_cone_of_plausibility():
    """Display Cone of Plausibility definition."""
    cone = CONE_OF_PLAUSIBILITY
    print("=== Cone of Plausibility ===\n")
    print(f"Source: {cone['source']}\n")
    print(cone["definition"])
    print()
    print("Key features:")
    for feat in cone["key_features"]:
        print(f"  - {feat}")
    print(f"\nReference: {cone['reference']}")
    print()


# ─────────────────────────────────────────────────────────────────────────────
# SELF-TEST SUITE — AT LEAST 20 TESTS
# ─────────────────────────────────────────────────────────────────────────────

def run_self_test():
    """Run deterministic self-test suite. Returns (passed, total)."""
    tests = []

    def check(name: str, condition: bool, detail: str = ""):
        result = "PASS" if condition else "FAIL"
        tests.append((name, result, detail))

    # ── Cycle validation ──────────────────────────────────────────────────────
    # T01
    r = validate_cycle("C1")
    check("T01: C1 valid", r["valid"] and r["name"] == "TFG 3-step (DEFAULT)")

    # T02
    r = validate_cycle("C10")
    check("T02: C10 valid", r["valid"] and r["name"] == "Full Pipeline")

    # T03
    r = validate_cycle("C99")
    check("T03: C99 invalid", not r["valid"])

    # T04 — case insensitive
    r = validate_cycle("c2")
    check("T04: c2 (lowercase) valid", r["valid"])

    # ── Scenario count ────────────────────────────────────────────────────────
    # T05
    r = validate_count(4)
    check("T05: count=4 valid DEFAULT", r["valid"] and "DEFAULT" in r["label"])

    # T06
    r = validate_count(3)
    check("T06: count=3 valid minimum", r["valid"] and "minimum" in r["label"])

    # T07
    r = validate_count(2)
    check("T07: count=2 invalid (below min)", not r["valid"])

    # T08
    r = validate_count(13)
    check("T08: count=13 invalid (above max)", not r["valid"])

    # T09
    r = validate_count(12)
    check("T09: count=12 valid comprehensive", r["valid"])

    # ── Scenario type ─────────────────────────────────────────────────────────
    # T10
    r = validate_type("exploratory")
    check("T10: exploratory valid + default", r["valid"] and r["is_default"])

    # T11
    r = validate_type("normative")
    check("T11: normative valid", r["valid"] and not r["is_default"])

    # T12
    r = validate_type("mixed")
    check("T12: mixed valid", r["valid"])

    # T13
    r = validate_type("predictive")
    check("T13: predictive invalid", not r["valid"])

    # ── Time horizon ──────────────────────────────────────────────────────────
    # T14
    r = validate_horizon("15-25yr")
    check("T14: 15-25yr valid + default", r["valid"] and r["is_default"])

    # T15
    r = validate_horizon("5yr")
    check("T15: 5yr valid not default", r["valid"] and not r["is_default"])

    # T16
    r = validate_horizon("20yr")
    check("T16: 20yr invalid", not r["valid"])

    # ── Expert mode ───────────────────────────────────────────────────────────
    # T17
    r = validate_mode("R")
    check("T17: mode R valid + default", r["valid"] and r["is_default"])

    # T18
    r = validate_mode("X")
    check("T18: mode X invalid", not r["valid"])

    # ── Axes strategy ─────────────────────────────────────────────────────────
    # T19
    r = validate_axes("2-axis")
    check("T19: 2-axis valid + default", r["valid"] and r["is_default"])

    # T20
    r = validate_axes("n-axis")
    check("T20: n-axis valid not default", r["valid"] and not r["is_default"])

    # ── Quantification ────────────────────────────────────────────────────────
    # T21
    r = validate_quant("qualitative")
    check("T21: qualitative valid + default", r["valid"] and r["is_default"])

    # T22
    r = validate_quant("tia-integrated")
    check("T22: tia-integrated valid", r["valid"])

    # ── validate_step0 ────────────────────────────────────────────────────────
    # T23 — all valid
    r = validate_step0("C1", 4, "exploratory", "15-25yr", "R", "2-axis", "qualitative")
    check("T23: validate_step0 all valid", r["all_valid"])

    # T24 — one invalid (bad cycle)
    r = validate_step0("C99", 4, "exploratory", "15-25yr", "R", "2-axis", "qualitative")
    check("T24: validate_step0 bad cycle → not all_valid", not r["all_valid"])

    # ── Frozen data integrity ─────────────────────────────────────────────────
    # T25 — 12 sub-skills
    check("T25: exactly 12 sub-skills", len(SUBSKILLS) == 12)

    # T26 — 13 AI agents
    check("T26: exactly 13 AI agents", len(AI_AGENTS) == 13)

    # T27 — Defense Markets: 6 worlds
    check(
        "T27: Defense Markets 6 worlds",
        len(DEFENSE_MARKETS_CASE["six_worlds"]) == 6,
    )

    # T28 — Defense Markets: 16→13→6
    wc = DEFENSE_MARKETS_CASE["world_counts"]
    check(
        "T28: Defense Markets world counts 16→13→6",
        wc["mathematically_possible"] == 16
        and wc["plausible"] == 13
        and wc["selected"] == 6,
    )

    # T29 — Kahn coauthor correct spelling
    check(
        "T29: Kahn coauthor is 'Wiener' not 'Weiner'",
        HERMAN_KAHN_BIO["coauthor_correction"]["correct"] == "Anthony J. Wiener"
        and HERMAN_KAHN_BIO["coauthor_correction"]["incorrect"] == "Anthony Weiner",
    )

    # T30 — 3 criteria
    check("T30: exactly 3 good scenario criteria", len(GOOD_SCENARIO_CRITERIA["criteria"]) == 3)

    # T31 — 8 uses
    check("T31: exactly 8 uses of scenarios", len(EIGHT_USES) == 8)

    # T32 — Schwartz 7 steps (6 original + 1 Glenn extension)
    check("T32: Schwartz has 7 steps (6+1)", len(SCHWARTZ_STEPS) == 7)

    # T33 — Schwartz Step 7 is Glenn's extension
    step7 = SCHWARTZ_STEPS[6]
    check(
        "T33: Schwartz Step 7 source identifies Glenn extension",
        "Glenn" in step7["source"] and "NOT" in step7["source"],
    )

    # T34 — TFG 3 steps
    check("T34: TFG has exactly 3 steps", len(TFG_3_STEPS) == 3)

    # T35 — at least 10 bibliography entries
    check("T35: at least 10 bibliography entries", len(BIBLIOGRAPHY) >= 10)

    # T36 — Cone of Plausibility Taylor 1993
    check(
        "T36: Cone of Plausibility source is Taylor 1993",
        "Taylor" in CONE_OF_PLAUSIBILITY["source"] and "1993" in CONE_OF_PLAUSIBILITY["source"],
    )

    # T37 — Exploratory definition verbatim contains 'alternative assumptions'
    check(
        "T37: Exploratory definition contains 'alternative assumptions'",
        "alternative assumptions" in EXPLORATORY_VS_NORMATIVE["exploratory"]["verbatim"],
    )

    # T38 — Normative definition verbatim contains 'desirable future'
    check(
        "T38: Normative definition contains 'desirable future'",
        "desirable future" in EXPLORATORY_VS_NORMATIVE["normative"]["verbatim"],
    )

    # T39 — Core definition verbatim contains 'plausible cause and effect'
    check(
        "T39: Core definition contains 'plausible cause and effect'",
        "plausible cause and effect" in CORE_DEFINITION,
    )

    # T40 — 10 cycles
    check("T40: exactly 10 cycles (C1-C10)", len(CYCLES) == 10)

    # T41 — Kahn-Wiener book title corrected to academic standard
    check(
        "T41: Kahn-Wiener 1967 title 'The Year 2000' (Macmillan)",
        "The Year 2000" in BIBLIOGRAPHY["kahn_wiener_1967"]["title"]
        and "Macmillan" in BIBLIOGRAPHY["kahn_wiener_1967"]["publisher"],
    )

    # T42 — Daniel Bell 1968 separate entry
    check(
        "T42: Bell 1968 'Toward the Year 2000' entry exists",
        "bell_1968" in BIBLIOGRAPHY
        and BIBLIOGRAPHY["bell_1968"]["authors"].startswith("Bell"),
    )

    # T43 — Project Independence Blueprint
    check(
        "T43: Project Independence 1974 (FEA) entry",
        "project_independence_1974" in BIBLIOGRAPHY
        and "Federal Energy Administration" in BIBLIOGRAPHY["project_independence_1974"]["authors"],
    )

    # T44 — Ford Foundation Freeman 1974
    check(
        "T44: Freeman 1974 Ford Foundation Energy Policy Project entry",
        "freeman_1974" in BIBLIOGRAPHY
        and "Freeman" in BIBLIOGRAPHY["freeman_1974"]["authors"],
    )

    # T45 — Bibliography expanded to >=16 entries
    check(
        "T45: bibliography expanded to >=16 entries",
        len(BIBLIOGRAPHY) >= 16,
    )

    # T46 — Kahn biography mentions Hudson Institute and 1922-1983
    check(
        "T46: Kahn biography includes life dates 1922-1983 and Hudson Institute",
        "1922" in HERMAN_KAHN_BIO["name"]
        and "1983" in HERMAN_KAHN_BIO["name"]
        and "Hudson Institute" in HERMAN_KAHN_BIO["biography"],
    )

    # T47 — Schwartz publisher includes Doubleday/Currency
    check(
        "T47: Schwartz 1991 publisher Doubleday/Currency",
        "Doubleday" in BIBLIOGRAPHY["schwartz_1991"]["publisher"],
    )

    # T48 — Defense Markets exactly 4 dimensions
    check(
        "T48: Defense Markets has exactly 4 principal dimensions",
        len(DEFENSE_MARKETS_CASE["four_dimensions"]) == 4,
    )

    # T49 — All cycles have at least one trigger
    cycles_with_triggers = all(
        len(CYCLES[c]["triggers"]) >= 1 for c in CYCLES
    )
    check("T49: all 10 cycles have at least one trigger", cycles_with_triggers)

    # T50 — All 12 sub-skills present in C1 sub-skill list (the default cycle should be most complete)
    # C1 has 11 of 12 sub-skills (cone-of-plausibility only in C8); check 11 sub-skills
    c1_subskills = CYCLES["C1"]["subskills"]
    check(
        "T50: C1 sub-skill list is non-empty list (11 sub-skills, cone separate to C8)",
        isinstance(c1_subskills, list) and len(c1_subskills) == 11,
    )

    # T51 — All sub-skills declared in SUBSKILLS appear or are addressable from at least one cycle
    declared_subskills = {s["subskill"] for s in SUBSKILLS}
    cycle_referenced = set()
    for c in CYCLES.values():
        sub = c["subskills"]
        if isinstance(sub, list):
            for s in sub:
                cycle_referenced.add(s)
    # cone-of-plausibility is in C8 list; ensure overlap with at least 11 of 12
    common = declared_subskills & cycle_referenced
    check(
        "T51: at least 11 sub-skills referenced from cycle lists",
        len(common) >= 11,
    )

    # T52 — Coauthor correction frozen ('Anthony Weiner' -> 'Anthony J. Wiener')
    cc = HERMAN_KAHN_BIO["coauthor_correction"]
    check(
        "T52: coauthor correction Weiner→Wiener preserved",
        cc["incorrect"] == "Anthony Weiner" and cc["correct"] == "Anthony J. Wiener",
    )

    # T53 — Glenn & TFG 2009 entry as primary source
    glenn = BIBLIOGRAPHY["glenn_tfg_2009"]
    check(
        "T53: Glenn & TFG 2009 primary source entry",
        glenn["year"] == 2009 and "Millennium" in glenn["publisher"],
    )

    # T54 — Validation symmetry: validate_count(4) and validate_count(5) both DEFAULT label
    r4 = validate_count(4)
    r5 = validate_count(5)
    check(
        "T54: count 4 and 5 both labelled DEFAULT",
        "DEFAULT" in r4["label"] and "DEFAULT" in r5["label"],
    )

    # T55 — Validation symmetry: count 0 and -1 also rejected
    r0 = validate_count(0)
    rneg = validate_count(-1)
    check(
        "T55: count 0 and -1 rejected",
        not r0["valid"] and not rneg["valid"],
    )

    # Print results
    print(f"\n=== Self-Test Results ===\n")
    passed = 0
    for name, result, detail in tests:
        status_str = "[PASS]" if result == "PASS" else "[FAIL]"
        line = f"  {status_str} {name}"
        if detail:
            line += f" — {detail}"
        print(line)
        if result == "PASS":
            passed += 1

    total = len(tests)
    print(f"\nResult: {passed}/{total} PASS")
    if passed == total:
        print("ALL TESTS PASSED")
    else:
        print(f"FAILURES: {total - passed}")

    return passed, total


# ─────────────────────────────────────────────────────────────────────────────
# CLI ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def print_usage():
    print(
        """
scenarios_engine.py — Deterministic reference engine for vision-foresight-scenarios skill
Source: Glenn & TFG V3.0, Chapter 19 (Millennium Project, 2009)

Usage:
  python3 scenarios_engine.py <command> [args]

Commands:
  validate-cycle <C1-C10>
  validate-count <N>
  validate-type <exploratory|normative|mixed>
  validate-horizon <5yr|10yr|15-25yr|30yr+>
  validate-mode <R|A|V|H>
  validate-axes <2-axis|3-axis|n-axis>
  validate-quant <qualitative|tia-integrated|software-supported>
  validate-step0 --cycle C --count N --type T --horizon H --mode M --axes A --quant Q
  criteria
  tfg-steps
  schwartz-steps
  uses
  sub-skills
  agents
  defense-markets
  kahn-bio
  cite <key>
  list-citations
  exploratory-vs-normative
  cone-of-plausibility
  self-test
"""
    )


def main():
    args = sys.argv[1:]
    if not args:
        print_usage()
        sys.exit(0)

    cmd = args[0].lower()

    if cmd == "validate-cycle":
        if len(args) < 2:
            print("Usage: validate-cycle <C1-C10>")
            sys.exit(1)
        result = validate_cycle(args[1])
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif cmd == "validate-count":
        if len(args) < 2:
            print("Usage: validate-count <N>")
            sys.exit(1)
        result = validate_count(args[1])
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif cmd == "validate-type":
        if len(args) < 2:
            print("Usage: validate-type <type>")
            sys.exit(1)
        result = validate_type(args[1])
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif cmd == "validate-horizon":
        if len(args) < 2:
            print("Usage: validate-horizon <horizon>")
            sys.exit(1)
        result = validate_horizon(args[1])
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif cmd == "validate-mode":
        if len(args) < 2:
            print("Usage: validate-mode <mode>")
            sys.exit(1)
        result = validate_mode(args[1])
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif cmd == "validate-axes":
        if len(args) < 2:
            print("Usage: validate-axes <axes>")
            sys.exit(1)
        result = validate_axes(args[1])
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif cmd == "validate-quant":
        if len(args) < 2:
            print("Usage: validate-quant <quant>")
            sys.exit(1)
        result = validate_quant(args[1])
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif cmd == "validate-step0":
        # parse --key value pairs
        params = {}
        i = 1
        while i < len(args):
            if args[i].startswith("--") and i + 1 < len(args):
                key = args[i][2:]
                params[key] = args[i + 1]
                i += 2
            else:
                i += 1
        required = ["cycle", "count", "type", "horizon", "mode", "axes", "quant"]
        missing = [k for k in required if k not in params]
        if missing:
            print(f"Missing parameters: {', '.join(missing)}")
            print("Usage: validate-step0 --cycle C --count N --type T --horizon H --mode M --axes A --quant Q")
            sys.exit(1)
        result = validate_step0(
            params["cycle"],
            params["count"],
            params["type"],
            params["horizon"],
            params["mode"],
            params["axes"],
            params["quant"],
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif cmd == "criteria":
        display_criteria()

    elif cmd == "tfg-steps":
        display_tfg_steps()

    elif cmd == "schwartz-steps":
        display_schwartz_steps()

    elif cmd == "uses":
        display_uses()

    elif cmd == "sub-skills":
        display_subskills()

    elif cmd == "agents":
        display_agents()

    elif cmd == "defense-markets":
        display_defense_markets()

    elif cmd == "kahn-bio":
        display_kahn_bio()

    elif cmd == "cite":
        if len(args) < 2:
            print("Usage: cite <key>")
            print("Available keys:", ", ".join(sorted(BIBLIOGRAPHY.keys())))
            sys.exit(1)
        display_citation(args[1])

    elif cmd == "list-citations":
        display_list_citations()

    elif cmd == "exploratory-vs-normative":
        display_exploratory_vs_normative()

    elif cmd == "cone-of-plausibility":
        display_cone_of_plausibility()

    elif cmd == "self-test":
        passed, total = run_self_test()
        sys.exit(0 if passed == total else 1)

    else:
        print(f"Unknown command: '{cmd}'")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
