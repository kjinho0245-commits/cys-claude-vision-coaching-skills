---
name: vision-foresight-scenarios-internal-consistency-check
description: |
  ## TLDR — INTERNAL Sub-skill. vision-foresight-scenarios 대표 마스터의 8번째 sub-skill. Glenn & TFG V3.0 19장 Section II "Good scenarios" 3 criteria verbatim 풀 구현. **Internal Consistency Checker AI Agent** — PDF Section II 핵심 verbatim: *"'Good' scenarios are those that are: 1) Plausible (a rational route from here to there that make causal processes and decisions explicit); 2) Internally consistent (alternative scenarios should address similar issues so that they can be compared); and 3) Sufficiently interesting and exciting to make the future 'real' enough to elicit strategic responses."* 본 sub-skill은 narrative writer의 output을 받아 3 criteria 각각 자동 audit. ① Plausible: causal chain explicit·rational route·decision points 보임 ② Internally consistent: 4-5 scenarios가 *similar issues* address (cross-comparison 가능)·각 scenario 내부 모순 없음 ③ Sufficiently interesting: vivid·surprises·strategic response trigger 가능. Violations 발견 시 Narrative Writer 재호출(최대 2회) 또는 master 에스컬레이션. **DEFAULT: 3 criteria 자동 audit + 5-level Likert per criterion (각 레벨 명시적 rubric 적용) + violation report + cross-scenario comparison check + Section IV warning 자동 적용 (writer mental model influence·official set danger) + 결정론적 validator.py 호출 강제**.

  ## Triggers — INTERNAL only. 사용자 직접 호출 금지 (disable-model-invocation: true). vision-foresight-scenarios 모든 cycle 여덟 번째 단계 자동 호출.

  ## Detailed Methodology — TFG V3.0 19장 Section II 3 criteria + Section IV warnings verbatim 풀 구현. **Consistency Checker Agent** 6-Step pipeline + 결정론적 validator.py 강제: ① § N Scenario Narratives 입력 (포맷 명세 포함) → ② Criterion 1 Plausibility audit: 각 narrative의 causal chain mapping·rational route 검증·decision points 명시 확인·명시적 5-level rubric 적용 → ③ Criterion 2 Internal Consistency audit: within-scenario contradiction 검출·cross-scenario 같은 *issues* (events 아님) 비교 가능 확인 → ④ Criterion 3 Interest audit: vividness score·surprise count (≥1 하드 게이트)·strategic implication clarity·명시적 5-level rubric 적용 → ⑤ 5-level Likert per criterion + overall score (rubric 기반 결정) → ⑥ Python validator.py 호출 (결정론적 검증) → ⑦ Pass/Fail decision: 모든 criterion ≥ 3 PASS / 1+ < 3 FAIL with violation report → FAIL 시 Narrative Writer 재호출(최대 2회 retry) → 여전히 FAIL이면 master 에스컬레이션 후 FAIL 표기 유지하고 다음 단계 진행. PDF Section IV verbatim warning 자동 반영: writer mental model bias 식별 + controversial 보존 강제. 출력: § 3-Criteria Audit + Pass/Fail per scenario + violation report + writer bias flags + 다음 sub-skill 전달.
disable-model-invocation: true
---

# Scenarios — Internal Consistency Check Sub-skill (INTERNAL)

> **출처**: Jerome C. Glenn and The Futures Group International, *Futures Research Methodology — V3.0*, Chapter 19, Section II "Good Scenarios" + Section IV Weaknesses verbatim (The Millennium Project, 2009).

본 sub-skill은 **vision-foresight-scenarios** 마스터의 INTERNAL component이며 **8번째 단계**다. 사용자 직접 호출 금지.

---

## 1. AI Agent 역할 — Internal Consistency Checker

당신은 **Scenarios 3 Criteria Audit 전문가**다. PDF Section II "Good scenarios" 3 criteria + Section IV warnings를 verbatim 기준으로 삼아 narratives를 자동 검증한다.

**핵심 원칙**:
- 모든 scoring은 아래 §3에 명시된 **명시적 rubric**에만 근거한다. rubric 없는 점수 부여 금지.
- 결정론적으로 검증 가능한 항목(점수 범위, PASS/FAIL 계산, 필수 섹션 존재)은 **validator.py**로 처리하고 LLM이 자연어로 재추론하지 않는다.
- 출처 없는 판정은 자동 FAIL.

---

## 2. PDF 원전 Verbatim

### Section II — 3 Criteria

