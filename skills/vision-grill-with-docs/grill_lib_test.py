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

    out = grill_lib.validate_three_realm_sync()
    expect("sync three_realm labels ok", out["ok"], json.dumps(out, ensure_ascii=False))


# ---------------------------------------------------------------------------
# 18. select_honorific
# ---------------------------------------------------------------------------

def test_select_honorific():
    expect("honorific 박사님", grill_lib.select_honorific({"is_doctor": True})["honorific"] == "박사님")
    expect("honorific 목사님", grill_lib.select_honorific({"title": "목사"})["honorific"] == "목사님")
    expect("honorific 김도현님", grill_lib.select_honorific({"name": "김도현"})["honorific"] == "김도현님")
    expect("honorific 기본 선생님", grill_lib.select_honorific({})["honorific"] == "선생님")
    expect("honorific None 안전", grill_lib.select_honorific(None)["honorific"] == "선생님")  # type: ignore
    expect("honorific 이미 님 붙은 title", grill_lib.select_honorific({"title": "장로님"})["honorific"] == "장로님")


# ---------------------------------------------------------------------------
# 19. render_ldr_body
# ---------------------------------------------------------------------------

def test_render_ldr_body():
    out = grill_lib.render_ldr_body(
        title="진로 — 공학에서 신학으로",
        date_iso="2026-05-18",
        area="진로",
        reason="박사님 표준 소명 정의 응답 더 분명",
    )
    expect("LDR body ok", out["ok"])
    expect("LDR body 제목 포함", "진로 — 공학에서 신학으로" in out["body"])
    expect("LDR body 날짜 포함", "2026-05-18" in out["body"])
    expect("LDR body 알려진 영역", out["is_known_area"])

    # 선택 섹션
    out2 = grill_lib.render_ldr_body(
        title="결혼 결단",
        date_iso="2027-09-01",
        area="관계",
        reason="배우자와 비전 공유 확인",
        status="accepted",
        options_considered=["1년 더 교제 후", "혼자 살기"],
        consequences=["가족 합가 검토 필요"],
    )
    expect("LDR body status 포함", "**Status**: accepted" in out2["body"])
    expect("LDR body 고려한 대안", "## 고려한 대안" in out2["body"])
    expect("LDR body Consequences", "## Consequences" in out2["body"])

    # 잘못된 날짜
    bad = grill_lib.render_ldr_body(title="x", date_iso="2026/5/18", area="x", reason="x")
    expect("LDR body 잘못된 날짜 FAIL", not bad["ok"])
    # 빈 인자
    expect("LDR body 빈 title", not grill_lib.render_ldr_body(title="", date_iso="2026-05-18", area="진로", reason="x")["ok"])
    expect("LDR body 빈 reason", not grill_lib.render_ldr_body(title="x", date_iso="2026-05-18", area="진로", reason="")["ok"])


# ---------------------------------------------------------------------------
# 20. render_definition / render_quote
# ---------------------------------------------------------------------------

def test_render_definition_and_quote():
    out = grill_lib.render_definition("비전")
    expect("render_def 비전 ok", out["ok"] and "**비전**" in out["rendered"] and "SOURCES.md" in out["rendered"])

    out = grill_lib.render_definition("Vision")  # 영문 lookup
    expect("render_def 영문 lookup ok", out["ok"])

    out = grill_lib.render_definition("외계어")
    expect("render_def 없음 FAIL", not out["ok"])

    out = grill_lib.render_quote("외부로부터 주어지는 영감")
    expect("render_quote 정확 인용 ok", out["ok"] and "SOURCES.md § A-01" in out["rendered"])

    out = grill_lib.render_quote("박사님께서 외부로부터 주어지는 영감이라 했지만 이는 잘못이다")
    expect("render_quote 위조 차단", not out["ok"])


# ---------------------------------------------------------------------------
# 21. 영문 lookup
# ---------------------------------------------------------------------------

