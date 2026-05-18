#!/usr/bin/env python3
"""
cone_permutation.py — Taylor Cone of Plausibility Step 8 결정론적 헬퍼

Taylor 1993 verbatim:
  "Through a process of permutation and sorting of the eight statements,
   the order of the four final statements is established at random."

8개 statements (4 positive + 4 opposing) → 4개 random 선택 (random 순서).
이 단계는 LLM 추론이 아닌 Python 결정론 함수로 처리한다.

Usage (stdin JSON):
  echo '[
    "Tech A+1", "Tech A+2", "Tech A+3", "Tech A+4",
    "Tech A-1", "Tech A-2", "Tech A-3", "Tech A-4"
  ]' | python3 cone_permutation.py

Usage (--statements pipe-separated):
  python3 cone_permutation.py --statements "S1|S2|S3|S4|S5|S6|S7|S8"

Options:
  --seed INT   재현 가능한 seed (생략 시 진짜 random)
  --scenario   시나리오 이름 (출력 헤더용, 선택)
"""

import json
import random
import sys
import argparse


def permute_and_select(statements: list, seed=None) -> list:
    """
    Taylor 1993 Step 8: 8개 statements에서 4개를 random 선택 + random 순서.

    Args:
        statements: 정확히 8개의 문장 리스트
        seed: 재현 seed (None = 진짜 random)

    Returns:
        4개 문장 리스트 (random 선택 + random 순서)

    Raises:
        ValueError: statements가 8개가 아닐 때
    """
    if len(statements) != 8:
        raise ValueError(
            f"Taylor verbatim: '4 positive + 4 opposing = 8 statements' 필요. "
            f"입력: {len(statements)}개"
        )

    rng = random.Random(seed)
    selected = rng.sample(statements, 4)
    return selected


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Taylor Cone of Plausibility Step 8: "
            "8 statements → 4 random selected (micro-scenario)"
        )
    )
    parser.add_argument(
        "--seed", type=int, default=None,
        help="Random seed (재현 가능한 결과; 생략 시 매번 달라짐)"
    )
    parser.add_argument(
        "--statements", type=str, default=None,
        help="| 구분자로 연결한 8개 statements"
    )
    parser.add_argument(
        "--scenario", type=str, default="",
        help="시나리오 이름 (출력 레이블용)"
    )
    args = parser.parse_args()

    if args.statements:
        statements = [s.strip() for s in args.statements.split("|")]
    else:
        raw = sys.stdin.read().strip()
        if not raw:
            print("오류: stdin이 비어 있습니다. JSON 배열을 파이프하거나 --statements를 사용하세요.", file=sys.stderr)
            sys.exit(1)
        statements = json.loads(raw)

    selected = permute_and_select(statements, seed=args.seed)

    result = {
        "scenario": args.scenario,
        "seed_used": args.seed,
        "input_count": len(statements),
        "selected_micro_scenario": selected
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
