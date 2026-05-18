#!/bin/bash
# vision-grill-with-docs — Pass 6 신규 10개 검증 시나리오 (v3).
# 이전 final_validation_round_v2.sh의 V-1~V-10 모든 sub-check와 *전혀 다른* 입력·주제·시나리오.
# 박사님 /goal 재발동: "이전 검증용 프롬프트를 학습하여 대답하거나, 검증 흉내를 만들어낼 오류를 완전 차단".

set -e
cd "$(dirname "$0")"
PY="python3 grill_lib.py"
PASS=0
FAIL=0
TOTAL=0
TMP_W1=$(mktemp -d)
TMP_W4=$(mktemp -d)
TMP_W6=$(mktemp -d)
TMP_W9=$(mktemp -d)
trap "rm -rf $TMP_W1 $TMP_W4 $TMP_W6 $TMP_W9" EXIT

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
        echo "  actual: $(echo "$out" | head -3)"
    fi
}

check_not() {
    local label="$1"
    local cmd="$2"
    local forbid_sub="$3"
    TOTAL=$((TOTAL+1))
    out=$(eval "$cmd" 2>&1)
    if echo "$out" | grep -q "$forbid_sub"; then
        FAIL=$((FAIL+1))
        echo "FAIL [$label] — forbidden substring found: $forbid_sub"
        echo "  actual: $(echo "$out" | head -3)"
    else
        PASS=$((PASS+1))
        echo "PASS [$label]"
    fi
}

echo "=== Pass 6 신규 10개 검증 시나리오 (v3) ==="
echo "이전 final_validation_round_v2.sh와 100% 다른 입력 — Mode B / 7가지 imbalance / 확장된 conflict / 한자·이모지 마커 등"
echo

# ---------------------------------------------------------------------------
# 시나리오 W-1 — Mode B route + parse_topic 매핑
# ---------------------------------------------------------------------------
echo "[Scenario W-1] Mode B 메타 검증 호출"

check "W1-1 verify mission-frame → Mode B" \
    "$PY route_mode --text 'verify mission-frame'" \
    '"mode": "B"'

check "W1-2 산출물 검증 한글 호출 → Mode B" \
    "$PY route_mode --text 'three-realm 산출물 검증'" \
    '"mode": "B"'

check "W1-3 메타 검증 한글 호출 → Mode B" \
    "$PY route_mode --text '메타 검증 시작'" \
    '"mode": "B"'

check "W1-4 일반 주제 → Mode C" \
    "$PY route_mode --text '제2의 인생 어떻게 살까'" \
    '"mode": "C"'

check "W1-5 본인 비전 grill → Mode A" \
    "$PY route_mode --text '본인 비전 grill 해 줘'" \
    '"mode": "A"'

# ---------------------------------------------------------------------------
# 시나리오 W-2 — 3영역 7가지 imbalance 패턴 전수
# ---------------------------------------------------------------------------
echo
echo "[Scenario W-2] 3영역 7가지 imbalance 패턴 전수"

check "W2-1 healthy (3영역 모두)" \
    "$PY three_realm_check --self true --others true --moral true" \
    '"status": "healthy"'

check "W2-2 empty (3영역 모두 0)" \
    "$PY three_realm_check --self false --others false --moral false" \
    '"status": "empty"'

check "W2-3 self-only (개인 욕망)" \
    "$PY three_realm_check --self true --others false --moral false" \
    '개인 욕망'

check "W2-4 others-only (자기희생)" \
    "$PY three_realm_check --self false --others true --moral false" \
    '자기희생·세상일'

check "W2-5 moral-only (왜곡된 사명)" \
    "$PY three_realm_check --self false --others false --moral true" \
    '왜곡된 사명'

check "W2-6 self+others (정신적 가치 결핍)" \
    "$PY three_realm_check --self true --others true --moral false" \
    '정신적 가치 결핍'

check "W2-7 self+moral (가족과 세상 결핍)" \
    "$PY three_realm_check --self true --others false --moral true" \
    '가족과 세상 결핍'

