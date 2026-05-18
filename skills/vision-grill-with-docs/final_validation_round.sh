#!/bin/bash
# vision-grill-with-docs — 최종 신규 10개 검증 시나리오.
# 이전 verification_round.sh·grill_lib_test.py와 *전혀 다른* 입력·시나리오로 구성.
# 박사님 /goal 명령: "검증용 10개의 작업 명령 프롬프트를 입력을 이전 검증 때와 전혀 다른 것으로".

set -e
cd "$(dirname "$0")"
PY="python3 grill_lib.py"
PASS=0
FAIL=0
TOTAL=0
TMP=$(mktemp -d)
trap "rm -rf $TMP" EXIT

check() {
    local label="$1"
    local cmd="$2"
    local expect_sub="$3"
    TOTAL=$((TOTAL+1))
    out=$(eval "$cmd" 2>&1)
    if echo "$out" | grep -q "$expect_sub"; then
        PASS=$((PASS+1))
        echo "PASS [$label]"
    else
        FAIL=$((FAIL+1))
        echo "FAIL [$label]"
        echo "  expect: $expect_sub"
        echo "  actual: $out" | head -3
    fi
}

echo "=== 최종 신규 10개 검증 시나리오 (이전 검증과 100% 다른 입력) ==="
echo

# ---------------------------------------------------------------------------
# 시나리오 1 — 박사님 본인의 시대적 소명 검증 (Mode C)
# 입력: 박사님 미래학자 본업과 집필 사역 통합 — 두 부르심 사이 grill
# ---------------------------------------------------------------------------
echo "[Scenario 1] 박사님 본인 — 미래학자·집필 두 부르심 통합 grill"

# 1.1 모드 분기 (자유 주제니 Mode C)
check "1.1 자유 주제 → Mode C" \
    "$PY route_mode --text '나는 미래학자로서 집필과 강의 두 사역을 어떻게 통합할 것인지 grill해달라'" \
    '"mode": "C"'

# 1.2 박사님 표준 사전 정의 lookup — "비전 프레임"
check "1.2 비전 프레임 lookup" \
    "$PY glossary_lookup --term '비전 프레임'" \
    '두 축이 (R) 강화 피드백 루프'

# 1.3 사용자가 박사님 정의를 정확히 인용 → clean
check "1.3 박사님 정의 정확 인용 clean" \
    "$PY detect_glossary_conflict --text '내 비전은 이 시대 한국 교회를 향한 가치 있는 시대적 소명이다'" \
    '"clean": true'

# ---------------------------------------------------------------------------
# 시나리오 2 — 청년부 김도현 학생 진로 코칭 (Mode A, 코치이 인터뷰)
# ---------------------------------------------------------------------------
echo
echo "[Scenario 2] 청년부 김도현 코치이 — 진로 grill"

# 2.1 Mode A 분기 (coachee:)
check "2.1 coachee → Mode A" \
    "$PY route_mode --text 'coachee:김도현 청년부 진로 grill'" \
    '"mode": "A"'

# 2.2 모호한 표현 — "꿈" 발화 → 박사님 표준 비전 통일 권고
check "2.2 꿈 발화 → 비전 통일 권고" \
    "$PY detect_glossary_conflict --text '김도현 학생의 꿈은 의사가 되어 가난한 사람을 돕는 것이다'" \
    '"standard_term": "비전"'

# ---------------------------------------------------------------------------
# 시나리오 3 — vision-five-stages 산출물 메타 검증 (Mode B)
# ---------------------------------------------------------------------------
echo
echo "[Scenario 3] vision-five-stages 산출물 메타 검증 — Mode B"

check "3.1 verify five-stages → Mode B" \
    "$PY route_mode --text 'verify vision-five-stages'" \
    '"mode": "B"'

# ---------------------------------------------------------------------------
# 시나리오 4 — 다목적 인터뷰: 50대 시니어 이모작 결단
# ---------------------------------------------------------------------------
echo
echo "[Scenario 4] 50대 시니어 — 이모작 진로 결단 (LDR 자격)"

# 4.1 주제 파싱 — 은퇴·이모작
check "4.1 이모작 키워드 매칭" \
    "$PY parse_topic --text '50대 후반 은퇴 직전 이모작 시니어 사역 결단'" \
    '이모작'

# 4.2 vision-five-stages 매핑
check "4.2 이모작 → vision-five-stages 매핑" \
    "$PY parse_topic --text '은퇴 후 이모작 사역 결단'" \
    'vision-five-stages'

