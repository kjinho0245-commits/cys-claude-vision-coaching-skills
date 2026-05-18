#!/usr/bin/env python3
"""
vision-foresight-scenarios-narrative-writing — Deterministic Validator
결정론적 검증기: 서사 작성 출력의 구조적 요건을 Python으로 강제 검증.
LLM이 자연어로 재추론하지 못하는 항목 전용.

Input JSON schema:
  {
    "metadata": {
      "focal_issue": str,
      "t0_year": int,
      "t_final_year": int,
      "cycle_type": str,          # "C1".."C10"
      "scenario_type": str,       # "Exploratory" | "Normative" | "Mixed"
      "driving_forces": [str],
      "controversial_items": [str],
      "n_scenarios": int
    },
    "scenarios": [
      {
        "id": int,
        "name": str,
        "word_count_self_reported": int,
        "surprise_count": int,
        "surprise_descriptions": [str],
        "has_future_pov": bool,
        "future_pov_marker": str,
        "sections_present": {
          "opening": bool,
          "setup": bool,
          "middle": bool,
          "climax": bool,
          "resolution": bool
        },
        "named_decision_points_count": int,
        "named_decision_points_list": [str],
        "causal_links_explicit": bool,
        "has_real_sounding_institution": bool,
        "filling_blanks_used": bool
      }
    ],
    "output_checks": {
      "header_format_h3_dash": bool,
      "metadata_block_present": bool,
      "surprise_inventory_table_present": bool
    }
  }

Usage:
  python3 validate_narrative.py --input narrative_data.json
  python3 validate_narrative.py --demo

Exit codes: 0=all valid, 1=errors found, 2=warnings only
"""

import json
import sys
import argparse
from typing import Any, Dict, List, Tuple

# ── Constants ────────────────────────────────────────────────────────────────

VALID_SCENARIO_TYPES = {"Exploratory", "Normative", "Mixed"}
VALID_CYCLE_TYPES = {f"C{i}" for i in range(1, 11)}
REQUIRED_SECTIONS = ("opening", "setup", "middle", "climax", "resolution")

WORD_COUNT_MIN = 3000
WORD_COUNT_MAX = 5000


# ── 1. Scenario count check ──────────────────────────────────────────────────

def check_scenario_count(n_declared: int, n_actual: int) -> Tuple[List[str], List[str]]:
    """
    TFG V3.0 Ch.19 Section III verbatim: "four to five worlds seems ideal."
    n < 1  → ERROR
    n == 1 → ERROR (cross-scenario comparison impossible)
    < 4    → WARN
    > 5    → WARN
    4-5    → OK
    Also verify declared count matches actual count.
    """
    errors: List[str] = []
    warnings: List[str] = []

    if n_declared != n_actual:
        errors.append(
            f"COUNT_MISMATCH: metadata.n_scenarios={n_declared} "
            f"but len(scenarios)={n_actual}"
        )

    n = n_actual
    if n < 1:
        errors.append("COUNT_ERROR: No scenarios found — cannot validate narrative output")
    elif n == 1:
        errors.append(
            "COUNT_ERROR: n=1 — downstream internal-consistency-check requires ≥2 scenarios "
            "(TFG V3.0 Ch.19 Section II: 'alternative scenarios should address similar issues "
            "so that they can be compared')"
        )
    elif n < 4:
        warnings.append(
            f"COUNT_WARN: n={n} — TFG V3.0 Ch.19 recommends 4-5 scenarios "
            "(Section III verbatim: 'four to five worlds seems ideal')"
        )
    elif n > 5:
        warnings.append(
            f"COUNT_WARN: n={n} — TFG V3.0 recommends max 5 scenarios for manageability. "
            "Audit proceeds with elevated comparison complexity."
        )

    return errors, warnings


# ── 2. Metadata checks ───────────────────────────────────────────────────────

