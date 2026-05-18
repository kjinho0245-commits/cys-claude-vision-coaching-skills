#!/bin/bash
# vision-grill-with-docs — Pass 5 신규 10개 검증 시나리오 (v2).
# 이전 final_validation_round.sh (Pass 4)의 33 sub-check와 *100% 다른* 입력·주제·시나리오.
# 박사님 /goal 재발동: "이전 검증 때와 전혀 다른 것으로".

set -e
cd "$(dirname "$0")"
PY="python3 grill_lib.py"
PASS=0
FAIL=0
TOTAL=0
TMP_A=$(mktemp -d)
TMP_B=$(mktemp -d)
TMP_C=$(mktemp -d)
trap "rm -rf $TMP_A $TMP_B $TMP_C" EXIT

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
        echo "  actual: $(echo "$out" | head -2)"
    fi
}

echo "=== Pass 5 신규 10개 검증 시나리오 (v2) ==="
echo "이전 final_validation_round.sh와 100% 다른 입력 — 박사님 미래학자 본업·재정 박사님 본인·이단 분별·해외 이주 등"
echo

# ---------------------------------------------------------------------------
# 시나리오 V-1 — 호칭 결정 (다양한 사용자 유형)
# ---------------------------------------------------------------------------
echo "[Scenario V-1] 호칭 결정 — 5가지 사용자 유형"

check "V1-1 박사님 본인" \
    "$PY select_honorific --meta-json '{\"is_doctor\":true}'" \
    '"honorific": "박사님"'

check "V1-2 강 목사님" \
    "$PY select_honorific --meta-json '{\"title\":\"목사\"}'" \
    '"honorific": "목사님"'

check "V1-3 정 장로님 (이미 님 포함)" \
    "$PY select_honorific --meta-json '{\"title\":\"장로님\"}'" \
    '"honorific": "장로님"'

check "V1-4 이름만 — 김도현님" \
    "$PY select_honorific --meta-json '{\"name\":\"김도현\"}'" \
    '"honorific": "김도현님"'

check "V1-5 빈 meta → 선생님" \
    "$PY select_honorific --meta-json '{}'" \
    '"honorific": "선생님"'

# ---------------------------------------------------------------------------
# 시나리오 V-2 — 영문 lookup (해외 청년 사용자 시나리오)
# ---------------------------------------------------------------------------
echo
echo "[Scenario V-2] 영문 용어 lookup — 해외 사용자 / 신학교 영어권 교재"

check "V2-1 Vision lookup" \
    "$PY glossary_lookup --term 'Vision'" \
    '"english_alias"'

check "V2-2 Spiritual Intuition lookup" \
    "$PY glossary_lookup --term 'Spiritual Intuition'" \
    '영감 + 정신적 가치'

check "V2-3 Reinforcing Feedback Loop" \
    "$PY glossary_lookup --term 'Reinforcing Feedback Loop'" \
    '강화 피드백 루프'

check "V2-4 대소문자 무시 — vision" \
    "$PY glossary_lookup --term 'vision'" \
    '"found": true'

# ---------------------------------------------------------------------------
# 시나리오 V-3 — VISION-CONTEXT.md § 1 시드 + 무결성 검증 통합
# ---------------------------------------------------------------------------
echo
echo "[Scenario V-3] § 1 박사님 표준 사전 시드 + 무결성"

check "V3-1 첫 시드 ok" \
    "$PY seed_standard_glossary --base $TMP_A --owner 박사님" \
    '"seeded": true'

check "V3-2 idempotent 두 번째 시드" \
    "$PY seed_standard_glossary --base $TMP_A --owner 박사님" \
    '"seeded": false'

check "V3-3 시드 후 무결성 검증 PASS" \
    "$PY validate_context_integrity --base $TMP_A" \
    '"ok": true'

# 시드된 파일 내용 확인
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
grep_test "$TMP_A/VISION-CONTEXT.md" "가치 있는 시대적 소명" "V3-4 시드 본문에 비전 정의 존재"
grep_test "$TMP_A/VISION-CONTEXT.md" "왜곡된 사명" "V3-5 시드 본문에 왜곡된 사명 존재"

# ---------------------------------------------------------------------------
# 시나리오 V-4 — 박사님 미래학자 본업 LDR 본문 자동 생성
# ---------------------------------------------------------------------------
echo
echo "[Scenario V-4] LDR 본문 자동 생성 — 박사님 미래학자 본업 / 해외 이주"

check "V4-1 박사님 본업 헌신 LDR" \
    "$PY render_ldr_body --title '미래학자 본업 5년 집중' --date 2026-06-01 --area '비전 영역 전환' --reason '시대적 부르심에 대한 응답이 강의·집필 영역에서 가장 분명함'" \
    '"is_known_area": true'