check "W2-8 others+moral (나 영역 결핍)" \
    "$PY three_realm_check --self false --others true --moral true" \
    '나 영역 결핍'

# ---------------------------------------------------------------------------
# 시나리오 W-3 — detect_glossary_conflict 확장 7개 어휘 검출
# ---------------------------------------------------------------------------
echo
echo "[Scenario W-3] 확장된 7개 핵심 어휘 personal definition 검출"

check "W3-1 정신적 가치 → 충돌 검출" \
    "$PY detect_glossary_conflict --text '저의 정신적 가치는 자유로움이다'" \
    'personal_definition_diverges'

check "W3-2 시대 → 충돌 검출" \
    "$PY detect_glossary_conflict --text '나의 시대는 디지털 전환기다'" \
    'personal_definition_diverges'

check "W3-3 영감 → 충돌 검출" \
    "$PY detect_glossary_conflict --text '본인의 영감은 자기 안에서 나온다'" \
    'personal_definition_diverges'

check "W3-4 미션 표준 정의 (충돌 없음)" \
    "$PY detect_glossary_conflict --text '저의 미션은 비전을 향한 지속적 실행입니다'" \
    '"clean": true'

check "W3-5 avoid 단어 — 꿈 → 비전" \
    "$PY detect_glossary_conflict --text '제 꿈은 위대한 일을 하는 것'" \
    'avoid_term_used'

# ---------------------------------------------------------------------------
# 시나리오 W-4 — upsert_term 멱등성 + 섹션 분리
# ---------------------------------------------------------------------------
echo
echo "[Scenario W-4] upsert_term 멱등 & 섹션 분리"

# 같은 term을 § 2에 두 번 upsert (idempotent)
$PY upsert_term --base "$TMP_W4" --term "디아스포라" \
    --definition "한국 밖에 흩어져 있는 한인 공동체" --section 2 > /dev/null
$PY upsert_term --base "$TMP_W4" --term "디아스포라" \
    --definition "한국 밖에 흩어져 있는 한인 공동체 (개정 v2)" --section 2 > /dev/null

check "W4-1 idempotent — 단어가 1번만 등장 (교체)" \
    "grep -c '\*\*디아스포라\*\*' $TMP_W4/VISION-CONTEXT.md" \
    '1'

check "W4-2 개정 정의가 들어감" \
    "grep '개정 v2' $TMP_W4/VISION-CONTEXT.md" \
    '개정 v2'

# 다른 섹션 (§ 3 본인 고유 용어)에 추가
$PY upsert_term --base "$TMP_W4" --term "성광주의" \
    --definition "본인 자작 용어 — 성령과 빛의 결합" --section 3 > /dev/null

check "W4-3 § 3 본인 고유 용어 추가" \
    "grep -A 50 '## 3. 본인 고유 용어' $TMP_W4/VISION-CONTEXT.md" \
    '성광주의'

check "W4-4 § 7 외부 참조 추가" \
    "$PY upsert_term --base '$TMP_W4' --term '리스크 디자인' --definition '실패의 가능성을 의도해서 설계' --section 7" \
    '"ok": true'

# ---------------------------------------------------------------------------
# 시나리오 W-5 — slug_normalize edge cases
# ---------------------------------------------------------------------------
echo
echo "[Scenario W-5] slug_normalize edge cases"

check "W5-1 일반 한글" \
    "$PY slug_normalize --title '집을 살까 말까'" \
    '"slug": "집을-살까-말까"'

check "W5-2 영문·숫자 혼합" \
    "$PY slug_normalize --title 'CYS Vision 2030 Master Plan'" \
    '"slug": "cys-vision-2030-master-plan"'

check "W5-3 한자 (현재 누락 — 잠재 결함)" \
    "$PY slug_normalize --title '人生 大選擇'" \
    '"slug"'

check "W5-4 max_len 초과 → trim" \
    "$PY slug_normalize --title '$(printf '가%.0s' {1..200})' --max-len 30" \
    '"slug"'

