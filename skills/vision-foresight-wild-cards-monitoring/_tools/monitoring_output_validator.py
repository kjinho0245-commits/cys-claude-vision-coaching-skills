#!/usr/bin/env python3
"""
monitoring_output_validator.py
결정론 환원 모듈 — monitoring_output JSON 구조 검증

출처: Petersen & Steinmüller (2009) Section III.3
  본 도구는 monitoring sub-skill의 최종 출력 JSON을 마스터에 반환하기 전에
  구조적 완결성을 검증한다. LLM이 출력 필드를 누락하거나 잘못된 값을
  반환하는 것을 차단한다.

검증 항목:
  1. 필수 최상위 필드 존재 여부
  2. 각 Wild Card 항목의 필수 필드
  3. weak_signal 수 제약 (3-7 per WC, PDF §III.3)
  4. signal_id 포맷 (WS-XXX-YY 패턴)
  5. trip_wire_id 포맷 (TW-XXX-YY 패턴)
  6. foresight_factor 값 (A-F)
  7. monitoring_feasibility 값
  8. vrmp_tier 값 (R-1·R-2·R-3)
  9. Type 3 Wild Card는 monitoring_feasibility=not_observable_type_3 강제
  10. foresight_factor_match boolean consistency check
  11. total_weak_signals vs 실제 합산 일치
  12. type_3_unknown_unknowns_skipped vs 실제 Type 3 WC 수 일치
  13. refresh_cadence_distribution 합산 vs total_weak_signals 일치
  14. weak_signals_detail signal_type·current_status·refresh_cadence 값 검증
  15. trip_wires_detail status 값 검증 (GREEN/YELLOW/RED/N/A)
  16. vrmp_tier=R-3 source_trail fallback 명시 경고
"""
import argparse
import json
import re
import sys
from typing import Any

# Constants
VALID_FF = set("ABCDEF")
VALID_FEASIBILITY = {"high", "medium", "low", "not_observable_type_3"}
VALID_VRMP_TIERS = {"R-1", "R-2", "R-3"}
VALID_WC_TYPES = {1, 2, 3}
VALID_CADENCES = {"daily", "weekly", "monthly", "quarterly"}
VALID_CADENCES_OR_NONE = VALID_CADENCES | {None}
VALID_SIGNAL_TYPES = {
    "precursor_event", "indicator_threshold", "trend_acceleration",
    "regulatory_warning", "academic_consensus_shift", "outlier_data_point",
}
VALID_CURRENT_STATUS = {"detected", "not_yet_detected", "partially_detected"}
VALID_TRIPWIRE_STATUS = {"GREEN", "YELLOW", "RED", "N/A"}
SIGNAL_ID_RE = re.compile(r"^WS-\d{3}-\d{2}$")
TRIPWIRE_ID_RE = re.compile(r"^TW-\d{3}-\d{2}$")
MIN_WS = 3
MAX_WS = 7

REQUIRED_TOP_FIELDS = [
    "meta",
    "per_wild_card",
    "weak_signals_detail",
    "trip_wires_detail",
    "early_warning_system_spec",
    "prediction_market_questions",
    "institutional_steps",
]

REQUIRED_PER_WC_FIELDS = [
    "wild_card_id",
    "title",
    "type",
    "monitoring_feasibility",
    "weak_signals",
    "trip_wires",
    "foresight_factor_revalidated",
    "foresight_factor_match",
]

REQUIRED_INSTITUTIONAL_STEPS = [
    "step_2_lesser_events",
    "step_3_scouting_persona",
    "step_4_clearing_house",
    "step_5_structure_info",
    "step_6_display_spatial",
    "step_9_trip_wire_gates",
]

REQUIRED_META_FIELDS = [
    "n_wild_cards_monitored",
    "total_weak_signals",
    "type_3_unknown_unknowns_skipped",
    "refresh_cadence_distribution",
]


