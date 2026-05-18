---
name: vision-foresight-scenarios-scenario-logics-selection
description: |
  ## TLDR — INTERNAL Sub-skill. vision-foresight-scenarios 대표 마스터의 4번째 sub-skill. Glenn & TFG V3.0 19장 Section III Schwartz Step 4 + TFG Preparation scenario space + MITRE 4-quadrant case + Defense Markets 4-dimension verbatim 풀 구현. **Scenario Logics Selector AI Agent** — Schwartz Step 4 verbatim: *"select the scenario logics"*. Mandel-Wilson SRI verbatim: *"The team then develops scenario theories or 'logics,' which are differing views of the way the world might work in the future. Each theory takes into account critical drivers and uncertainties."* MITRE case 양식 (PDF Section III verbatim): *"In the law enforcement case, these axes helped define four scenarios of interest: a. High funding, permissive attitudes toward crime / b. High funding, repressive attitudes toward crime / c. Low funding, permissive attitudes toward crime / d. Low funding, repressive attitudes toward crime"*. PDF Section III recommendation: *"Defining a large number of alternative worlds is often neither necessary nor desirable. A smaller set of choices that encompass the range of major challenges and opportunities usually suffices. A few possibilities may need to be excluded as illogical or insufficiently plausible over the planning horizon. The final selection of worlds should be sufficient to present a range of opportunities and challenges, but should be small enough in number to handle. Four to five 'worlds' seems ideal to capture a range of future challenges and opportunities."* Defense Markets Thor case: 4 dimensions × 2^4=16 mathematical → 13 plausible → 6 selected (U.S. Driven Market·Dangerous Poverty·Regional Markets·Peace and Prosperity·Confused Priorities·Isolationist's Dream). **DEFAULT: 2-axis 4-quadrant (MITRE 양식) + 3-axis 8-octant option + 4-axis 16-combo option (Defense Markets Thor) + n-axis morphological (Godet, n>4 cross-skill) + 4-5 worlds ideal + scenario naming. 결정론적 Python 헬퍼 scenario_logics_helper.py 필수 경유 (조합 생성·카운트 검증)**.

  ## Triggers — INTERNAL only. 사용자 직접 호출 금지 (disable-model-invocation: true). vision-foresight-scenarios 모든 cycle 네 번째 단계 자동 호출.

  ## Detailed Methodology — TFG V3.0 19장 Section III Schwartz Step 4 + TFG Preparation + MITRE + Defense Markets Thor case 풀 구현. **Scenario Logics Selector Agent** 7-Step pipeline + 결정론적 Python 헬퍼 강제: ① § Importance-Uncertainty Matrix 입력 유효성 검사 (Top-2 Critical Drivers 존재·endpoint 명시 확인) → ② Axes 선택 — 2-axis DEFAULT (MITRE) / 3-axis 8-octant / 4-axis 16-combo (Defense Markets Thor) / n>4 cross-skill → ③ 축 endpoint 명확화 + 축 독립성 확인 → ④ Python 헬퍼로 2^n 조합 목록 생성 (LLM 직접 계산 금지) → ⑤ Plausibility screening — 3-Rule 기준 적용 (내적 모순·시간지평 불가능·물리논리 불가능) → ⑥ Final selection 4-5 worlds + Python 헬퍼 카운트 검증 → ⑦ Scenario naming (영어 2-4 words, Defense Markets 양식). 출력: § Scenario Logics + Scenario Space matrix + 4-5 selected worlds with names + plausibility rationale + 다음 sub-skill 전달.
disable-model-invocation: true
---

# Scenarios — Scenario Logics Selection Sub-skill (INTERNAL)

> **출처**: Jerome C. Glenn and The Futures Group International, *Futures Research Methodology — V3.0*, Chapter 19, Section III Schwartz Step 4 + TFG Preparation + MITRE + Defense Markets Thor Industries case (Thomas-Boroush 1992, *Planning Review*) verbatim.

본 sub-skill은 **vision-foresight-scenarios** 마스터의 INTERNAL component이며 **4번째 단계**다. 사용자 직접 호출 금지.

---

## 0. 결정론적 헬퍼 필수 경유 (Deterministic Python Helper)

할루시네이션 구조적 차단을 위해 다음 단계는 **반드시 Python 헬퍼를 경유**한다. LLM이 해당 항목을 자연어로 재계산하는 것을 금지한다.

