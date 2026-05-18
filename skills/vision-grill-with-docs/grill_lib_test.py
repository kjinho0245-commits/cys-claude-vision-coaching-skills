"""
grill_lib.py 단위 테스트 (v2 — 결함 보강 후).

실행:
    python3 grill_lib_test.py

각 테스트는 자체 assert. 모두 통과하면 마지막에 "ALL PASS" 출력.
"""

from __future__ import annotations

import os
import sys
import tempfile
import json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import grill_lib  # noqa: E402


PASS = 0
FAIL = 0


def expect(label: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"PASS [{label}]")
    else:
        FAIL += 1
        print(f"FAIL [{label}]  {detail[:300]}")


# ---------------------------------------------------------------------------
# 1. route_mode
# ---------------------------------------------------------------------------

def test_route_mode():
    expect("route B - verify mission-frame", grill_lib.route_mode("verify mission-frame")["mode"] == "B")
    expect("route B - verify three-realm-balance", grill_lib.route_mode("verify three-realm-balance")["mode"] == "B")
    expect("route A - me", grill_lib.route_mode("me")["mode"] == "A")
    expect("route A - coachee:김도현", grill_lib.route_mode("coachee:김도현")["mode"] == "A")
    expect("route A - 내 비전 무너뜨려봐", grill_lib.route_mode("내 비전 무너뜨려봐")["mode"] == "A")
    expect("route C - 진로 결정", grill_lib.route_mode("진로 결정 — 전공·학교 코칭")["mode"] == "C")
    expect("route menu - empty", grill_lib.route_mode("")["mode"] == "menu")
    expect("route C - non-string None", grill_lib.route_mode(None)["mode"] == "C")  # type: ignore
    expect("route C - non-string int", grill_lib.route_mode(123)["mode"] == "C")  # type: ignore


# ---------------------------------------------------------------------------
# 2. parse_topic
# ---------------------------------------------------------------------------

def test_parse_topic():
    out = grill_lib.parse_topic("진로 결정 — 전공·학교 코칭")
    expect("parse 진로 매칭", "진로" in out["matched_keywords"], json.dumps(out, ensure_ascii=False))
    expect("parse 전공 매칭", "전공" in out["matched_keywords"])
    expect("parse 진로 → career-recommendation", "vision-career-recommendation" in out["related_skills"])

    out = grill_lib.parse_topic("집을 살까 말까")
    expect("parse 집 매칭", "집" in out["matched_keywords"])
    expect("parse 집 → 3shields-3windows", "vision-financial-3shields-3windows" in out["related_skills"])

    out = grill_lib.parse_topic("결혼 결정")
    expect("parse 결혼 매칭", "결혼" in out["matched_keywords"])
    expect("parse 결혼 → three-realm-balance", "vision-three-realm-balance" in out["related_skills"])

    out = grill_lib.parse_topic("선교지로 갈까 말까")
    expect("parse 선교 매칭", "선교" in out["matched_keywords"])

    out = grill_lib.parse_topic("")
    expect("parse 빈 입력 → 빈 결과", out["related_skills"] == [])

    out = grill_lib.parse_topic("외계어 zzz qqq")
    expect("parse 매칭 없음", out["related_skills"] == [])

    out = grill_lib.parse_topic(None)  # type: ignore
    expect("parse None 안전", out["related_skills"] == [])

    # 한국어 띄어쓰기 없는 입력
    out = grill_lib.parse_topic("진로결정코칭")
    expect("parse 띄어쓰기 없는 진로결정 → 진로 매칭", "진로" in out["matched_keywords"])


# ---------------------------------------------------------------------------
# 3. glossary_lookup
# ---------------------------------------------------------------------------

def test_glossary_lookup():
    out = grill_lib.glossary_lookup("비전")
    expect("lookup 비전", out["found"] and out["definition"] == "가치 있는 시대적 소명")
    expect("lookup 소명", grill_lib.glossary_lookup("소명")["found"])
    expect("lookup 영적 직관력", grill_lib.glossary_lookup("영적 직관력")["found"])
    expect("lookup 강화 피드백 루프", grill_lib.glossary_lookup("강화 피드백 루프")["found"])
    expect("lookup 외계어 not found", not grill_lib.glossary_lookup("외계어xyz")["found"])
    expect("lookup non-string", not grill_lib.glossary_lookup(123)["found"])  # type: ignore