check "V4-2 해외 이주 LDR (선택 섹션 포함)" \
    "$PY render_ldr_body --title '한국→북미 이주' --date 2028-03-15 --area 관계 --reason '자녀 교육·다음 세대 사역 통합' --status accepted --options-json '[\"한국 잔류\",\"단기 안식년만\"]' --consequences-json '[\"재정 시나리오 재구성 필요\",\"교회 멤버십 이전\"]'" \
    'Consequences'

check "V4-3 잘못된 날짜 차단" \
    "$PY render_ldr_body --title 'x' --date '5/18' --area '진로' --reason 'x'" \
    '"ok": false'

# ---------------------------------------------------------------------------
# 시나리오 V-5 — 박사님 정의 표준 표기 (인터뷰 인용 자동화)
# ---------------------------------------------------------------------------
echo
echo "[Scenario V-5] 박사님 정의·인용 표준 포맷"

check "V5-1 미션 정의 표준 표기" \
    "$PY render_definition --term '미션'" \
    'SOURCES.md § A-01'

check "V5-2 정신적 가치 정의" \
    "$PY render_definition --term '정신적 가치'" \
    '영감을 객관적으로 검증하는 안전장치'

check "V5-3 박사님 책 긴 인용 표준 표기" \
    "$PY render_quote --text '비전 프레임이란 \"가치 있는 + 시대적 + 소명\"이 어떻게 성장하는지를 설명하기 위해 필자가 만든 단어이다'" \
    '> '

check "V5-4 출처 없는 인용 차단" \
    "$PY render_quote --text '박사님께서 비전은 자기실현이라 했다'" \
    '"ok": false'

# ---------------------------------------------------------------------------
# 시나리오 V-6 — 시나리오 4종 주제 자동 치환 (재정 박사님 본인)
# ---------------------------------------------------------------------------
echo
echo "[Scenario V-6] 시나리오 자동 주제 치환 — 박사님 본인 재정 / 교회 사역 중심 이동"

check "V6-1 박사님 재정 큰 결정 — 주제 치환 확인" \
    "$PY scenario_expand --topic '강남 아파트 매도 후 지방 이주 + 사역 자본금 투입'" \
    '강남 아파트 매도 후 지방 이주'

check "V6-2 사역 중심 이동 — 주제 치환" \
    "$PY scenario_expand --topic '교회 사역 전임 헌신'" \
    '교회 사역 전임 헌신'

check "V6-3 빈 주제 → 이 결정" \
    "$PY scenario_expand --topic ''" \
    '이 결정'

# ---------------------------------------------------------------------------
# 시나리오 V-7 — LDR 체인 검증 (superseded by 시나리오)
# ---------------------------------------------------------------------------
echo
echo "[Scenario V-7] LDR 체인 무결성 — 박사님 진로 결단 변경 이력 추적"

mkdir -p "$TMP_B/docs/ldr"
cat > "$TMP_B/docs/ldr/0001-초기진로.md" <<'EOF'
# 초기 진로 결단

**날짜**: 2024-01-15
**영역**: 진로
**Status**: deprecated, superseded by LDR-0002

처음에는 학자로의 진로를 결단함.
EOF
cat > "$TMP_B/docs/ldr/0002-진로재구성.md" <<'EOF'
# 진로 재구성 — 미래학자 본업

**날짜**: 2026-05-18
**영역**: 진로
**Status**: accepted

학자에서 미래학자 본업으로 진로 재구성. LDR-0001을 supersede.
EOF

check "V7-1 정상 체인 (0001 → 0002)" \
    "$PY validate_ldr_chain --base $TMP_B" \
    '"ok": true'

# 깨진 체인 시뮬레이션
cat > "$TMP_B/docs/ldr/0003-깨진참조.md" <<'EOF'
# 깨진 참조

**날짜**: 2026-07-01
**영역**: 비전 영역 전환

superseded by LDR-9999
EOF

check "V7-2 깨진 참조 검출" \
    "$PY validate_ldr_chain --base $TMP_B" \
    '"broken_chains"'

# ---------------------------------------------------------------------------
# 시나리오 V-8 — three_realm sync (박사님 책 라벨 정확성)
# ---------------------------------------------------------------------------
echo
echo "[Scenario V-8] three_realm 라벨 ↔ glossary sync"

check "V8-1 three_realm sync ok" \
    "$PY validate_three_realm_sync" \
    '"ok": true'

check "V8-2 sync 결과에 3개 라벨 모두 명시" \
    "$PY validate_three_realm_sync" \
    '개인 욕망'