# 4.3 LDR 3조건 — 사역 헌신은 자격 충족
check "4.3 사역 헌신 LDR 자격" \
    "$PY check_ldr_criteria --decision '60세 은퇴 후 시니어 사역 전임 헌신' --reversibility hard --surprising true --tradeoff true" \
    '"qualifies": true'

# ---------------------------------------------------------------------------
# 시나리오 5 — 결혼 결단 → 3영역 균형 검사
# ---------------------------------------------------------------------------
echo
echo "[Scenario 5] 결혼 결단 — 3영역 균형 검사"

# 5.1 결혼 키워드 → three-realm-balance
check "5.1 결혼 → three-realm-balance" \
    "$PY parse_topic --text '내년 봄 결혼 결단 깊이 grill'" \
    'vision-three-realm-balance'

# 5.2 3영역 — 본인 행복 + 가족 기쁨 모두 있는데 정신적 가치 측면 미정
check "5.2 정신적 가치 결핍 진단" \
    "$PY three_realm_check --self true --others true --moral false" \
    '정신적 가치'

# 5.3 LDR 결혼 결정 발행 자격
check "5.3 결혼 LDR 자격" \
    "$PY check_ldr_criteria --decision '2027년 봄 결혼' --reversibility hard --surprising false --tradeoff true" \
    '"qualifies": false'

# ---------------------------------------------------------------------------
# 시나리오 6 — 박사님 인용 위조 차단 (할루시네이션)
# ---------------------------------------------------------------------------
echo
echo "[Scenario 6] 박사님 인용 위조 차단 — 다양한 위조 패턴"

# 6.1 박사님이 한 적 없는 발언 차단
check "6.1 가짜 박사님 발언 차단" \
    "$PY verify_quote --text '박사님께서 비전이란 결국 자기 행복이라고 하셨다'" \
    '"match": false'

# 6.2 부분 인용 wrapper 위조 차단
check "6.2 wrapper 위조 차단" \
    "$PY verify_quote --text '사실 박사님께서 외부로부터 주어지는 영감이라는 표현을 쓰셨지만 의미는 그게 아니다'" \
    '"match": false'

# 6.3 정확 인용 통과
check "6.3 정확 인용 PASS" \
    "$PY verify_quote --text '비전 프레임이란 \"가치 있는 + 시대적 + 소명\"이 어떻게 성장하는지를 설명하기 위해 필자가 만든 단어이다'" \
    '"match": true'

# ---------------------------------------------------------------------------
# 시나리오 7 — VISION-CONTEXT.md lazy 생성 + idempotent
# ---------------------------------------------------------------------------
echo
echo "[Scenario 7] VISION-CONTEXT.md lazy 생성 + idempotent + § 6 충돌 기록"

# 7.1 첫 용어 upsert — 파일 생성됨
check "7.1 첫 upsert lazy 생성" \
    "$PY upsert_term --base $TMP --term '본인 시대' --definition '지금 한국 사회 — 디지털 전환 + 고령화 + 청년 실업' --section 2 --owner 박사님" \
    '"created": true'

# 7.2 같은 term 재upsert — replaced
check "7.2 같은 term idempotent" \
    "$PY upsert_term --base $TMP --term '본인 시대' --definition '지금 한국 사회 — 인공지능 시대 + 4차 산업혁명' --section 2" \
    '"replaced": true'

# 7.3 § 6 충돌 기록
check "7.3 충돌 기록 추가" \
    "$PY flag_conflict --base $TMP --term '가치' --user-usage '돈 많이 버는 것' --resolution '박사님 표준 정의 채택 — 영감이 정신적 가치로 검증된 것'" \
    '"ok": true'

# 7.4 결과 파일에 모든 변경 반영
grep_test() {
    if grep -q "$2" "$1"; then
        PASS=$((PASS+1))
        TOTAL=$((TOTAL+1))
        echo "PASS [$3]"
    else
        FAIL=$((FAIL+1))
        TOTAL=$((TOTAL+1))
        echo "FAIL [$3]"
    fi
}
grep_test "$TMP/VISION-CONTEXT.md" "인공지능 시대" "7.4 idempotent 갱신 반영"
grep_test "$TMP/VISION-CONTEXT.md" "충돌 기록" "7.5 § 6 헤더 존재"

# ---------------------------------------------------------------------------
# 시나리오 8 — 멀티 컨텍스트 전환 (단일 → 멀티)
# ---------------------------------------------------------------------------
echo
echo "[Scenario 8] 단일 → 멀티 컨텍스트 전환"

