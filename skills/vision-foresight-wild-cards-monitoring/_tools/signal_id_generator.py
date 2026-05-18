#!/usr/bin/env python3
"""
signal_id_generator.py
결정론 환원 모듈 — Weak Signal ID / Trip-wire ID 생성

출처: Petersen & Steinmüller (2009) Section III.3
  본 도구는 LLM이 임의로 ID를 만들거나 충돌하는 것을 방지한다.

ID 체계:
  Weak Signal:  WS-{WC_NUM}-{SEQ}  예: WS-001-01, WS-003-02
  Trip-wire:    TW-{WC_NUM}-{SEQ}  예: TW-001-01, TW-001-02

규칙:
  - WC_NUM: Wild Card 번호 (001-999, 3자리 zero-padded)
  - SEQ: 해당 Wild Card 내 순번 (01-99, 2자리 zero-padded)
  - 같은 Wild Card의 Weak Signal 수: 3-7개 (PDF § III.3 권장)
  - Trip-wire ID는 대응 Weak Signal ID와 동일 WC_NUM·SEQ 공유
"""
import argparse
import json
import sys

MIN_SIGNALS_PER_WC = 3  # PDF §III.3 "3-7 weak signals"
MAX_SIGNALS_PER_WC = 7

SIGNAL_TYPES = [
    "precursor_event",
    "indicator_threshold",
    "trend_acceleration",
    "regulatory_warning",
    "academic_consensus_shift",
    "outlier_data_point",
]

CURRENT_STATUS_OPTIONS = ["detected", "not_yet_detected", "partially_detected"]


def generate_signal_id(wc_num: int, seq: int, id_type: str = "WS") -> str:
    """Return a canonical signal ID string."""
    if id_type not in ("WS", "TW"):
        raise ValueError(f"id_type must be 'WS' or 'TW', got '{id_type}'")
    if not (1 <= wc_num <= 999):
        raise ValueError(f"wc_num must be 1-999, got {wc_num}")
    if not (1 <= seq <= 99):
        raise ValueError(f"seq must be 1-99, got {seq}")
    return f"{id_type}-{wc_num:03d}-{seq:02d}"


def batch_generate(wc_num: int, n_signals: int, id_type: str = "WS") -> dict:
    """Generate a batch of IDs for one Wild Card."""
    errors = []
    if not (1 <= wc_num <= 999):
        errors.append(f"wc_num={wc_num} out of range 1-999")
    if not (MIN_SIGNALS_PER_WC <= n_signals <= MAX_SIGNALS_PER_WC):
        errors.append(
            f"n_signals={n_signals} violates PDF §III.3 constraint [{MIN_SIGNALS_PER_WC},{MAX_SIGNALS_PER_WC}]"
        )
    if errors:
        return {"error": errors, "source": "Petersen & Steinmüller (2009) Section III.3"}

    ids = [generate_signal_id(wc_num, i + 1, id_type) for i in range(n_signals)]
    return {
        "wc_num": wc_num,
        "id_type": id_type,
        "n_signals": n_signals,
        "ids": ids,
        "constraint_check": f"PDF §III.3 mandates {MIN_SIGNALS_PER_WC}-{MAX_SIGNALS_PER_WC} signals per Wild Card — OK",
        "source": "Petersen & Steinmüller (2009) Section III.3",
    }


def validate_signal_type(signal_type: str) -> dict:
    valid = signal_type in SIGNAL_TYPES
    return {
        "signal_type": signal_type,
        "valid": valid,
        "allowed": SIGNAL_TYPES,
        "error": f"'{signal_type}' not in allowed signal_types" if not valid else None,
    }


def validate_current_status(status: str) -> dict:
    valid = status in CURRENT_STATUS_OPTIONS
    return {
        "status": status,
        "valid": valid,
        "allowed": CURRENT_STATUS_OPTIONS,
        "error": f"'{status}' not in allowed current_status options" if not valid else None,
    }


def list_conventions() -> dict:
    return {
        "id_format": {
            "weak_signal": "WS-{WC_NUM:3d}-{SEQ:2d}  e.g. WS-001-01",
            "trip_wire": "TW-{WC_NUM:3d}-{SEQ:2d}  e.g. TW-001-01",
        },
        "constraints": {
            "wc_num_range": "001-999",
            "seq_range": "01-99",
            "min_signals_per_wc": MIN_SIGNALS_PER_WC,
            "max_signals_per_wc": MAX_SIGNALS_PER_WC,
            "pdf_source": "Petersen & Steinmüller (2009) Section III.3 '3-7 weak signals per Wild Card'",
        },
        "signal_types": SIGNAL_TYPES,
        "current_status_options": CURRENT_STATUS_OPTIONS,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Deterministic Weak Signal / Trip-wire ID generator"
    )
    subparsers = parser.add_subparsers(dest="cmd")

    # generate subcommand
    gen = subparsers.add_parser("generate", help="Generate IDs for one Wild Card")
    gen.add_argument("--wc", type=int, required=True, help="Wild Card number (1-999)")
    gen.add_argument("--n", type=int, required=True, help="Number of signals (3-7)")
    gen.add_argument("--type", default="WS", choices=["WS", "TW"], help="ID type")

    # single subcommand
    single = subparsers.add_parser("single", help="Generate a single ID")
    single.add_argument("--wc", type=int, required=True)
    single.add_argument("--seq", type=int, required=True)
    single.add_argument("--type", default="WS", choices=["WS", "TW"])

    # validate-type subcommand
    vt = subparsers.add_parser("validate-type", help="Validate a signal_type string")
    vt.add_argument("--signal-type", required=True)

    # list subcommand
    subparsers.add_parser("list", help="List all conventions")

    args = parser.parse_args()

    if args.cmd == "generate":
        result = batch_generate(args.wc, args.n, args.type)
    elif args.cmd == "single":
        try:
            result = {"id": generate_signal_id(args.wc, args.seq, args.type)}
        except ValueError as e:
            result = {"error": str(e)}
    elif args.cmd == "validate-type":
        result = validate_signal_type(args.signal_type)
    elif args.cmd == "list":
        result = list_conventions()
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