def check_metadata(meta: Dict) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []

    # scenario_type validation
    stype = meta.get("scenario_type", "")
    if stype not in VALID_SCENARIO_TYPES:
        errors.append(
            f"SCENARIO_TYPE_ERROR: scenario_type={stype!r} not in "
            f"{sorted(VALID_SCENARIO_TYPES)}. "
            "Must be 'Exploratory', 'Normative', or 'Mixed'."
        )

    # cycle_type validation (warn only — LLM may legitimately extend)
    ctype = meta.get("cycle_type", "")
    if ctype and ctype not in VALID_CYCLE_TYPES:
        warnings.append(
            f"CYCLE_TYPE_WARN: cycle_type={ctype!r} not in C1..C10. "
            "Verify master Step 0 cycle assignment."
        )

    # year sanity
    t0 = meta.get("t0_year")
    tf = meta.get("t_final_year")
    if isinstance(t0, int) and isinstance(tf, int):
        if tf <= t0:
            errors.append(
                f"YEAR_ERROR: t_final_year={tf} must be strictly greater than "
                f"t0_year={t0}"
            )
        if (tf - t0) < 3:
            warnings.append(
                f"YEAR_WARN: time horizon={tf - t0} years is very short. "
                "TFG V3.0 default is 15-25 years."
            )

    # driving_forces presence
    dfs = meta.get("driving_forces", [])
    if not isinstance(dfs, list) or len(dfs) == 0:
        warnings.append(
            "DRIVING_FORCES_WARN: driving_forces is empty. "
            "Internal-consistency-check requires driving forces for cross-scenario audit."
        )

    # focal_issue presence
    fi = meta.get("focal_issue", "")
    if not fi:
        errors.append(
            "FOCAL_ISSUE_ERROR: focal_issue is empty. "
            "Required for internal-consistency-check §5 Input Format."
        )

    return errors, warnings


# ── 3. Per-scenario checks ───────────────────────────────────────────────────

def check_scenario(s: Dict, idx: int) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    label = f"Scenario[{idx}]({s.get('name', '?')})"

    # ── 3a. Word count ───────────────────────────────────────────────────────
    wc = s.get("word_count_self_reported")
    if not isinstance(wc, int) or isinstance(wc, bool):
        errors.append(
            f"TYPE_ERROR: {label}.word_count_self_reported must be int, "
            f"got {type(wc).__name__!r}"
        )
    elif wc < WORD_COUNT_MIN:
        errors.append(
            f"WORD_COUNT_ERROR: {label} word_count={wc} < {WORD_COUNT_MIN}. "
            f"TFG V3.0 Appendix A·B style requires 3000-5000 words per scenario."
        )
    elif wc > WORD_COUNT_MAX:
        warnings.append(
            f"WORD_COUNT_WARN: {label} word_count={wc} > {WORD_COUNT_MAX}. "
            "Consider trimming for manageability."
        )

    # ── 3b. Surprise count — Section IV verbatim hard gate ───────────────────
    sc = s.get("surprise_count")
    if not isinstance(sc, int) or isinstance(sc, bool):
        errors.append(
            f"TYPE_ERROR: {label}.surprise_count must be int, "
            f"got {type(sc).__name__!r}"
        )
    elif sc < 1:
        errors.append(
            f"SURPRISE_GATE_ERROR: {label} surprise_count=0. "
            "Section IV verbatim hard gate: 'scenarios should have some surprises in them — "
            "even in surprise-free or business-as-usual scenarios, because the rate of change "
            "is accelerating' (TFG V3.0 Ch.19 Section IV). "
            "Interest score will be capped at 2/5 by downstream internal-consistency-check."
        )
    else:
        # Verify surprise_descriptions matches count
        descs = s.get("surprise_descriptions", [])
        if not isinstance(descs, list):
            errors.append(
                f"TYPE_ERROR: {label}.surprise_descriptions must be a list"
            )
        elif len(descs) == 0:
            errors.append(
                f"SURPRISE_DESC_ERROR: {label} surprise_count={sc} but "
                "surprise_descriptions is empty. Each surprise must have a description."
            )
        elif len(descs) != sc:
            errors.append(
                f"SURPRISE_COUNT_MISMATCH: {label} surprise_count={sc} but "
                f"len(surprise_descriptions)={len(descs)}. These must match."
            )

    # ── 3c. Future POV ────────────────────────────────────────────────────────
    has_pov = s.get("has_future_pov")
    if not isinstance(has_pov, bool):
        errors.append(
            f"TYPE_ERROR: {label}.has_future_pov must be bool, "
            f"got {type(has_pov).__name__!r}"
        )
    elif not has_pov:
        errors.append(
            f"FUTURE_POV_ERROR: {label} has_future_pov=false. "
            "Step 3 requires past tense from future POV: "
            "'It is now [T_final]. The world experienced...' OR "
            "'By [T_final], [scenario name] world emerged when...' "
            "(TFG V3.0 Ch.19 Section II verbatim: "
            "'future history — that is, the evolution from present conditions'). "
            "Narrative must look BACK from target year, NOT predict forward."
        )
    else:
        marker = s.get("future_pov_marker", "")
        if not marker:
            warnings.append(
                f"FUTURE_POV_WARN: {label} has_future_pov=true but "
                "future_pov_marker is empty. Provide opening sentence as example."
            )

    # ── 3d. Required narrative sections ──────────────────────────────────────
    sections = s.get("sections_present", {})
    if not isinstance(sections, dict):
        errors.append(
            f"TYPE_ERROR: {label}.sections_present must be a JSON object"
        )
    else:
        for sec in REQUIRED_SECTIONS:
            if not sections.get(sec, False):
                errors.append(
                    f"SECTION_ERROR: {label} section '{sec}' missing or false. "
                    "Step 2 Narrative Architecture requires all five sections: "
                    "opening·setup·middle·climax·resolution."
                )

    # ── 3e. Named decision points (warn → downstream Plausibility cap) ────────
    ndp = s.get("named_decision_points_count", 0)
    if isinstance(ndp, int) and not isinstance(ndp, bool) and ndp == 0:
        warnings.append(
            f"DECISION_POINT_WARN: {label} named_decision_points_count=0. "
            "Downstream internal-consistency-check Plausibility rubric §3.1 caps "
            "score at 2/5 when named_decision_points=0. Add ≥1 explicit decision point."
        )

    # ── 3f. Causal links explicit ──────────────────────────────────────────────
    cel = s.get("causal_links_explicit")
    if not isinstance(cel, bool):
        errors.append(
            f"TYPE_ERROR: {label}.causal_links_explicit must be bool"
        )
    elif not cel:
        errors.append(
            f"CAUSAL_LINK_ERROR: {label} causal_links_explicit=false. "
            "Step 5 requires explicit causal connectors throughout the narrative: "
            "'Because X happened, Y followed', 'This decision led to Z', "
            "'The combination of A + B produced C' "
            "(TFG verbatim: 'plausible cause and effect links')."
        )

    # ── 3g. Real-sounding institution (warn) ──────────────────────────────────
    rsi = s.get("has_real_sounding_institution")
    if isinstance(rsi, bool) and not rsi:
        warnings.append(
            f"INSTITUTION_WARN: {label} has_real_sounding_institution=false. "
            "Step 7 (Appendix A·B style) requires ≥1 named fictional institution/program "
            "per scenario (GLEEM Plan style: acronym + full name + scope + action items)."
        )

    return errors, warnings