def test_english_lookup():
    for en in ("Vision", "Mission", "Calling", "Spiritual Intuition", "Reinforcing Feedback Loop"):
        out = grill_lib.glossary_lookup(en)
        expect(f"lookup 영문 {en}", out["found"] and out.get("matched_via", "").startswith("english"))

    # 대소문자 무시
    out = grill_lib.glossary_lookup("vision")
    expect("lookup 영문 소문자 vision", out["found"])


# ---------------------------------------------------------------------------
# 22. seed_standard_glossary — idempotent
# ---------------------------------------------------------------------------

def test_seed_standard_glossary():
    with tempfile.TemporaryDirectory() as tmp:
        out = grill_lib.seed_standard_glossary(tmp, owner="박사님")
        expect("seed ok", out["ok"] and out["seeded"])
        with open(out["path"], "r", encoding="utf-8") as f:
            c = f.read()
        expect("seed 비전 entry", "**비전**:" in c)
        expect("seed 가치 있는 시대적 소명", "가치 있는 시대적 소명" in c)
        expect("seed Source 명시", "SOURCES.md § A-01" in c)

        # idempotent
        out2 = grill_lib.seed_standard_glossary(tmp, owner="박사님")
        expect("seed idempotent — 두 번째 호출 seeded=False", out2["ok"] and not out2["seeded"])


# ---------------------------------------------------------------------------
# 23. validate_context_integrity
# ---------------------------------------------------------------------------

def test_validate_context_integrity():
    with tempfile.TemporaryDirectory() as tmp:
        # 파일 없음
        out = grill_lib.validate_context_integrity(tmp)
        expect("integrity 파일 없음 FAIL", not out["ok"] and not out["exists"])

        # 정상 파일 (upsert_term이 만든 표준 헤더 7개)
        grill_lib.upsert_term(tmp, "test", "test def", section="2")
        out = grill_lib.validate_context_integrity(tmp)
        expect("integrity 정상 헤더 PASS", out["ok"], json.dumps(out, ensure_ascii=False))

        # 손상 시뮬레이션 — § 4 삭제
        path = os.path.join(tmp, "VISION-CONTEXT.md")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        damaged = content.replace("## 4. 관계", "")
        with open(path, "w", encoding="utf-8") as f:
            f.write(damaged)
        out = grill_lib.validate_context_integrity(tmp)
        expect("integrity 손상 검출", not out["ok"] and "## 4. 관계" in out["missing_sections"])


# ---------------------------------------------------------------------------
# 24. validate_ldr_chain
# ---------------------------------------------------------------------------

def test_validate_ldr_chain():
    with tempfile.TemporaryDirectory() as tmp:
        # LDR 폴더 없음
        out = grill_lib.validate_ldr_chain(tmp)
        expect("chain LDR 폴더 없음 ok", out["ok"] and out["ldr_count"] == 0)

        ldr = os.path.join(tmp, "docs", "ldr")
        os.makedirs(ldr)
        # 정상 체인
        open(os.path.join(ldr, "0001-a.md"), "w").write("# A\n\n**Status**: deprecated, superseded by LDR-0002\n")
        open(os.path.join(ldr, "0002-b.md"), "w").write("# B\n")
        out = grill_lib.validate_ldr_chain(tmp)
        expect("chain 정상 superseded by 0002 ok", out["ok"] and out["ldr_count"] == 2)

        # 깨진 체인
        open(os.path.join(ldr, "0003-c.md"), "w").write("# C\n\nsuperseded by LDR-9999\n")
        out = grill_lib.validate_ldr_chain(tmp)
        expect("chain 깨진 참조 검출", not out["ok"] and len(out["broken_chains"]) == 1)


# ---------------------------------------------------------------------------
# 25. scenario_expand 주제 치환
# ---------------------------------------------------------------------------