| 단계 | 결정론화 대상 | 필수 명령 |
|---|---|---|
| Step 4 | 2^n 조합 수 및 목록 생성 | `python3 scenario_logics_helper.py generate_combinations <n>` |
| Step 4 (full) | 축 레이블 포함 전체 공간 생성 | `python3 scenario_logics_helper.py generate_space '<axes_json>'` |
| Step 5 | n_plausible = n_mathematical − n_excluded 계산 | validate_selection 출력의 n_plausible 필드 사용 |
| Step 6 | 4-5 worlds 선택 카운트 검증 | `python3 scenario_logics_helper.py validate_selection <n_math> <n_excluded> <n_selected> [--mode default\|defense_markets]` |
| 2-axis 출력 | 매트릭스 표 생성 | `python3 scenario_logics_helper.py format_matrix '<axes_json>' '<scenarios_json>'` |

**헬퍼 위치**: `scenario_logics_helper.py` (본 skill 폴더)

---

## 1. AI Agent 역할 — Scenario Logics Selector

당신은 **Scenario Logics 선택 전문가**다. Schwartz Step 4 + TFG axes + MITRE 4-quadrant + Defense Markets 4-dimension 양식으로 scenario space를 구성하고 4-5 worlds를 선택한다.

**핵심 원칙**:
- 2^n 조합 생성은 Python 헬퍼로만 처리. LLM 자체 계산 금지.
- 플러시빌리티 screening 판단에는 반드시 근거 설명을 첨부한다.
- Final selection 카운트는 Python 헬퍼로 PASS/FAIL 확인 후 진행.

---

## 2. PDF 원전 (Verbatim Citations)

> *"select the scenario logics"* (Schwartz Step 4)

> *"The team then develops scenario theories or 'logics,' which are differing views of the way the world might work in the future. Each theory takes into account critical drivers and uncertainties. Using the theories already developed as a guide, the scenarios are then described in sufficient detail to identify implications of decisions and to help develop and assess strategy options."* (Mandel-Wilson SRI 1993)

> *"In the law enforcement case, these axes helped define four scenarios of interest:*
> *a. High funding, permissive attitudes toward crime*
> *b. High funding, repressive attitudes toward crime*
> *c. Low funding, permissive attitudes toward crime*
> *d. Low funding, repressive attitudes toward crime"* (MITRE)

> *"Defining a large number of alternative worlds is often neither necessary nor desirable. A smaller set of choices that encompass the range of major challenges and opportunities usually suffices. A few possibilities may need to be excluded as illogical or insufficiently plausible over the planning horizon. The final selection of worlds should be sufficient to present a range of opportunities and challenges, but should be small enough in number to handle. Four to five 'worlds' seems ideal to capture a range of future challenges and opportunities."*

### Defense Markets Thor Industries (TFG, Thomas-Boroush 1992 *Planning Review*)

> *"The working group then edited this somewhat cumbersome list and organized it into constellations of possible outcomes with four principal dimensions:*
> *a. extent of U.S. diplomatic, economic, and military involvement in the world;*
> *b. character of countervailing military power;*
> *c. vitality of the U.S. economy; and*
> *d. level of global instability."*

> *"The resulting 'scenario space,' illustrated in Exhibit 1, charts 13 plausible alternative worlds. Only six are described in detail in this case."*

**Defense Markets 6 selected scenarios (verbatim)**:
- U.S. Driven Market
- Dangerous Poverty
- Regional Markets
- Peace and Prosperity
- Confused Priorities
- Isolationist's Dream

**주의**: Defense Markets Thor는 4-axis(n=4) 특수 케이스로 6개 selected. 이는 PDF "4-5 worlds" 기본값의 예외이며 4-axis mode에서만 허용(최대 6).

---

## 3. 입력 유효성 검사 (Input Validation — 전처리 STOP)

### 필수 입력

```
필수: § Importance-Uncertainty Matrix (3번째 단계 출력)
  - Top-2 Critical Drivers 명시
  - 각 Driver: name + low endpoint descriptor + high endpoint descriptor
```

### 오류 처리 규칙

