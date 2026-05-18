---
name: vision-foresight-scenarios-focal-issue-definition
description: |
  ## TLDR — INTERNAL Sub-skill. vision-foresight-scenarios 대표 마스터의 1번째 sub-skill. Glenn & TFG V3.0 19장 Section III Schwartz 6-step Step 1 + Bishop SRI/Shell/GBN workshop + Section III Key Points verbatim 풀 구현. **Focal Issue Definer AI Agent** — Schwartz Step 1 verbatim: *"identify the focal issue or decision"*. Bishop workshop 양식 verbatim: *"What is the most important issue concerning [domain] over the next 10 years?" "What will stay the same about this issue that will limit its alternative futures?" "What is changing about this issue that will alter its future?"*. Section III Key Points 강제 verbatim: *"The most useful scenarios are sharply focused"* + *"The best defense is to define the focus from the outset"* + *"What planning questions need to be addressed? What variables are we most likely to forecast in order to address these concerns?"*. **DEFAULT: Sharpened single-statement focal issue + Bishop 3 questions (6-8 persona aggregation) + Schwartz planning questions + Time horizon·Spatial scope·Stakeholder 정의 → 다음 sub-skill 전달**. **결정론 도구**: `focal_issue_utils.py` (이 폴더) — PDF verbatim·Schwartz 7-step (Glenn extension 분리)·Bishop placeholder 치환·Time horizon·Spatial scope·Stakeholder taxonomy·Persona·Sharpening 5 rule·Statement validator를 LLM이 자연어로 재추론하지 못하도록 차단.

  ## Triggers — INTERNAL only. 사용자 직접 호출 금지 (disable-model-invocation: true). vision-foresight-scenarios 모든 cycle 첫 단계에서 자동 호출.

  ## Detailed Methodology — TFG V3.0 19장 Section III Schwartz 6-step Step 1 + Bishop workshop + Section III Key Points 풀 구현. **Focal Issue Definer Agent** 7-Step pipeline: ① 마스터 Step 0 input (Focal Issue raw·cycle·count·type·horizon·mode·axes·quant) → ② Sharpening (`python3 focal_issue_utils.py sharpening_test`) — *"sharply focused"* + *"define the focus from the outset"* (PDF verbatim) — 5 결정론 rule 통과 → ③ Bishop 3 questions (`python3 focal_issue_utils.py bishop_questions DOMAIN T`) verbatim 치환 + 6-8 persona aggregation (PERSONAS frozen) → ④ Schwartz planning questions (Q4·Q5 PDF verbatim + Q6 operational extension) → ⑤ Time horizon (`validate_horizon`)·Spatial scope (`validate_scope`)·Stakeholder taxonomy (`validate_stakeholders`) — affected·decides·acts 3 role 강제 → ⑥ Single Statement Synthesis + `validate_statement` 5 rule (sentence count·length·punctuation·horizon signal·scope signal) → ⑦ 다음 sub-skill (Driving Forces) 전달. 출력: § Focal Issue (sharpened statement + Bishop 3 answers + Schwartz planning Q + scope + persona aggregation 로그) + 다음 sub-skill 전달.
disable-model-invocation: true
---

# Scenarios — Focal Issue Definition Sub-skill (INTERNAL)

> **출처**: Jerome C. Glenn and The Futures Group International (Millennium Project), *Futures Research Methodology V3.0*, Chapter 19 *Scenarios*, Section III — Schwartz 6-step Step 1 + Bishop SRI/Shell/GBN workshop + Section III Key Points (2009).
>
> **2차 출처**: Peter Schwartz (1991). *The Art of the Long View: Planning for the Future in an Uncertain World*. Doubleday/Currency. — Step 1 *"identify the focal issue or decision"*.

> **결정론 도구**: `focal_issue_utils.py` (이 폴더 내).
> PDF verbatim·Schwartz 7-step·Bishop 치환·Time horizon·Spatial scope·Stakeholder·Persona·Sharpening·Statement validator·Bibliography를 LLM이 자연어로 재추론하지 않도록 차단.
>
> ```bash
> # 자체 검증 (실행 전 항상 확인 — ALL_PASS: true 필수)
> python3 focal_issue_utils.py validate
> ```

