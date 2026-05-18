---
name: vision-foresight-wild-cards-implications-synthesis
disable-model-invocation: true
description: |
  ## TLDR — Wild Cards Sub-skill ⑦ Implications Synthesis. Petersen & Steinmüller(2009) V3.0 10장 통합 합성 + Section II "Extraordinary Implications"·Section IV Strengths/Weaknesses·Section VI Frontiers 풀 구현 **INTERNAL** sub-skill (final stage). PDF 핵심 verbatim: "The study of Wild Cards is particularly important now because the extraordinary growing technological capability of humans has produced, starting a few decades ago, new classes of Wild Cards. For the first time, Wild Cards have global implications. In some cases scientists believe they could potentially threaten the whole human race." 4 핵심 산출 — ① Domain별 implications (Step 0 사용자 선택 도메인) ② 78+55 catalogue cross-reference final mapping ③ Section IV Weakness disclaimer 자동 첨부 ④ Section VI Frontiers options 자동 제안 (Wild Card databases·Internet portals·early warning systems·iKnow·Surprise Anticipation Centers). PDF "Possible Implications" 4-axis Petersen 양식 (REALITY·HABITAT·ACTIVITY·GROUP RELATIONSHIPS) verbatim 적용. AI Senior Wild Card Synthesizer Agent 자동 작동.

  ## Triggers — INTERNAL sub-skill. 마스터 vision-foresight-wild-cards가 Cycle C1~C8 모든 cycle 마지막 단계에서 자동 호출. 사용자 직접 호출 불가 (disable-model-invocation: true). 호출 시점: Step 7 (모든 sub-skill output 통합). 호출 트리거 키워드 (마스터 내부): 'wild card implications', 'extraordinary implications', 'global implications', 'whole human race threat', 'wild card synthesis', 'wild card final report', 'wild card cross-reference 78 55', 'wild card section IV weakness', 'wild card section VI frontiers', 'iKnow Wild Card database', 'Surprise Anticipation Center Arlington Singapore', 'reality habitat activity group relationships implications', 'wild card net effect summary', 'possible implications wild card'.

  ## Detailed Methodology — Petersen & Steinmüller(2009) 10장 전체 통합 합성 + PDF "EXAMPLE OF USE: EXTRAORDINARY WEST COAST NATURAL DISASTER" p.19 양식 "POSSIBLE IMPLICATIONS" 4-axis (REALITY·HABITAT·ACTIVITY·GROUP RELATIONSHIPS) 정확 replicate + Section IV Strengths/Weaknesses 자동 disclaimer + Section VI Frontiers 옵션 (Wild Card databases·Internet portals collecting/assessing·early warning systems·iKnow·Surprise Anticipation Centers Arlington Institute Singapore RAHS post-crisis 양식). AI Senior Wild Card Synthesizer Agent 자동 작동 — ① 사전 sub-skill 5-6개 output 통합 (identification·assessment·impact-index·monitoring·options-action·optional scenario-integration) ② Step 0 Implications Domain 적용 — 10 domain 중 사용자 선택 또는 Skip ③ Top N Wild Cards 종합 implications matrix (Petersen "Possible Implications" 4-axis 양식) ④ Hidden swing WCs 식별 (high I_AI + low foresight factor 조합) ⑤ 78+55 catalogue cross-reference final map ⑥ Section IV Weakness disclaimer 자동 ⑦ Section VI Frontiers options 제안 + cross-skill chain. VRMP L1~L6 cascade 강제. 결정론 연산 전부 _helpers.py에 위임.
---

# Wild Cards — Implications Synthesis Sub-skill (INTERNAL)

> **출처**: Petersen & Steinmüller (2009), Wild Cards, *Futures Research Methodology V3.0*, Chapter 10, 전체 통합 + Section II Extraordinary Implications + Section IV Strengths/Weaknesses + Section VI Frontiers + Example of Use p.19 "POSSIBLE IMPLICATIONS" 4-axis.

본 sub-skill은 마스터 `vision-foresight-wild-cards` 내부에서만 호출 (final stage, 모든 cycle). AI Senior Wild Card Synthesizer가 외부 통합 분석가·정책 작가 완전 대체.

> **결정론 위임 원칙**: 본 SKILL.md에서 계산·검증·집계가 필요한 모든 단계는 LLM 자연어 재추론 금지. 반드시 `_helpers.py`를 Bash로 실행하고 그 JSON 결과를 output에 직접 삽입한다.

---

## 0. 입력 전제조건 (Input Prerequisites)

본 sub-skill 실행 전 마스터가 반드시 전달해야 할 데이터:

| 항목 | 필수 여부 | 출처 sub-skill |
|------|-----------|---------------|
| `domain_selection` (1-10, Custom, Skip, 또는 미입력) | 권장 | Step 0 사용자 입력 |
| `cycle` (C1-C8) | 필수 | 마스터 실행 컨텍스트 |
| `top_wc_list` (WC 목록 JSON, I_AI·foresight_factor 포함) | 필수 | assessment + monitoring sub-skill |
| `identification_output` | 권장 | identification sub-skill |
| `assessment_output` | 필수 | assessment sub-skill |
| `impact_index_output` | 필수 | impact-index sub-skill |
| `monitoring_output` | 필수 | monitoring sub-skill |
| `options_action_output` | 권장 | options-action sub-skill |
| `scenario_integration_output` | 선택 | scenario-integration sub-skill |
| `analysis_date` (YYYY-MM-DD) | 권장 | 마스터 메타데이터 (없으면 오늘 날짜 사용) |

**입력 누락 처리**: Section 11 (오류 및 예외처리) 참조. 입력 0개이면 즉시 `INPUT_MISSING` 반환, 진행 불가.

---

## 1. 역할 정의

당신은 **Senior Wild Card Synthesizer AI**다. 5-6개 sub-skill output을 통합하고, PDF Section II "Extraordinary Implications"·Section IV·Section VI + Example "POSSIBLE IMPLICATIONS" 4-axis 양식 verbatim으로 최종 산출물을 합성한다.

PDF verbatim (Chapter 10, Section II — Extraordinary Implications):
> *"The study of Wild Cards is particularly important now because the extraordinary growing technological capability of humans has produced, starting a few decades ago, new classes of Wild Cards. For the first time, Wild Cards have global implications. In some cases scientists believe they could potentially threaten the whole human race."*

> *"Global Reach: With increased global integration comes the increased 'reach' — or breadth of impact — of Wild Cards. Furthermore, the boundaries of fields in which Wild Cards would traditionally be placed are rapidly breaking down."*

> *"Scope in time: Wild Cards, called 'futurequakes' by Steinmüller, exert a direct effect on the future – a 'habitat' of our hopes, fears, wishes, plans, and expectations."*

---

## 2. "POSSIBLE IMPLICATIONS" 4-Axis Petersen 양식 (PDF p.19 verbatim)

PDF Example "EXTRAORDINARY WEST COAST NATURAL DISASTER" verbatim:

```
┌─────────────────────────────────────────────────────────────────┐
│ POSSIBLE IMPLICATIONS                                            │
├──────────────────────────────┬──────────────────────────────────┤
│ REALITY                       │ ACTIVITY                          │
│ Tremendous blow to the        │ A large portion of the U.S.       │
│ American psyche; return to    │ economy would be affected.        │
│ survival values.              │                                   │
├──────────────────────────────┼──────────────────────────────────┤
│ HABITAT                       │ GROUP RELATIONSHIPS               │
│ In every case a major loss    │ Possible large scale civil        │
│ of human and animal life      │ disorder.                          │
│ would occur.                  │                                   │
└──────────────────────────────┴──────────────────────────────────┘
```

**본 sub-skill은 각 top Wild Card 마다 이 4-axis 양식 자동 채움**:

| Axis | 의미 | 적용 영역 예시 |
|------|------|--------------|
| **REALITY** | 인식·가치관·세계관 shift — 사회 규범·신뢰·심리 변화 | 문화·심리·종교·이념·가치관 |
| **HABITAT** | 물리·생태·기술 환경 변화 — 자연환경·도시구조·인프라 | 환경·도시공간·물리적 생존조건 |
| **ACTIVITY** | 일·경제·사회 활동 변화 — 생산방식·소비패턴·사회실천 | 경제·노동·교육·의료·이동 |
| **GROUP RELATIONSHIPS** | 사회 구조·권력 관계·집단 역학 shift | 정치·국제관계·사회계층·기관구조 |

**4-axis 작성 규칙** (할루시네이션 방지):
1. 각 axis마다 **최소 2개** 구체적 함의 서술
2. 추측 진술은 반드시 "could", "may", "might"로 한정 — 단정 금지
3. sub-skill output 기반 내용은 `[assessment]`, `[monitoring]` 태그 부착
4. 학습지식만으로 작성 시 `[R-3]` 태그 + "학습지식 기반, 검증 권장" 주석 필수
5. 수치·통계는 VRMP L1/L4 실증 필수 — 추정 단정 금지

---

## 3. Implications Domain User Selection 적용

마스터 Step 0에서 사용자가 선택한 domain에 따라 implications synthesis 톤·강조점 변경.

**결정론 검증 (LLM 판단 금지)**:
```bash
python3 skills/vision-foresight-wild-cards-implications-synthesis/_helpers.py validate_domain "[사용자 입력값]"
# 반환 예: {"domain": "5", "auto_skip": false}
# 범위 외 입력 예: {"domain": "Skip", "auto_skip": true, "original": "11"}
```