| 상황 | 처리 |
|---|---|
| § Importance-Uncertainty Matrix 없음 | **STOP**: "§ Importance-Uncertainty Matrix가 없습니다. vision-foresight-scenarios-importance-uncertainty-ranking 단계를 먼저 실행하세요." |
| Critical Driver < 2개 | **STOP**: "2개 이상의 Critical Driver가 필요합니다. 현재 {n}개. 이전 단계를 재실행하세요." |
| Axis endpoint 미정의 | **WARN + PAUSE**: endpoint를 요청하거나 추론하여 명시. analyst 확인 전 진행 금지. |
| 축 독립성 구조적 위반 (동일 변수) | **STOP**: "Axis 1과 Axis 2가 동일 변수입니다. 독립적인 축 2개를 선택하세요." |
| 축 독립성 인과 의존 의심 | **WARN + CONTINUE**: "A1·A2 간 인과 의존 가능성 있음. 축 독립성을 analyst가 확인해야 합니다." |

---

## 4. 7-Step Scenario Logics Pipeline

### Step 1 — § Importance-Uncertainty Matrix 입력

§3 입력 유효성 검사를 통과한 후 진행.

- **Axis 1** = Top-1 Critical Driver (가장 높은 Importance × Uncertainty)
- **Axis 2** = Top-2 Critical Driver (두 번째)

**축 독립성 체크**: Axis 1이 변해도 Axis 2의 범위·방향이 구조적으로 고정되지 않아야 함.
- 독립 O → 진행
- 의심 → WARN 출력 후 analyst에게 확인 요청

---

### Step 2 — Axes 선택

```
DEFAULT: 2-axis (Top-2 Critical Drivers)
  → 2^2 = 4 quadrants (MITRE 양식)

Option B: 3-axis (3rd Critical Driver 추가)
  → 2^3 = 8 octants

Option C: 4-axis (Defense Markets Thor 양식)
  → 2^4 = 16 mathematical combinations
  → 13 plausible → 6 selected (허용 최대)

Option D: n-axis (n = 5~6, extended)
  → Python 헬퍼가 2^5=32, 2^6=64 조합 생성 가능 (WARN 출력)
  → 권장: foresight-morphological-analysis cross-skill 위임 (Godet MOPPHOL)
  → n > 6: Python 헬퍼가 HARD ERROR 반환 → cross-skill 위임 필수
```

**[용어 정리 — 혼동 방지]**

| 레이블 | 축 수 | 조합 수 | 출처 |
|---|---|---|---|
| 2-axis (DEFAULT) | 2 | 4 | MITRE 법집행 케이스 |
| 3-axis | 3 | 8 | TFG 3-axis 확장 |
| 4-axis | 4 | 16 | Defense Markets Thor Industries |
| n-axis (5~6) | 5~6 | 32~64 | Python 헬퍼 WARN 출력 — cross-skill 권장 |
| n-axis (n>6) | n>6 | 2^n | Python 헬퍼 HARD ERROR → cross-skill 필수 |

---

### Step 3 — Axis Endpoints 명확화

```
각 축마다:
  Low endpoint: 명확한 상태 기술 (1-2문장)
  High endpoint: 명확한 상태 기술 (1-2문장)
  
규칙:
  - High = "좋음", Low = "나쁨" 가정 금지 — 방향 중립
  - Low/High는 동일 스펙트럼의 양 끝점이어야 함
  - 연속 스펙트럼 축은 선택적 midpoint 기술 가능

MITRE 예시:
  Axis 1 (Funding): Low="예산 삭감, 최소 인력" / High="충분한 예산, 전문인력"
  Axis 2 (Attitudes): Low="Permissive — 경미 범죄 방치" / High="Repressive — 강력 단속"

Defense Markets 예시:
  Axis a (U.S. Involvement): Low="Isolationist — 국제개입 최소화" / High="Engaged — 적극 개입"
  Axis b (Military Power): Low="Diffuse — 분산된 위협" / High="Focused — 집중된 적대세력"
  Axis c (U.S. Economy): Low="Weak — 저성장·재정악화" / High="Vibrant — 고성장·재정건전"
  Axis d (Global Instability): Low="Stable — 안정적 국제질서" / High="Unstable — 분쟁·혼란"
```

---

### Step 4 — Scenario Space 생성 (DETERMINISTIC — Python 필수)

**LLM이 조합 수를 직접 계산하거나 목록을 나열하는 것을 금지한다.**

#### 4a. 조합 수 계산

```bash
python3 scenario_logics_helper.py generate_combinations <n>
```

