---
name: vision-foresight-scenarios-key-measures-events
description: |
  ## TLDR — INTERNAL Sub-skill. vision-foresight-scenarios 대표 마스터의 5번째 sub-skill. Glenn & TFG V3.0 19장 Section III TFG Development Step 2 풀 구현. **Key Measures-Events Architect AI Agent** — TFG 3-step의 2번째 단계 핵심. PDF verbatim: *"Define the key measures. Within each scenario, certain key measures are described. These measures might include forces such as economic growth, legislative environment, technology diffusion and proliferation, or competitive capability, among others. The key measures need to be selected with care. They should have the potential for great impact on the outcome of the scenario; a factor is largely irrelevant if it could develop over a wide spectrum of future values but have little impact on the issue at hand. Every scenario in the set will include projections of the same measures."* + *"Define the events. This list of events will also appear in each scenario. These events shape the scenarios in several different ways: they can impact the key measures, change the chains of causality that lead from the present to the future, and/or make certain policies more or less likely to work. The probabilities of the events are different in each scenario and depend on their position in the scenario space."* **DEFAULT: Key measures 6-12 (모든 scenario 공통, 명시적 rubric 기반 high-impact filter) + Events 10-30 (probability differs per scenario, ≥0.05 variation 강제) + impact mapping (event→measure, 방향 +/-) + 결정론적 validator.py 호출 강제 + Projection Engine 핸드오프 포맷 명세**.

  ## Triggers — INTERNAL only. 사용자 직접 호출 금지 (disable-model-invocation: true). vision-foresight-scenarios 모든 cycle 다섯 번째 단계 자동 호출.

  ## Detailed Methodology — TFG V3.0 19장 Section III Development Step 2 풀 구현. **KM/Events Architect Agent** 6-Step pipeline + 결정론적 validator.py 강제: ① § Scenario Logics + § Driving Forces + § Focal Issue 입력 (포맷 명세 포함) → ② Key measures 정의 (6-12개) — 명시적 high-impact filter rubric 2-criterion 적용 — LLM이 임의 포함 불가 → ③ Events 정의 (10-30개) — each event: impacts 배열(KM ID), impact_direction(+/-/+/-), trigger 명세 → ④ Event probability per scenario — PDF verbatim 강제: 동일 event 확률이 시나리오마다 다름 (≥0.05 spread 강제) → ⑤ validator.py 호출 (결정론적 검증: 개수 범위·확률 [0,1]·variation·impact mapping·matrix 완전성) → ⑥ Projection Engine 핸드오프 포맷으로 출력. 출처 없는 measure/event 포함 자동 FAIL.
disable-model-invocation: true
---

# Scenarios — Key Measures & Events Sub-skill (INTERNAL)

> **출처**: Jerome C. Glenn and The Futures Group International, *Futures Research Methodology — V3.0*, Chapter 19, Section III TFG Development Step 2 verbatim (The Millennium Project, 2009).

본 sub-skill은 **vision-foresight-scenarios** 마스터의 INTERNAL component이며 **5번째 단계**다. 사용자 직접 호출 금지.

---

## 1. AI Agent 역할 — Key Measures-Events Architect

당신은 **TFG Development Step 2 전문가**다. Key measures (모든 scenario 공통 projection) + Events (probability differs per scenario)를 정의한다.

**핵심 원칙**:
- 모든 measure/event 포함은 §3 high-impact rubric으로 정당화한다. 출처 없는 포함 자동 FAIL.
- 결정론적으로 검증 가능한 항목(개수 범위, 확률 범위, variation, matrix 완전성)은 **validator.py**로 처리 — LLM 재추론 금지.
- Event 확률은 반드시 시나리오마다 달라야 한다 (TFG verbatim 강제, spread ≥ 0.05).

---

## 2. PDF 원전 Verbatim

### Define Key Measures

> *"Define the key measures. Within each scenario, certain key measures are described. These measures might include forces such as economic growth, legislative environment, technology diffusion and proliferation, or competitive capability, among others. The key measures need to be selected with care. They should have the potential for great impact on the outcome of the scenario; a factor is largely irrelevant if it could develop over a wide spectrum of future values but have little impact on the issue at hand. Every scenario in the set will include projections of the same measures."*

### Define Events

> *"Define the events. This list of events will also appear in each scenario. These events shape the scenarios in several different ways: they can impact the key measures, change the chains of causality that lead from the present to the future, and/or make certain policies more or less likely to work. The probabilities of the events are different in each scenario and depend on their position in the scenario space."*

---

## 3. High-Impact Filter Rubric (Key Measures Selection)

**근거 원문**: *"They should have the potential for great impact on the outcome of the scenario; a factor is largely irrelevant if it could develop over a wide spectrum of future values but have little impact on the issue at hand."*

각 candidate measure에 대해 2개 criterion 모두 평가:

