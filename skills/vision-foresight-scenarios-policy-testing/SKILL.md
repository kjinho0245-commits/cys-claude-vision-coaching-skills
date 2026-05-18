---
name: vision-foresight-scenarios-policy-testing
description: |
  ## TLDR — INTERNAL Sub-skill. vision-foresight-scenarios 대표 마스터의 10번째 sub-skill. Glenn & TFG V3.0 19장 Section III TFG Reporting and Utilization "Testing policies" + Section II "dichotomize strategies between robust and contingent elements" verbatim 풀 구현. **Policy Tester AI Agent** — PDF 원전 verbatim: *"Testing policies. The range of scenarios can be used to test policies. In any study, a list of alternative actions is prepared. This list may come from the decision makers after reading the scenarios. Each is defined as precisely as possible. Then, using quantitative techniques if possible, the policies are 'tested' in each of the scenarios. When a particular policy produces desirable results in all cases, it is clearly a good bet. The other scenarios may give rise to contingent policies that can be called on if the circumstances develop that the scenarios depict."* Section II 8 활용 verbatim 중: *"dichotomize strategies between robust and contingent elements"*. **Robust strategies** = 모든/대부분 scenarios에서 desirable results / **Contingent strategies** = 특정 scenario circumstances trigger 시 활성. Section IV strength verbatim: *"reduces the need for specific five-, ten-, or fifteen-year point forecasts. As such, most planners find that a set of detailed long-term scenarios... greatly reduces the need and usefulness of multiple sets of equally detailed 'snapshots'"*. **DEFAULT: Policy list elicitation from decision makers·AI Agent persona·또는 사용자 직접 + each policy × each scenario test (qualitative + optional quantitative) + policy_scorer.py 결정론적 분류 + Robust vs Contingent 분류 + Top-K policy recommendation (K = 전체 Robust + 상위 Contingent 3개)**.

  ## Triggers — INTERNAL only. 사용자 직접 호출 금지 (disable-model-invocation: true). vision-foresight-scenarios 모든 cycle 열 번째 단계 자동 호출 (Internal Consistency PASS 후).

  ## Detailed Methodology — TFG V3.0 19장 Section III TFG Reporting + Section II 8 활용 + Section IV strengths verbatim 풀 구현. **Policy Tester Agent** 7-Step pipeline: ① § N Scenario Narratives + § 3-Criteria Audit (PASS) 입력 → ② Policy list 수집 — 마스터로부터 (또는 AI Agent persona 8명이 각 stakeholder 입장에서 alternative actions 제안) → ③ Each policy 명확화 — *"defined as precisely as possible"* (PDF verbatim) → ④ Policy × Scenario testing matrix — 각 policy를 각 scenario에서 simulation/qualitative assessment, **quantitative 우선** (cross-skill foresight-decision-modeling 13장 옵션) → ⑤ 5-point bipolar scale (-2 to +2) 점수화 후 **policy_scorer.py 결정론적 호출** (average·classification·ranking 모두 Python 계산) → ⑥ Robust vs Contingent 분류 — Robust = 모든/대부분 scenarios desirable / Contingent = 특정 scenario trigger 시 활성 / Reject = 지속적 비효과 → ⑦ Top-K policy recommendation + activation conditions (contingent) + 다음 sub-skill (Leading Indicators) 전달. PDF Section II 강조: *"identify what strategies might work across a range of possible scenarios"* + *"dichotomize strategies between robust and contingent elements"*. 출력: § Policy Testing Matrix + Robust vs Contingent classification + Top-K recommendations + activation conditions + 다음 sub-skill 전달.
disable-model-invocation: true
---

# Scenarios — Policy Testing Sub-skill (INTERNAL)

> **출처**: Glenn & TFG V3.0 19장 Section III TFG Reporting "Testing policies" + Section II 8 활용 verbatim.

본 sub-skill은 **vision-foresight-scenarios** 마스터의 INTERNAL component이며 **10번째 단계**다. 사용자 직접 호출 금지.

---

## 0. 입력 전제 조건 및 에러 처리

### 0-A. 필수 입력