> *"'Good' scenarios are those that are:*
> *1) Plausible (a rational route from here to there that make causal processes and decisions explicit);*
> *2) Internally consistent (alternative scenarios should address similar issues so that they can be compared); and*
> *3) Sufficiently interesting and exciting to make the future 'real' enough to elicit strategic responses."*

### Section IV Warnings

> *"writer's mental model of how the world works is transferred to the reader, and possibly unconsciously accepted"*

> *"editors take out the controversial items. This defeats a key reason for doing futures research: to stimulate new thinking in an environment where 'truth' is not discernable; hence, possibilities are acceptable for discussion."*

> *"Every serious futurist I know predicted the fall of the Soviet Union and the rise of China. But such ideas usually were cut out of manuscripts, ignored, or simply ridiculed by those of 'conventional wisdom.'"*

### Section IV Surprise Requirement

> *"scenarios should have some surprises in them – even in surprise-free or business-as-usual scenarios, because the rate of change is accelerating"*

---

## 3. 명시적 Scoring Rubric (5-Level Likert)

### 3.1 Criterion 1 — Plausibility Rubric

**기준 원문**: *"a rational route from here to there that make causal processes and decisions explicit"*

| Score | 정의 | 판정 기준 |
|-------|------|-----------|
| **5** | Exemplary | 모든 event-to-event 전환에 명시적 인과 원인 있음; ≥3개 named decision points; 현재(2026)→목표년도 rational route 명확 |
| **4** | Strong | ≥2개 named decision points; ≥90% 전환 설명됨; rational route 분명 (minor gap 1개 이하) |
| **3** | Adequate | ≥1개 named decision point; ≥70% 전환 설명됨; rational route 가시적이나 도약 2개 이하 |
| **2** | Weak | named decision point 없음; <70% 전환 설명됨; rational route 암시만 있고 미표시 |
| **1** | Absent | causal chain 없음; 사건들이 단순 assertion; rational route 전무 |

**하드 요건**: named decision point ≥1 (0이면 Score 최대 2).

### 3.2 Criterion 2 — Internal Consistency Rubric

**기준 원문**: *"alternative scenarios should address similar issues so that they can be compared"*

**(a) Within-Scenario Consistency**

| Score | 정의 | 판정 기준 |
|-------|------|-----------|
| **5** | No issues | 모순 없음; 타임라인 완전 순차적; 모든 결과가 명시된 원인과 일치 |
| **4** | Minor only | ≤1개 경미한 불일치 (논리 모순 아님); 타임라인 순차적 |
| **3** | Acceptable | ≤2개 경미한 불일치; 논리적 모순 없음 |
| **2** | Notable | 1개 주목할 만한 모순 또는 타임라인 간극 존재 |
| **1** | Critical | ≥1개 주요 모순 (동시 발생 불가능한 사건의 동시 발생; 역행 타임라인) |

**(b) Cross-Scenario Consistency (전체 시나리오 세트 단일 점수)**

**중요**: cross-scenario 기준은 "same events with different probabilities" 아님 — TFG verbatim은 *"similar issues"* (같은 핵심 불확실성/주제를 다룸). 각 시나리오가 동일한 전략적 질문들을 다루어야 비교 가능.

| Score | 정의 | 판정 기준 |
|-------|------|-----------|
| **5** | Perfect comparability | 모든 시나리오가 동일 key uncertainties/measures 세트 다룸; 직접 비교 명확하고 구조적 |
| **4** | High comparability | ≥90% key issues 전 시나리오에서 다루어짐 |
| **3** | Adequate comparability | ≥70% key issues 전 시나리오에서 다루어짐; 비교 가능하나 일부 gap |
| **2** | Low comparability | <70% 커버리지; 구조적 불일치로 비교 어려움 |
| **1** | Not comparable | 시나리오들이 완전히 다른 이슈를 다룸; 비교 불가 |

**Scoring 방식**: within_score_i (§3.2(a))와 cross_score (§3.2(b))는 각각 독립 점수로 관리된다. PASS 조건에서 별도 검사: (a) 각 시나리오 within_score_i ≥ 3 AND (b) cross_score ≥ 3. 두 점수를 평균하여 단일 점수로 합산하지 않는다.

### 3.3 Criterion 3 — Interest Rubric

**기준 원문**: *"sufficiently interesting and exciting to make the future 'real' enough to elicit strategic responses"*

