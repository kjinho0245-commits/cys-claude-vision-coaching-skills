#!/bin/bash
# vision-grill-with-docs — 최종 검증 라운드.
# grill_lib_test.py 단위 테스트와 *완전히 다른* 입력으로 결정론 라이브러리 작동 확인.
# 다목적 인터뷰 엔진의 핵심 경로(3-모드 분기·주제 파싱·박사님 사전·LDR·3영역·시나리오·인용·VISION-CONTEXT)를 종단 검증.

set -e
cd "$(dirname "$0")"
PYTHON="python3 grill_lib.py"
PASS=0
FAIL=0
TOTAL=0
TMP_BASE=$(mktemp -d)
trap "rm -rf $TMP_BASE" EXIT

run_test() {
    local label="$1"
    local cmd="$2"
    local expected_substring="$3"
    TOTAL=$((TOTAL+1))
    out=$(eval "$cmd" 2>&1)
    if echo "$out" | grep -q "$expected_substring"; then
        PASS=$((PASS+1))
        echo "PASS [$label]"
    else
        FAIL=$((FAIL+1))
        echo "FAIL [$label]"
        echo "  Expected substring: $expected_substring"
        echo "  Actual: $out"
    fi
}

echo "=== vision-grill-with-docs 최종 검증 라운드 (다목적 인터뷰 시뮬레이션) ==="
echo

# ---------------------------------------------------------------------------
# 1. 모드 분기 — 박사님 직접 호출 시나리오
# ---------------------------------------------------------------------------

run_test "M1 Mode B — verify 5-stages" \
    "$PYTHON route_mode --text 'verify five-stages'" \
    '"mode": "B"'

run_test "M2 Mode A — coachee 청년" \
    "$PYTHON route_mode --text 'coachee:청년부 김민수'" \
    '"mode": "A"'

run_test "M3 Mode C — 박사님 예시 (진로·전공·학교)" \
    "$PYTHON route_mode --text '나의 역량·실력·미래 비전 가능성을 종합해서 진로 결정을 했으면 한다. 전공, 학교에 관한 코칭'" \
    '"mode": "C"'

run_test "M4 Mode C — 막혔다 시나리오" \
    "$PYTHON route_mode --text '비전이 막혀있다. 생각 정리부터'" \
    '"mode": "C"'

run_test "M5 Mode menu — 빈 호출" \
    "$PYTHON route_mode --text ''" \
    '"mode": "menu"'

# ---------------------------------------------------------------------------
# 2. 주제 파싱 — 다양한 사용자 입력
# ---------------------------------------------------------------------------

run_test "T1 진로·전공·학교 종합" \
    "$PYTHON parse_topic --text '나의 역량·실력·미래 비전 가능성을 종합해서 진로 결정. 전공·학교 코칭'" \
    'vision-career-recommendation'

run_test "T2 재정 — 집·창업·자녀유학" \
    "$PYTHON parse_topic --text '집을 살까 말까 + 자녀 유학비 + 창업 자본'" \
    'vision-financial-3shields-3windows'

run_test "T3 사역 — 선교사 헌신" \
    "$PYTHON parse_topic --text '선교지로 갈까 말까 — 단기 vs 장기'" \
    'sermon-augustine-coaching'

run_test "T4 관계 — 결혼·자녀·부모" \
    "$PYTHON parse_topic --text '결혼 결정 + 자녀 출산 시점 + 부모 부양'" \
    'vision-three-realm-balance'

run_test "T5 미래 시뮬레이션 — 5년·10년" \
    "$PYTHON parse_topic --text '5년 후·10년 후 미래 모습 시뮬레이션'" \
    'vision-futures-timeline-map'

run_test "T6 메타 비전 — 막혔다" \
    "$PYTHON parse_topic --text '비전이 막혀있다. 어디서부터 시작할지 모르겠다'" \
    'vision-clarity-coaching'

run_test "T7 매칭 없음 (방어)" \
    "$PYTHON parse_topic --text '아무 의미 없는 외계 단어 zzz qqq'" \
    '"related_skills": \[\]'

# ---------------------------------------------------------------------------
# 3. 박사님 표준 사전 충돌 검출
# ---------------------------------------------------------------------------

run_test "G1 꿈 → 비전 통일 권고" \
    "$PYTHON detect_glossary_conflict --text '내 꿈은 큰 회사 사장이 되는 것'" \
    '"user_term": "꿈"'

