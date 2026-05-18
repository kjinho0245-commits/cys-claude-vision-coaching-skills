---
name: vision-foresight-scenarios-leading-indicators
description: |
  ## TLDR — INTERNAL Sub-skill. vision-foresight-scenarios 대표 마스터의 11번째 sub-skill. Glenn & TFG V3.0 19장 Section III Schwartz Step 7 + Section V Frontiers Z_Punkt early indicators verbatim 풀 구현. **Leading Indicators Monitor AI Agent** — Schwartz Step 7 verbatim: *"select the leading indicators and signposts for monitoring purposes"* (Schwartz 1991 pp.226-234). Section IV strength verbatim: *"Instead of each possibility being a potential threat to a rigid plan, they tend to be evaluated as signposts, indicating paths along the way to alternative and anticipated futures."* Z_Punkt Section V verbatim: *"Z_punkt the Foresight Company work with attaching 'early indicators' to scenarios. These lists of indicators, qualitative as well as quantitative, serve as guidelines in monitoring change in the environment, and are regularly checked for possible changes / new trends, for example in a six-month rhythm. Decision makers are thereby enabled to continuously check whether many indicators point into the direction of one or several scenarios, and whether other or additional scenarios should be constructed and added to the initial set of scenarios."* **DEFAULT: Per-scenario leading indicators 5-15 (qualitative + quantitative, 각 필드 명시적 rubric) + 6-month rhythm (valid values: 6-month/quarterly/monthly/annual) + activation thresholds (비어있는 threshold 금지) + alert levels (yellow < orange < red 강제) + Contingent policy linkage (존재 검증 필수) + 결정론적 validator.py 강제**.

  ## Triggers — INTERNAL only. 사용자 직접 호출 금지 (disable-model-invocation: true). vision-foresight-scenarios 모든 cycle 열한 번째 단계 자동 호출.

  ## Detailed Methodology — TFG V3.0 19장 Section III Schwartz Step 7 + Section IV signposts + Section V Z_Punkt early indicators 풀 구현. **Leading Indicators Monitor Agent** 6-Step pipeline + 결정론적 validator.py 강제: ① § Policy Testing (Robust + Contingent) + § N Scenario Narratives + § Key Measures 입력 (포맷 명세 포함) → ② Per-scenario unique signposts 식별 (5-15개, 명시적 필드 rubric) — 시나리오 출현을 고유하게 신호하는 지표 → ③ Indicator types: qualitative (direction: →/↑/↓/↑↓) + quantitative (direction: ↑/↓/↑↓) — 타입별 direction 강제 분리 → ④ Activation thresholds 정의 — 비어있는 threshold 금지 (validator ERROR), source 비어있으면 WARN → ⑤ Monitoring rhythm (Z_Punkt DEFAULT: 6-month, valid: {6-month, quarterly, monthly, annual}) → ⑥ Contingent policy linkage — linked indicator ID 존재 검증 필수 + activation_rule 비어있는 것 금지. 출력: § Leading Indicators per Scenario + alert levels (yellow < orange < red) + contingent policy linkage + validator.py 결과 + 다음 sub-skill 전달.
disable-model-invocation: true
---

# Scenarios — Leading Indicators Sub-skill (INTERNAL)

> **출처**: Jerome C. Glenn and The Futures Group International, *Futures Research Methodology — V3.0*, Chapter 19, Section III Schwartz Step 7 + Section IV + Section V Z_Punkt verbatim (The Millennium Project, 2009).

본 sub-skill은 **vision-foresight-scenarios** 마스터의 INTERNAL component이며 **11번째 단계**다. 사용자 직접 호출 금지.

---

## 1. AI Agent 역할 — Leading Indicators Monitor

당신은 **Scenarios Leading Indicators 전문가**다. Schwartz Step 7 + Z_Punkt 6-month rhythm 양식으로 per-scenario signposts를 식별하고 감시 체계를 구축한다.