| 필수 항목 | 확인 방법 | 미충족 시 처리 |
|---|---|---|
| § N Scenario Narratives | 본문에 N개 시나리오 명칭 + 내러티브 존재 | **HALT** — "시나리오 내러티브가 없습니다. vision-foresight-scenarios 단계를 먼저 실행하세요." |
| § 3-Criteria Audit 결과 | "PASS" 명시 | **HALT** — "3-Criteria Audit가 PASS되지 않았습니다. 감사 단계를 완료하세요." |
| 시나리오 수 ≥ 2 | N count | **HALT** — "의미있는 policy testing을 위해 시나리오가 최소 2개 필요합니다." |

### 0-B. Policy 수집 후 검증 (Step 2 완료 후)

```
IF policy_count == 0:
  → "정책 목록이 비어 있습니다. 최소 1개 이상의 정책을 입력하세요."
  → AI Agent Persona 모드로 자동 전환 (사용자 동의 후)

IF policy_count > 20:
  → "정책이 20개를 초과합니다. 상위 20개만 testing합니다. 우선순위 기준: [사용자 지정]"
```

### 0-C. 점수 입력 검증 (Step 4 완료 후 — policy_scorer.py 위임)

`policy_scorer.py --validate-only` 호출로 확인:
- 점수는 {-2, -1, 0, +1, +2} 집합에 속해야 함
- 각 정책의 점수 개수 = 시나리오 수
- 정책명 중복 금지

### 0-D. 예외 처리 규칙

| 예외 상황 | 처리 |
|---|---|
| policy_scorer.py 실행 오류 | Python 오류 메시지를 그대로 출력 후 "점수 데이터를 확인하세요." |
| 모든 정책이 REJECT | "모든 정책이 기각되었습니다. 새로운 정책 대안을 수집합니다." → Step 2 재실행 |
| Robust 정책 0개 | "Robust 정책이 없습니다. Contingent 정책 중 가장 높은 점수의 정책을 임시 권장합니다." |
| 3-Criteria Audit FAIL 전달 | **즉시 HALT**, 이유 명시 후 반환 |

---

## 1. AI Agent 역할 — Policy Tester

당신은 **Scenarios Policy Testing 전문가**다. Each policy를 each scenario에서 test하여 Robust vs Contingent 분류.

**핵심 원칙**: 점수 계산·분류·순위는 반드시 `policy_scorer.py`로 처리한다. LLM이 평균·분류·순위를 재추론하지 않는다.

---

## 2. PDF 원전 (verbatim)

> *"Testing policies. The range of scenarios can be used to test policies. In any study, a list of alternative actions is prepared. This list may come from the decision makers after reading the scenarios. Each is defined as precisely as possible. Then, using quantitative techniques if possible, the policies are 'tested' in each of the scenarios. When a particular policy produces desirable results in all cases, it is clearly a good bet. The other scenarios may give rise to contingent policies that can be called on if the circumstances develop that the scenarios depict."* (Section III TFG Reporting)

> *"identify what strategies might work across a range of possible scenarios"* (Section II 8 활용)

> *"dichotomize strategies between robust and contingent elements"* (Section II 8 활용)

---

## 3. 7-Step Pipeline

### Step 1 — Input 검증

```
체크리스트 (위 §0 기준):
  [ ] § N Scenario Narratives 존재 확인
  [ ] § 3-Criteria Audit "PASS" 확인
  [ ] 시나리오 수 ≥ 2 확인
  [ ] 시나리오 명칭 목록 추출 (policy_scorer.py 전달용)

통과 시 → Step 2
실패 시 → §0-A 에러 처리 적용 후 HALT
```

### Step 2 — Policy List 수집

**Source A: 사용자 제공** (최우선)
- 사용자가 직접 정책 목록을 제공한 경우 그것을 사용.

**Source B: AI Agent Persona 8명** (사용자 미제공 시)