# ── 4. Output format checks ──────────────────────────────────────────────────

def check_output_format(oc: Dict) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []

    # Header format — must be H3 with dash separator
    if not oc.get("header_format_h3_dash", False):
        errors.append(
            "FORMAT_ERROR: Scenario headers must use '### Scenario N — [Name]' format "
            "(H3 heading + em-dash separator). "
            "NOT '#### Scenario N: [Name]' (H4 + colon). "
            "Required for vision-foresight-scenarios-internal-consistency-check §5 Input Format compatibility."
        )

    # Metadata block
    if not oc.get("metadata_block_present", False):
        errors.append(
            "FORMAT_ERROR: metadata_block_present=false. "
            "Output must include metadata block with: Focal Issue, Time Horizon, Cycle Type, "
            "Scenario Type, Driving Forces, Controversial Items. "
            "Required by vision-foresight-scenarios-internal-consistency-check §5."
        )

    # Surprise inventory table
    if not oc.get("surprise_inventory_table_present", False):
        warnings.append(
            "FORMAT_WARN: surprise_inventory_table_present=false. "
            "Output template requires Surprise Elements Inventory table "
            "(§4 Output Format specification)."
        )

    return errors, warnings


# ── 5. Main validation orchestrator ─────────────────────────────────────────

def validate_narrative_output(data: Dict) -> Dict:
    """
    Run all deterministic checks on the LLM-generated narrative JSON.
    Returns:
      {
        "valid": bool,
        "overall_pass_fail": "PASS" | "FAIL",
        "scenario_count": int,
        "scenario_results": [...],
        "errors": [str, ...],
        "warnings": [str, ...]
      }
    """
    all_errors: List[str] = []
    all_warnings: List[str] = []
    scenario_results: List[Dict] = []

    # Metadata
    meta = data.get("metadata", {})
    if not isinstance(meta, dict):
        all_errors.append("TYPE_ERROR: 'metadata' must be a JSON object")
        meta = {}
    else:
        m_errs, m_warns = check_metadata(meta)
        all_errors.extend(m_errs)
        all_warnings.extend(m_warns)

    # Scenarios
    scenarios = data.get("scenarios", [])
    if not isinstance(scenarios, list):
        all_errors.append("TYPE_ERROR: 'scenarios' must be a JSON array")
        scenarios = []

    n_declared = meta.get("n_scenarios", len(scenarios))
    if not isinstance(n_declared, int):
        all_errors.append(
            f"TYPE_ERROR: metadata.n_scenarios must be int, got {type(n_declared).__name__!r}"
        )
        n_declared = len(scenarios)

    count_errs, count_warns = check_scenario_count(n_declared, len(scenarios))
    all_errors.extend(count_errs)
    all_warnings.extend(count_warns)

    for i, s in enumerate(scenarios):
        if not isinstance(s, dict):
            all_errors.append(f"TYPE_ERROR: scenarios[{i}] must be a JSON object")
            continue
        s_errs, s_warns = check_scenario(s, i + 1)
        all_errors.extend(s_errs)
        all_warnings.extend(s_warns)
        scenario_results.append({
            "id": s.get("id", i + 1),
            "name": s.get("name", f"Scenario {i+1}"),
            "word_count": s.get("word_count_self_reported"),
            "surprise_count": s.get("surprise_count"),
            "errors": s_errs,
            "warnings": s_warns,
            "valid": len(s_errs) == 0,
        })

    # Output checks
    oc = data.get("output_checks", {})
    if isinstance(oc, dict):
        oc_errs, oc_warns = check_output_format(oc)
        all_errors.extend(oc_errs)
        all_warnings.extend(oc_warns)

    return {
        "valid": len(all_errors) == 0,
        "overall_pass_fail": "PASS" if len(all_errors) == 0 else "FAIL",
        "scenario_count": len(scenarios),
        "scenario_results": scenario_results,
        "errors": all_errors,
        "warnings": all_warnings,
    }