run_test "G2 야망 → 비전 통일 권고" \
    "$PYTHON detect_glossary_conflict --text '내 야망은 한국 최고가 되는 것'" \
    '"user_term": "야망"'

run_test "G3 트렌드 → 시대 통일 권고" \
    "$PYTHON detect_glossary_conflict --text '요즘 트렌드를 따라야 한다'" \
    '"user_term": "트렌드"'

run_test "G4 개인정의-소명 분기 검출" \
    "$PYTHON detect_glossary_conflict --text '저의 소명은 돈을 많이 버는 것입니다.'" \
    'personal_definition_diverges'

run_test "G5 박사님 표준 정의 사용 → clean" \
    "$PYTHON detect_glossary_conflict --text '나의 비전은 가치 있는 시대적 소명이다'" \
    '"clean": true'

# ---------------------------------------------------------------------------
# 4. 박사님 표준 사전 lookup
# ---------------------------------------------------------------------------

run_test "L1 비전 정의" \
    "$PYTHON glossary_lookup --term '비전'" \
    '"가치 있는 시대적 소명"'

run_test "L2 영감 정의" \
    "$PYTHON glossary_lookup --term '영감'" \
    '"외부로부터 주어지는 영감"'

run_test "L3 왜곡된 사명 정의" \
    "$PYTHON glossary_lookup --term '왜곡된 사명'" \
    '"found": true'

run_test "L4 외계어 not found" \
    "$PYTHON glossary_lookup --term 'unknown_term_xyz'" \
    '"found": false'

# ---------------------------------------------------------------------------
# 5. LDR 3조건 자동 체크
# ---------------------------------------------------------------------------

run_test "D1 진로 전환 — 3조건 충족 → LDR 발행" \
    "$PYTHON check_ldr_criteria --decision '대기업에서 신학교로' --reversibility hard --surprising true --tradeoff true" \
    '"qualifies": true'

run_test "D2 점심 메뉴 — 모두 미충족 → 미발행" \
    "$PYTHON check_ldr_criteria --decision '오늘 점심 한식' --reversibility easy --surprising false --tradeoff false" \
    '"qualifies": false'

run_test "D3 surprising 누락 → 미발행" \
    "$PYTHON check_ldr_criteria --decision '자취 시작' --reversibility hard --surprising false --tradeoff true" \
    '"qualifies": false'

run_test "D4 tradeoff 누락 → 미발행" \
    "$PYTHON check_ldr_criteria --decision '관성으로 한 결정' --reversibility hard --surprising true --tradeoff false" \
    '"qualifies": false'

run_test "D5 선교 헌신 3조건 모두 충족" \
    "$PYTHON check_ldr_criteria --decision '장기 선교사 헌신' --reversibility hard --surprising true --tradeoff true" \
    '"qualifies": true'

# ---------------------------------------------------------------------------
# 6. 3영역 균형 검사 (vision-three-realm 1:1)
# ---------------------------------------------------------------------------

run_test "R1 건강 — 3영역 모두" \
    "$PYTHON three_realm_check --self true --others true --moral true" \
    '"status": "healthy"'

run_test "R2 왜곡된 사명 (정신적 가치만)" \
    "$PYTHON three_realm_check --self false --others false --moral true" \
    '왜곡된 사명'

run_test "R3 개인 욕망 (나만)" \
    "$PYTHON three_realm_check --self true --others false --moral false" \
    '개인 욕망'

run_test "R4 자기희생 (가족과 세상만)" \
    "$PYTHON three_realm_check --self false --others true --moral false" \
    '자기희생'

run_test "R5 empty (다 비어 있음)" \
    "$PYTHON three_realm_check --self false --others false --moral false" \
    '"status": "empty"'

# ---------------------------------------------------------------------------
# 7. 시나리오 4종 강제 확장
# ---------------------------------------------------------------------------

run_test "S1 5년 시나리오" \
    "$PYTHON scenario_expand --topic '신학교 전과'" \
    '5년 후 시나리오'

run_test "S2 실패 시나리오" \
    "$PYTHON scenario_expand --topic '신학교 전과'" \
    '실패 시나리오'

run_test "S3 기회비용 시나리오" \
    "$PYTHON scenario_expand --topic '신학교 전과'" \
    '기회비용 시나리오'

# ---------------------------------------------------------------------------
# 8. 박사님 인용 검증 (할루시네이션 차단)
# ---------------------------------------------------------------------------