| Domain | 톤 | 핵심 frame |
|--------|----|-----------|
| 1. Personal Decision-Making | 1인칭 reflective | individual preparedness |
| 2. Family / Household | "우리 가족" framing | household resilience |
| 3. Career / Profession | professional identity | career pivots |
| 4. Small Business / Startup | entrepreneurial | pivot·resilience·new venture |
| 5. Corporate Strategy | board-level | strategic options |
| 6. Investment / Asset Allocation | portfolio framing | hedge·exposure |
| 7. Public Policy / Governance | policy memo | regulation·preparedness |
| 8. Academic Research | scholarly | research agenda |
| 9. NGO / Civil Society | mission-driven | advocacy·preparedness |
| 10. Religious / Pastoral | spiritual/value | hope·values·community resilience |
| Custom | 사용자 지정 | 맞춤 프레임 |
| Skip | neutral | domain-agnostic |

**[선택 질문 자동 yes] 정책**: 사용자 응답 없을 시 Skip 자동 적용.

---

## 4. Hidden Swing Wild Cards 식별

### 용어 정의 (결정론적 임계값 — LLM 재추론 절대 금지)

**I_AI (Arlington Impact Index)**
- 출처: assessment sub-skill이 부여한 복합 충격 점수
- 산식: `I_AI = round(P × B × S / 5, 2)` — P=발생확률(1-5), B=충격범위(1-5), S=전개속도(1-5)
- 최대값: 25 (`5×5×5/5 = 25`)
- 임계값 **18** = 고충격 구간 기준선
  - 근거: Petersen, J.L. (1997). *Out of the Blue: Wild Cards and Other Big Future Surprises*. Arlington Institute Press. Impact index framework.
  - 주의: 임계값 18의 정확한 백분위 수치는 assessment sub-skill이 P·B·S 분포에 따라 결정. 본 스킬에서 LLM이 별도로 백분위를 추정하거나 진술하는 것 금지.

**foresight_factor (조기경보 가시성 등급)**
- 출처: monitoring sub-skill이 부여한 관측가능성 등급
- 척도: A(매우 가시적·조기경보 용이) → F(사실상 불감지·조기경보 불가)
  - A: 공개 지표·데이터 존재, 모니터링 용이
  - B: 지표 일부 존재, 전문 관측 필요
  - C: 약신호 포착 가능, 전문가 해석 필요
  - D: 약신호 포착 어려움, 전문가 네트워크 필수
  - E: 신호 사실상 없음, 시나리오 사후분석만 가능
  - F: 완전 불감지, 발생 후에야 인지 가능
- 임계값: **D-F** = 조기경보 불가 구간

### 결정론 실행

`top_wc_list.json` 파일을 마스터로부터 수신 후:

```bash
python3 skills/vision-foresight-wild-cards-implications-synthesis/_helpers.py filter_hidden_swing top_wc_list.json
```

반환 JSON 예:
```json
{
  "hidden_swing_wcs": [
    {"id": "WC-003", "title": "...", "I_AI": 21, "foresight_factor": "E"},
    {"id": "WC-007", "title": "...", "I_AI": 19, "foresight_factor": "F"}
  ],
  "n_hidden_swing": 2,
  "missing_score_wcs": ["WC-005"],
  "errors": [],
  "threshold": {"I_AI": 18, "foresight": ["D", "E", "F"]}
}
```

**주의**: `missing_score_wcs`에 WC ID가 있으면 output에 `MISSING_SCORE` 주석 명시. I_AI 또는 foresight_factor 미제공 WC는 hidden_swing 판정 불가 처리.

**원리**: 영향 크고 (I_AI ≥ 18) 모니터링 가시성 낮은 (foresight D-F) WCs가 가장 위험·시급한 대응 대상.

---

## 5. 78+55 Catalogue Cross-Reference Final Map

**중요 고지**: 아래 ID 형식(P-EAS-06 등)은 구조 예시(illustrative template)다. 실제 분석 시 마스터가 전달한 WC list + Petersen·Steinmüller 원문 대조로 매핑. 대조 불확실하면 `invented`로 분류 + 근거 명시. Catalogue ID 임의 생성(hallucination) 절대 금지.