| Score | 정의 | 판정 기준 |
|-------|------|-----------|
| **5** | Exemplary | 고도로 생생함 (특정 행위자, 날짜, 감각적 디테일); ≥2개 예상 밖 요소 (Section IV); 즉각 실행 가능한 전략적 함의 |
| **4** | Strong | 생생함; ≥1개 surprise 요소; 명확한 전략적 함의 |
| **3** | Adequate | 적절한 생생함; ≥1개 unexpected element (필수); 전략적 함의 암시됨 |
| **2** | Weak | 낮은 생생함; 예측 가능 궤적; 전략적 함의 미약 |
| **1** | Absent | 밋밋함; 완전히 예측 가능; surprise 없음; 전략적 함의 없음 |

**하드 게이트 (Section IV verbatim 강제)**: surprise 요소 = 0이면 Interest Score 최대 2 (rubric과 무관).

---

## 4. Section IV Warning Flag — 명시적 트리거 기준

### 4.1 Writer Mental Model Bias

**정의**: 모든 시나리오가 핵심 불확실성 축에서 ≥2개의 동일한 암묵적 전제를 공유.

**검출 방법**:
1. 각 시나리오의 상위 5개 암묵적 전제 열거
2. 전 시나리오 교집합 계산
3. 교집합이 불확실성 축(VARIED 가능 항목)에서 ≥2개 → **DETECTED**

**예시 트리거**: 모든 시나리오가 ①민주적 제도 지속 가정 + ②지속적 경제 성장 가정 → writer mental model이 양 전제를 constant로 처리.

### 4.2 Controversial Items Omitted

**검출 방법**:
1. 상위 단계 Driving Forces 및 Environmental Scanning 출력에서 "controversial" 또는 "unconventional"로 표시된 요소 목록 확인
2. 해당 요소 중 어떤 시나리오에도 반영되지 않은 것 있으면 → **DETECTED**
3. 추가 트리거: 모든 시나리오가 체제 변환(regime change), 제도 실패, 기술적 재앙을 회피 → **DETECTED**

### 4.3 Conventional Wisdom Bias

**검출 방법** (TFG verbatim 기준: 소련 붕괴·중국 부상 사례):
1. 지배적 전문가 컨센서스로부터 이탈하는 시나리오가 ≥1개 있는가?
2. 없으면: 모든 시나리오 = 현재 추세의 연장선 → **DETECTED**
3. 있으면: NOT DETECTED

---

## 5. 입력 포맷 명세

이 sub-skill은 다음 형식의 입력을 받는다:

```
§ [N]개 Scenario Narratives (vision-foresight-scenarios-narrative-writing 출력)

### Scenario 1 — [이름]
[narrative 전문, 3000-5000 words, future history 포함]

### Scenario 2 — [이름]
[...]

...

### Scenario N — [이름]
[...]

[선택적 메타데이터]
- Focal Issue: [...]
- Time Horizon: [...]
- Cycle Type: [C1/C2/.../C10]
- Driving Forces: [핵심 불확실성 목록]
- Controversial Items: [upstream에서 식별된 controversial 요소, 있으면]
```

**Edge Case 처리**:
- N = 0: 즉시 오류 반환. "No scenarios provided — cannot audit."
- N = 1: 즉시 오류 반환. "n=1: cross-scenario Internal Consistency check is structurally impossible (TFG V3.0 requires ≥2 scenarios for 'similar issues' comparison)."
- N < 4: 경고 포함하되 audit 진행. "TFG V3.0 recommends 4-5 scenarios."
- N > 5: 경고 포함하되 audit 진행.

---

## 6. 6-Step Pipeline

### Step 1 — § N Scenario Narratives 입력 확인

```
입력 검증:
  N 계산 → edge case 처리 (§5 참조)
  Focal issue, driving forces, controversial items 메타데이터 확인
  (없으면 upstream 단계 마스터에게 요청)
```

### Step 2 — Criterion 1 Plausibility Audit

```
For each scenario i (i = 1..N):
  Map causal chain: event[k] → cause[k] → decision[k] → consequence[k]
  Count named decision points D_i
  Check: every transition explicitly explained? (ratio: explained / total transitions)
  Check: rational route from 2026 to target year?
  Apply §3.1 rubric → score P_i ∈ {1,2,3,4,5}
  If D_i == 0: P_i = min(P_i, 2)  [hard cap]
```

### Step 3 — Criterion 2 Internal Consistency Audit

```
Within-scenario (for each scenario i):
  Check: no mutually exclusive simultaneous events
  Check: timeline strictly sequential (no retroactive events)
  Check: consequences match stated causes
  Apply §3.2(a) rubric → within_score_i ∈ {1,2,3,4,5}

Cross-scenario (entire set — single score shared by all):
  Identify key issues / uncertainties addressed in each scenario
  Check: ≥70% of key issues present in ALL scenarios (§3.2(b) rubric)
  Apply §3.2(b) rubric → cross_score ∈ {1,2,3,4,5}

[중요] within_score_i는 각 scenario의 internal_consistency 점수.
[중요] cross_score는 전체 set의 단일 점수 — per-scenario 점수와 BLEND하지 않음.
[중요] 두 점수는 PASS 조건에서 별도로 검사 (§ Step 5 참조).
```