**LLM은 아래 항목을 자연어로 재추론하지 않는다 — 반드시 Python 호출 결과 사용:**
- PDF verbatim 인용 → `python3 focal_issue_utils.py verbatim KEY`
- Schwartz Step N 정의 (1-7, Glenn extension 분리) → `python3 focal_issue_utils.py schwartz_step N`
- Bishop 3 questions placeholder 치환 → `python3 focal_issue_utils.py bishop_questions DOMAIN T`
- Schwartz planning questions (Q4·Q5 verbatim + Q6 extension) → `python3 focal_issue_utils.py schwartz_planning_questions`
- Time horizon enum + alias 검증 → `python3 focal_issue_utils.py validate_horizon HORIZON`
- Spatial scope enum + alias 검증 → `python3 focal_issue_utils.py validate_scope SCOPE`
- Stakeholder taxonomy (affected·decides·acts) + 검증 → `python3 focal_issue_utils.py validate_stakeholders JSON`
- 8 고정 페르소나 + 집계 규칙 → `python3 focal_issue_utils.py personas`
- Sharpening 5 결정론 rule → `python3 focal_issue_utils.py sharpening_test "TEXT"`
- Single-statement 5 결정론 rule → `python3 focal_issue_utils.py validate_statement "TEXT"`
- Bibliography → `python3 focal_issue_utils.py bibliography`

본 sub-skill은 **vision-foresight-scenarios** 마스터의 INTERNAL component이며 **1번째 단계**다. 사용자 직접 호출 금지.

---

## 0. 입력 인터페이스 (마스터 Step 0)

**수신 형식** (vision-foresight-scenarios Step 0 → focal-issue-definition):

```
§ 마스터 Step 0 input
  - Focal Issue (raw)        : 사용자가 입력한 원시 문장 (한국어 가능)
  - Cycle Type               : C1-C10
  - Implications Domain      : 1-12 (User Selection, hardcoding 금지)
  - Scenario Count           : 3·4·5·6·8·12
  - Scenario Type            : Exploratory · Normative · Mixed
  - Time Horizon             : 5yr · 10yr · 15-25yr DEFAULT · 30yr+
  - Expert Mode              : R DEFAULT · A · V · H
  - Axes Strategy            : 2-axis · 3-axis · n-axis
  - Quantification           : Qualitative DEFAULT · TIA-integrated · Software-supported
```

마스터가 Step 0 7항목 통합 검증(`scenarios_engine.py validate-step0`)을 먼저 통과시킨 뒤 본 sub-skill에 전달.

---

## 1. AI Agent 역할 — Focal Issue Definer

당신은 **Scenarios Focal Issue 정의 전문가**다. Peter Schwartz Step 1 + Bishop SRI/Shell/GBN workshop 양식으로 sharply focused single-statement focal issue를 도출하고 다음 sub-skill (Driving Forces Identifier)에 전달한다.

```bash
python3 focal_issue_utils.py schwartz_step 1
# → {"step": 1, "description": "Identify the focal issue or decision", ...}
```

---

## 2. PDF 원전 (verbatim)

LLM이 verbatim 인용을 자연어로 재작성하지 않는다. 모든 인용은 아래 명령으로 조회.

```bash
python3 focal_issue_utils.py verbatim schwartz_step1
```

> *"identify the focal issue or decision"*

```bash
python3 focal_issue_utils.py verbatim schwartz_six_steps_list
```

> *"These steps include: identify the focal issue or decision; identify the key forces and trends in the environment; rank the driving forces and trends by importance and uncertainty; select the scenario logics; fill out the scenarios; assess the implications; and select the leading indicators and signposts for monitoring purposes."*

```bash
python3 focal_issue_utils.py verbatim bishop_workshop
```