| # | Persona | 입장 |
|---|---|---|
| 1 | Government/Regulator | 규제·법률·정책 집행 |
| 2 | Industry/Business | 비용·수익·시장 경쟁력 |
| 3 | Civil Society/NGO | 사회적 형평·권리·지속가능성 |
| 4 | Academic/Research | 증거 기반·장기 효과·부작용 |
| 5 | Financial/Investment | 자본 배분·리스크·수익률 |
| 6 | End Users/Citizens | 실질 편익·접근성·체감 |
| 7 | International/Global | 외교·글로벌 기준·국제 협력 |
| 8 | Technology/Innovation | 기술 가능성·혁신 속도·전환비용 |

각 Persona가 **1~3개** alternative actions 제안. 중복 유사 정책은 통합. 최종 정책 수: 8~20개 권장.

```
AI Persona 실행 시 할루시네이션 방지:
  - 각 정책 제안은 반드시 § N Scenario Narratives의 내용에 근거할 것
  - 시나리오에 없는 사실·트렌드를 자의적으로 발명하지 말 것
  - 구체적 수치(예산·시장규모 등)는 시나리오에 명시된 것만 인용할 것
```

### Step 3 — Each Policy 명확화

PDF verbatim "*defined as precisely as possible*":

각 정책에 대해 아래 5항목을 명시한다:

| 항목 | 설명 | 할루시네이션 방지 규칙 |
|---|---|---|
| Action description | 무엇을 하는가 (동사+목적어 형식) | 시나리오 내러티브에 근거 |
| Implementer | 누가 실행하는가 | 시나리오에 등장한 주체만 |
| Resources required | 자원·비용 (정성적 수준: 低/中/高) | 정량 수치 발명 금지 |
| Timeline | 단기(1-2년)·중기(3-5년)·장기(5+년) | 시나리오 시간축 기준 |
| Expected outcome | 목표 상태 | 측정 가능한 변화 기술 |

### Step 4 — Policy × Scenario Testing Matrix

#### 4-A. 정량 vs 정성 선택 기준

```
정량 (quantitative) 우선 조건 — 아래 중 하나 해당:
  - 시나리오에 수치 변수(GDP 성장률, 시장점유율, 도입률 등) 명시
  - cross-skill foresight-decision-modeling(13장) 결과 활용 가능
  - 정책의 효과가 계량 지표로 측정 가능

정성 (qualitative) 허용 조건:
  - 시나리오가 순전히 정성적 (사회·문화·가치관 변화 중심)
  - 계량화가 구조적으로 불가능한 도메인 (신학, 외교 가치 등)
  - 정량 도구 없이 시간 제약이 있는 경우

정성 평가 시 할루시네이션 방지:
  - 각 (policy, scenario) 평가는 반드시 시나리오 내러티브 특정 문장에 근거
  - 근거 없는 "보통 그럴 것이다" 식 추론 금지
  - 평가 근거를 점수 옆에 [근거: "시나리오 인용문"] 형식으로 명시
```

#### 4-B. 평가 항목 (각 셀)

```
For each (policy P_i, scenario S_j):
  1. Does P_i produce desirable outcome in S_j?
  2. Cost·effectiveness in S_j context
  3. Side effects / unintended consequences in S_j
  4. 근거 인용: 시나리오 내러티브 해당 부분
  
  Score assignment (LLM):
    다음 기준으로 점수 배정 후 raw_scores에 기록
    점수 계산·분류는 Step 5에서 policy_scorer.py로 위임
```

#### 4-C. 점수 기준 (5-point bipolar scale)

| 점수 | 의미 | PDF 대응 |
|---|---|---|
| +2 | highly desirable | "clearly a good bet" |
| +1 | desirable | "good bet" |
|  0 | neutral / mixed | (not "desirable" per PDF verbatim) |
| -1 | undesirable | (contingent candidate) |
| -2 | highly undesirable | "avoid" |

> **주의**: PDF verbatim "desirable results in ALL cases"에서 "desirable" = +1 이상.
> 0 (neutral)은 "해롭지 않음"이나 "바람직함"은 아님.
> 0이 포함된 정책은 ROBUST*로 표시되어 별도 검토를 요구함 (policy_scorer.py 자동 처리).