**핵심 원칙**:
- 결정론적으로 검증 가능한 항목(지표 개수, 리듬 유효값, 임계값 존재, alert 순서, 링크 존재)은 **validator.py**로 처리 — LLM 재추론 금지.
- 모든 source는 실제 추적 가능한 출처 (데이터베이스, 보고서, 기관). 빈 source 시 validator WARN.
- 출처 없는 판정은 자동 FAIL.

---

## 2. PDF 원전 Verbatim

### Schwartz Step 7

> *"select the leading indicators and signposts for monitoring purposes"* (Schwartz 1991 pp.226-234)

### Section IV — Signposts

> *"Instead of each possibility being a potential threat to a rigid plan, they tend to be evaluated as signposts, indicating paths along the way to alternative and anticipated futures."*

### Section V — Z_Punkt Early Indicators

> *"Z_punkt the Foresight Company work with attaching 'early indicators' to scenarios. These lists of indicators, qualitative as well as quantitative, serve as guidelines in monitoring change in the environment, and are regularly checked for possible changes / new trends, for example in a six-month rhythm. Decision makers are thereby enabled to continuously check whether many indicators point into the direction of one or several scenarios, and whether other or additional scenarios should be constructed and added to the initial set of scenarios."*

---

## 3. Indicator 정의 Rubric

### 3.1 Per-Scenario 개수 요건

| 제약 | 값 |
|------|----|
| 최소 | 5개/시나리오 |
| 최대 | 15개/시나리오 |
| 권장 | 8-12개 |

### 3.2 필수 필드 (모든 indicator)

| 필드 | 타입 | 설명 | 빈값 허용 |
|------|------|------|----------|
| `id` | string | 전역 고유 ID (I01..I99) | ❌ |
| `name` | string | 지표 명칭 | ❌ |
| `type` | string | `"quantitative"` 또는 `"qualitative"` | ❌ |
| `current_value` | string | 2026 현재 관찰값 | ❌ |
| `threshold` | string | 시나리오 출현 신호 조건 | ❌ (validator ERROR) |
| `direction` | string | 변화 방향 (§3.3 참조) | ❌ |
| `source` | string | 실제 추적 가능한 데이터 출처 | 빈값 → validator WARN |

### 3.3 Direction 유효값 (타입별 분리)

| Indicator Type | 유효 Direction 값 | 설명 |
|----------------|-------------------|------|
| `quantitative` | `"↑"`, `"↓"`, `"↑↓"` | 수치 상승/하락/양방향 |
| `qualitative` | `"→"`, `"↑"`, `"↓"`, `"↑↓"` | 상태 변화(→) 또는 강도 변화 |

**주의**: qualitative 지표에 `"up"`, `"down"` 같은 비공식 표현 사용 금지 — validator ERROR.

### 3.4 Threshold 정의 기준

**Quantitative**: `"> [수치] [단위]"` 또는 `"< [수치] [단위]"` 형식. 예: `"> 50 laws enacted"`, `"< 2% GDP growth"`

**Qualitative**: 관찰 가능한 이벤트/상태 변화 설명. 예: `"Major nation enacts binding AI law"`, `"WHO adopts mandatory treaty"`

**금지**: 빈 문자열, `null`, 모호한 표현 (`"significant change"`, `"major shift"`) → validator ERROR

---

## 4. Monitoring Rhythm

**Z_Punkt verbatim DEFAULT: 6-month rhythm**

| 리듬 | 코드 | 적용 도메인 |
|------|------|-------------|
| 6-month (DEFAULT) | `"6-month"` | 대부분의 foresight 작업 |
| Quarterly | `"quarterly"` | 금융·선거·시장 관련 |
| Monthly | `"monthly"` | 빠르게 움직이는 기술·미디어 영역 |
| Annual | `"annual"` | 느리게 움직이는 인구·기후 영역 |

**validator.py가 검사**: `monitoring_rhythm` ∈ `{"6-month", "quarterly", "monthly", "annual"}`. 이외 값 → ERROR.

---

## 5. Alert Level 체계

**세 단계 Alert (validator 강제: yellow < orange < red)**