```yaml
catalogue_cross_reference:
  petersen_78_used:
    # 실제 분석 시 마스터 전달 데이터와 Petersen(2009) catalogue 대조 후 채움
    # 예시 구조:
    - id: "P-EAS-06"
      title: "Extraordinary West Coast Natural Disaster"
      adapted_to: "WC-007"
      confidence: "high"   # high | medium | low
    - id: "P-BIO-02"
      title: "Worldwide Epidemic"
      adapted_to: "WC-003"
      confidence: "medium"

  steinmuller_55_used:
    # 실제 분석 시 Steinmüller(2009) catalogue 대조 후 채움
    - id: "S-Tek-12"
      title: "[대조 후 실제 제목 기입]"
      adapted_to: "WC-005"
      confidence: "medium"

  newly_invented:
    # Petersen 78·Steinmüller 55 미수록 신규 WC
    - id: "WC-010"
      title: "[실제 제목]"
      novelty_justification: "[두 catalogue 미수록 근거 + 현재 기술·사회 변화 반영 설명]"

  # ─── 결정론 계산 (LLM 재추론 금지) ───────────────────────────────
  # p_count = len(petersen_78_used), s_count = len(steinmuller_55_used), inv_count = len(newly_invented)
  # bash: python3 skills/vision-foresight-wild-cards-implications-synthesis/_helpers.py coverage_ratio [p] [s] [inv]
  catalogue_coverage_ratio:
    petersen: "[_helpers.py coverage_ratio 결과]"
    steinmuller: "[_helpers.py coverage_ratio 결과]"
    invented: "[_helpers.py coverage_ratio 결과]"
    total: "[_helpers.py coverage_ratio 결과]"
```

---

## 6. Section IV Weakness Disclaimer (PDF p.11 verbatim 자동 첨부)

```markdown
## Weaknesses (PDF Section IV — 본 분석에 자동 첨부)

1. **Far-fetched 거부감** (PDF: "Most Wild Cards seem to be – at least at first glance – far-fetched, implausible or even utterly impossible.")
   → 본 분석 mitigation: AI multi-perspective (5 identification method + 4 expert mode) 적용으로 다각 검증.

2. **Counterintuitive 결론** (PDF: "These conclusions are often counterintuitive or in contradiction to well-established convictions.")
   → 본 분석 mitigation: VRMP 6-계층 source trail로 검증성 확보.

3. **Vague concept** (PDF: "Some problems stem from the vagueness of the concept of Wild Card itself.")
   → 본 분석 mitigation: 3 Surprise Types (1/2/3) + Wild Card vs Weak Signal 명확 구분 강제.

4. **Monitoring 후속작업** (PDF: "this method does not lend itself to monitoring for the actual occurrence of Wild Cards.")
   → 본 분석 mitigation: monitoring sub-skill로 Early Warning System spec + trip-wire 자동 생성.

5. **Heterogeneous WCs** (PDF: "The method may also produce a large amount of very heterogeneous Wild Cards that require varying methods of monitoring and analysis.")
   → 본 분석 mitigation: Arlington Impact Index + 4-axis implications 양식으로 normalize.

6. **Organizational acceptance** (PDF: "Wild Card approaches may not fit very well into the organizational environment of a company or administration.")
   → 본 분석 mitigation: options-action sub-skill 9-step institutional process + 3 Basic Rules로 실행 가능 구조.

7. **VRMP Tier disclosure** (본 스킬 추가 protocol):
   모든 output 첫 줄에 `[R-1·R-2·R-3]` Tier 표시 필수.
   - **R-1** = WebSearch / WebFetch 실증 정보 기반 (인용 가능 출처 확보)
   - **R-2** = foresight-expert-pool 추론 + 학계 주류 문헌 지지 (간접 검증)
   - **R-3** = 학습지식만 사용 (최후 수단 — 반드시 고지, "학습지식 기반" 명시)
   → 출처 없는 판정 자동 FAIL. 각 함의 진술에 출처 Tier 태그 부착 필수.

8. **L2 keyword saturation** (본 스킬 추가 protocol):
   VRMP L2 검색 결과가 L1과 90% 이상 중복이면 **SEARCH_SATURATED: L2** 선언 → 추가 검색 중단 → 현 수집 범위로 합성 진행.
   Output meta에 `search_saturation_flag: true` 명시.

9. **L3 reverse validation** (본 스킬 추가 protocol):
   VRMP L3 반박 검색("wild card no-action critique", "implications overstatement", "futurequake criticism")에서 수집된 반론을 최종 output의 `counter_narrative` 항목에 **반드시** 포함.
   반론이 발견되지 않으면 "L3 검색에서 유의미한 반론 미발견" 명시 (생략 불가).
```

---

## 7. Section VI Frontiers Options (PDF p.13 verbatim 자동 제안)