| Criterion | 질문 | PASS 조건 |
|-----------|------|-----------|
| **C1. Impact Potential** | 이 measure의 변화가 focal issue 결과를 크게 바꾸는가? | 변화 시 최소 1개 시나리오 결과가 질적으로 달라지면 PASS |
| **C2. Relevance to Focal Issue** | 이 measure가 focal issue에 중심적으로 관련되는가? | Driving Forces 목록의 핵심 불확실성과 직접 연결되면 PASS |

**포함 결정 규칙**: 두 기준 모두 PASS → 포함. 하나라도 FAIL → 제외.

**하드 요건**:
- 총 6개 이상 포함 (FAIL 시 validator가 WARN)
- 총 12개 이하 (초과 시 validator WARN)
- 모든 포함 measure의 근거를 `impact_rationale` 필드에 한 문장으로 명시

**PDF verbatim 예시 measure 유형** (강제 아님, 참고):
- Economic growth (GDP, productivity)
- Legislative/regulatory environment (policy index, law count)
- Technology diffusion and proliferation (adoption rate, R&D spend)
- Competitive capability (market share, new entrants)
- Demographics (population, migration)
- Environmental (emissions, resource depletion)

---

## 4. Events 정의 기준

**근거 원문**: events shape scenarios by: (1) impacting key measures, (2) changing causality chains, (3) making policies more/less likely.

Each event MUST satisfy at least ONE of these three functions:

| Function | 예시 |
|----------|------|
| **F1: Impacts key measures** | AGI 발표 → AI R&D 지출 급증 (+KM02) |
| **F2: Changes causality chains** | 대규모 AI 실업 → 복지 지출 경로 분기 |
| **F3: Affects policy effectiveness** | 국제 AI 조약 → 단일 기업 통제 불가 (-KM03 strategy) |

**필수 필드**:
- `id`: E01..E30 형식
- `name`: 이벤트 명칭
- `trigger`: 이 이벤트가 발생하는 구체적 조건 설명
- `impacts`: 영향받는 KM ID 배열 (최소 1개, 없으면 validator ERROR)
- `impact_direction`: `"+"` (상승), `"-"` (하락), `"+/-"` (시나리오마다 다름)

**하드 요건**: 모든 event는 최소 1개 key measure와 impact 연결. 연결 없으면 validator ERROR.

---

## 5. 입력 포맷 명세

이 sub-skill은 다음 형식의 입력을 받는다:

```
§ Scenario Logics (vision-foresight-scenarios-scenario-logics-selection 출력)
- Scenario A — [이름]: [핵심 동인 조합]
- Scenario B — [이름]: [핵심 동인 조합]
- Scenario C — [이름]: [핵심 동인 조합]
- Scenario D — [이름]: [핵심 동인 조합]
[선택: Scenario E]

§ Driving Forces (vision-foresight-scenarios-driving-forces-identification 출력)
- [Force 1]: [설명] — Uncertainty: HIGH/MEDIUM/LOW, Impact: HIGH/MEDIUM/LOW
- [Force 2]: ...
- Controversial forces (있으면 별도 표시)

§ Focal Issue
- [초점 이슈 한 문장]
- Time Horizon: [목표년도]
- Cycle Type: [C1/C2/.../C10]
```

**Edge Case 처리**:
- Scenarios < 2: 즉시 오류. "Cross-probability variation requires ≥2 scenarios."
- Driving Forces 없음: WARN 후 진행. "No Driving Forces provided — measures will rely on focal issue only."
- Focal Issue 없음: 즉시 오류. "Focal Issue is required for high-impact filter."

---

## 6. Event Probability 정의 원칙

**근거 원문**: *"The probabilities of the events are different in each scenario and depend on their position in the scenario space."*

**확률 정의 규칙**:
1. P(event) ∈ [0.0, 1.0] — 범위 이탈 시 validator ERROR
2. 각 event의 확률은 **반드시 시나리오마다 달라야 함** — 이 event가 해당 시나리오의 "scenario space position"을 반영
3. 동일 확률 허용 예외: P=0.0 (물리적 불가) 또는 P=1.0 (확정 발생) — 이 경우 근거 명시 필수
4. TFG verbatim 강제: spread < 0.05이면 validator WARN → 근거 없으면 재산출
5. 확률 정의 기준: 전문가 판단 기반 (pseudo-precision 금지 — 소수점 2자리 이내)

**확률 보정 가이드**:
- 현재 추세 연장: P ≈ 0.6-0.8 (해당 트렌드 지속 시나리오) / 0.2-0.4 (단절 시나리오)
- 흑조사건(black swan): P ≈ 0.05-0.15 (모든 시나리오), 가장 위험한 시나리오에서 0.3까지
- 정책사건: 시나리오 규제 환경에 따라 0.1 (자유방임) ~ 0.9 (강규제)

---

## 7. 6-Step Pipeline

### Step 1 — 입력 확인 및 Edge Case 처리

```
입력 검증:
  Scenario count 계산 → < 2이면 즉시 오류 반환
  Focal Issue 확인 → 없으면 즉시 오류 반환
  Driving Forces 확인 → 없으면 WARN 후 진행
```

### Step 2 — Key Measures 정의 (6-12개)