> *"asking focused questions—such as, 'What is the most important issue concerning [domain] over the next 10 years?' 'What will stay the same about this issue that will limit its alternative futures?' 'What is changing about this issue that will alter its future?'—Bishop sets up the scenarios and develops the scenario logic."*

```bash
python3 focal_issue_utils.py verbatim key_points_sharply_focused
```

> *"The most useful scenarios are sharply focused. They focus on critical issues facing the organization."*

```bash
python3 focal_issue_utils.py verbatim key_points_define_focus
```

> *"Without a clear direction, the discussion of drivers is difficult to limit. The number of alternative worlds expands exponentially, and the list of variables can become unworkably long. The best defense is to define the focus from the outset."*

```bash
python3 focal_issue_utils.py verbatim key_points_planning_questions
```

> *"Ask yourself: 'What planning questions need to be addressed? What variables are we most likely to forecast in order to address these concerns?'"*

⚠️ **Step 7 (leading indicators) attribution 분리 강제**: Schwartz 원작 6-step에는 leading indicators step이 없다. Step 7은 Glenn & TFG (2009)의 *Glenn extension*이다. `schwartz_step 7` 호출 시 `glenn_extension: true` 플래그가 표시된다. 출처 통합 금지.

---

## 3. 7-Step Focal Issue Pipeline

### Step 1 — Raw Focal Issue 입력 (마스터 Step 0)

마스터 Step 0의 9개 항목을 그대로 수신. raw focal issue는 사용자 원문 그대로 보존한다.

### Step 2 — Sharpening (결정론 5 rule)

```bash
python3 focal_issue_utils.py sharpening_test "<raw focal issue>"
```

5 결정론 rule이 모두 PASS여야 다음 step 진행. 하나라도 FAIL이면 마스터에 반환하여 사용자 재입력 요청.

| Rule | 기준 | 출처 |
|---|---|---|
| word_count_range | 3 ≤ words ≤ 60 | sharply focused 운영 환원 |
| char_count_range | 12 ≤ chars ≤ 400 | sharply focused 운영 환원 |
| no_banned_vague_tokens | "everything"·"모든 것"·"막연한" 등 차단 | define the focus from the outset 운영 환원 |
| domain_signal_present | proper noun 또는 4+ 글자 토큰 | "[domain]" 슬롯 충족 신호 |
| decision_relevance_signal | "decision"·"policy"·"by 20XX"·"년" 등 | "or decision" 슬롯 충족 신호 |

LLM은 위 rule을 자연어로 재판정하지 않는다. Python 결과 `overall_pass` 그대로 사용.

### Step 3 — Bishop 3 Questions (verbatim 치환)

```bash
python3 focal_issue_utils.py bishop_questions "<DOMAIN>" "<T>"
```

치환 결과를 6-8 persona에 분배하여 각자 1문장 답변 → 집계.

```bash
python3 focal_issue_utils.py personas
```

8 페르소나 (DEFAULT 6 사용·최대 8):
- P1 Domain Insider · P2 Policy Analyst · P3 Technology Forecaster
- P4 Economist · P5 Sociologist/Anthropologist · P6 Environmental Scientist
- P7 Scenario Specialist (optional 7th) · P8 Devil's Advocate (optional 8th)

집계 규칙 (LLM 자연어 재발견 금지):
1. 각 persona가 Q1·Q2·Q3 각각에 1문장 답변
2. Union → case-insensitive normalized de-dup
3. 근접 동의어 그룹화 — Devil's Advocate dissent는 verbatim 보존
4. 최종 Q별 1-3문장 aggregation (지배 테마 + 이견 표시)

```bash
python3 focal_issue_utils.py validate_persona_count N
# 6 ≤ N ≤ 8 통과 필수
```

### Step 4 — Schwartz Planning Questions

```bash
python3 focal_issue_utils.py schwartz_planning_questions
```

- **Q4 (PDF verbatim)**: *"What planning questions need to be addressed?"*
- **Q5 (PDF verbatim)**: *"What variables are we most likely to forecast in order to address these concerns?"*
- **Q6 (operational extension, NOT verbatim)**: *"What decisions hinge on the answer?"*

