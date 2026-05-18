#!/usr/bin/env python3
"""
tripwire_evaluator.py
결정론 환원 모듈 — Trip-wire 임계값 상태 평가

출처: Petersen & Steinmüller (2009) Section III.3 verbatim
  "Set gates or trip wires that generate increased attention to a particular
   event, as it appears more likely." (9-step institutional process, Step 9)

목적: LLM이 yellow/red 상태를 주관적으로 판단하는 것을 차단.
  current_value, yellow_threshold, red_threshold 세 값을 받아
  결정론적으로 status를 반환한다.

상태 체계:
  GREEN  = current_value < yellow_threshold (정상 — 주의 불필요)
  YELLOW = yellow_threshold <= current_value < red_threshold (주의 — 경계 강화)
  RED    = current_value >= red_threshold (경보 — options-action plan 즉시 활성화)
  N/A    = 정량화 불가 (qualitative only)

PDF 연계:
  YELLOW → "increased attention" (Step 9 verbatim)
  RED    → "activate options-action plan" (options-action sub-skill 호출)
"""
import argparse
import json
import sys
from typing import Optional


STATUS_GREEN = "GREEN"
STATUS_YELLOW = "YELLOW"
STATUS_RED = "RED"
STATUS_NA = "N/A"

ESCALATION_MAP = {
    STATUS_GREEN: "no_action",
    STATUS_YELLOW: "notify — increased attention (PDF §III.3 Step 9 verbatim)",
    STATUS_RED: "activate_options_action_plan — forward to vision-foresight-wild-cards-options-action",
    STATUS_NA: "qualitative_monitor_only",
}


def evaluate(
    current_value: Optional[float],
    yellow_threshold: Optional[float],
    red_threshold: Optional[float],
    signal_id: str = "unknown",
) -> dict:
    """Evaluate trip-wire status."""
    # Handle qualitative / N/A case
    if current_value is None or yellow_threshold is None or red_threshold is None:
        return {
            "signal_id": signal_id,
            "status": STATUS_NA,
            "escalation_action": ESCALATION_MAP[STATUS_NA],
            "note": "Qualitative signal — no numeric threshold available",
            "source": "Petersen & Steinmüller (2009) Section III.3 Step 9",
        }

    # Validate threshold ordering
    if yellow_threshold >= red_threshold:
        return {
            "signal_id": signal_id,
            "error": f"Invalid thresholds: yellow_threshold ({yellow_threshold}) must be < red_threshold ({red_threshold})",
            "source": "tripwire_evaluator.py validation rule",
        }

    # Determine status
    if current_value >= red_threshold:
        status = STATUS_RED
    elif current_value >= yellow_threshold:
        status = STATUS_YELLOW
    else:
        status = STATUS_GREEN

    return {
        "signal_id": signal_id,
        "current_value": current_value,
        "yellow_threshold": yellow_threshold,
        "red_threshold": red_threshold,
        "status": status,
        "escalation_action": ESCALATION_MAP[status],
        "comparison": {
            "vs_yellow": f"{current_value} {'≥' if current_value >= yellow_threshold else '<'} {yellow_threshold}",
            "vs_red": f"{current_value} {'≥' if current_value >= red_threshold else '<'} {red_threshold}",
        },
        "source": "Petersen & Steinmüller (2009) Section III.3 Step 9 verbatim",
    }


def batch_evaluate(entries: list) -> dict:
    """Evaluate a list of trip-wire entries."""
    results = []
    summary = {STATUS_GREEN: 0, STATUS_YELLOW: 0, STATUS_RED: 0, STATUS_NA: 0}
    for entry in entries:
        r = evaluate(
            entry.get("current_value"),
            entry.get("yellow_threshold"),
            entry.get("red_threshold"),
            entry.get("signal_id", "unknown"),
        )
        results.append(r)
        s = r.get("status", STATUS_NA)
        if s in summary:
            summary[s] += 1

    red_signals = [r["signal_id"] for r in results if r.get("status") == STATUS_RED]
    return {
        "n_evaluated": len(results),
        "summary": summary,
        "red_alerts": red_signals,
        "requires_immediate_action": len(red_signals) > 0,
        "results": results,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Trip-wire threshold evaluator — deterministic GREEN/YELLOW/RED"
    )
    subparsers = parser.add_subparsers(dest="cmd")

    # single evaluation
    ev = subparsers.add_parser("eval", help="Evaluate a single trip-wire")
    ev.add_argument("--id", default="unknown", help="Signal ID")
    ev.add_argument("--current", type=float, help="Current value (omit for N/A)")
    ev.add_argument("--yellow", type=float, help="Yellow threshold")
    ev.add_argument("--red", type=float, help="Red threshold")

    # batch from JSON file
    batch = subparsers.add_parser("batch", help="Batch evaluate from JSON file")
    batch.add_argument("--file", required=True, help="JSON file with list of {signal_id, current_value, yellow_threshold, red_threshold}")

    # show escalation map
    subparsers.add_parser("escalation", help="Show escalation action map")

    args = parser.parse_args()

    if args.cmd == "eval":
        result = evaluate(
            current_value=args.current,
            yellow_threshold=args.yellow,
            red_threshold=args.red,
            signal_id=args.id,
        )
    elif args.cmd == "batch":
        try:
            with open(args.file) as f:
                entries = json.load(f)
            result = batch_evaluate(entries)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            result = {"error": str(e)}
    elif args.cmd == "escalation":
        result = ESCALATION_MAP
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