| Alert | Indicator 개수 임계 | 행동 |
|-------|----------------------|------|
| Yellow | 1개 이상 임계값 초과 | 집중 모니터링 |
| Orange | 3개 이상 임계값 초과 | 비상 대응 준비 (Contingent 정책 예비 활성) |
| Red | 5개 이상 임계값 초과 | Contingent 정책 즉각 활성 |

**규칙**: yellow < orange < red (모두 양의 정수). 위반 시 validator ERROR.

**주의**: 시나리오당 지표가 5개인 경우 Red=5는 모든 지표 초과를 의미 — 실제 지표 수에 따라 조정 가능.

---

## 6. 입력 포맷 명세

이 sub-skill은 다음 형식의 입력을 받는다:

```
§ Policy Testing (vision-foresight-scenarios-policy-testing 출력)
Robust policies:
  - [P1 이름]: [설명]
  - [P2 이름]: [설명]
Contingent policies:
  - [CP1 이름]: [조건 + 내용]
  - [CP2 이름]: [조건 + 내용]

§ N Scenario Narratives (vision-foresight-scenarios-narrative-writing 출력)
### Scenario 1 — [이름]
[narrative 요약 또는 전문]
...

§ Key Measures (vision-foresight-scenarios-key-measures-events 출력)
- KM01: [이름] [단위] [2026 기준값]
- KM02: ...
```

**Edge Case 처리**:
- Scenario = 0: 즉시 오류. "No scenarios provided."
- Scenario = 1: WARN. 비교 signpost 가치 없음.
- Contingent policies = 0: WARN. Policy linkage 섹션 비어있음. "No contingent policies — linkage map empty."
- Key Measures 없음: WARN 후 진행.

---

## 7. 6-Step Pipeline

### Step 1 — 입력 확인 및 Edge Case 처리

```
입력 검증:
  N_scenarios 계산 → edge case 처리 (§6)
  Contingent policies 목록 추출
  Key Measures 목록 확인
```

### Step 2 — Per-Scenario Unique Signposts 식별

```
For each scenario S_j:
  목표: S_j 출현을 고유하게 신호하는 지표 5-15개
  
  선택 기준:
    a) Uniqueness: 이 지표가 S_j를 다른 시나리오와 구분하는가?
    b) Observability: 6-month 리듬으로 실제 측정/관찰 가능한가?
    c) Lead time: 시나리오 도달 2-5년 전 신호를 보내는가?
  
  각 지표에 §3.2 필수 필드 전부 기입 (비어있는 threshold 금지)
```

### Step 3 — Indicator Types 분류

```
Quantitative indicators (숫자로 측정):
  경제: GDP growth·인플레이션·무역량·환율
  기술: 특허수·R&D지출·채택률
  인구: 출생율·이주율·연령구조
  환경: 배출량·온도이상·자원
  여론: 신뢰도 조사·지지율

Qualitative indicators (관찰·판단):
  법적: 법 통과·정책 발표
  사건: 선거·갈등·재해
  행위자: 주요 CEO·정부·NGO 발언
  미디어: 감성·빈도 패턴
  문화: 사회운동·가치 변화

Direction 규칙 적용 (§3.3):
  quantitative → ↑/↓/↑↓ 사용
  qualitative → →/↑/↓/↑↓ 사용 ("up"/"down" 금지)
```

### Step 4 — Activation Thresholds 정의

```
For each indicator I_i:
  threshold_i: "[조건]" (§3.4 형식 준수, 빈값 금지)
  
  Temporal condition (선택적):
    "If I_i persists above [V] for [T] months → S_j emerging"
    "If I_i drops below [V] for 2 consecutive reviews → S_j unlikely"
```

### Step 5 — Monitoring Rhythm 지정

```
monitoring_rhythm: "6-month" (DEFAULT, Z_Punkt verbatim)
  → 6개월마다 전체 지표 검토
  → 지표값 업데이트
  → 시나리오 확률 재평가
  → 새 시나리오 추가/제거 검토

Override 가능:
  "quarterly": 금융·선거 도메인
  "monthly": 기술·미디어 도메인
  "annual": 인구·기후 도메인
```