run_test "Q1 허용 — 외부 영감" \
    "$PYTHON verify_quote --text '외부로부터 주어지는 영감'" \
    '"match": true'

run_test "Q2 허용 — 비전 정의" \
    "$PYTHON verify_quote --text '가치 있는 시대적 소명'" \
    '"match": true'

run_test "Q3 비허용 — 가짜 박사님 인용" \
    "$PYTHON verify_quote --text '박사님께서 비전은 그냥 꿈이라고 하셨다'" \
    '"match": false'

run_test "Q4 비허용 — 학자 인용 위조" \
    "$PYTHON verify_quote --text 'Gardner는 비전이 10가지 지능이라 했다'" \
    '"match": false'

# ---------------------------------------------------------------------------
# 9. 관련 산출물 후보 식별
# ---------------------------------------------------------------------------

run_test "A1 재정 결정 → 재정 스킬 후보" \
    "$PYTHON find_related_artifact --topic '집을 살까 말까 + 대출 부담'" \
    'vision-financial-coach'

run_test "A2 사역 결단 → sermon 시리즈 후보" \
    "$PYTHON find_related_artifact --topic '선교사 장기 헌신'" \
    'sermon-augustine-coaching'

# ---------------------------------------------------------------------------
# 10. 작업 폴더 구조 감지·LDR 번호·VISION-CONTEXT lazy 생성
# ---------------------------------------------------------------------------

run_test "F1 빈 폴더 → structure none" \
    "$PYTHON is_multi_context --base $TMP_BASE" \
    '"structure": "none"'

# 첫 용어 upsert로 VISION-CONTEXT.md lazy 생성
run_test "F2 upsert_term lazy 생성 ok" \
    "$PYTHON upsert_term --base $TMP_BASE --term '중간 비전' --definition '5년 단위 마일스톤' --section 3 --owner 박사님" \
    '"created": true'

run_test "F3 lazy 생성 후 → structure single" \
    "$PYTHON is_multi_context --base $TMP_BASE" \
    '"structure": "single"'

# 두 번째 upsert — 이미 있는 파일에 추가
run_test "F4 두 번째 upsert 추가 (not created)" \
    "$PYTHON upsert_term --base $TMP_BASE --term '본인 소명' --definition '시대적 부르심에 응답한 일터 헌신' --section 2 --owner 박사님" \
    '"created": false'

# LDR 번호 — 폴더 없음 → 0001
run_test "F5 LDR 폴더 없음 → 0001" \
    "$PYTHON next_ldr_number --base $TMP_BASE" \
    '"next": "0001"'

# LDR 폴더 + 더미 파일 → 0002
mkdir -p "$TMP_BASE/docs/ldr"
cat > "$TMP_BASE/docs/ldr/0001-stub.md" <<'EOF'
# stub
EOF
run_test "F6 LDR 0001 존재 → 0002" \
    "$PYTHON next_ldr_number --base $TMP_BASE" \
    '"next": "0002"'

# 멀티 컨텍스트 — VISION-CONTEXT-MAP.md 생성
cat > "$TMP_BASE/VISION-CONTEXT-MAP.md" <<'EOF'
# Context Map
EOF
run_test "F7 multi 감지" \
    "$PYTHON is_multi_context --base $TMP_BASE" \
    '"structure": "multi"'

# ---------------------------------------------------------------------------
# 11. 단위 테스트 통합 실행 — 본 검증 라운드의 마무리
# ---------------------------------------------------------------------------

echo
echo "--- 단위 테스트 (grill_lib_test.py) 실행 ---"
if python3 grill_lib_test.py | tail -3 | grep -q "ALL PASS"; then
    PASS=$((PASS+1))
    TOTAL=$((TOTAL+1))
    echo "PASS [Unit tests — grill_lib_test.py ALL PASS]"
else
    FAIL=$((FAIL+1))
    TOTAL=$((TOTAL+1))
    echo "FAIL [Unit tests — grill_lib_test.py]"
fi

# ---------------------------------------------------------------------------
# 결과
# ---------------------------------------------------------------------------

echo
echo "=== 결과: $PASS/$TOTAL PASS ==="
if [ "$FAIL" -eq 0 ]; then
    echo "ALL PASS — vision-grill-with-docs 결정론 모듈 정상 작동"
    exit 0
else
    echo "FAIL: $FAIL"
    exit 1
fi