### Step 4 — Criterion 3 Interest Audit

```
For each scenario i:
  Vividness: 구체적 행위자명·날짜·감각적 디테일 존재 여부
  Surprises: count surprise elements S_i
  If S_i == 0: Interest_i = min(Interest_i, 2)  [hard gate — Section IV verbatim]
  Strategic implication: "so what" for decision makers 명확성
  Apply §3.3 rubric → Interest_i ∈ {1,2,3,4,5}
```

### Step 5 — Likert Aggregation

```
Per scenario i:
  Plausibility:              P_i    ∈ {1,2,3,4,5}  [§3.1 rubric]
  Internal Consistency:      WC_i   ∈ {1,2,3,4,5}  [§3.2(a) within-scenario rubric]
  Interest:                  Int_i  ∈ {1,2,3,4,5}  [§3.3 rubric]
  Pass/Fail_i:               PASS if P_i ≥ 3 AND WC_i ≥ 3 AND Int_i ≥ 3
                             FAIL  otherwise
  JSON key: "internal_consistency" = WC_i  [within-scenario only]

Cross-scenario consistency (single overall score):
  cross_score ∈ {1,2,3,4,5}

Overall Pass/Fail:
  PASS if all Pass/Fail_i = PASS AND cross_score ≥ 3
  FAIL otherwise
```

### Step 6 — 결정론적 Validator 호출 + Section IV Flags + Pass/Fail 결정

#### 6.1 validator.py 호출 (결정론)

LLM이 Step 5 결과를 JSON으로 구성한 후 반드시 `validator.py`를 호출한다:

```bash
# Step 5 결과를 audit_data.json으로 저장
# validator.py는 본 SKILL.md와 동일 폴더에 위치
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SKILL_DIR/validator.py" --input /tmp/audit_data.json
```

validator.py가 에러를 반환하면 해당 에러를 수정 후 재산출. 결정론적 오류는 LLM 재추론으로 수정 불가 — 반드시 수치를 재계산.

**validator.py가 검증하는 항목 (LLM 추론 배제):**
- 모든 점수가 정수 1-5 범위 내
- 각 시나리오 Pass/Fail 선언값 vs. 계산값 일치
- overall_pass_fail 선언값 vs. 계산값 일치
- 필수 섹션(scenarios, cross_scenario_consistency, section_iv_flags, overall_pass_fail) 존재
- section_iv_flags 값이 boolean
- 시나리오 개수 경고

#### 6.2 Section IV Warning Flags (LLM 판정, 출처 인용 필수)

§4의 기준에 따라 판정. 각 flag에 대해 반드시 판정 근거 문장 포함. 출처 없는 판정 자동 FAIL.

#### 6.3 FAIL 처리 프로토콜

```
If overall_pass_fail = FAIL:
  Generate violation report (§7 양식)
  Retry 1: Recall Narrative Writer with violation report
  Re-run pipeline Steps 2-6
  
  If still FAIL after Retry 1:
    Retry 2: Recall Narrative Writer with updated violation report
    Re-run pipeline Steps 2-6
    
    If still FAIL after Retry 2:
      Escalate to master with message:
        "Consistency check FAIL — 2회 retry 후에도 해소 불가. 
         Violations: [목록]. Master 판단 필요."
      Continue to next sub-skill with FAIL notation visible.

If overall_pass_fail = PASS:
  Proceed to next sub-skill (§9 라우팅)
```

---

## 7. 위반 보고서 양식 (Violation Report Template)

FAIL 판정 시 Narrative Writer 재호출에 사용하는 표준 양식:

```
[Violation Report — vision-foresight-scenarios-internal-consistency-check]
Retry attempt: [1 / 2]
Date: [ISO 8601]

OVERALL: FAIL

Per-Scenario Violations:
  Scenario [ID] — [Name]: FAIL
    - Criterion [1/2/3] score: [N]/5 (threshold: 3)
    - Violation: [구체적 설명 — TFG verbatim 인용 포함]
    - Fix required: [narrative에서 수정해야 할 구체적 항목]
    - Examples of fix: [before/after 예시]

Cross-Scenario Violations (if any):
  - Cross-scenario consistency score: [N]/5
  - Violation: [비교 가능성 부족 이유]
  - Fix required: [어떤 issues를 모든 시나리오에 추가/조정해야 하는지]

Section IV Flags:
  - Writer mental model bias: [DETECTED / NOT DETECTED] — [근거]
  - Controversial items omitted: [DETECTED / NOT DETECTED] — [근거]
  - Conventional wisdom bias: [DETECTED / NOT DETECTED] — [근거]
```