# ---------------------------------------------------------------------------
# 4. detect_glossary_conflict
# ---------------------------------------------------------------------------

def test_detect_glossary_conflict():
    out = grill_lib.detect_glossary_conflict("내 꿈은 부자가 되는 것")
    expect("conflict 꿈 검출", any(c["user_term"] == "꿈" for c in out["conflicts"]))

    out = grill_lib.detect_glossary_conflict("저의 소명은 가족을 잘 부양하는 것입니다.")
    expect("conflict 개인정의-소명", any(c["type"] == "personal_definition_diverges" and c["term"] == "소명" for c in out["conflicts"]))

    out = grill_lib.detect_glossary_conflict("나의 비전은 가치 있는 시대적 소명입니다.")
    expect("conflict 박사님 정의 일치 → clean", out["clean"])

    expect("conflict 빈 입력 clean", grill_lib.detect_glossary_conflict("").clean if False else grill_lib.detect_glossary_conflict("")["clean"])
    expect("conflict None 안전", grill_lib.detect_glossary_conflict(None)["clean"])  # type: ignore


# ---------------------------------------------------------------------------
# 5. check_ldr_criteria
# ---------------------------------------------------------------------------

def test_check_ldr_criteria():
    out = grill_lib.check_ldr_criteria("공학 → 신학 전과", "hard", True, True)
    expect("LDR 3조건 충족 PASS", out["qualifies"])

    out = grill_lib.check_ldr_criteria("점심 한식", "easy", False, False)
    expect("LDR 모두 미충족 FAIL", not out["qualifies"])

    out = grill_lib.check_ldr_criteria("자취 시작", "hard", False, True)
    expect("LDR surprising 누락 FAIL", not out["qualifies"])

    out = grill_lib.check_ldr_criteria("관성 결정", "hard", True, False)
    expect("LDR tradeoff 누락 FAIL", not out["qualifies"])

    out = grill_lib.check_ldr_criteria("", "hard", True, True)
    expect("LDR 빈 결정 FAIL", not out["qualifies"])

    out = grill_lib.check_ldr_criteria("선택", "MAYBE", True, True)  # type: ignore
    expect("LDR 잘못된 reversibility FAIL", not out["qualifies"])

    out = grill_lib.check_ldr_criteria("선택", None, True, True)  # type: ignore
    expect("LDR None reversibility FAIL", not out["qualifies"])


# ---------------------------------------------------------------------------
# 6. next_ldr_number — boundary
# ---------------------------------------------------------------------------

def test_next_ldr_number():
    with tempfile.TemporaryDirectory() as tmp:
        expect("LDR 폴더 없음 → 0001", grill_lib.next_ldr_number(tmp)["next"] == "0001")
        ldr = os.path.join(tmp, "docs", "ldr")
        os.makedirs(ldr)
        for fn in ("0001-a.md", "0005-b.md", "0042-c.md"):
            open(os.path.join(ldr, fn), "w").write("# x\n")
        expect("LDR 0042 → 0043", grill_lib.next_ldr_number(tmp)["next"] == "0043")

        # 9999 boundary
        open(os.path.join(ldr, "9999-z.md"), "w").write("# x\n")
        out = grill_lib.next_ldr_number(tmp)
        expect("LDR 9999 → error", out["next"] is None and "error" in out)


# ---------------------------------------------------------------------------
# 7. is_multi_context / list_contexts / promote_to_multi
# ---------------------------------------------------------------------------