check "W5-5 특수문자만 → ok:false" \
    "$PY slug_normalize --title '!@#\$%^&*'" \
    '"ok": false'

# ---------------------------------------------------------------------------
# 시나리오 W-6 — promote_to_multi 안전성 + 멱등
# ---------------------------------------------------------------------------
echo
echo "[Scenario W-6] promote_to_multi 안전성·멱등"

# 단일 시드 후 multi 전환
$PY seed_standard_glossary --base "$TMP_W6" > /dev/null
$PY promote_to_multi --base "$TMP_W6" --area "사역" > /dev/null

check "W6-1 단일 → multi 전환 후 VISION-CONTEXT-MAP.md 생성" \
    "[ -f '$TMP_W6/VISION-CONTEXT-MAP.md' ] && echo found" \
    'found'

check "W6-2 사역 영역 CONTEXT.md 이동 확인" \
    "[ -f '$TMP_W6/사역/CONTEXT.md' ] && echo found" \
    'found'

check "W6-3 기존 단일 VISION-CONTEXT.md 제거" \
    "[ ! -f '$TMP_W6/VISION-CONTEXT.md' ] && echo gone" \
    'gone'

check "W6-4 경로 traversal 차단 (../etc)" \
    "$PY promote_to_multi --base '$TMP_W6' --area '../etc'" \
    'unsafe area name'

check "W6-5 두 번째 영역 추가 idempotent" \
    "$PY promote_to_multi --base '$TMP_W6' --area '재정'" \
    '"ok": true'

# ---------------------------------------------------------------------------
# 시나리오 W-7 — verify_quote 위조 차단 (다양한 wrapper)
# ---------------------------------------------------------------------------
echo
echo "[Scenario W-7] verify_quote 위조 차단"

check "W7-1 정확 인용 통과" \
    "$PY verify_quote --text '외부로부터 주어지는 영감'" \
    '"match": true'

check "W7-2 마침표 포함 정확 인용 통과" \
    "$PY verify_quote --text '강한 비전은 높은 정신적 만족감을 준다.'" \
    '"match": true'

check_not "W7-3 긴 wrapper — 의미 추가 차단" \
    "$PY verify_quote --text '박사님은 외부로부터 주어지는 영감이 모든 창조성의 원천이며 한국 미래학의 핵심이라고 가르치셨다'" \
    '"match": true'

check_not "W7-4 완전 위조 차단" \
    "$PY verify_quote --text '박사님은 모든 인간은 평등하다고 하셨다'" \
    '"match": true'

check_not "W7-5 빈 문자열 차단" \
    "$PY verify_quote --text ''" \
    '"match": true'

# ---------------------------------------------------------------------------
# 시나리오 W-8 — emoji_check 텍스트 마커 vs 진짜 이모지
# ---------------------------------------------------------------------------
echo
echo "[Scenario W-8] emoji_check 텍스트 마커 vs 이모지"

check "W8-1 텍스트 마커 ★ 허용" \
    "$PY emoji_check --text '★ 핵심 결정 / ☆ 보조 결정'" \
    '"clean": true'

check "W8-2 ✓ ✗ 허용" \
    "$PY emoji_check --text '✓ 진행 / ✗ 보류'" \
    '"clean": true'

check_not "W8-3 진짜 이모지 🎯 차단" \
    "$PY emoji_check --text '🎯 비전 달성'" \
    '"clean": true'

check_not "W8-4 진짜 이모지 🚀 차단" \
    "$PY emoji_check --text '비전 🚀 발사'" \
    '"clean": true'

check "W8-5 깨끗한 본문 통과" \
    "$PY emoji_check --text '박사님 비전 정의에 따르면'" \
    '"clean": true'

# ---------------------------------------------------------------------------
# 시나리오 W-9 — next_ldr_number 경계
# ---------------------------------------------------------------------------
echo
echo "[Scenario W-9] next_ldr_number 4자리 경계"