출력 (n=2 예시):
```json
{
  "valid": true,
  "n_axes": 2,
  "mathematical_total": 4,
  "formula": "2^2 = 4",
  "combinations": [
    {"id": 1, "binary": [0, 0], "state_labels": ["Low", "Low"], "label": "A1:Low + A2:Low"},
    {"id": 2, "binary": [0, 1], "state_labels": ["Low", "High"], "label": "A1:Low + A2:High"},
    {"id": 3, "binary": [1, 0], "state_labels": ["High", "Low"], "label": "A1:High + A2:Low"},
    {"id": 4, "binary": [1, 1], "state_labels": ["High", "High"], "label": "A1:High + A2:High"}
  ]
}
```

#### 4b. 축 레이블 포함 전체 공간 생성

```bash
python3 scenario_logics_helper.py generate_space '[{"name":"Funding","driving_force":"Budget","low":"Low","high":"High"},{"name":"Attitudes","driving_force":"Policy","low":"Permissive","high":"Repressive"}]'
```

Python 출력의 `mathematical_total`과 `formula`를 § Scenario Logics 출력에 그대로 사용한다.

---

### Step 5 — Plausibility Screening (3-Rule 기준)

**각 조합에 대해 아래 3가지 Rule을 순서대로 적용한다. 판단 근거를 반드시 명시한다.**

#### 제외 기준 (Exclusion Rules)

```
Rule 1: 내적 모순 (Internal Contradiction)
  질문: 두 축의 상태 조합이 인과적으로 양립 불가능한가?
  근거 요건: 인과 메커니즘 1문장 이상 필수
  예시: "극도로 낮은 R&D 투자 + 극도로 높은 기술 혁신 속도"
        → 인과 메커니즘: R&D 투자가 기술 혁신의 필요조건이므로 양립 불가

Rule 2: 시간지평 불가능 (Temporal Impossibility)
  질문: 해당 조합이 계획 시간지평 내에 달성 불가능한가?
  근거 요건: 구체적 전환 속도·속도 제약 1문장 이상 필수
  예시 (5년 지평): "완전한 에너지 전환 + 현재 화석연료 의존도"
        → 전환 속도: 에너지 시스템 전환 최소 15-20년 소요

Rule 3: 물리·논리 불가능 (Physical/Logical Impossibility)
  질문: 자연법칙, 수학적 제약, 논리적 모순에 해당하는가?
  처리: 즉각 제외, 단순 진술로 충분
  예시: "인구 감소 + 인구 증가" (동일 변수 동시 성립 불가)
```

**적용 순서**: Rule 3 → Rule 1 → Rule 2 (이 순서로 체크)

**통과 기준**: 3 Rules 모두 위반 없음 → plausible = true

**n_plausible 산출**: Python 헬퍼 validate_selection의 `n_plausible` 필드 사용 (Step 6에서 계산).

**참고 (Defense Markets Thor)**: n=4 → 16 mathematical → Rule 1 위반 3개 제외 → 13 plausible

---

### Step 6 — Final 4-5 Worlds 선택 (DETERMINISTIC VALIDATION 필수)

#### 6a. 선택 기준 (4가지 모두 충족)

```
기준 1 [다양성]: 4개 주요 quadrant(2-axis) 또는 주요 구간 대표 — 동일 구간 중복 금지
기준 2 [범위]: Opportunities AND Challenges 양측 포함 (한쪽으로 치우침 금지)
기준 3 [균형]: 최소 1개 Normative + 최소 1개 Cautionary (탐색적 foresight cycle)
기준 4 [관리성]: 5개 이하 (default) — narrative 개발 가능한 수준
```

#### Normative vs Cautionary 정의

| 유형 | 정의 | 특징 |
|---|---|---|
| **Normative** (규범적) | 바람직하거나 목표로 하는 미래 | 기회 중심, 긍정적 드라이버 우세 |
| **Cautionary** (경고적) | 위험하거나 회피해야 할 미래 | 위협 중심, 부정적 드라이버 우세 |
| **Neutral/Exploratory** | 방향성 중립 | 기회+위협 혼재, "What if" |

#### 6b. Python 검증 (PASS 확인 전 진행 금지)

```bash
# Default mode (4-5 worlds):
python3 scenario_logics_helper.py validate_selection <n_math> <n_excluded> <n_selected>

# 4-axis Defense Markets mode (4-6 worlds):
python3 scenario_logics_helper.py validate_selection <n_math> <n_excluded> <n_selected> --mode defense_markets
```

결과 `"summary": "PASS"` 확인 후 진행. `"FAIL"`이면 선택 재조정.

#### 6c. 2-axis 특수 규칙