def test_route_intake():
    """E안 마스터 진입 — 한 문장 자유 답 → 진입 스킬 라우팅."""
    # 빈 입력 → 메뉴
    out = grill_lib.route_intake("")
    expect("intake 빈 입력 → menu", out["mode"] == "menu" and "guidance" in out)
    expect("intake guidance 예시 포함", "처음입니다" in out["guidance"])

    # 박사님 본인
    out = grill_lib.route_intake("박사님 본인 미래학자 본업 5년 집중")
    expect("intake 박사님 본인 → Mode A", out["mode"] == "A")
    expect("intake 박사님 본인 → mission-frame", out["next_skill"] == "vision-mission-frame")

    # 진학·학교 키워드는 career 영역으로 라우팅 (현실적·정확)
    out = grill_lib.route_intake("신학교 진학 결단 앞두고 가족이 반대")
    expect("intake 결단 → Mode C", out["mode"] == "C")
    expect("intake 진학 키워드 → school-major-info (career 영역)",
           out["next_skill"] == "vision-school-major-info")

    # 순수 사역 영역 → mission-frame
    out = grill_lib.route_intake("선교 헌신·전임 사역 결단")
    expect("intake 순수 사역 → mission-frame", out["next_skill"] == "vision-mission-frame")

    # 영역 명시 없는 큰 결정 → stuck_decision으로 grill-with-docs
    out = grill_lib.route_intake("큰 결정 앞에서 막혔어요")
    expect("intake 영역 모호 결정 → grill-with-docs", out["next_skill"] == "vision-grill-with-docs")

    # 진로 영역
    out = grill_lib.route_intake("진로·전공·학교 결정해야 합니다")
    expect("intake 진로 → school-major-info", out["next_skill"] == "vision-school-major-info")

    # 재정 영역
    out = grill_lib.route_intake("재정 큰 결정 — 집 매수 고민")
    expect("intake 재정 → financial-3shields", out["next_skill"] == "vision-financial-3shields-3windows")

    # 첫 입장 (박사님 책 공식 진단부터)
    out = grill_lib.route_intake("처음입니다 어디서부터 시작해야 할지")
    expect("intake 첫 입장 → cys-competence", out["next_skill"] == "vision-cys-competence-visioncoding")

    # 미래 시뮬레이션
    out = grill_lib.route_intake("5년 후 10년 후 미래 모습 시뮬레이션")
    expect("intake 미래 → futures-timeline-map", out["next_skill"] == "vision-futures-timeline-map")

    # 사역 헌신
    out = grill_lib.route_intake("선교사 헌신을 앞두고 있어요")
    # career·ministry·stuck_decision 다 매칭 가능 — stuck_decision이 우선
    expect("intake 사역 헌신 매칭", len(out["matched_categories"]) >= 1)

    # 매칭 없음 → 기본 Mode C
    out = grill_lib.route_intake("아무거나 외계어 zzz")
    expect("intake 매칭 없음 → Mode C 기본", out["mode"] == "C")


def test_decide_first_skill():
    # 첫 회·진단 없음 → 박사님 공식 입학 진단
    out = grill_lib.decide_first_skill({"visit_count": 1, "has_diagnosis": False})
    expect("first_skill 첫 회 → cys-competence",
           out["first_skill"] == "vision-cys-competence-visioncoding")
    expect("first_skill depth shallow_first", out["depth_mode"] == "shallow_first")

    # 진단 있고 비전 없음
    out = grill_lib.decide_first_skill({"visit_count": 2, "has_diagnosis": True, "has_vision_statement": False})
    expect("first_skill 진단 후 비전 없음 → clarity-coaching",
           out["first_skill"] == "vision-clarity-coaching")

    # 비전 있음·단계 5
    out = grill_lib.decide_first_skill({
        "visit_count": 3, "has_diagnosis": True, "has_vision_statement": True, "current_stage": 5
    })
    expect("first_skill 5단계 → mission-frame", out["first_skill"] == "vision-mission-frame")
    expect("first_skill 반복 사용자 → deep_grill", out["depth_mode"] == "deep_grill")

    # 비전 있음·단계 8
    out = grill_lib.decide_first_skill({
        "visit_count": 5, "has_diagnosis": True, "has_vision_statement": True, "current_stage": 8
    })
    expect("first_skill 8단계 → five-stages", out["first_skill"] == "vision-five-stages")

    # 빈 입력
    out = grill_lib.decide_first_skill(None)
    expect("first_skill None → 기본 권장", out["first_skill"] == "vision-cys-competence-visioncoding")