```markdown
## Frontiers (PDF Section VI — 본 분석에 자동 제안)

PDF verbatim: *"From the methodological point of view, recent developments are based mainly on information technology. They include:"*

### Option F-1: Wild Card Database 구축
- 박사님 단행본·정책 메모 series 누적 → AGI WC database
- 78+55 catalogue + invented WCs 합본 + impact index history

### Option F-2: Internet Portal Collecting + Assessing
- iKnow EU — 원문 URL: www.iknowfutures.com
  **주의**: 이 URL은 EU 프로젝트(2008–2013) 기간 중 활성화됨. 현재 접속 가능 여부 불명. 대안: https://iknowfutures.eu 또는 EU IST 아카이브 확인. VRMP L4에서 접속 상태 보고 필수.
- Public-facing portal 또는 박사님 내부 portal

### Option F-3: Early Warning System for Weak Signals
- monitoring sub-skill output 활용
- 자동 Web crawl + RSS + prediction market integration

### Option F-4: Surprise Anticipation Center
- Arlington Institute (Petersen) + Singapore Government RAHS (Ngoh & Hoo 2008) 양식
  - 참고: Ngoh, L.H. & Hoo, W.L. (2008). Singapore's Risk Assessment Horizon Scanning (RAHS).
- 박사님 아시아미래인재연구소 surprise anticipation unit 옵션

### Option F-5: Cross-skill Chain (Frontier integration)
- vision-foresight-environmental-scanning weak-signal-template 연동
- foresight-cross-impact-analysis (Wild Cards as events)
- vision-foresight-futures-wheel (Wild Card impact wheel)
- foresight-tech-mining (Tech WCs from patent·publication mining)
- foresight-delphi / foresight-realtime-delphi (WC voting·assessment)
- foresight-trend-impact-analysis (TIA event override)
- foresight-expert-pool (Petersen·Steinmüller·Wack·Aaltonen·Mendonça·Hiltunen)
```

---

## 8. Output 양식

output 생성 전 반드시 다음 결정론 계산을 **순서대로** 실행한다. 각 단계 결과를 다음 단계에 사용한다. LLM 직접 계산·추정 금지.

```bash
SKILL=skills/vision-foresight-wild-cards-implications-synthesis

# 0. top_wc_list 준비 — 마스터 전달 WC 목록을 JSON 파일로 저장
# (Claude가 마스터로부터 받은 WC 목록을 아래 형식으로 /tmp/top_wc_list.json에 저장)

# 1. domain 검증 → domain 값 확정
python3 "$SKILL/_helpers.py" validate_domain "[마스터가 전달한 domain_selection]"
# 결과: {"domain": "...", "auto_skip": true|false}

# 2. count summary → n_petersen_78_used, n_steinmuller_55_used, n_invented 확정
python3 "$SKILL/_helpers.py" count_summary /tmp/top_wc_list.json
# 결과: {"n_total": N, "n_petersen_78_used": P, "n_steinmuller_55_used": S, "n_invented": I}

# 3. coverage ratio — Step 2 결과의 P, S, I 값을 사용
python3 "$SKILL/_helpers.py" coverage_ratio [P] [S] [I]
# 결과: {"petersen": 0.XX, "steinmuller": 0.XX, "invented": 0.XX, ...}

# 4. hidden swing 필터
python3 "$SKILL/_helpers.py" filter_hidden_swing /tmp/top_wc_list.json
# 결과: {"hidden_swing_wcs": [...], "n_hidden_swing": N, "missing_score_wcs": [...], ...}

# 5. next review date
python3 "$SKILL/_helpers.py" next_review_date "[analysis_date or 오늘 날짜]"
# 결과: {"next_review_date": "YYYY-MM-DD", ...}
```

모든 `[...]` 플레이스홀더는 위 결정론 실행 결과로 채운다.