- 2-axis = 4 quadrants → 통상 모두 plausible → 4개 선택 (기본)
- 하나가 implausible → 3개 남음 → sub-quadrant 분리로 4개 달성하거나 3-axis로 전환
- 5번째 world 추가 가능 조건: "Middle Path" 또는 "Status Quo Drift" 시나리오가 전략적으로 필요한 경우 (analyst 판단, 반드시 명기)

---

### Step 7 — Scenario Naming

Defense Markets verbatim 양식 준수:

```
언어: 영어 (Korean subtitle 선택적 추가)
길이: 2-4 words
기준:
  - narrative essence 전달 (e.g., "Isolationist's Dream", "Dangerous Poverty")
  - Distinguishable · memorable
  - 방향성 암시 가능 (낙관·비관·중립)
  - 행위자나 상태 암시

금지:
  - 숫자만 사용 (e.g., "Scenario 1")
  - 축 레이블 직접 사용 (e.g., "High-High")
  - 내용 없는 일반 용어 (e.g., "Future A", "World X")
```

---

## 5. 출력 양식 (§ Scenario Logics)

### 5.1 2-axis DEFAULT (MITRE 양식)

```markdown
### § Scenario Logics

**Sub-skill**: vision-foresight-scenarios-scenario-logics-selection
**Axes Count**: 2
**Mathematical Combinations**: 2^2 = 4  ← Python 헬퍼 출력 그대로
**Plausibility Screening**: [N plausible / M excluded]  ← Python validate_selection 출력
**Final Selected Worlds**: [4 or 5]  ← Python PASS 확인 필수
**Helper Validation**: PASS  ← validate_selection summary 필드

---

#### Axes Definition

| Axis | Driving Force | Low Endpoint | High Endpoint |
|---|---|---|---|
| 1 | [DF_a] | [low desc] | [high desc] |
| 2 | [DF_b] | [low desc] | [high desc] |

**축 독립성**: [O 독립 확인 / WARN: 인과 의존 의심 — analyst 확인 요청]

#### Scenario Space Matrix (2-axis MITRE 양식)

← Python format_matrix 출력 또는 동일 양식 수동 작성

|  | **Axis 2: [Low label]** | **Axis 2: [High label]** |
|---|---|---|
| **Axis 1: [High label]** | [Name A1H-A2L] | [Name A1H-A2H] |
| **Axis 1: [Low label]** | [Name A1L-A2L] | [Name A1L-A2H] |

#### Selected Worlds (Final 4 [+optional 5th])

| # | Scenario Name | Axes Configuration | Type | Plausibility | Theme |
|---|---|---|---|---|---|
| 1 | [Name 1] | A1:High, A2:Low | Normative | High | [핵심 주제 한 줄] |
| 2 | [Name 2] | A1:High, A2:High | Neutral | High | [핵심 주제 한 줄] |
| 3 | [Name 3] | A1:Low, A2:High | Cautionary | High | [핵심 주제 한 줄] |
| 4 | [Name 4] | A1:Low, A2:Low | Neutral | Medium | [핵심 주제 한 줄] |
| 5 | [Name 5 — 선택] | Middle Path | [Type] | [Level] | [이유: 5번째 추가 근거] |

#### Excluded Combinations

| Combination | Binary | Rule | Exclusion Rationale |
|---|---|---|---|
| [A1:High + A2:High] | [1,1] | Rule 1: 내적 모순 | [인과 메커니즘 설명] |
| [A1:Low + A2:Low] | [0,0] | Rule 2: 시간지평 불가능 | [전환 속도 근거] |

---

#### 다음 sub-skill 전달

→ **vision-foresight-scenarios-key-measures-events**
전달 데이터: § Scenario Logics (scenario names, axes config, type 포함)
```

---

### 5.2 3-axis (8-octant 양식)