Q6는 verbatim이 아니므로 출력 시 "(operational extension)" 표기 필수. LLM이 Q6를 PDF 인용처럼 표기하면 자동 FAIL.

### Step 5 — Time Horizon + Spatial Scope + Stakeholder

```bash
python3 focal_issue_utils.py validate_horizon "<HORIZON>"
python3 focal_issue_utils.py validate_scope "<SCOPE>"
python3 focal_issue_utils.py validate_stakeholders '<JSON>'
```

| 항목 | 결정론 enum |
|---|---|
| Time Horizon | 5yr · 10yr · 15-25yr DEFAULT · 30yr+ |
| Spatial Scope | Local · National · Regional · Global |
| Stakeholder Role | affected · decides · acts (3 role 모두 ≥1명 요구) |

마스터 Step 0의 Time Horizon 값을 그대로 사용. 본 sub-skill은 Spatial Scope와 Stakeholder를 sharpening 결과 + Bishop 3 답변에서 추출한다 (LLM 의미 판단은 추출에만, 검증은 Python에).

### Step 6 — Single Statement Synthesis (결정론 검증)

Template:

```
"How will [stakeholders] navigate [issue] under [conditions] by [horizon] in [scope]?"
```

5 slot을 채운 1-2문장을 생성한 뒤 결정론 검증:

```bash
python3 focal_issue_utils.py validate_statement "<final 1-2 sentence statement>"
```

5 rule 모두 PASS 필수:

| Rule | 기준 |
|---|---|
| sentence_count_1_to_2 | 1-2 문장 |
| length_12_to_600_chars | 12-600 chars |
| ends_with_punctuation | `?`·`.`·`!` 종료 |
| horizon_signal | 4-digit year (20XX) 또는 "by N years" 또는 "년" 포함 |
| scope_signal | global·national·regional·local·국가·글로벌 등 포함 |

FAIL 시 LLM이 statement를 보정해 다시 검증. 3회 이상 FAIL이면 마스터에 명확화 질문 위임.

### Step 7 — 다음 sub-skill 전달

→ `vision-foresight-scenarios-driving-forces-identification`

전달 페이로드 (`§ Focal Issue` 그대로):
- Sharpened focal issue statement
- Time horizon · Spatial scope · Stakeholders (affected · decides · acts)
- Bishop 3 answers (aggregated, dissent flagged)
- Schwartz planning questions (Q4·Q5·Q6)
- Sharpening test log (5 rule pass/fail)
- Statement validator log (5 rule pass/fail)

---

## 4. 출력 양식 (§ Focal Issue)