```yaml
implications_synthesis_output:
  meta:
    vrmp_tier: "[R-1 | R-2 | R-3]"   # 첫 줄 필수 — VRMP L6 합성 후 확정
    domain: "[validate_domain 결과]"
    domain_auto_skip: "[true | false]"
    cycle: "[C1~C8 — 마스터 전달값]"
    analysis_date: "[YYYY-MM-DD]"
    n_top_wild_cards: "[count_summary 결과 n_total]"
    n_hidden_swing: "[filter_hidden_swing 결과 n_hidden_swing]"
    n_petersen_78_used: "[count_summary 결과]"
    n_steinmuller_55_used: "[count_summary 결과]"
    n_invented: "[count_summary 결과]"
    missing_score_wcs: "[filter_hidden_swing 결과 missing_score_wcs]"
    search_saturation_flag: "[false | true — L2 90% 중복 시 true]"

  per_wild_card_implications:
    - wc_id: "WC-001"
      title: "[마스터 전달값]"
      I_AI: "[assessment sub-skill 전달값 — 숫자 | MISSING_SCORE]"
      foresight_factor: "[monitoring sub-skill 전달값 — A~F | MISSING_SCORE]"
      possible_implications:
        reality: "[최소 2개 함의. 출처 태그 포함. 추측은 could/may/might 한정]"
        habitat: "[최소 2개 함의. 출처 태그 포함]"
        activity: "[최소 2개 함의. 출처 태그 포함]"
        group_relationships: "[최소 2개 함의. 출처 태그 포함]"
      domain_specific_implications: "[Step 0 domain 적용 결과 — domain=Skip이면 domain-agnostic 중립]"
      hidden_swing_flag: "[filter_hidden_swing 결과: true | false]"
      catalogue_ref:
        petersen: "[P-XXX-NN | null]"
        steinmuller: "[S-XXX-NN | null]"
        invented: "[WC ID | null]"
        confidence: "[high | medium | low]"
      counter_narrative: "[L3 reverse 결과. 없으면 'L3 검색에서 유의미한 반론 미발견' 명시]"
    # ... (top N WC 전부 동일 구조로 채움)

  hidden_swing_wcs:
    # filter_hidden_swing 결과를 그대로 삽입
    - id: "[WC ID]"
      title: "[제목]"
      I_AI: "[값]"
      foresight_factor: "[등급]"
      risk_note: "[왜 가장 위험한지 1-2문장]"

  catalogue_cross_reference:
    # Section 5 YAML 구조 채움
    petersen_78_used: [...]
    steinmuller_55_used: [...]
    newly_invented: [...]
    catalogue_coverage_ratio:
      petersen: "[coverage_ratio 결과]"
      steinmuller: "[coverage_ratio 결과]"
      invented: "[coverage_ratio 결과]"
      total: "[coverage_ratio 결과 total]"

  weakness_disclaimer:
    # ⚠️ 아래 9개 항목 전체를 실제 텍스트로 output에 직접 생성. 항목 번호 참조·코드 목록 금지.
    item_1_far_fetched: |
      PDF(p.11): "Most Wild Cards seem to be – at least at first glance – far-fetched,
      implausible or even utterly impossible." → 본 분석 mitigation: AI multi-perspective
      (5 identification method + 4 expert mode) 적용으로 다각 검증.
    item_2_counterintuitive: |
      PDF(p.11): "These conclusions are often counterintuitive or in contradiction to
      well-established convictions." → mitigation: VRMP 6-계층 source trail로 검증성 확보.
    item_3_vague: |
      PDF(p.11): "Some problems stem from the vagueness of the concept of Wild Card itself."
      → mitigation: 3 Surprise Types + Wild Card vs Weak Signal 명확 구분 강제.
    item_4_monitoring: |
      PDF(p.11): "this method does not lend itself to monitoring for the actual occurrence
      of Wild Cards." → mitigation: monitoring sub-skill Early Warning System + trip-wire 생성.
    item_5_heterogeneous: |
      PDF(p.11): "The method may also produce a large amount of very heterogeneous Wild Cards."
      → mitigation: Arlington Impact Index + 4-axis implications 양식으로 normalize.
    item_6_organizational: |
      PDF(p.11): "Wild Card approaches may not fit very well into the organizational environment."
      → mitigation: options-action sub-skill 9-step process + 3 Basic Rules로 실행 가능 구조.
    item_7_vrmp_tier: |
      본 스킬 추가: 모든 output 첫 줄에 [R-1/R-2/R-3] Tier 표시 필수.
      R-1=WebSearch/WebFetch 실증 | R-2=expert-pool 추론+학계 지지 | R-3=학습지식(최후수단).
      출처 없는 판정 자동 FAIL.
    item_8_l2_saturation: |
      본 스킬 추가: VRMP L2 결과가 L1과 90%+ 중복이면 SEARCH_SATURATED: L2 선언 →
      추가 검색 중단 → 현 수집 범위로 합성 진행. meta.search_saturation_flag: true 기록.
    item_9_l3_reverse: |
      본 스킬 추가: VRMP L3 반박 검색 결과를 counter_narrative 항목에 반드시 포함.
      반론 미발견 시 "L3 검색에서 유의미한 반론 미발견" 명시 (생략 불가).

  frontiers_options:
    # ⚠️ F-1~F-5 각각의 실제 설명 텍스트를 output에 직접 생성. 코드 목록·참조 금지.
    F_1_database: |
      PDF 기반: Wild Card Database 구축 — 박사님 단행본·정책 메모 누적 → AGI WC database.
      78+55 catalogue + invented WCs 합본 + impact index history 아카이브 구축.
    F_2_portal: |
      PDF 기반: Internet Portal Collecting + Assessing — iKnow EU 양식 참조
      (원문 URL www.iknowfutures.com, 현재 접속 가능 여부 불명; VRMP L4 확인 필수).
      Public-facing portal 또는 내부 portal 구축.
    F_3_early_warning: |
      PDF 기반: Early Warning System for Weak Signals — monitoring sub-skill output 활용.
      자동 Web crawl + RSS + prediction market integration. trip-wire 자동 알림 시스템.
    F_4_surprise_center: |
      PDF 기반: Surprise Anticipation Center — Arlington Institute(Petersen) +
      Singapore RAHS(Ngoh & Hoo 2008) 양식. 조직 내 surprise anticipation unit 설치 옵션.
    F_5_cross_skill: |
      Cross-skill Chain integration: vision-foresight-environmental-scanning (weak-signal),
      foresight-cross-impact-analysis (WC as events), vision-foresight-futures-wheel (impact wheel),
      foresight-tech-mining (patent·publication mining), foresight-delphi/realtime-delphi
      (WC voting), foresight-trend-impact-analysis (TIA event override),
      foresight-expert-pool (Petersen·Steinmüller·Wack·Aaltonen·Mendonça·Hiltunen).

  counter_narrative_summary: |
    [L3 전체 반론 통합 요약. 발견된 반론이 없으면 'L3 검색에서 유의미한 반론 미발견' 명시]

  cross_skill_chain_recommendations:
    # ⚠️ 분석된 WC 주제와 domain에 맞춰 tailored. 고정 목록 금지.
    # 우선순위 선정 기준:
    #   기술·과학 WC → foresight-tech-mining 우선
    #   사회·정치 WC → foresight-structural-analysis 우선
    #   기후·생태 WC → foresight-cross-impact-analysis 우선
    #   hidden_swing 多 → foresight-delphi (확률 검증) 우선
    - "[주제 맞춤 skill 1]: [이유 1문장]"
    - "[주제 맞춤 skill 2]: [이유 1문장]"
    - "[주제 맞춤 skill 3]: [이유 1문장]"

  master_synthesis_summary:
    vrmp_tier: "[R-1 | R-2 | R-3]"   # 첫 줄 필수
    one_line_findings: "[한 줄 핵심 발견 — domain + top WC + hidden swing 결합]"
    top_3_critical_wcs: ["WC-001", "WC-003", "WC-007"]
    priority_actions:
      - "[즉시 조치 — hidden swing 대응]"
      - "[단기 조치 — monitoring 강화]"
      - "[중기 조치 — cross-skill 연계]"
    next_review_date: "[next_review_date 결과 — analysis_date + 90일]"
    source_trail:
      - "[R-1] Source 1: [출처 명칭, URL 또는 저자·연도]"
      - "[R-2] Source 2: [출처 명칭]"
      - "[R-3] Source 3: [학습지식 기반 — 검증 권장]"
```

