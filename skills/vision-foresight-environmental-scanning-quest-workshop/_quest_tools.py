#!/usr/bin/env python3
"""
QUEST Workshop Deterministic Tools
=====================================
결정론적 Python 함수로 할루시네이션 구조 차단.
LLM이 자연어로 재추론하지 못하도록 수치 계산·범위 검사·존재 검증을 전담.

Functions:
  cross_impact_rank        — Cross-impact 매트릭스 행·열 합산 → 순위
  validate_scenario_probs  — 시나리오 확률 합계 100% 검증
  validate_participants    — 참가자 수 범위 검사
  validate_workshop_time   — 세그먼트 합산 vs 기대 시간 검증
  validate_domain          — 트렌드 분류 도메인 존재 검증

Usage:
  python3 _quest_tools.py cross_impact --trends "T1,T2,T3" \\
      --scores '[{"from":0,"to":1,"score":2},{"from":1,"to":2,"score":-1}]'

  python3 _quest_tools.py validate_probs \\
      --probs '{"5y":[25,35,10,30],"10y":[35,40,5,20],"15y":[30,35,5,30]}'

  python3 _quest_tools.py validate_participants --count 13 --context general

  python3 _quest_tools.py validate_time \\
      --segments '[{"name":"Opening","minutes":30},{"name":"Mission","minutes":90}]' \\
      --expected 120

  python3 _quest_tools.py validate_domain --domain "Science and Technology"

Sources:
  Gordon & Glenn (2009) 9 domains — UNDP/African Futures NLTPS process
  Slaughter (1990) QUEST 4 phases — *Futures* journal
  Nanus (1982) QUEST original — USC Center for Futures Research
"""

import sys
import json
import argparse

# ──────────────────────────────────────────────────────────────────────────────
# 상수: Gordon & Glenn (2009) 9 Scanning Domains + Spirituality (박사님 추가)
# ──────────────────────────────────────────────────────────────────────────────
VALID_DOMAINS = [
    "Conflict and Governance",          # 갈등·거버넌스 (정치·지정학)
    "Science and Technology",           # 과학·기술
    "Agriculture and Food Security",    # 농업·식량 안보
    "Natural Resources and Environment",# 자연자원·환경
    "Energy",                           # 에너지
    "Population and Human Welfare",     # 인구·복지·교육
    "Communications and Transportation",# 통신·교통
    "Economics",                        # 경제 (지역·국제)
    "Social and Cultural Issues",       # 사회·문화
    "Spirituality",                     # 영성 (박사님 컨텍스트 추가 도메인)
]

# Cross-impact score 허용 범위
SCORE_MIN, SCORE_MAX = -3, 3

# 참가자 수 컨텍스트별 허용 범위
PARTICIPANT_RANGES = {
    "general":  (12, 15),
    "research": (12, 15),
    "church":   (12, 15),
    "finance":  (5, 7),
}