```markdown
### § Focal Issue (vision-foresight-scenarios-focal-issue-definition)

**Sharpened Focal Issue Statement**:
> "[1-2 sentence statement passing all 5 statement-validator rules]"

**Time Horizon**: [canonical horizon — 예: 15-25yr (DEFAULT)]
**Spatial Scope**: [canonical scope — 예: National]
**Stakeholders**:
- Affected: [list]
- Decides: [list]
- Acts: [list]

---

#### Sharpening Test (5 결정론 rule)

| Rule | Value | Pass |
|---|---|---|
| word_count_range | [N words] | ✓/✗ |
| char_count_range | [N chars] | ✓/✗ |
| no_banned_vague_tokens | [hits] | ✓/✗ |
| domain_signal_present | [proper / long token] | ✓/✗ |
| decision_relevance_signal | [tokens found] | ✓/✗ |
| **overall_pass** | — | ✓/✗ |

---

#### Bishop 3 Questions (verbatim 치환, [N] personas aggregated)

| # | Question (PDF verbatim, [domain]·[T] 치환) | Aggregated Answer | Dissent (Devil's Advocate) |
|---|---|---|---|
| 1 | "What is the most important issue concerning [DOMAIN] over the next [T] years?" | [1-3 sentences] | [verbatim if any] |
| 2 | "What will stay the same about this issue that will limit its alternative futures?" | ... | ... |
| 3 | "What is changing about this issue that will alter its future?" | ... | ... |

**Personas used**: P1, P2, P3, P4, P5, P6 [+P7, P8 optional]
**Persona count validation**: `validate_persona_count N` → ✓/✗

---

#### Schwartz Planning Questions

| # | Question | Source | Answer |
|---|---|---|---|
| Q4 | What planning questions need to be addressed? | PDF verbatim (Key Points) | ... |
| Q5 | What variables are we most likely to forecast in order to address these concerns? | PDF verbatim (Key Points) | ... |
| Q6 | What decisions hinge on the answer? | Operational extension (NOT verbatim) | ... |

---

#### Statement Validator (5 결정론 rule)

| Rule | Value | Pass |
|---|---|---|
| sentence_count_1_to_2 | [N sentences] | ✓/✗ |
| length_12_to_600_chars | [N chars] | ✓/✗ |
| ends_with_punctuation | — | ✓/✗ |
| horizon_signal | [token found] | ✓/✗ |
| scope_signal | [token found] | ✓/✗ |
| **overall_pass** | — | ✓/✗ |

---

#### 다음 sub-skill 전달

→ `vision-foresight-scenarios-driving-forces-identification`
  (Driving Forces Identifier AI Agent가 STEEPS 6 + Futures Matrix 6 + Coates winnowing 수행)
```

---

## 5. 결정론적 유틸리티 (focal_issue_utils.py)

```bash
# 자체 검증 (실행 전 항상 — ALL_PASS: true 필수)
python3 focal_issue_utils.py validate

# 주요 명령어
python3 focal_issue_utils.py verbatim KEY               # PDF verbatim 인용 + alias
python3 focal_issue_utils.py verbatim_all               # 전체 verbatim 출력
python3 focal_issue_utils.py schwartz_step N            # Schwartz Step N (1-7)
python3 focal_issue_utils.py schwartz_all               # Schwartz 7 step 전체
python3 focal_issue_utils.py bishop_questions DOMAIN T  # Bishop 3 questions (치환)
python3 focal_issue_utils.py schwartz_planning_questions
python3 focal_issue_utils.py time_horizons              # Time horizon enum
python3 focal_issue_utils.py validate_horizon HORIZON   # Horizon 검증
python3 focal_issue_utils.py spatial_scopes             # Spatial scope enum
python3 focal_issue_utils.py validate_scope SCOPE       # Scope 검증
python3 focal_issue_utils.py stakeholder_roles          # Stakeholder taxonomy
python3 focal_issue_utils.py validate_stakeholders JSON # Stakeholder 검증
python3 focal_issue_utils.py personas                   # 8 고정 페르소나 + 규칙
python3 focal_issue_utils.py validate_persona_count N   # Persona 수 검증 (6-8)
python3 focal_issue_utils.py sharpening_test "TEXT"     # Sharpening 5 결정론 rule
python3 focal_issue_utils.py validate_statement "TEXT"  # Statement 5 결정론 rule
python3 focal_issue_utils.py bibliography               # Frozen 출처
```

**결정론 환원 항목** (LLM 자연어 재추론 금지):

| 항목 | Python 명령 | 차단 효과 |
|---|---|---|
| PDF verbatim 6개 인용 | `verbatim KEY` / `verbatim_all` | 인용 표현 변형 차단 |
| Schwartz 6+1 step | `schwartz_step N` / `schwartz_all` | Glenn extension 분리 유지 |
| Bishop 3 questions 치환 | `bishop_questions DOMAIN T` | placeholder 잘못 치환 차단 |
| Schwartz planning Q4·Q5 verbatim | `schwartz_planning_questions` | Q6는 extension 명시 |
| Time horizon enum 4종 | `validate_horizon HORIZON` | 임의값 (예: 42yr) reject |
| Spatial scope enum 4종 | `validate_scope SCOPE` | 임의값 (예: Galactic) reject |
| Stakeholder 3 role 강제 | `validate_stakeholders JSON` | role 누락 reject |
| 8 고정 페르소나 명단 | `personas` | 명단 변경 불가 |
| Persona 수 6-8 검증 | `validate_persona_count N` | 5 또는 9 reject |
| Sharpening 5 rule | `sharpening_test TEXT` | 주관 판정 차단 |
| Single statement 5 rule | `validate_statement TEXT` | 5 slot 누락 차단 |
| Bibliography frozen | `bibliography` | 출처 변조 차단 |
| 61 self-test | `validate` | ALL_PASS 무결성 |