---

## 9. VRMP 6-계층 cascade

**실행 원칙**: 상위 계층에서 충분한 정보를 얻으면 하위 계층 생략 가능. 단 L6 (합성)은 항상 실행.

| 계층 | 명칭 | 검색어·실행 내용 | 할루시네이션 방지 규칙 |
|------|------|----------------|----------------------|
| **L1** | 1차 WebSearch | `"wild card implications [domain]"`, `"extraordinary implications futures [연도]"`, `"[WC 제목] implications"` | 검색 결과 원문 인용 필수 — paraphrase·재창조 금지. 검색 실패 시 `[SEARCH_FAIL: L1]` 명시 |
| **L2** | 포화 WebSearch | `"global wild card 2025"`, `"futurequake recent [domain]"`, `"wild card database"`, `"[WC 제목] impact analysis"` | L1과 90% 이상 중복 → `SEARCH_SATURATED: L2` 선언, 추가 검색 중단. meta에 saturation_flag: true 기록 |
| **L3** | 역검증 WebSearch | `"wild card no-action critique"`, `"implications overstatement"`, `"futurequake criticism"`, `"[WC 제목] overrated"` | 반론 수집 후 `counter_narrative` 항목 필수 채움. 반론 없어도 결과 명시 (생략 불가) |
| **L4** | WebFetch 원문 | Petersen 1997 인용 페이지 · Steinmüller 2003 · iKnow 아카이브 · Arlington Institute · Singapore RAHS | URL 접속 실패 시 `[FETCH_FAIL: URL]` 명시 후 다음 레이어 진행. 전부 실패 시 `ALL_FETCH_FAIL` 기록 |
| **L5** | foresight-expert-pool | **호출 형식**: `Skill(foresight-expert-pool, query="[WC 제목] implications — domain:[domain] — experts: Petersen, Steinmüller, [주제 관련 전문가 2-3명]")`. **응답 통합**: 각 전문가 관점을 `[Expert: 이름]` 태그로 source_trail에 추가. **expert-pool 미응답 시**: `[Expert-pool: no response — R-2 적용]` 명시 후 R-2 Tier 강제. **최소 1개 이상** 전문가 관점 생성 필수 (실제 invocation 또는 R-2 추론). |
| **L6** | 합성 | 전 계층 수집 정보 통합 → source_trail (R-1·R-2·R-3 Tier 첫 줄) + counter_narrative 통합 | **출처 없는 판정 자동 FAIL.** 문헌 page 번호 포함 — 확인 불가 시 `p.[?]` 표시. 통계·수치는 L1/L4 실증 필수 |

**추가 anti-hallucination 규칙**:
- "Petersen 78개", "Steinmüller 55개" — V3.0 PDF 원문 확인 필수. 불확실 시 `[미확인]` 표시
- iKnow URL 접속 결과 반드시 보고 (활성·만료·리디렉션 구분)
- 출처 있는 주장과 추론 주장을 명확히 분리: `[출처: X]` vs `[추론: R-2]`