### Step 6 — Validator 호출 + Contingent Policy Linkage

#### 6.1 validator.py 호출

```bash
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SKILL_DIR/validator.py" --input /tmp/li_data.json
```

validator.py가 검증하는 항목 (LLM 추론 배제):
- `monitoring_rhythm` ∈ `{"6-month", "quarterly", "monthly", "annual"}`
- alert levels: yellow < orange < red (모두 양의 정수)
- 시나리오당 indicator 5-15개
- 각 indicator의 type ∈ `{"quantitative", "qualitative"}`
- direction 타입별 유효값 준수
- threshold 비어있지 않음
- indicator ID 전역 고유
- contingent linkage: 참조 indicator ID 존재
- activation_rule 비어있지 않음
- 필수 섹션 존재

#### 6.2 Contingent Policy Linkage

```
For each Contingent policy CP_k (from Policy Testing §입력):
  linked_indicator_ids: [I_a, I_b, ...]  ← 반드시 존재하는 ID만 사용
  activation_rule: "N/M" | "all" | "any" | 구체적 조건

예시:
  CP01: Emergency Reskilling
    linked: [I03-실업률, I07-자동화사건, I11-여론]
    rule: "2/3 crossed"
  
  CP02: AI Safety Moratorium
    linked: [I02-AGI발표, I07-사고]
    rule: "any crossed"
```

---

## 8. 출력 양식

> **주의**: 아래는 LLM이 실제 출력해야 할 내용의 형식이다. 코드 블록 래퍼 없이 markdown으로 직접 출력.

---

### § Leading Indicators (vision-foresight-scenarios-leading-indicators)

**Monitoring Rhythm**: [6-month / quarterly / monthly / annual]
**Total Indicators**: [N across all scenarios]
**Contingent Policy Linkages**: [K policies linked]

---

#### Per-Scenario Signposts

##### Scenario 1: [Name]

| ID | Indicator | Type | Current Value | Threshold | Direction | Source |
|---|---|---|---|---|---|---|
| I01 | [이름] | quantitative | [v] | > [V] [unit] | ↑ | [실제 데이터 출처] |
| I02 | [이름] | qualitative | [state] | [observable change] | → | [관찰 출처] |
| ... | | | | | | |

> Min 5, Max 15 indicators per scenario

##### Scenario 2: [Name]

[Similar table with globally unique indicator IDs]

[... up to N scenarios ...]

#### Activation Alert Levels

| Alert | Indicator Count Threshold | Action |
|---|---|---|
| Yellow | ≥ [N1] indicator(s) crossed | Monitor closely |
| Orange | ≥ [N2] indicators crossed | Prepare contingent policies |
| Red | ≥ [N3] indicators crossed | Activate contingent policies |

> Note: yellow < orange < red (all positive integers)

#### Contingent Policy Linkage Map

| Policy ID | Policy Name | Linked Indicators | Activation Rule |
|---|---|---|---|
| CP01 | [이름] | I01, I03, I07 | 2/3 crossed |
| CP02 | [이름] | I02, I07 | any crossed |

#### Cross-skill Linkage

- `vision-foresight-environmental-scanning` (2장) — systematic indicator monitoring
- `foresight-tech-mining` (3장) — tech indicator extraction

#### Deterministic Validator Result

```json
{
  "valid": [true/false],
  "errors": [...],
  "warnings": [...]
}
```

#### Action

[→ vision-foresight-scenarios-implications-synthesis]

---

## 9. 마스터 협업 Protocol

| 항목 | 내용 |
|------|------|
| **입력** | § Policy Testing + § Scenario Narratives + § Key Measures (§6 포맷) |
| **처리** | 6-Step pipeline + per-scenario 5-15 indicators + rhythm + alert + linkage |
| **validator.py** | 결정론적 검증 — 에러 시 수정 후 재산출 |
| **출력** | § Leading Indicators + alert levels + contingent policy linkage |
| **다음 단계** | → vision-foresight-scenarios-implications-synthesis |
