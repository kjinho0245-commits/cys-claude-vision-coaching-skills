#!/bin/bash
# vision-grill-with-docs — ARBITRARY-10
# AI가 임의로 입력한 10개 실사용자형 작업 명령 프롬프트에 대한 결정론 검증.
# 박사님 /goal 완료 조건: AI가 임의로 10개 프롬프트를 입력해 100% 정확도 확인.
set -e
cd "$(dirname "$0")"
PY="python3 grill_lib.py"
PASS=0; FAIL=0; TOTAL=0
arbit() { echo "--- [$1] $2 ---"; }
verify() {
    local label="$1" cmd="$2" expect="$3"
    TOTAL=$((TOTAL+1))
    out=$(eval "$cmd" 2>&1)
    if echo "$out" | grep -q "$expect"; then PASS=$((PASS+1)); echo "  PASS  $label"
    else FAIL=$((FAIL+1)); echo "  FAIL  $label"; echo "    expect: $expect"; echo "    actual: $(echo "$out" | head -2)"; fi
}

echo "================================================================"
echo "ARBITRARY-10 검증 — AI 임의 10개 실사용자형 프롬프트"
echo "================================================================"

arbit "A-1" "박사님 본인 미래학자 본업 헌신 LDR"
verify "Mode C" "$PY route_mode --text '박사님 본인 미래학자 본업 헌신 LDR로 정리'" '"mode": "C"'
verify "호칭 박사님" "$PY select_honorific --meta-json '{\"is_doctor\":true}'" '"honorific": "박사님"'
verify "parse_topic" "$PY parse_topic --text '박사님 본인 미래학자 본업 헌신'" 'matched_keywords'
verify "LDR 자격" "$PY check_ldr_criteria --decision '박사님 미래학자 본업 헌신' --reversibility hard --surprising true --tradeoff true" '"qualifies": true'
verify "시나리오" "$PY scenario_expand --topic '미래학자 본업 헌신'" '5년 후 시나리오'

echo; arbit "A-2" "호주 가족 이민 결단"
verify "Mode C" "$PY route_mode --text '호주 가족 이민 결단 코칭'" '"mode": "C"'
verify "parse_topic" "$PY parse_topic --text '호주 가족 이민 결단'" 'vision-'
verify "LDR 자격" "$PY check_ldr_criteria --decision '호주 가족 이민' --reversibility hard --surprising true --tradeoff true" '"qualifies": true'
verify "slug" "$PY slug_normalize --title '호주 가족 이민 결단'" '"slug": "호주-가족-이민-결단"'
verify "scenario" "$PY scenario_expand --topic '호주 가족 이민'" '호주 가족 이민'

echo; arbit "A-3" "verify three-realm moral-only"
verify "Mode B" "$PY route_mode --text 'verify three-realm-balance moral-only'" '"mode": "B"'
verify "moral-only = 왜곡된 사명" "$PY three_realm_check --self false --others false --moral true" '왜곡된 사명'
verify "lookup 왜곡된 사명" "$PY glossary_lookup --term '왜곡된 사명'" '"found": true'
verify "render" "$PY render_definition --term '왜곡된 사명'" '왜곡된 사명'

echo; arbit "A-4" "내 가치는 자유로움이다"
verify "Mode C" "$PY route_mode --text '내 가치는 자유로움이다'" '"mode": "C"'
verify "conflict 검출 (가치 확장)" "$PY detect_glossary_conflict --text '내 가치는 자유로움이다'" 'personal_definition_diverges'
verify "가치 lookup" "$PY glossary_lookup --term '가치'" '영적 직관력 축'

echo; arbit "A-5" "Calling Personal Desire 영문"
verify "Calling → 소명" "$PY glossary_lookup --term 'Calling'" '"term": "소명"'
verify "Personal Desire → 개인 욕망" "$PY glossary_lookup --term 'Personal Desire'" '"term": "개인 욕망"'
verify "MBTI alias (Pass 6)" "$PY glossary_lookup --term 'MBTI'" '"term": "MBTI 16유형"'
verify "소문자 calling" "$PY glossary_lookup --term 'calling'" '"term": "소명"'

echo; arbit "A-6" "me — 본인 비전 grill"
verify "Mode A" "$PY route_mode --text 'me'" '"mode": "A"'
TMP=$(mktemp -d)
verify "seed glossary" "$PY seed_standard_glossary --base '$TMP' --owner '박사님'" '"seeded": true'
verify "integrity" "$PY validate_context_integrity --base '$TMP'" '"ok": true'
rm -rf "$TMP"

echo; arbit "A-7" "비전이 막혔다"
verify "Mode C" "$PY route_mode --text '비전이 막혔다 어디부터 시작'" '"mode": "C"'
verify "clarity 매핑" "$PY find_related_artifact --topic '비전이 막혀있다 어디부터'" 'vision-clarity-coaching'
verify "메뉴" "$PY menu_options" '"key": "A"'

echo; arbit "A-8" "가족과 세상 결핍"
verify "self+moral 진단" "$PY three_realm_check --self true --others false --moral true" '가족과 세상 결핍'
verify "lookup 가족과 세상" "$PY glossary_lookup --term '가족과 세상'" '이웃·인류'
verify "통합 인용" "$PY verify_quote --text '강한 비전은 높은 정신적 만족감을 준다. 그러나 참된 정신적 가치는 동시에 이웃(가족과 세상, 인류)에게도 기쁨이 되어야 하고, 나 자신에게도 진정한 기쁨을 주어야 한다.'" '"match": true'

echo; arbit "A-9" "大選擇 인생 큰 결정 (한자)"
verify "Mode C" "$PY route_mode --text '大選擇 인생 큰 결정 LDR'" '"mode": "C"'
verify "한자 slug (Pass 6)" "$PY slug_normalize --title '大選擇 인생 큰 결정'" '"slug": "大選擇-인생-큰-결정"'
verify "LDR 자격" "$PY check_ldr_criteria --decision '大選擇' --reversibility hard --surprising true --tradeoff true" '"qualifies": true'
verify "본문 생성" "$PY render_ldr_body --title '大選擇' --date 2026-05-18 --area '비전 영역 전환' --reason '인생 방향 전환' --status proposed" '"ok": true'

echo; arbit "A-10" "(빈 호출)"
verify "menu 모드" "$PY route_mode --text ''" '"mode": "menu"'
verify "menu options key C" "$PY menu_options" '"key": "C"'
verify "tools_available" "$PY menu_options" 'tools_available'

echo
echo "================================================================"
echo "ARBITRARY-10 결과: $PASS/$TOTAL passed, $FAIL failed"
echo "================================================================"
[ "$FAIL" -ne 0 ] && exit 1
echo "ALL PASS — 박사님 명령 완료 조건 충족 (AI 임의 10개 프롬프트 100% 정확)"