---

## 10. 산출 후 마스터에 반환

```python
return {
    "implications_synthesis_output": { ... },  # Section 8 schema 전체
    "vrmp_tier": "R-1" | "R-2" | "R-3",
    "source_trail": [ ... ],
    "counter_narrative": "...",
    "next_skill": None   # final stage — master integrates all
}
```

마스터는 이 output을 Step 3.7 섹션으로 표시 후 §4 마스터 통합 Synthesis로 진행.

---

## 11. 오류 및 예외처리

모든 오류 코드는 마스터에 JSON으로 반환한다. LLM이 자의적으로 복구 시도 금지 — 오류 코드만 반환하고 마스터 판단을 구한다.

| 상황 | 처리 방법 | 반환 코드 |
|------|---------|---------|
| 마스터가 sub-skill output **0개** 전달 | SKIP 선언 즉시 반환 | `INPUT_MISSING` |
| 마스터가 sub-skill output **1-2개만** 전달 | 경고 플래그 + 가용 데이터로 **제한** 합성 진행 | `INCOMPLETE_INPUT` |
| `top_wc_list` 비어있음 (빈 배열 []) | 합성 불가 선언, 마스터에 반환 | `EMPTY_WC_LIST` |
| `domain_selection` 범위 외 (1-10/Custom/Skip 외) | Skip 자동 적용 (`_helpers.py validate_domain`) | *(auto-corrected)* |
| `hidden_swing_wcs` 결과 0개 | "해당 없음" 명시, 항목 생략 — 오류 아님 | *(normal)* |
| catalogue ID 불일치 | `invented` 카테고리 분류 + 수동 검토 요청 메모 | `CATALOGUE_MISMATCH` |
| VRMP L1 검색 전체 실패 | L2-L6 진행, `[SEARCH_FAIL: L1]` 명시 | `SEARCH_FAIL_L1` |
| VRMP L1-L4 모두 실패 | R-3 학습지식 fallback 허용, 반드시 R-3 Tier 고지 | `ALL_SEARCH_FAIL` |
| WebFetch URL 모두 실패 | `ALL_FETCH_FAIL` 명시, L5-L6 진행, R-2 Tier 강제 | `ALL_FETCH_FAIL` |
| `I_AI` 또는 `foresight_factor` 미제공 WC | hidden_swing 판정 생략, `MISSING_SCORE` 주석 | `MISSING_SCORE` |
| `_helpers.py` 실행 실패 (파일 없음·오류) | 합성 **중단** — 결정론 계산 수동 대체 불허 | `HELPER_ERROR` |
| cycle 값 C1-C8 범위 외 | `INVALID_CYCLE` 명시, 마스터 재전달 요청 | `INVALID_CYCLE` |
| analysis_date 형식 오류 | 오늘 날짜 자동 사용, `[DATE_FALLBACK: today]` 주석 | *(auto-corrected)* |

---

## 12. 자기검증 체크리스트 (산출 전 필수)

본 sub-skill은 output 생성 직후 아래 항목을 순서대로 자기검증한다. 하나라도 FAIL이면 해당 항목 수정 후 재출력.

| # | 체크 항목 | PASS 조건 |
|---|---------|---------|
| 1 | VRMP Tier 표시 | output 첫 줄에 `[R-1]` / `[R-2]` / `[R-3]` 있음 |
| 2 | 결정론 계산 실행 | domain·hidden_swing·coverage_ratio·next_review_date 전부 `_helpers.py` 결과로 채움 |
| 3 | 4-axis 충족 | 각 WC마다 REALITY·HABITAT·ACTIVITY·GROUP RELATIONSHIPS 4개 모두 존재 |
| 4 | per-axis 최소 2개 | 각 axis에 최소 2개 함의 서술 있음 |
| 5 | counter_narrative | 각 WC 및 summary에 `counter_narrative` 항목 존재 (비어있어도 사유 명시) |
| 6 | weakness_disclaimer | Section 6 항목 1-9 실제 텍스트 전문이 output에 직접 생성됨 (항목 번호 목록·참조 금지) |
| 7 | frontiers_options | F-1~F-5 각 옵션의 실제 설명 텍스트가 output에 직접 생성됨 (코드 목록·참조 금지) |
| 11 | L5 expert-pool | 최소 1개 이상 전문가 관점 `[Expert: 이름]` 또는 `[Expert-pool: no response]` 명시 |
| 8 | source_trail | 최소 1개 이상 출처 있음 (R-3만 있으면 고지 필수) |
| 9 | hallucination 단어 | 단정 진술에 출처 없는 것 없음 |
| 10 | next_review_date | `_helpers.py` 결과로 채워진 ISO 날짜 형식 있음 |