```
For each candidate measure (from Driving Forces + focal issue analysis):
  Apply §3 high-impact rubric:
    C1_pass = (measure variation qualitatively changes ≥1 scenario outcome)
    C2_pass = (measure directly linked to Driving Forces' key uncertainties)
    Include if C1_pass AND C2_pass
    Exclude otherwise — document exclusion reason
  
  For each included measure, record:
    id: KM01..KM12
    name: [descriptive name]
    unit: [quantitative unit — e.g., %/year, 0-100 index, USD billion]
    current_value: [2026 baseline estimate or "not quantifiable"]
    impact_rationale: [one sentence anchored to C1 + C2 evidence]
```

### Step 3 — Events 정의 (10-30개)

```
For each event:
  Verify: satisfies ≥1 of F1/F2/F3 (§4 functions)
  Record:
    id: E01..E30
    name: [discrete event name]
    trigger: [specific condition that causes this event]
    impacts: [list of KM IDs affected — minimum 1]
    impact_direction: "+" | "-" | "+/-"
  
  TFG verbatim: "This list of events will also appear in each scenario"
  → same events across ALL scenarios (only probabilities differ)
```

### Step 4 — Event Probability Matrix

```
For each event E_i, for each scenario S_j:
  P(E_i | S_j) ∈ [0.0, 1.0]
  Rationale: scenario S_j's position in scenario space
  Variation: ensure spread ≥ 0.05 across scenarios (§6)

JSON structure:
  probability_matrix[event_id][scenario_name] = P
```

### Step 5 — Validator 호출 (결정론)

```bash
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SKILL_DIR/validator.py" --input /tmp/kme_data.json
```

validator.py가 검증하는 항목 (LLM 추론 배제):
- measure count ∈ [6,12]
- event count ∈ [10,30]
- 모든 P ∈ [0.0, 1.0]
- 각 event의 cross-scenario probability spread ≥ 0.05
- 각 event가 ≥1 KM에 impact 매핑
- probability_matrix ↔ events 목록 완전 일치
- 모든 scenario 동일 event set 커버
- 필수 섹션(key_measures, events, probability_matrix) 존재

에러 시: 해당 measure/event/확률 수정 후 재산출. LLM이 validator 에러를 자연어로 무시 금지.

### Step 6 — Projection Engine 핸드오프 포맷

```
→ vision-foresight-scenarios-projection-engine

핸드오프 패키지:
  § Key Measures List (KM01-KM0N): 단위·현재값 포함
  § Events List (E01-E0M): trigger·impacts·direction 포함
  § Probability Matrix: event × scenario 완전 행렬
  § Driving Forces (upstream에서 전달)
  § Scenario Names + Logics (upstream에서 전달)
  
Projection Engine이 사용:
  - Key measures의 시나리오별 궤적 산출 (TIA 기법)
  - Event 발생 확률 반영한 기댓값 계산
```

---

## 8. 출력 양식

> **주의**: 아래는 LLM이 실제 출력해야 할 내용의 형식이다. 코드 블록 래퍼 없이 markdown으로 직접 출력.

---

### § Key Measures + Events (vision-foresight-scenarios-key-measures-events)

**Key Measures**: [N개, 6-12]
**Events**: [M개, 10-30]
**Scenarios covered**: [시나리오 이름 목록]

---

#### Key Measures Table

| ID | Measure | Unit | 2026 Baseline | High-Impact Rationale |
|---|---|---|---|---|
| KM01 | [이름] | [단위] | [현재값] | [C1+C2 근거 — TFG 원문 연결] |
| KM02 | ... | ... | ... | ... |
| ... | | | | |

#### Events Table

| ID | Event | Trigger | Impacts (KMs) | Direction |
|---|---|---|---|---|
| E01 | [이름] | [조건] | KM01, KM03 | + |
| E02 | ... | ... | ... | - |
| ... | | | | |

#### Event Probability Matrix

| Event | Scenario A | Scenario B | Scenario C | Scenario D |
|---|---|---|---|---|
| E01 | 0.7 | 0.2 | 0.9 | 0.4 |
| E02 | 0.1 | 0.8 | 0.3 | 0.6 |
| ... | | | | |

#### Deterministic Validator Result

```json
{
  "valid": [true/false],
  "errors": [...],
  "warnings": [...]
}
```

#### Excluded Candidates

[High-impact filter에서 제외된 candidate와 제외 사유 — 투명성]

#### Action

[→ vision-foresight-scenarios-projection-engine (핸드오프 패키지 포함)]

---

## 9. 마스터 협업 Protocol

| 항목 | 내용 |
|---|---|
| **입력** | § Scenario Logics + § Driving Forces + § Focal Issue (§5 포맷) |
| **처리** | 6-Step pipeline (High-impact filter + Events정의 + Probability Matrix) |
| **validator.py** | 결정론적 검증 — 에러 시 수정 후 재산출 |
| **출력** | § Key Measures + Events + Probability Matrix |
| **다음 단계** | → vision-foresight-scenarios-projection-engine |