def test_context_structure():
    with tempfile.TemporaryDirectory() as tmp:
        expect("multi none 초기", grill_lib.is_multi_context(tmp)["structure"] == "none")
        open(os.path.join(tmp, "VISION-CONTEXT.md"), "w").write("# x\n")
        expect("single 감지", grill_lib.is_multi_context(tmp)["structure"] == "single")

        # promote_to_multi
        out = grill_lib.promote_to_multi(tmp, "진로")
        expect("promote ok", out["ok"])
        expect("promote moved single", out["moved_single_to_area"])
        expect("promote created map", out["created_map"])
        expect("multi 감지", grill_lib.is_multi_context(tmp)["structure"] == "multi")
        expect("진로 영역 파일 존재", os.path.exists(os.path.join(tmp, "진로", "CONTEXT.md")))

        # list_contexts
        lc = grill_lib.list_contexts(tmp)
        expect("list_contexts multi", lc["structure"] == "multi")
        expect("list_contexts 진로 등록", any(a["name"] == "진로" for a in lc["areas"]))

        # idempotent — 두 번째 promote
        out2 = grill_lib.promote_to_multi(tmp, "재정")
        expect("promote 재정 추가 ok", out2["ok"])
        expect("재정 영역 생성", os.path.exists(os.path.join(tmp, "재정", "CONTEXT.md")))

        # 같은 영역 또 호출 → 멱등
        out3 = grill_lib.promote_to_multi(tmp, "재정")
        expect("promote 재정 멱등 ok", out3["ok"])

    with tempfile.TemporaryDirectory() as tmp2:
        # 단일 사전 없이 바로 multi
        out = grill_lib.promote_to_multi(tmp2, "관계")
        expect("promote w/o single ok", out["ok"])
        expect("관계 영역 lazy 생성", os.path.exists(os.path.join(tmp2, "관계", "CONTEXT.md")))

        # path traversal 차단
        expect("promote 경로 traversal '/' 차단", not grill_lib.promote_to_multi(tmp2, "../etc")["ok"])
        expect("promote '..' 차단", not grill_lib.promote_to_multi(tmp2, "..")["ok"])
        expect("promote 슬래시 차단", not grill_lib.promote_to_multi(tmp2, "a/b")["ok"])
        expect("promote 백슬래시 차단", not grill_lib.promote_to_multi(tmp2, "a\\b")["ok"])
        expect("promote 점-시작 차단", not grill_lib.promote_to_multi(tmp2, ".hidden")["ok"])
        expect("promote 너무 긴 area 차단", not grill_lib.promote_to_multi(tmp2, "X" * 60)["ok"])


# ---------------------------------------------------------------------------
# 8. three_realm_check — type 엄격
# ---------------------------------------------------------------------------

def test_three_realm_check():
    expect("3realm 건강", grill_lib.three_realm_check(True, True, True)["status"] == "healthy")
    expect("3realm 개인 욕망", "개인 욕망" in grill_lib.three_realm_check(True, False, False)["label"])
    expect("3realm 자기희생", "자기희생" in grill_lib.three_realm_check(False, True, False)["label"])
    expect("3realm 왜곡된 사명", "왜곡된 사명" in grill_lib.three_realm_check(False, False, True)["label"])
    expect("3realm empty", grill_lib.three_realm_check(False, False, False)["status"] == "empty")
    expect("3realm 정신적 가치 결핍", "정신적 가치" in grill_lib.three_realm_check(True, True, False)["label"])
    expect("3realm 가족과 세상 결핍", "가족과 세상" in grill_lib.three_realm_check(True, False, True)["label"])
    expect("3realm 나 영역 결핍", "나 영역" in grill_lib.three_realm_check(False, True, True)["label"])

    # 문자열 "true"/"false" 허용
    expect("3realm str 'true' 변환", grill_lib.three_realm_check("true", "true", "true")["status"] == "healthy")

    # 잘못된 type
    out = grill_lib.three_realm_check([], True, True)  # type: ignore
    expect("3realm list type → error", out["status"] == "error")

    out = grill_lib.three_realm_check("maybe", True, True)  # type: ignore
    expect("3realm 'maybe' → error", out["status"] == "error")


# ---------------------------------------------------------------------------
# 9. scenario_expand
# ---------------------------------------------------------------------------

def test_scenario_expand():
    out = grill_lib.scenario_expand("공학 전공")
    expect("scenario 4종", len(out["scenarios"]) == 4)
    names = [s["name"] for s in out["scenarios"]]
    for n in ("5년 후 시나리오", "10년 후 시나리오", "실패 시나리오", "기회비용 시나리오"):
        expect(f"scenario {n}", n in names)


# ---------------------------------------------------------------------------
# 10. verify_quote — 강화된 매칭
# ---------------------------------------------------------------------------