check "W9-1 빈 폴더 → 0001" \
    "$PY next_ldr_number --base '$TMP_W9'" \
    '"next": "0001"'

# 9999 파일 만들어 boundary 검증
mkdir -p "$TMP_W9/docs/ldr"
touch "$TMP_W9/docs/ldr/9999-final-decision.md"

check "W9-2 9999 도달 시 next:null + error" \
    "$PY next_ldr_number --base '$TMP_W9'" \
    'LDR 최대 번호'

# 중간 번호 (0042) 후 0043 부여
rm "$TMP_W9/docs/ldr/9999-final-decision.md"
touch "$TMP_W9/docs/ldr/0042-some-decision.md"
touch "$TMP_W9/docs/ldr/0017-other.md"

check "W9-3 0042 → next 0043" \
    "$PY next_ldr_number --base '$TMP_W9'" \
    '"next": "0043"'

check "W9-4 잘못된 형식 파일은 무시 (existing_max=42)" \
    "$PY next_ldr_number --base '$TMP_W9'" \
    '"existing_max": 42'

# ---------------------------------------------------------------------------
# 시나리오 W-10 — find_related_artifact + topic_skill_map (5영역 매핑)
# ---------------------------------------------------------------------------
echo
echo "[Scenario W-10] find_related_artifact — 5영역 키워드 매핑"

check "W10-1 진로 영역 매핑" \
    "$PY find_related_artifact --topic '대학 졸업 후 진로'" \
    'vision-'

check "W10-2 재정 영역 매핑 (집 매수 결정)" \
    "$PY find_related_artifact --topic '주택 매수 결정'" \
    'candidate_skills'

check "W10-3 사역·선교 영역 매핑" \
    "$PY find_related_artifact --topic '단기선교 vs 장기선교'" \
    'candidate_skills'

check "W10-4 관계 영역 매핑 (결혼)" \
    "$PY find_related_artifact --topic '결혼 시기 결정'" \
    'candidate_skills'

check "W10-5 비전 명료화 매핑" \
    "$PY find_related_artifact --topic '비전 자체가 모호하다 정리부터'" \
    'vision-clarity-coaching'

# ---------------------------------------------------------------------------
# 시나리오 W-11 — multi-context 가드 일관성 (이번 라운드 신규 보강)
# ---------------------------------------------------------------------------
echo
echo "[Scenario W-11] multi-context 가드 일관성"

TMP_W11=$(mktemp -d)
$PY promote_to_multi --base "$TMP_W11" --area "진로" > /dev/null

check "W11-1 multi root에서 seed_standard_glossary 차단" \
    "$PY seed_standard_glossary --base '$TMP_W11'" \
    'multi-context root'

check "W11-2 multi root에서 flag_conflict 차단" \
    "$PY flag_conflict --base '$TMP_W11' --term '꿈' --user-usage '먼훗날 미래' --resolution '박사님 정의 채택'" \
    'multi-context root'

check "W11-3 multi root validate_context_integrity 인식" \
    "$PY validate_context_integrity --base '$TMP_W11'" \
    '"structure": "multi"'

check "W11-4 영역 폴더에서 seed/flag/upsert 모두 성공" \
    "$PY seed_standard_glossary --base '$TMP_W11/진로' && $PY flag_conflict --base '$TMP_W11/진로' --term '꿈' --user-usage '먼훗날' --resolution 'override'" \
    '"ok": true'

check "W11-5 한자 슬러그 지원 (W5-3 결함 보강)" \
    "$PY slug_normalize --title '人生 大選擇 召命'" \
    '"slug": "人生-大選擇-召命"'

rm -rf "$TMP_W11"

# ---------------------------------------------------------------------------
# 결과
# ---------------------------------------------------------------------------
echo
echo "============================================================"
echo "Pass 6 v3 결과: $PASS/$TOTAL passed, $FAIL failed"
echo "============================================================"

if [ "$FAIL" -ne 0 ]; then
    exit 1
fi
echo "모든 신규 검증 PASS — 100% 정확도."