# ── 6. Demo data ─────────────────────────────────────────────────────────────

DEMO_VALID = {
    "metadata": {
        "focal_issue": "한국 AGI 2030-2041 시나리오",
        "t0_year": 2026,
        "t_final_year": 2041,
        "cycle_type": "C1",
        "scenario_type": "Exploratory",
        "driving_forces": ["AI regulation stringency", "AGI capability trajectory"],
        "controversial_items": ["AI singularity risk", "mass unemployment scenario"],
        "n_scenarios": 4
    },
    "scenarios": [
        {
            "id": 1, "name": "Controlled Ascent",
            "word_count_self_reported": 3800,
            "surprise_count": 2,
            "surprise_descriptions": [
                "AGI emerged 3 years ahead of consensus forecast via unexpected BCI synthesis",
                "South Korea became global AI governance standard-setter, not the US or China"
            ],
            "has_future_pov": True,
            "future_pov_marker": "It is now 2041. The world experienced a decade of measured AI development...",
            "sections_present": {"opening": True, "setup": True, "middle": True, "climax": True, "resolution": True},
            "named_decision_points_count": 3,
            "named_decision_points_list": [
                "2028 Seoul AGI Safety Accord — multilateral moratorium on unsupervised training runs",
                "2033 Global Deployment Pause — six-month freeze following Seoul Accord review",
                "2038 AGI Rights Framework — landmark legal personhood determination"
            ],
            "causal_links_explicit": True,
            "has_real_sounding_institution": True,
            "filling_blanks_used": False
        },
        {
            "id": 2, "name": "Fragmented Race",
            "word_count_self_reported": 4100,
            "surprise_count": 1,
            "surprise_descriptions": [
                "US-China AGI arms race collapsed simultaneously following shared systemic failure event"
            ],
            "has_future_pov": True,
            "future_pov_marker": "By 2041, the Fragmented Race world had crystallized when the 2029 bilateral moratorium collapsed...",
            "sections_present": {"opening": True, "setup": True, "middle": True, "climax": True, "resolution": True},
            "named_decision_points_count": 2,
            "named_decision_points_list": [
                "2029 bilateral AI moratorium — quickly abandoned within 8 months",
                "2036 defection event — first nation to deploy autonomous AGI system"
            ],
            "causal_links_explicit": True,
            "has_real_sounding_institution": True,
            "filling_blanks_used": False
        },
        {
            "id": 3, "name": "Open Source Dawn",
            "word_count_self_reported": 3500,
            "surprise_count": 1,
            "surprise_descriptions": [
                "Decentralized open-source AGI outperformed all proprietary systems by 2033"
            ],
            "has_future_pov": True,
            "future_pov_marker": "It is now 2041. The Open Source Dawn scenario unfolded against all predictions...",
            "sections_present": {"opening": True, "setup": True, "middle": True, "climax": True, "resolution": True},
            "named_decision_points_count": 2,
            "named_decision_points_list": [
                "2030 OAGI Foundation charter — open governance framework",
                "2035 OAGI v3.0 release — first AGI system passed Turing-plus evaluation"
            ],
            "causal_links_explicit": True,
            "has_real_sounding_institution": True,
            "filling_blanks_used": False
        },
        {
            "id": 4, "name": "Winter of Consequence",
            "word_count_self_reported": 3200,
            "surprise_count": 2,
            "surprise_descriptions": [
                "AGI winter followed near-miss incident (not an actual catastrophe, but close enough)",
                "Unexpected renaissance of symbolic AI and rule-based systems after LLM failures"
            ],
            "has_future_pov": True,
            "future_pov_marker": "By 2041, the Winter of Consequence had settled in after the 2031 Seoul incident...",
            "sections_present": {"opening": True, "setup": True, "middle": True, "climax": True, "resolution": True},
            "named_decision_points_count": 2,
            "named_decision_points_list": [
                "2031 emergency shutdown order — global 18-month moratorium",
                "2035 ACAI Restart Framework — new risk-tiered deployment protocol"
            ],
            "causal_links_explicit": True,
            "has_real_sounding_institution": True,
            "filling_blanks_used": False
        }
    ],
    "output_checks": {
        "header_format_h3_dash": True,
        "metadata_block_present": True,
        "surprise_inventory_table_present": True
    }
}