# ──────────────────────────────────────────────────────────────────────────────
# Function 1: Cross-impact 매트릭스 랭킹
# ──────────────────────────────────────────────────────────────────────────────
def cross_impact_rank(trends: list, scores: list) -> dict:
    """
    Cross-impact 매트릭스의 행합(영향력)·열합(피영향력)을 계산해 순위 반환.

    Args:
        trends : list[str]  — 트렌드 이름 목록 (n개)
        scores : list[dict] — [{"from": i, "to": j, "score": v}, ...] (v ∈ -3..+3)

    Returns:
        dict with keys:
          most_influential  — 행합 절대값 내림차순 (영향을 많이 주는 트렌드)
          most_affected     — 열합 절대값 내림차순 (영향을 많이 받는 트렌드)
          raw_matrix        — n×n 정수 매트릭스
          errors            — 범위 위반 목록
    """
    n = len(trends)
    matrix = [[0] * n for _ in range(n)]
    errors = []

    for item in scores:
        i, j, v = item["from"], item["to"], item["score"]
        if i == j:
            errors.append(f"자기 참조 금지: trends[{i}] → trends[{i}]")
            continue
        if not (SCORE_MIN <= v <= SCORE_MAX):
            errors.append(f"점수 범위 초과: ({i},{j}) = {v} (허용 {SCORE_MIN}~{SCORE_MAX})")
            continue
        matrix[i][j] = v

    # 행합: trend i 가 다른 모든 trend에 주는 순영향
    row_sums = [(trends[i], sum(matrix[i][j] for j in range(n) if j != i))
                for i in range(n)]
    # 열합: trend j 가 다른 모든 trend로부터 받는 순영향
    col_sums = [(trends[j], sum(matrix[i][j] for i in range(n) if i != j))
                for j in range(n)]

    most_influential = sorted(row_sums, key=lambda x: abs(x[1]), reverse=True)
    most_affected    = sorted(col_sums, key=lambda x: abs(x[1]), reverse=True)

    return {
        "most_influential": [{"trend": t, "net_influence": s} for t, s in most_influential],
        "most_affected":    [{"trend": t, "net_received":  s} for t, s in most_affected],
        "raw_matrix": matrix,
        "errors": errors,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Function 2: 시나리오 확률 합계 검증
# ──────────────────────────────────────────────────────────────────────────────
def validate_scenario_probs(probs: dict, tolerance: int = 2) -> dict:
    """
    시나리오 확률 목록이 horizon별로 100%에 수렴하는지 검증.

    Args:
        probs     : dict[str, list[float]] — {"5y": [25,35,10,30], ...}
        tolerance : 허용 오차 (기본 ±2%)

    Returns:
        dict with keys:
          horizons   — horizon별 {total, diff, passed, message}
          all_pass   — 모든 horizon PASS 여부
    """
    results = {}
    all_pass = True

    for horizon, prob_list in probs.items():
        total = sum(prob_list)
        diff  = abs(total - 100)
        passed = diff <= tolerance
        if not passed:
            all_pass = False
        results[horizon] = {
            "total":   total,
            "diff":    diff,
            "passed":  passed,
            "message": f"{'PASS' if passed else 'FAIL'}: {total}% (±{tolerance}% 허용, 오차 {diff}%)",
        }

    return {"horizons": results, "all_pass": all_pass}


# ──────────────────────────────────────────────────────────────────────────────
# Function 3: 참가자 수 범위 검사
# ──────────────────────────────────────────────────────────────────────────────
def validate_participants(count: int, context: str = "general") -> dict:
    """
    QUEST 스펙(Slaughter 1990)에 따른 참가자 수 범위 검사.

    Context 범위 (Nanus 원전 + 박사님 컨텍스트):
      general/research/church : 12~15명
      finance                 : 5~7명  (소규모 개인 투자 워크숍)

    Args:
        count   : 실제 참가자 수
        context : 워크숍 컨텍스트

    Returns:
        dict with keys: count, context, range, passed, message
    """
    lo, hi = PARTICIPANT_RANGES.get(context, (12, 15))
    passed  = lo <= count <= hi

    return {
        "count":   count,
        "context": context,
        "range":   f"{lo}~{hi}",
        "passed":  passed,
        "message": (
            f"PASS: {count}명 — '{context}' 기준 {lo}~{hi}명 범위 내"
            if passed else
            f"FAIL: {count}명 — '{context}' 기준 {lo}~{hi}명 범위 벗어남"
        ),
    }


# ──────────────────────────────────────────────────────────────────────────────
# Function 4: 워크숍 시간 세그먼트 검증
# ──────────────────────────────────────────────────────────────────────────────
def validate_workshop_time(segments: list, expected_minutes: int) -> dict:
    """
    워크숍 세그먼트 합산이 기대 총시간과 일치하는지 검증.

    Args:
        segments        : list[dict] — [{"name": "Opening", "minutes": 30}, ...]
        expected_minutes: 기대 총시간 (분)

    Returns:
        dict with keys: segment_detail, total_minutes, expected_minutes, diff, passed, message
    """
    total = sum(s["minutes"] for s in segments)
    diff  = abs(total - expected_minutes)
    passed = diff == 0

    segment_detail = [
        {"name": s["name"], "minutes": s["minutes"]} for s in segments
    ]

    return {
        "segment_detail":   segment_detail,
        "total_minutes":    total,
        "expected_minutes": expected_minutes,
        "diff":             diff,
        "passed":           passed,
        "message": (
            f"PASS: {total}분 ({total // 60}시간 {total % 60}분) — 기대 {expected_minutes}분 일치"
            if passed else
            f"FAIL: {total}분 vs 기대 {expected_minutes}분 ({diff}분 차이)"
        ),
    }


# ──────────────────────────────────────────────────────────────────────────────
# Function 5: 도메인 이름 존재 검증
# ──────────────────────────────────────────────────────────────────────────────
def validate_domain(domain: str) -> dict:
    """
    트렌드 분류 도메인이 Gordon & Glenn (2009) 10개 도메인 목록에 있는지 검증.
    LLM이 임의 도메인명을 생성하는 할루시네이션 차단.

    Args:
        domain : 분류할 도메인 이름 (대소문자 민감)

    Returns:
        dict with keys: domain, passed, valid_domains, message
    """
    passed = domain in VALID_DOMAINS

    return {
        "domain":       domain,
        "passed":       passed,
        "valid_domains": VALID_DOMAINS,
        "message": (
            f"PASS: '{domain}' — 유효한 도메인"
            if passed else
            f"FAIL: '{domain}' — 목록에 없음. 유효 도메인: {VALID_DOMAINS}"
        ),
    }


# ──────────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="QUEST Workshop Deterministic Tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd")

    # cross_impact
    p1 = sub.add_parser("cross_impact", help="Cross-impact 매트릭스 랭킹")
    p1.add_argument("--trends", required=True,
                    help="쉼표 구분 트렌드 이름 (예: T1,T2,T3)")
    p1.add_argument("--scores", required=True,
                    help='JSON 배열 [{"from":0,"to":1,"score":2}, ...]')

    # validate_probs
    p2 = sub.add_parser("validate_probs", help="시나리오 확률 합계 검증")
    p2.add_argument("--probs", required=True,
                    help='JSON {"5y":[25,35,10,30],"10y":[35,40,5,20],"15y":[30,35,5,30]}')
    p2.add_argument("--tolerance", type=int, default=2, help="허용 오차 퍼센트 (기본 2)")

    # validate_participants
    p3 = sub.add_parser("validate_participants", help="참가자 수 범위 검사")
    p3.add_argument("--count", type=int, required=True, help="참가자 수")
    p3.add_argument("--context", default="general",
                    choices=list(PARTICIPANT_RANGES.keys()),
                    help="워크숍 컨텍스트")

    # validate_time
    p4 = sub.add_parser("validate_time", help="워크숍 시간 세그먼트 검증")
    p4.add_argument("--segments", required=True,
                    help='JSON [{"name":"Opening","minutes":30}, ...]')
    p4.add_argument("--expected", type=int, required=True, help="기대 총시간 (분)")

    # validate_domain
    p5 = sub.add_parser("validate_domain", help="도메인 이름 존재 검증")
    p5.add_argument("--domain", required=True, help="검증할 도메인 이름")

    args = parser.parse_args()

    if args.cmd == "cross_impact":
        trends = [t.strip() for t in args.trends.split(",")]
        scores = json.loads(args.scores)
        result = cross_impact_rank(trends, scores)

    elif args.cmd == "validate_probs":
        probs  = json.loads(args.probs)
        result = validate_scenario_probs(probs, args.tolerance)

    elif args.cmd == "validate_participants":
        result = validate_participants(args.count, args.context)

    elif args.cmd == "validate_time":
        segments = json.loads(args.segments)
        result   = validate_workshop_time(segments, args.expected)

    elif args.cmd == "validate_domain":
        result = validate_domain(args.domain)

    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