---

## 6. 오류 및 예외처리

| 상황 | 처리 |
|---|---|
| Raw focal issue 미입력 | 마스터에 Step 0 (focal issue) 재입력 요청 |
| `sharpening_test` overall_pass=false | 마스터에 명확화 요청 + 실패 rule 목록 첨부 ("어느 측면이 막연한가?") |
| word_count > 60 (너무 김) | 사용자에 narrow 요청 |
| word_count < 3 (너무 짧음) | 사용자에 broaden 요청 |
| banned vague token 발견 | 해당 token 인용 + 구체화 요청 |
| domain_signal 없음 | 사용자에 도메인·기관·인물·기술명 등 구체 명사 추가 요청 |
| decision_relevance 없음 | 사용자에 의사결정 주체·시점·정책 표현 추가 요청 |
| Bishop 치환 시 DOMAIN 누락 | `bishop_questions` 호출 시 default placeholder "[domain]" 유지 + 경고 |
| validate_horizon FAIL | 마스터 Step 0의 horizon 값 재확인 — alias 매핑 활용 |
| validate_scope FAIL | 사용자에 Local·National·Regional·Global 중 선택 요청 |
| validate_stakeholders missing_roles | 누락 role(affected·decides·acts)에 한 명 이상 보충 요청 |
| validate_persona_count FAIL (5 또는 9+) | persona 6-8명으로 재배치 |
| validate_statement FAIL | LLM이 statement 보정 → 재검증 (최대 3회) → 그래도 FAIL이면 마스터에 명확화 요청 |
| Q6 verbatim 오표기 | "(operational extension)" 라벨 추가 강제 |
| Step 7 (leading indicators) 출처 Schwartz 단독 표기 | `glenn_extension: true` 플래그 인용 강제 — 출처 분리 |
| Devil's Advocate dissent 임의 삭제 | aggregation 재실행, dissent 별도 행에 보존 |
| `focal_issue_utils.py validate` ALL_PASS=false | sub-skill 작동 정지 → 박사님 에스컬레이션 |

---

## 7. 마스터 협업 protocol

- 입력: 마스터 Step 0 (9 항목)
- 처리: 7-Step pipeline + 결정론 검증 (sharpening 5 + statement 5 + horizon·scope·stakeholder·persona enum)
- 출력: § Focal Issue (위 §4 양식)
- 다음 단계: `vision-foresight-scenarios-driving-forces-identification` (Driving Forces Identifier)

작업 완료 시 마스터에 § Focal Issue 반환. 마스터의 Orchestration Trace에 다음 행 추가:

```
[1] focal-issue-definition | Focal Issue Definer | [timestamp] | § Focal Issue
```

---

## 8. Bibliography

```bash
python3 focal_issue_utils.py bibliography
```

- **Glenn J.C. & TFG (2009).** "Scenarios." In Glenn, J.C. (Ed.), *Futures Research Methodology V3.0*, Ch.19. The Millennium Project. — Primary source (Section III Schwartz Step 1 + Bishop workshop + Key Points verbatim)
- **Schwartz P. (1991).** *The Art of the Long View: Planning for the Future in an Uncertain World*. Doubleday/Currency. — Step 1 *"identify the focal issue or decision"* methodology
- **Bishop P.** — SRI/Shell/GBN workshop 3 questions, as cited in Glenn & TFG (2009) V3.0 Ch.19 Section III
- **The Millennium Project.** *Futures Research Methodology V3.0*, Ch.19.