def validate(data: dict) -> dict:
    errors = []
    warnings = []

    # 1. Top-level fields
    for field in REQUIRED_TOP_FIELDS:
        if field not in data:
            errors.append(f"missing top-level field: '{field}'")

    if errors:  # bail early if structure broken
        return _result(errors, warnings)

    meta = data.get("meta", {})
    per_wc = data.get("per_wild_card", [])
    ws_detail = data.get("weak_signals_detail", [])
    tw_detail = data.get("trip_wires_detail", [])
    inst = data.get("institutional_steps", {})

    # 2. Meta fields
    for f in REQUIRED_META_FIELDS:
        if f not in meta:
            errors.append(f"meta: missing field '{f}'")

    # 3. n_wild_cards_monitored consistency
    n_wc = meta.get("n_wild_cards_monitored", 0)
    if isinstance(n_wc, int) and n_wc != len(per_wc):
        errors.append(
            f"meta.n_wild_cards_monitored={n_wc} but len(per_wild_card)={len(per_wc)}"
        )

    # 3b. total_weak_signals consistency — BUG 19 FIX
    total_ws_declared = meta.get("total_weak_signals", None)
    actual_ws_total = sum(len(wc.get("weak_signals", [])) for wc in per_wc)
    if isinstance(total_ws_declared, int):
        if total_ws_declared != actual_ws_total:
            errors.append(
                f"meta.total_weak_signals={total_ws_declared} but actual sum of weak_signals "
                f"across all per_wild_card={actual_ws_total} — must match"
            )

    # 3c. type_3_unknown_unknowns_skipped consistency — BUG 22 FIX (WEAKNESS A)
    t3_declared = meta.get("type_3_unknown_unknowns_skipped", None)
    if isinstance(t3_declared, int):
        actual_t3 = sum(1 for wc in per_wc if wc.get("type") == 3)
        if t3_declared != actual_t3:
            errors.append(
                f"meta.type_3_unknown_unknowns_skipped={t3_declared} but actual Type 3 WC "
                f"count in per_wild_card={actual_t3} — must match"
            )

    # 4. refresh_cadence_distribution key validation
    rcd = meta.get("refresh_cadence_distribution", {})
    if isinstance(rcd, dict):
        for k in rcd:
            if k not in VALID_CADENCES:
                errors.append(f"meta.refresh_cadence_distribution: invalid cadence key '{k}'")

    # 4b. refresh_cadence_distribution sum vs total_weak_signals — BUG 23 FIX (WEAKNESS B)
    if isinstance(rcd, dict) and isinstance(total_ws_declared, int):
        cadence_sum = sum(v for v in rcd.values() if isinstance(v, int))
        if cadence_sum != actual_ws_total:
            errors.append(
                f"meta.refresh_cadence_distribution sum={cadence_sum} does not equal "
                f"actual total_weak_signals={actual_ws_total} — all signals must appear in cadence distribution"
            )

    # 5. Per-WC checks
    all_ws_ids = set()
    all_tw_ids = set()
    for i, wc in enumerate(per_wc):
        prefix = f"per_wild_card[{i}] ({wc.get('wild_card_id', '?')})"
        for f in REQUIRED_PER_WC_FIELDS:
            if f not in wc:
                errors.append(f"{prefix}: missing field '{f}'")

        # type check
        wc_type = wc.get("type")
        if wc_type not in VALID_WC_TYPES:
            errors.append(f"{prefix}: type={wc_type} not in {VALID_WC_TYPES}")

        # monitoring_feasibility
        mf = wc.get("monitoring_feasibility")
        if mf not in VALID_FEASIBILITY:
            errors.append(f"{prefix}: monitoring_feasibility='{mf}' not in {VALID_FEASIBILITY}")

        # Type 3 → must be not_observable
        if wc_type == 3 and mf != "not_observable_type_3":
            errors.append(
                f"{prefix}: Type 3 WC must have monitoring_feasibility='not_observable_type_3', "
                f"got '{mf}' — PDF §III.3 verbatim"
            )

        # foresight_factor_revalidated
        ff = wc.get("foresight_factor_revalidated")
        if ff not in VALID_FF:
            errors.append(f"{prefix}: foresight_factor_revalidated='{ff}' not in A-F")

        # Type 3 → must be F
        if wc_type == 3 and ff != "F":
            errors.append(
                f"{prefix}: Type 3 WC must have foresight_factor_revalidated='F', got '{ff}' "
                f"— PDF §III.3: 'escape from any kind of observation'"
            )

        # foresight_factor_match consistency check — BUG 20 FIX
        ff_impact = wc.get("foresight_factor_impact_index_value")
        ff_match = wc.get("foresight_factor_match")
        ff_mismatch_explanation = wc.get("foresight_factor_mismatch_explanation")
        if ff in VALID_FF and isinstance(ff_impact, str) and ff_impact not in ("N/A", ""):
            if ff_impact in VALID_FF:
                expected_match = (ff == ff_impact)
                if ff_match is not None and ff_match != expected_match:
                    errors.append(
                        f"{prefix}: foresight_factor_match={ff_match} is inconsistent — "
                        f"revalidated='{ff}' vs impact_index='{ff_impact}' → should be match={expected_match}"
                    )
                # If match=false, mismatch_explanation must be non-null and non-empty
                if ff_match is False and (not ff_mismatch_explanation or str(ff_mismatch_explanation).strip() == ""):
                    errors.append(
                        f"{prefix}: foresight_factor_match=false requires non-empty "
                        f"foresight_factor_mismatch_explanation"
                    )
                # If match=true, mismatch_explanation should be null
                if ff_match is True and ff_mismatch_explanation not in (None, ""):
                    warnings.append(
                        f"{prefix}: foresight_factor_match=true but mismatch_explanation is non-null"
                    )

        # weak_signals list
        ws_list = wc.get("weak_signals", [])
        if not isinstance(ws_list, list):
            errors.append(f"{prefix}: weak_signals must be a list")
        elif wc_type != 3:
            if not (MIN_WS <= len(ws_list) <= MAX_WS):
                errors.append(
                    f"{prefix}: {len(ws_list)} weak signals violates PDF §III.3 constraint [{MIN_WS},{MAX_WS}]"
                )
            for ws_id in ws_list:
                if not SIGNAL_ID_RE.match(str(ws_id)):
                    errors.append(f"{prefix}: weak_signal id '{ws_id}' does not match WS-XXX-YY pattern")
                if ws_id in all_ws_ids:
                    errors.append(f"{prefix}: duplicate weak_signal id '{ws_id}'")
                all_ws_ids.add(ws_id)

        # trip_wires list
        tw_list = wc.get("trip_wires", [])
        if not isinstance(tw_list, list):
            errors.append(f"{prefix}: trip_wires must be a list")
        elif wc_type != 3:
            for tw_id in tw_list:
                if not TRIPWIRE_ID_RE.match(str(tw_id)):
                    errors.append(f"{prefix}: trip_wire id '{tw_id}' does not match TW-XXX-YY pattern")
                if tw_id in all_tw_ids:
                    errors.append(f"{prefix}: duplicate trip_wire id '{tw_id}'")
                all_tw_ids.add(tw_id)

    # 6. weak_signals_detail — BUG 24 FIX (WEAKNESS C)
    detail_ws_ids = set()
    for j, ws in enumerate(ws_detail):
        ws_id = ws.get("signal_id", "")
        if not SIGNAL_ID_RE.match(str(ws_id)):
            errors.append(f"weak_signals_detail[{j}]: signal_id='{ws_id}' malformed")
        if ws_id in detail_ws_ids:
            errors.append(f"weak_signals_detail: duplicate signal_id '{ws_id}'")
        detail_ws_ids.add(ws_id)
        # Validate optional field values if provided
        st = ws.get("signal_type")
        if st is not None and st not in VALID_SIGNAL_TYPES:
            errors.append(
                f"weak_signals_detail[{j}] ({ws_id}): signal_type='{st}' not in allowed set "
                f"{sorted(VALID_SIGNAL_TYPES)}"
            )
        cs = ws.get("current_status")
        if cs is not None and cs not in VALID_CURRENT_STATUS:
            errors.append(
                f"weak_signals_detail[{j}] ({ws_id}): current_status='{cs}' not in "
                f"{sorted(VALID_CURRENT_STATUS)}"
            )
        rc = ws.get("refresh_cadence")
        if rc is not None and rc not in VALID_CADENCES:
            errors.append(
                f"weak_signals_detail[{j}] ({ws_id}): refresh_cadence='{rc}' not in "
                f"{sorted(VALID_CADENCES)}"
            )

    # 7. trip_wires_detail — BUG 25 FIX (WEAKNESS F)
    detail_tw_ids = set()
    for k, tw in enumerate(tw_detail):
        tw_id = tw.get("trip_id", tw.get("signal_id", ""))
        if not TRIPWIRE_ID_RE.match(str(tw_id)):
            errors.append(f"trip_wires_detail[{k}]: id='{tw_id}' malformed")
        if tw_id in detail_tw_ids:
            errors.append(f"trip_wires_detail: duplicate id '{tw_id}'")
        detail_tw_ids.add(tw_id)
        # Validate status field if provided
        tw_status = tw.get("status")
        if tw_status is not None and tw_status not in VALID_TRIPWIRE_STATUS:
            errors.append(
                f"trip_wires_detail[{k}] ({tw_id}): status='{tw_status}' not in "
                f"{sorted(VALID_TRIPWIRE_STATUS)}"
            )

    # 8. Institutional steps
    for step_key in REQUIRED_INSTITUTIONAL_STEPS:
        if step_key not in inst:
            errors.append(f"institutional_steps: missing key '{step_key}'")
        elif not inst[step_key]:
            warnings.append(f"institutional_steps.{step_key} is empty")

    # 9. vrmp_tier in return envelope (if present at top level)
    vt = data.get("vrmp_tier")
    if vt is not None and vt not in VALID_VRMP_TIERS:
        errors.append(f"vrmp_tier='{vt}' not in {VALID_VRMP_TIERS}")

    # 10. source_trail R-3 fallback check — BUG 21 FIX
    # SKILL.md §8: "R-3: source_trail에 'R-3 fallback — [이유]' 명시 필수"
    source_trail = data.get("source_trail", [])
    if vt == "R-3" and isinstance(source_trail, list):
        trail_text = " ".join(str(s) for s in source_trail).lower()
        if "r-3" not in trail_text and "fallback" not in trail_text:
            warnings.append(
                "vrmp_tier=R-3 but source_trail does not contain 'R-3 fallback' mention "
                "— SKILL.md §8 mandates: source_trail에 'R-3 fallback — [이유]' 명시 필수"
            )
    if vt in ("R-1", "R-2") and isinstance(source_trail, list) and len(source_trail) == 0:
        warnings.append(
            f"vrmp_tier={vt} but source_trail is empty — SKILL.md §8 requires populated source_trail"
        )

    return _result(errors, warnings)


def _result(errors: list, warnings: list) -> dict:
    return {
        "pass": len(errors) == 0,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "source": "monitoring_output_validator.py — Petersen & Steinmüller (2009) §III.3",
    }


def main():
    parser = argparse.ArgumentParser(
        description="Validate monitoring_output JSON before returning to master"
    )
    parser.add_argument("--file", help="Path to monitoring_output JSON file")
    parser.add_argument("--stdin", action="store_true", help="Read JSON from stdin")
    args = parser.parse_args()

    if args.stdin:
        raw = sys.stdin.read()
    elif args.file:
        with open(args.file) as f:
            raw = f.read()
    else:
        parser.print_help()
        sys.exit(1)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(json.dumps({"pass": False, "error": f"JSON parse error: {e}"}, indent=2))
        sys.exit(1)

    result = validate(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