# ---------------------------------------------------------------------------
# 시나리오 V-9 — 무결성 검증 손상 시나리오 (방어 검증)
# ---------------------------------------------------------------------------
echo
echo "[Scenario V-9] VISION-CONTEXT.md 손상 시뮬레이션"

# 첫 시드
$PY seed_standard_glossary --base "$TMP_C" --owner 박사님 > /dev/null
check "V9-1 정상 시드 → 무결성 PASS" \
    "$PY validate_context_integrity --base $TMP_C" \
    '"ok": true'

# § 4 헤더 제거 시뮬레이션 (의도적 손상)
python3 -c "
import sys
p = '$TMP_C/VISION-CONTEXT.md'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('## 4. 관계', '')
with open(p, 'w', encoding='utf-8') as f:
    f.write(c)
"
check "V9-2 § 4 손상 검출" \
    "$PY validate_context_integrity --base $TMP_C" \
    '"## 4. 관계"'

# ---------------------------------------------------------------------------
# 시나리오 V-10 — 박사님 미래학자 본업 종합 — 모든 보조 함수 통합
# ---------------------------------------------------------------------------
echo
echo "[Scenario V-10] 박사님 미래학자 본업 종합 인터뷰 시뮬레이션"

# 사용자 입력 — Mode C
check "V10-1 모드 분기 C" \
    "$PY route_mode --text '박사님 미래학자 본업과 집필 사역 5년 집중 계획'" \
    '"mode": "C"'

# 주제 파싱
check "V10-2 미래 키워드 매칭" \
    "$PY parse_topic --text '박사님 미래학자 본업 5년 시나리오 — 10년 후 미래 모습'" \
    'vision-personal-future-research'

# 박사님 본업 영문 lookup
check "V10-3 영문 Vision lookup" \
    "$PY glossary_lookup --term 'Vision'" \
    '"english_input": "Vision"'

# 박사님 책 인용 표준 표기
check "V10-4 박사님 책 인용 표준 표기 ok" \
    "$PY render_quote --text '가치 있는 시대적 소명'" \
    'SOURCES.md § A-01'

# 시나리오 자동 치환
check "V10-5 박사님 본업 시나리오 4종" \
    "$PY scenario_expand --topic '박사님 본업 미래학자 5년 집중'" \
    '박사님 본업'

# LDR 자격 — 박사님 본업 5년 헌신
check "V10-6 LDR 자격 통과" \
    "$PY check_ldr_criteria --decision '박사님 본업 5년 집중 헌신' --reversibility hard --surprising true --tradeoff true" \
    '"qualifies": true'

# LDR 본문 자동 생성
check "V10-7 LDR 본문 자동 생성" \
    "$PY render_ldr_body --title '박사님 본업 5년 집중' --date 2026-06-01 --area '비전 영역 전환' --reason '시대적 부르심 응답 — 강의·집필 영역 확장'" \
    '"ok": true'

# ---------------------------------------------------------------------------
# 단위 + 기존 검증 라운드 통합
# ---------------------------------------------------------------------------
echo
echo "--- 단위 테스트 (확장 174개) 통합 ---"
unit_out=$(python3 grill_lib_test.py 2>&1 | tail -3)
if echo "$unit_out" | grep -q "ALL PASS"; then
    PASS=$((PASS+1))
    TOTAL=$((TOTAL+1))
    echo "PASS [통합 단위 테스트 174 ALL PASS]"
else
    FAIL=$((FAIL+1))
    TOTAL=$((TOTAL+1))
    echo "FAIL [단위 테스트]"
    echo "$unit_out"
fi

echo
echo "--- 이전 Pass 4 final_validation_round.sh 통합 ---"
pass4_out=$(bash final_validation_round.sh 2>&1 | tail -3)
if echo "$pass4_out" | grep -q "ALL PASS"; then
    PASS=$((PASS+1))
    TOTAL=$((TOTAL+1))
    echo "PASS [Pass 4 33 sub-check ALL PASS]"
else
    FAIL=$((FAIL+1))
    TOTAL=$((TOTAL+1))
    echo "FAIL [Pass 4 검증]"
    echo "$pass4_out"
fi

echo
echo "============================================================"
echo "Pass 5 v2 최종 검증 결과: $PASS/$TOTAL PASS"
echo "============================================================"
if [ "$FAIL" -eq 0 ]; then
    echo "ALL PASS — vision-grill-with-docs Pass 5 v2 100% 검증 완료"
    exit 0
else
    echo "FAIL: $FAIL — 추가 보강 필요"
    exit 1
fi