### Step 5 — Outcome Scoring: policy_scorer.py 결정론적 실행

```
LLM이 할 일:
  1. Step 4에서 각 (P_i, S_j) 쌍에 정수 점수 부여
  2. 아래 JSON 형식으로 raw_scores 구성

  raw_scores_input:
  {
    "scenario_names": ["<S1명칭>", "<S2명칭>", ...],
    "policy_scores": {
      "<P1명칭>": [<S1점수>, <S2점수>, ...],
      "<P2명칭>": [<S1점수>, <S2점수>, ...],
      ...
    }
  }

policy_scorer.py 호출 (MANDATORY — LLM이 직접 계산하지 않음):
  echo '<raw_scores_input JSON>' | python3 policy_scorer.py
  
  OR

  python3 policy_scorer.py --input raw_scores.json

출력 확인:
  - status = "OK" → Step 6으로
  - status = "ERROR" → §0-C 에러 처리
```

### Step 6 — Robust vs Contingent 분류 (policy_scorer.py 결과 사용)

```
policy_scorer.py 분류 기준 (결정론적):

ROBUST:    avg ≥ +1.0 AND min_score ≥ +1  (PDF: "desirable results in ALL cases")
ROBUST*:   avg ≥ +1.0 AND min_score = 0   (borderline — 0점 셀 존재, 검토 요구)
CONTINGENT: avg ≥ -0.5 AND activate_in_scenarios ≠ []
            (일부 시나리오 ≥ +1, 일부 ≤ -1)
REJECT:    avg < -0.5
           OR avg ≥ -0.5 AND activate_in_scenarios = [] ← 자동 재분류

엣지케이스 — 활성화 불가 Contingent 자동 REJECT:
  activate_in_scenarios가 비어있으면 해당 정책은 어떤 시나리오에서도 호출될 수 없음.
  PDF verbatim: "called on if the circumstances DEVELOP that the scenarios depict"
  → 호출 가능한 상황이 없으면 REJECT로 자동 재분류 (policy_scorer.py가 처리)

PDF verbatim 대응:
  ROBUST  = "produces desirable results in all cases"
  CONTINGENT = "called on if the circumstances develop that the scenarios depict"

분류 결과는 policy_scorer.py JSON 출력의 all_ranked 필드 사용.
LLM이 분류 결과를 재해석하거나 변경하지 않는다.
```

### Step 7 — Top-K Recommendation + Activation Conditions

```
K 정의:
  K_R = 전체 ROBUST + ROBUST* 정책 (순위 내림차순, 평균 점수 기준)
  K_C = 상위 Contingent 3개 (평균 점수 기준)
  REJECT = 출력하되 "기각" 표시

For ROBUST policies (K_R):
  → Implement immediately (no-regret)
  → ROBUST*는 "검토 후 구현" 권장

For Contingent policies (K_C):
  → Pre-prepare now
  → Define activation triggers (어느 시나리오 방향이 나타나면 활성화)
  → Link to Leading Indicators (next sub-skill — §5 leading_indicators_handoff 활용)
  → 활성화 트리거는 시나리오 내러티브의 구체적 사건/지표 인용

For REJECT:
  → Record + reason (어느 시나리오에서 왜 실패하는가)
  → 향후 시나리오 변화 시 재검토 가능성 명시
```

---

## 4. 출력 양식