def test_verify_quote():
    expect("verify 허용 정확 매칭", grill_lib.verify_quote("외부로부터 주어지는 영감")["match"])
    expect("verify 비전 정의 매칭", grill_lib.verify_quote("가치 있는 시대적 소명")["match"])
    expect("verify 긴 통합 인용 매칭", grill_lib.verify_quote(
        "강한 비전은 높은 정신적 만족감을 준다. 그러나 참된 정신적 가치는 동시에 이웃(가족과 세상, 인류)에게도 기쁨이 되어야 하고, 나 자신에게도 진정한 기쁨을 주어야 한다."
    )["match"])

    # 위조 차단 — wrapper에 길게 끼워넣음
    expect(
        "verify 위조 차단 — 박사님께서 ... 라고 하셨다",
        not grill_lib.verify_quote(
            "박사님께서는 외부로부터 주어지는 영감이라고 했지만 이는 잘못된 표현이다"
        )["match"],
    )
    expect(
        "verify 위조 차단 — 가짜 학자 인용",
        not grill_lib.verify_quote("Gardner는 비전이 10가지 지능이라 했다")["match"],
    )
    expect("verify 비-인용 차단", not grill_lib.verify_quote("아무 텍스트 던지기")["match"])

    # 따옴표 둘러싼 입력
    expect(
        'verify 따옴표 포함 정확 매칭',
        grill_lib.verify_quote('"외부로부터 주어지는 영감"')["match"],
    )

    expect("verify non-string", not grill_lib.verify_quote(123)["match"])  # type: ignore
    expect("verify 빈 텍스트", not grill_lib.verify_quote("")["match"])


# ---------------------------------------------------------------------------
# 11. find_related_artifact
# ---------------------------------------------------------------------------

def test_find_related_artifact():
    out = grill_lib.find_related_artifact("재정 결정 — 집 매수")
    expect("related 재정 매칭", "vision-financial-coach" in out["candidate_skills"])
    expect("related 매칭 키워드 반환", len(out["matched_keywords"]) > 0)


# ---------------------------------------------------------------------------
# 12. upsert_term — idempotent
# ---------------------------------------------------------------------------

def test_upsert_term():
    with tempfile.TemporaryDirectory() as tmp:
        out = grill_lib.upsert_term(tmp, "중간 비전", "5년 마일스톤 비전", "단기 목표", "3")
        expect("upsert ok", out["ok"] and out["created"])

        with open(out["path"], "r", encoding="utf-8") as f:
            c = f.read()
        expect("upsert term in body", "중간 비전" in c)
        expect("upsert def in body", "5년 마일스톤 비전" in c)
        expect("upsert avoid in body", "단기 목표" in c)

        # idempotent — 같은 term 다시 upsert → 교체
        out2 = grill_lib.upsert_term(tmp, "중간 비전", "수정된 정의", section="3")
        expect("upsert idempotent replaced", out2["ok"] and out2.get("replaced"))
        with open(out2["path"], "r", encoding="utf-8") as f:
            c2 = f.read()
        expect("upsert 수정된 정의 반영", "수정된 정의" in c2)
        expect("upsert 중복 없음 (오래된 정의 제거)", "5년 마일스톤 비전" not in c2)

        # § 2에 다른 term 추가
        out3 = grill_lib.upsert_term(tmp, "본인 소명", "일터 헌신", section="2")
        expect("upsert § 2 새 term ok", out3["ok"])

        # 잘못된 인자
        expect("upsert 빈 term", not grill_lib.upsert_term(tmp, "", "x")["ok"])
        expect("upsert 빈 def", not grill_lib.upsert_term(tmp, "x", "")["ok"])
        expect("upsert invalid section", not grill_lib.upsert_term(tmp, "x", "y", section="9")["ok"])


# ---------------------------------------------------------------------------
# 13. flag_conflict — § 6 충돌 기록
# ---------------------------------------------------------------------------

def test_flag_conflict():
    with tempfile.TemporaryDirectory() as tmp:
        out = grill_lib.flag_conflict(tmp, "소명", "가족 부양", "박사님 표준 정의 채택")
        expect("flag_conflict ok", out["ok"])
        with open(out["path"], "r", encoding="utf-8") as f:
            c = f.read()
        expect("flag § 6 헤더 존재", "## 6. 충돌 기록" in c)
        expect("flag entry term", "소명" in c)
        expect("flag entry usage", "가족 부양" in c)
        expect("flag entry resolution", "박사님 표준 정의 채택" in c)

        # 두 번째 충돌 추가
        out2 = grill_lib.flag_conflict(tmp, "비전", "꿈과 동의어", "박사님 정의 채택")
        expect("flag 2nd ok", out2["ok"])
        with open(out2["path"], "r", encoding="utf-8") as f:
            c2 = f.read()
        expect("flag 두 충돌 모두 보존", "소명" in c2 and "비전" in c2)

        expect("flag 빈 term", not grill_lib.flag_conflict(tmp, "", "x", "y")["ok"])
        expect("flag 빈 usage", not grill_lib.flag_conflict(tmp, "x", "", "y")["ok"])
        expect("flag 빈 resolution", not grill_lib.flag_conflict(tmp, "x", "y", "")["ok"])