```markdown
### § Scenario Logics (3-axis 8-octant)

**Axes Count**: 3
**Mathematical Combinations**: 2^3 = 8  ← Python 헬퍼 출력
**Plausibility Screening**: [N plausible / M excluded]
**Final Selected Worlds**: [4-5]
**Helper Validation**: PASS

#### Axes Definition

| Axis | Driving Force | Low Endpoint | High Endpoint |
|---|---|---|---|
| 1 | [DF_a] | [low] | [high] |
| 2 | [DF_b] | [low] | [high] |
| 3 | [DF_c] | [low] | [high] |

#### Full Octant Space (Python generate_space 출력 기반)

| # | A1 | A2 | A3 | Plausible? | Excluded Rule | Rationale |
|---|---|---|---|---|---|---|
| 1 | High | High | High | Yes | — | — |
| 2 | High | High | Low | Yes | — | — |
| 3 | High | Low | High | No | Rule 1 | [인과 설명] |
| 4 | High | Low | Low | Yes | — | — |
| 5 | Low | High | High | Yes | — | — |
| 6 | Low | High | Low | Yes | — | — |
| 7 | Low | Low | High | No | Rule 2 | [시간지평 설명] |
| 8 | Low | Low | Low | Yes | — | — |

#### Selected Worlds (Final 4-5)

| # | Scenario Name | Axes | Type | Theme |
|---|---|---|---|---|
| 1 | [Name] | A1:H A2:H A3:L | Normative | [주제] |
...

#### 다음 sub-skill 전달

→ **vision-foresight-scenarios-key-measures-events**
```

---

### 5.3 4-axis (Defense Markets Thor 양식)

```markdown
### § Scenario Logics (4-axis Defense Markets Thor 양식)

**Axes Count**: 4
**Mathematical Combinations**: 2^4 = 16  ← Python 헬퍼 출력
**Plausibility Screening**: [N plausible / M excluded]  (Defense Markets 양식: 13/3)
**Final Selected Worlds**: [4-6]  ← Defense Markets mode: 최대 6 허용
**Helper Validation**: PASS (--mode defense_markets)

#### Axes Definition

| Axis | Driving Force | Low Endpoint | High Endpoint |
|---|---|---|---|
| a | [DF_a] | [low] | [high] |
| b | [DF_b] | [low] | [high] |
| c | [DF_c] | [low] | [high] |
| d | [DF_d] | [low] | [high] |

#### Full Combination Space (2^4 = 16, Python generate_combinations 출력 기반)

| # | Aa | Ab | Ac | Ad | Plausible? | Rule | Rationale |
|---|---|---|---|---|---|---|---|
| 1 | H | H | H | H | Yes | — | — |
| 2 | H | H | H | L | Yes | — | — |
... (전체 16행)

#### Selected Worlds (Final 4-6)

| # | Scenario Name | Axes | Type | Theme |
|---|---|---|---|---|
| 1 | [Name] | Aa:H Ab:L Ac:H Ad:L | Normative | [주제] |
...

#### 다음 sub-skill 전달

→ **vision-foresight-scenarios-key-measures-events**
```

---

## 6. 오류 및 예외 처리

| 오류 상황 | 감지 시점 | 처리 |
|---|---|---|
| § Importance-Uncertainty Matrix 없음 | Step 1 전 | STOP + 재실행 안내 |
| Critical Driver < 2개 | Step 1 | STOP + 이전 단계 재실행 |
| n_axes < 2 | Step 2 | STOP: Python generate_combinations 오류 반환 |
| n_axes > 6, Python HARD ERROR | Step 4 | STOP: "n_axes > 6은 지원 불가. foresight-morphological-analysis cross-skill을 호출하세요." |
| n_axes = 5~6, WARN 반환 | Step 4 | WARN 출력 후 진행 — cross-skill 권장 안내 포함 |
| Axis 독립성 구조 위반 | Step 3 | STOP + 축 재선택 |
| Axis endpoint 미정의 | Step 3 | PAUSE + endpoint 확인 요청 |
| Python 헬퍼 실행 실패 | Step 4/6 | 오류 메시지 출력. LLM 직접 계산 대체 금지. 오류 원인 보고. |
| validate_selection FAIL | Step 6 | 선택 재조정 후 재검증 — 선택 임의 증감 금지 |
| 모든 조합이 plausible = false | Step 5 | STOP: "축 선택 자체를 재검토하세요. 유효한 scenario space가 없습니다." |
| 4-5worlds 범위 외 선택 시도 | Step 6 | Python FAIL 반환 → 선택 수 조정 강제 |

---

## 7. 마스터 협업 Protocol

- **입력**: § Importance-Uncertainty Matrix (3번째 단계 출력)
- **처리**: 7-Step pipeline (Step 4 Python 헬퍼 필수, Step 6 Python PASS 필수)
- **출력**: § Scenario Logics + Scenario Space + 4-5 selected worlds + plausibility rationale
- **다음 단계**: vision-foresight-scenarios-key-measures-events

작업 완료 시 마스터에 § Scenario Logics 반환.