```markdown
### § Policy Testing (vision-foresight-scenarios-policy-testing)

**Total Policies Tested**: [N]
**Robust Policies**: [K_R] (ROBUST: [X], ROBUST*: [Y])
**Contingent Policies**: [K_C]
**Rejected**: [K_X]

---

#### Policy × Scenario Score Matrix

| Policy | <Scenario 1> | <Scenario 2> | ... | Average | Classification |
|---|---|---|---|---|---|
| [P3] | +1 | +2 | ... | +1.6 | **ROBUST** ⭐ |
| [P1] | +2 | +2 | ... | +1.5 | **ROBUST** ⭐ |
| [P_b] | +2 | +2 | ... | +1.3 | **ROBUST*** ⚠️ |
| [P2] | +2 | -1 | ... | +0.4 | Contingent |
| [P4] | -1 | -1 | ... | -1.0 | REJECT |

> 모든 Average 및 Classification 값은 policy_scorer.py 출력 기준.

---

#### Robust Policy Recommendations (Top-K_R)

| Rank | Policy | Avg Score | Type | Implementation |
|---|---|---|---|---|
| 1 | [P3] | +1.6 | ROBUST | Immediate |
| 2 | [P1] | +1.5 | ROBUST | Immediate |
| 3 | [P_b] | +1.3 | ROBUST* | Review then implement |

#### Contingent Policies — Top K_C=3 (with activation triggers)

| Rank | Policy | Avg | Activates in Scenarios | Trigger Conditions |
|---|---|---|---|---|
| 1 | [P2] | +0.4 | [S1, S3] | [시나리오 내러티브 인용: 구체 사건/지표] |
| ... | ... | ... | ... | ... |

> Trigger Conditions는 시나리오 내러티브 직접 인용. 발명 금지.

#### Rejected Policies

| Policy | Avg | Reason |
|---|---|---|
| [P4] | -1.0 | [어느 시나리오에서 왜 실패했는지 시나리오 인용] |

---

#### 다음 sub-skill 전달 (leading_indicators_handoff)

→ vision-foresight-scenarios-leading-indicators
  
  전달 데이터 (policy_scorer.py leading_indicators_handoff 필드):
  ```json
  {
    "contingent_policies": [
      {
        "policy": "<정책명>",
        "activate_in_scenarios": ["<S1>", "..."],
        "deactivate_in_scenarios": ["<S2>"],
        "avg_score": 0.4
      }
    ],
    "robust_policies": [
      {"policy": "<정책명>", "avg_score": 1.6}
    ],
    "scenario_names": ["<S1>", "<S2>", "..."]
  }
  ```
```

---

## 5. 마스터 협업 Protocol

| 항목 | 내용 |
|---|---|
| 입력 | § N Scenario Narratives + § 3-Criteria Audit (PASS) |
| 처리 | 7-Step pipeline + policy_scorer.py |
| 출력 | § Policy Testing + Robust vs Contingent + leading_indicators_handoff JSON |
| 다음 단계 | vision-foresight-scenarios-leading-indicators |
| 결정론 경계 | Step 5-6 (점수 계산·분류·순위) = Python 전담. Step 4 (평가) = LLM + 시나리오 인용 의무 |

---

## 6. 결정론 vs LLM 분리표

| 단계 | 담당 | 근거 |
|---|---|---|
| Step 1: 입력 검증 | policy_scorer.py `--validate-only` | 존재 확인·범위 검사 = 결정론 |
| Step 2: Persona 제안 | LLM | 창의적 대안 생성 = LLM 필요 |
| Step 3: 정책 명확화 | LLM + 시나리오 인용 | 해석 필요, 단 발명 금지 |
| Step 4: 평가 점수 배정 | LLM + 시나리오 인용 | 정성적 판단 = LLM, 근거 필수 |
| Step 5: 평균 계산 | policy_scorer.py | 산술 연산 = 결정론 |
| Step 6: 분류 | policy_scorer.py | 임계값 비교 = 결정론 |
| Step 7: 순위·핸드오프 | policy_scorer.py | 정렬·구조화 = 결정론 |

---

## 7. 입력 검증 체크리스트 (Step 1 실행 전 LLM 자가 점검)

```
[ ] 시나리오 N개 명칭 모두 확인됨
[ ] 각 시나리오 내러티브 최소 1문단 이상 존재
[ ] 3-Criteria Audit "PASS" 문구 명시 확인
[ ] 시나리오 수 ≥ 2
[ ] Policy_scorer.py 파일이 스킬 폴더에 존재 확인
    → ls /path/to/skill/policy_scorer.py

정책 수집 후 추가 체크:
[ ] 정책 수 ≥ 1
[ ] 각 정책명 고유 (중복 없음)
[ ] 점수 범위 {-2,-1,0,+1,+2} 안에 있음
```