# 7번 시나리오의 TMP를 그대로 사용 → 단일 VISION-CONTEXT.md 존재
# 8.1 진로 영역으로 promote
check "8.1 promote_to_multi 진로" \
    "$PY promote_to_multi --base $TMP --area 진로" \
    '"moved_single_to_area": true'

# 8.2 구조 multi 감지
check "8.2 multi 감지" \
    "$PY is_multi_context --base $TMP" \
    '"structure": "multi"'

# 8.3 list_contexts에 진로 영역 등록
check "8.3 진로 영역 등록 확인" \
    "$PY list_contexts --base $TMP" \
    '"name": "진로"'

# 8.4 재정 영역 추가
check "8.4 재정 영역 추가 ok" \
    "$PY promote_to_multi --base $TMP --area 재정" \
    '"ok": true'

# ---------------------------------------------------------------------------
# 시나리오 9 — 슬러그 정규화 + LDR 번호 부여 통합
# ---------------------------------------------------------------------------
echo
echo "[Scenario 9] LDR 발행 통합 — 슬러그 + 번호"

LDR_TMP=$(mktemp -d)
trap "rm -rf $TMP $LDR_TMP" EXIT

# 9.1 첫 LDR 번호
check "9.1 빈 폴더 LDR 번호" \
    "$PY next_ldr_number --base $LDR_TMP" \
    '"next": "0001"'

# 9.2 슬러그 정규화 — 박사님식 한글 제목
check "9.2 슬러그 — 한글 결정 제목" \
    "$PY slug_normalize --title '재정 — 강남 아파트 매도 + 지방 이주 결단 (2026 가을)'" \
    '"ok": true'

# 9.3 한글+숫자 정확히 보존
check "9.3 슬러그 숫자 보존" \
    "$PY slug_normalize --title '진로 — 2030년 신학 박사 진학 결단'" \
    '2030년'

# 9.4 LDR 파일 시뮬레이션 후 번호 증가
mkdir -p "$LDR_TMP/docs/ldr"
echo "# stub" > "$LDR_TMP/docs/ldr/0001-foo.md"
echo "# stub" > "$LDR_TMP/docs/ldr/0023-bar.md"
check "9.4 LDR 0023 → 0024" \
    "$PY next_ldr_number --base $LDR_TMP" \
    '"next": "0024"'

# ---------------------------------------------------------------------------
# 시나리오 10 — SYNC 검증 통합 (drift 자동 차단)
# ---------------------------------------------------------------------------
echo
echo "[Scenario 10] SYNC 검증 — 사양 ↔ 코드 drift 자동 차단"

# 10.1 glossary sync
check "10.1 glossary sync ok" \
    "$PY validate_glossary_sync" \
    '"ok": true'

# 10.2 quotes sync
check "10.2 quotes sync ok" \
    "$PY validate_quotes_sync" \
    '"ok": true'

# 10.3 topic_map sync (vision-*)
check "10.3 topic_map vision-* sync ok" \
    "$PY validate_topic_map_skills" \
    '"missing_vision_skills": \[\]'

# 10.4 단위 테스트 통합 실행
echo
echo "--- 단위 테스트 통합 실행 ---"
unit_out=$(python3 grill_lib_test.py 2>&1 | tail -3)
if echo "$unit_out" | grep -q "ALL PASS"; then
    PASS=$((PASS+1))
    TOTAL=$((TOTAL+1))
    echo "PASS [10.4 124개 단위 테스트 ALL PASS]"
else
    FAIL=$((FAIL+1))
    TOTAL=$((TOTAL+1))
    echo "FAIL [10.4 단위 테스트]"
    echo "$unit_out"
fi

# 10.5 verification_round.sh (기존 검증 라운드) 통합 실행
echo
echo "--- 기존 verification_round.sh 통합 ---"
prev_out=$(bash verification_round.sh 2>&1 | tail -3)
if echo "$prev_out" | grep -q "ALL PASS"; then
    PASS=$((PASS+1))
    TOTAL=$((TOTAL+1))
    echo "PASS [10.5 기존 검증 라운드 ALL PASS]"
else
    FAIL=$((FAIL+1))
    TOTAL=$((TOTAL+1))
    echo "FAIL [10.5 기존 검증]"
    echo "$prev_out"
fi

# ---------------------------------------------------------------------------
# 결과
# ---------------------------------------------------------------------------
echo
echo "============================================================"
echo "최종 신규 검증 결과: $PASS/$TOTAL PASS"
echo "============================================================"
if [ "$FAIL" -eq 0 ]; then
    echo "ALL PASS — vision-grill-with-docs 100% 검증 완료"
    exit 0
else
    echo "FAIL: $FAIL — 추가 보강 필요"
    exit 1
fi