# ---------------------------------------------------------------------------
# 14. emoji_check
# ---------------------------------------------------------------------------

def test_emoji_check():
    expect("emoji clean text", grill_lib.emoji_check("순수 한글 텍스트입니다")["clean"])
    expect("emoji 🎯 detected", not grill_lib.emoji_check("비전 🎯 찾았다")["clean"])
    expect("emoji 😀 detected", not grill_lib.emoji_check("좋아요 😀")["clean"])
    expect("emoji ★ NOT in default range", grill_lib.emoji_check("★ 핵심 단계")["clean"])
    expect("emoji 빈 입력", grill_lib.emoji_check("")["clean"])
    expect("emoji None 안전", grill_lib.emoji_check(None)["clean"])  # type: ignore


# ---------------------------------------------------------------------------
# 15. slug_normalize
# ---------------------------------------------------------------------------

def test_slug_normalize():
    out = grill_lib.slug_normalize("진로 — 공학에서 신학으로 전환")
    expect("slug 한글 케밥", out["ok"] and out["slug"] == "진로-공학에서-신학으로-전환")

    out = grill_lib.slug_normalize("Career: Move from Engineering to Theology!")
    expect("slug 영어 lowercase 케밥", out["ok"] and out["slug"] == "career-move-from-engineering-to-theology")

    out = grill_lib.slug_normalize("결혼 결정 — 2027년 가을!")
    expect("slug 숫자 보존", out["ok"] and "2027년" in out["slug"])

    out = grill_lib.slug_normalize("")
    expect("slug 빈 입력 fail", not out["ok"])

    out = grill_lib.slug_normalize("!@#$%^&*()")
    expect("slug 모두 구두점 fail", not out["ok"])

    out = grill_lib.slug_normalize("매우 긴 제목을 만들어서 max_len을 초과하는지 본다 진로 전공 학교 결정 종합", max_len=20)
    expect("slug max_len 자르기", out["ok"] and len(out["slug"]) <= 20)


# ---------------------------------------------------------------------------
# 16. menu_options
# ---------------------------------------------------------------------------

def test_menu_options():
    m = grill_lib.menu_options()
    expect("menu 3 modes", len(m["modes"]) == 3)
    mode_keys = [mo["key"] for mo in m["modes"]]
    for k in ("A", "B", "C"):
        expect(f"menu mode {k}", k in mode_keys)
    expect("menu tools list", len(m["tools_available"]) >= 5)


# ---------------------------------------------------------------------------
# 17. SYNC 검증 — 사양 ↔ 코드
# ---------------------------------------------------------------------------

def test_sync_validators():
    out = grill_lib.validate_glossary_sync()
    expect("sync glossary ok", out["ok"], json.dumps(out, ensure_ascii=False))

    out = grill_lib.validate_quotes_sync()
    expect("sync quotes ok (missing_in_code empty)", out["ok"], json.dumps(out, ensure_ascii=False))

    out = grill_lib.validate_topic_map_skills()
    expect("sync topic_map vision-* ok", out["ok"], json.dumps(out, ensure_ascii=False))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print("=== grill_lib_test.py (v2) ===")
    test_route_mode()
    test_parse_topic()
    test_glossary_lookup()
    test_detect_glossary_conflict()
    test_check_ldr_criteria()
    test_next_ldr_number()
    test_context_structure()
    test_three_realm_check()
    test_scenario_expand()
    test_verify_quote()
    test_find_related_artifact()
    test_upsert_term()
    test_flag_conflict()
    test_emoji_check()
    test_slug_normalize()
    test_menu_options()
    test_sync_validators()

    total = PASS + FAIL
    print()
    print(f"=== {PASS}/{total} PASS ===")
    if FAIL == 0:
        print("ALL PASS")
        return 0
    print(f"FAIL: {FAIL}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