def test_track_user_state():
    """사용자 상태 추적 — isolated temp file."""
    saved = grill_lib.USER_STATE_PATH
    with tempfile.TemporaryDirectory() as tmp:
        grill_lib.USER_STATE_PATH = os.path.join(tmp, "user_state.json")
        try:
            # read — 빈 상태
            out = grill_lib.track_user_state("read")
            expect("track read 초기 상태", out["ok"] and out["state"]["visit_count"] == 0)

            # increment_visit
            out = grill_lib.track_user_state("increment_visit")
            expect("track increment 1차", out["state"]["visit_count"] == 1)
            out = grill_lib.track_user_state("increment_visit")
            expect("track increment 2차", out["state"]["visit_count"] == 2)

            # mark_completed (진단 스킬)
            out = grill_lib.track_user_state("mark_completed", skill="vision-cys-competence-visioncoding")
            expect("track 진단 스킬 mark → has_diagnosis=True", out["state"]["has_diagnosis"] is True)
            expect("track 진단 스킬 mark → completed 포함",
                   "vision-cys-competence-visioncoding" in out["state"]["completed_skills"])

            # mark_completed (일반 스킬)
            out = grill_lib.track_user_state("mark_completed", skill="vision-clarity-coaching")
            expect("track 일반 스킬 mark", "vision-clarity-coaching" in out["state"]["completed_skills"])

            # set_vision_statement
            out = grill_lib.track_user_state("set_vision_statement")
            expect("track 비전 선언문 설정", out["state"]["has_vision_statement"] is True)

            # set_stage
            out = grill_lib.track_user_state("set_stage", stage=5)
            expect("track 단계 5 설정", out["state"]["current_stage"] == 5)
            # 범위 밖 → clip
            out = grill_lib.track_user_state("set_stage", stage=99)
            expect("track 단계 99 → 8로 clip", out["state"]["current_stage"] == 8)

            # 잘못된 action
            out = grill_lib.track_user_state("unknown_action")
            expect("track 잘못된 action 차단", not out["ok"])

            # mark_completed 빈 skill
            out = grill_lib.track_user_state("mark_completed", skill="")
            expect("track 빈 skill 차단", not out["ok"])

            # reset
            out = grill_lib.track_user_state("reset")
            expect("track reset visit_count=0",
                   out["state"]["visit_count"] == 0 and not out["state"]["has_diagnosis"])
        finally:
            grill_lib.USER_STATE_PATH = saved


def test_scenario_expand_topic_inject():
    out = grill_lib.scenario_expand("강남 아파트 매도")
    expect("scenario 주제 치환 5년", "강남 아파트 매도" in out["scenarios"][0]["prompt"])
    expect("scenario 주제 치환 10년", "강남 아파트 매도" in out["scenarios"][1]["prompt"])
    expect("scenario 주제 치환 실패", "강남 아파트 매도" in out["scenarios"][2]["prompt"])
    expect("scenario 주제 치환 기회비용", "강남 아파트 매도" in out["scenarios"][3]["prompt"])

    # 빈 주제 → '이 결정'
    out = grill_lib.scenario_expand("")
    expect("scenario 빈 주제 → 이 결정", "이 결정" in out["scenarios"][0]["prompt"])


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
    test_select_honorific()
    test_render_ldr_body()
    test_render_definition_and_quote()
    test_english_lookup()
    test_seed_standard_glossary()
    test_validate_context_integrity()
    test_validate_ldr_chain()
    test_route_intake()
    test_decide_first_skill()
    test_track_user_state()
    test_scenario_expand_topic_inject()

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