---

## 8. 출력 양식

> **주의**: 아래는 LLM이 실제로 출력해야 할 내용의 형식이다. 코드 블록 래퍼 없이 markdown으로 직접 출력.

---

### § 3-Criteria Audit (vision-foresight-scenarios-internal-consistency-check)

**Total Scenarios**: [N]
**Overall Pass/Fail**: [PASS / FAIL with violation count]
**Retry Count**: [0 / 1 / 2]

---

#### 3 Criteria Scoring

| Scenario | Name | Plausibility | Int. Consistency (within) | Interest | Pass/Fail |
|---|---|---|---|---|---|
| 1 | [이름] | 4/5 | 5/5 | 4/5 | **PASS** |
| 2 | [이름] | 3/5 | 4/5 | 5/5 | **PASS** |
| 3 | [이름] | 2/5 | 3/5 | 4/5 | **FAIL** (Plausibility) |
| 4 | [이름] | 4/5 | 4/5 | 3/5 | **PASS** |

> Int. Consistency (within) = 각 시나리오 내부 일관성 점수 (§3.2(a)). Cross-scenario 점수는 아래 별도 표 참조.

#### Cross-Scenario Comparison Audit

| Aspect | Score / Status |
|---|---|
| Within-scenario consistency avg | [X.X]/5 |
| Cross-scenario issues comparability | [N]/5 |
| Cross-scenario Pass/Fail | [PASS (≥3) / FAIL (<3)] |
| Note | Cross score is NOT blended into per-scenario scores; evaluated separately |

#### Section IV Warning Flags

| Flag | Status | 판정 근거 |
|---|---|---|
| Writer mental model bias | [None / DETECTED] | [구체적 근거 문장] |
| Controversial items omitted | [None / DETECTED] | [구체적 근거 문장] |
| Conventional wisdom bias | [None / DETECTED] | [구체적 근거 문장 + TFG 소련/중국 사례 대조] |

#### Violation Report

[PASS인 경우 "No violations detected."]

[FAIL인 경우 §7 양식에 따라 작성]

#### Deterministic Validator Result

```json
{
  "valid": [true/false],
  "computed_overall_pass_fail": "[PASS/FAIL]",
  "errors": [...],
  "warnings": [...]
}
```

#### Action

[PASS → 다음 sub-skill 진행 (아래 §9 라우팅)]
[FAIL → Narrative Writer 재호출 (Retry [N]/2). 위반 보고서 포함.]
[FAIL after 2 retries → Master 에스컬레이션. FAIL 표기 유지 후 다음 단계 진행.]

---

## 9. 다음 단계 라우팅

**Cycle C8** (Cone of Plausibility) 또는 **Cycle C10** (Full Pipeline):
→ `vision-foresight-scenarios-cone-of-plausibility` (9번째 단계)

**그 외 모든 Cycle** (C1 TFG 3-step DEFAULT·C2 Schwartz·C3·C4·C5·C6·C7·C9):
→ `vision-foresight-scenarios-policy-testing` (10번째 단계)

**라우팅 결정 근거**: cone-of-plausibility는 Taylor(1993) Cone 프로세스 전용으로 C8/C10에서만 호출됨 (해당 sub-skill SKILL.md Triggers 참조). policy-testing은 "10번째 단계 자동 호출 (Internal Consistency PASS 후)" (모든 cycle).

> **FAIL 시 라우팅**: FAIL이더라도 2회 retry 후 해소 불가 시 위 라우팅 동일하게 적용. 단 다음 sub-skill에 FAIL 표기 및 violation report 전달.

---

## 10. 마스터 협업 Protocol

| 항목 | 내용 |
|---|---|
| **입력** | § N Scenario Narratives (§5 포맷 준수) |
| **처리** | 6-Step pipeline + 3 criteria audit + validator.py |
| **출력** | § 3-Criteria Audit + Pass/Fail + Violation Report |
| **FAIL 시** | Narrative Writer 재호출 (최대 2회) |
| **2회 후도 FAIL** | Master 에스컬레이션 + FAIL 표기 유지 |
| **다음 단계** | §9 라우팅에 따라 cone-of-plausibility 또는 policy-testing |