DEMO_INVALID = {
    "metadata": {
        "focal_issue": "",          # ERROR: empty focal_issue
        "t0_year": 2041,
        "t_final_year": 2026,       # ERROR: t_final <= t0
        "cycle_type": "C1",
        "scenario_type": "Futuristic",  # ERROR: not in valid set
        "driving_forces": [],
        "n_scenarios": 3            # MISMATCH: actual is 2
    },
    "scenarios": [
        {
            "id": 1, "name": "Scenario A",
            "word_count_self_reported": 1500,   # ERROR: < 3000
            "surprise_count": 0,                # ERROR: hard gate
            "surprise_descriptions": [],
            "has_future_pov": False,             # ERROR
            "future_pov_marker": "",
            "sections_present": {"opening": True, "setup": False, "middle": True, "climax": False, "resolution": True},  # ERROR: missing setup, climax
            "named_decision_points_count": 0,   # WARN
            "named_decision_points_list": [],
            "causal_links_explicit": True,
            "has_real_sounding_institution": False,
            "filling_blanks_used": False
        },
        {
            "id": 2, "name": "Scenario B",
            "word_count_self_reported": 3200,
            "surprise_count": 1,
            "surprise_descriptions": ["unexpected breakthrough"],
            "has_future_pov": True,
            "future_pov_marker": "It is now 2041...",
            "sections_present": {"opening": True, "setup": True, "middle": True, "climax": True, "resolution": True},
            "named_decision_points_count": 1,
            "named_decision_points_list": ["Decision X"],
            "causal_links_explicit": False,     # ERROR
            "has_real_sounding_institution": False,
            "filling_blanks_used": False
        }
    ],
    "output_checks": {
        "header_format_h3_dash": False,         # ERROR
        "metadata_block_present": False,        # ERROR
        "surprise_inventory_table_present": False  # WARN
    }
}


def run_demo() -> None:
    print("=== DEMO: Valid narrative output (4 scenarios — should show 0 errors) ===")
    r = validate_narrative_output(DEMO_VALID)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    print()
    print("=== DEMO: Invalid narrative output (multiple errors expected) ===")
    r2 = validate_narrative_output(DEMO_INVALID)
    print(json.dumps(r2, ensure_ascii=False, indent=2))


# ── 7. CLI entry point ────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Deterministic validator for vision-foresight-scenarios-narrative-writing output JSON. "
            "Checks: scenario count, word count, surprise count (Section IV hard gate), "
            "future POV, narrative sections, causal links, output format."
        )
    )
    parser.add_argument("--input", help="Path to narrative JSON file")
    parser.add_argument("--demo", action="store_true", help="Run self-test with demo data")
    args = parser.parse_args()

    if args.demo:
        run_demo()
        sys.exit(0)

    if not args.input:
        parser.print_help()
        sys.exit(2)

    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)

    result = validate_narrative_output(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result["valid"]:
        sys.exit(1)
    elif result["warnings"]:
        sys.exit(2)
    else:
        sys.exit(0)
