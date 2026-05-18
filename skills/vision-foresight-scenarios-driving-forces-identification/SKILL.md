---
name: vision-foresight-scenarios-driving-forces-identification
description: |
  ## TLDR — INTERNAL Sub-skill. vision-foresight-scenarios 대표 마스터의 2번째 sub-skill. Glenn & TFG V3.0 19장 Section III Schwartz Step 2 + TFG Preparation 풀 구현. **Driving Forces Identifier AI Agent** — Peter Schwartz Step 2 verbatim: *"identify the key forces and trends in the environment"* + Schwartz *"driving forces as the building blocks of scenarios"*. TFG: *"Define the scenario space. A scenario study begins by defining the domain of interest. Given a clear statement of the domain, analysts list key driving forces thought to be important to the future of the domain."* (Section III verbatim). MITRE case 양식: *"driving forces of law enforcement funding and social attitudes toward crime were defined as ultimately important. To the degree possible, these driving forces should be independent 'axes' in a scenario space."* Mandel & Wilson SRI verbatim: *"The team then analyzes forces that will shape the future business environment, both from within their own industry (competition) and outside of it (social, political, economic, etc.)"*. Coates & Jarratt: *"some 6 to 30 variables affecting the future situation are nominated. This list is then winnowed down by eliminating redundancies, a process that usually results in 6 to 20 variables."* Millennium Project Futures Matrix 6 domains: Demographics·Environment·Tech·Governance·Economics·Integration. **DEFAULT: STEEPS 6 domains scan (standard 5 + Spiritual 6th extension) + Millennium Futures Matrix + 8 persona simulation → 6-20 raw variables → 6-12 curated driving forces**. **결정론 도구**: driving_forces_utils.py (이 폴더 내) — verbatim·STEEPS·Futures Matrix·변수 수 검증·페르소나·winnowing 알고리즘을 LLM이 자연어로 재추론하지 않도록 차단.

  ## Triggers — INTERNAL only. 사용자 직접 호출 금지 (disable-model-invocation: true). vision-foresight-scenarios 모든 cycle 두 번째 단계 자동 호출.

  ## Detailed Methodology — TFG V3.0 19장 Section III Schwartz Step 2 + TFG Preparation + MITRE + Coates·Mandel·Wilson + Millennium Futures Matrix 풀 구현. **Driving Forces Identifier Agent** 7-Step pipeline: ① § Focal Issue 입력 → ② AI Agent 8 고정 페르소나 시뮬레이션 (P1 Industry Insider·P2 Scenario Specialist·P3 Policy Analyst·P4 Tech Expert·P5 Sociologist·P6 Economist·P7 Environmental Scientist·P8 Devil's Advocate) — Union → deduplicate → STEEPS → Futures Matrix 매핑 → ③ STEEPS 6 domains scan: Social·Technological·Economic·Environmental·Political·Spiritual (6th non-standard extension) → ④ Millennium Project Futures Matrix 6 domains 보완 적용 → ⑤ Coates winnowing — 6-30 raw → 6-20 winnowed → 6-12 final (`python3 driving_forces_utils.py validate_count N STAGE`) → ⑥ Schwartz building blocks 분류 — predetermined elements vs critical uncertainties (`python3 driving_forces_utils.py force_types`) → ⑦ 다음 sub-skill (Ranker) 전달. Internal + external industries 모두 scan (Mandel-Wilson SRI verbatim). 출력: § Driving Forces (6-12 curated) + STEEPS 분류 + Futures Matrix 매핑 + predetermined vs uncertain 분류 + 다음 sub-skill 전달.
disable-model-invocation: true
---

# Scenarios — Driving Forces Identification Sub-skill (INTERNAL)

> **출처**: Glenn & TFG V3.0 19장 Section III Schwartz Step 2 + TFG Preparation + MITRE·Coates·Mandel-Wilson + Millennium Futures Matrix verbatim.

> **결정론 도구**: `driving_forces_utils.py` (이 폴더 내)
> PDF verbatim·STEEPS domains·Futures Matrix·변수 수 범위 검증·페르소나·winnowing 알고리즘을
> LLM이 자연어로 재추론하지 않도록 차단.
>
> ```bash
> # 자체 검증 (실행 전 항상 확인)
> python3 driving_forces_utils.py validate   # ALL_PASS: true 필수
> ```

**LLM은 아래 항목을 자연어로 재추론하지 않는다 — 반드시 Python 호출 결과 사용:**
- PDF verbatim 인용 → `python3 driving_forces_utils.py verbatim KEY`
- STEEPS 6 domains 정의 → `python3 driving_forces_utils.py steeps`
- Futures Matrix 6 domains → `python3 driving_forces_utils.py futures_matrix`
- 8 고정 페르소나 + 집계 규칙 → `python3 driving_forces_utils.py personas`
- 변수 수 범위 검증 → `python3 driving_forces_utils.py validate_count N STAGE`
- Predetermined vs Uncertainty 분류 기준 → `python3 driving_forces_utils.py force_types`
- Schwartz Step 2 정의 → `python3 driving_forces_utils.py schwartz_step 2`
- winnowing 알고리즘 → `python3 driving_forces_utils.py winnowing_algorithm`

본 sub-skill은 **vision-foresight-scenarios** 마스터의 INTERNAL component이며 **2번째 단계**다. 사용자 직접 호출 금지.

---

## 0. 입력 인터페이스 (§ Focal Issue)

**수신 형식** (vision-foresight-scenarios Step 1 → Driving Forces Identification):

```
§ Focal Issue
  - Focal Issue Statement: [주요 의사결정 또는 분석 대상]
  - Domain / Sector: [산업·분야·지역·조직 범위]
  - Decision Horizon: [시간적 범위 — 예: 5년, 10년, 2030, 2035]
  - Stakeholders: [주요 이해관계자 목록]
  - Scope Boundaries: [내부/외부 force 포함 범위]
```

---

## 1. AI Agent 역할 — Driving Forces Identifier

당신은 **Scenarios Driving Forces 식별 전문가**다. Schwartz Step 2 + STEEPS scan + Millennium Futures Matrix로 *building blocks of scenarios* 도출.

```bash
python3 driving_forces_utils.py schwartz_step 2
# → "identify the key forces and trends in the environment"
```

---

## 2. PDF 원전 (verbatim)

```bash
python3 driving_forces_utils.py verbatim schwartz_step2
```

> *"identify the key forces and trends in the environment"* — Schwartz Step 2

```bash
python3 driving_forces_utils.py verbatim building_blocks
```

> *"Schwartz uses the driving forces as the building blocks of scenarios"*

```bash
python3 driving_forces_utils.py verbatim tfg_define
```

> *"Define the scenario space. A scenario study begins by defining the domain of interest. Given a clear statement of the domain, analysts list key driving forces thought to be important to the future of the domain."*

```bash
python3 driving_forces_utils.py verbatim mitre_case
```

> *"In a study performed by The Futures Group for MITRE Corporation about the social environment of crime, driving forces of law enforcement funding and social attitudes toward crime were defined as ultimately important. To the degree possible, these driving forces should be independent 'axes' in a scenario space."*

```bash
python3 driving_forces_utils.py verbatim mandel_wilson
```

> *"The team then analyzes forces that will shape the future business environment, both from within their own industry (competition) and outside of it (social, political, economic, etc.)"*

```bash
python3 driving_forces_utils.py verbatim coates_winnowing
```

> *"some 6 to 30 variables affecting the future situation are nominated. This list is then winnowed down by eliminating redundancies, a process that usually results in 6 to 20 variables."*

### Millennium Project Futures Matrix 6 Domains

```bash
python3 driving_forces_utils.py futures_matrix
```

- Demographics and Human Resources
- Environmental Change and Biodiversity
- Technological Capacity
- Governance and Conflict
- International Economics and Wealth
- Integration or Whole Futures

---

## 3. 7-Step Driving Forces Pipeline

### Step 1 — § Focal Issue 입력

Section 0 입력 인터페이스에서 수신:
- Focal Issue Statement
- Domain / Sector
- Decision Horizon
- Stakeholders

### Step 2 — AI Agent 8 고정 페르소나 풀 시뮬레이션

```bash
python3 driving_forces_utils.py personas
```

```
8 고정 페르소나:
  P1. Industry Insider       — 내부 forces (경쟁, sector-specific)
  P2. Scenario Specialist    — 외부 macro-environmental forces
  P3. Policy Analyst         — Political/regulatory forces
  P4. Technology Expert      — Technological driving forces
  P5. Sociologist/Anthropologist — Social·cultural·demographic forces
  P6. Economist              — Economic forces
  P7. Environmental Scientist — Environmental·ecological forces
  P8. Devil's Advocate       — Wild cards, overlooked forces, edge cases

집계 규칙 (결정론 알고리즘):
  Step A. Union of all 8 proposals
  Step B. 중복 제거 (exact/near-synonym)
  Step C. STEEPS domain 분류
  Step D. Futures Matrix 매핑
  Step E. Coates winnowing → 6-20 (validate_count N winnowed)
  Step F. Final curation → 6-12 (validate_count N final)
  Step G. Predetermined vs Critical Uncertainty 분류
```

**내부 + 외부 force 모두 포함** (Mandel-Wilson SRI verbatim):
- Internal: P1 Industry Insider → competition, sector-specific trends
- External: P2-P8 → macro-environment (social, political, economic, etc.)

### Step 3 — STEEPS 6 Domains Scan

```bash
python3 driving_forces_utils.py steeps
```

| Domain | Code | Examples |
|---|---|---|
| **S**ocial | S | Demographics·values·lifestyles·culture·education |
| **T**echnological | T | Innovation·diffusion·obsolescence·AI·biotech |
| **E**conomic | E | Markets·resources·trade·inequality·investment |
| **E**nvironmental | E2 | Climate·biodiversity·sustainability·resources |
| **P**olitical | P | Governance·regulation·conflict·alliances·geopolitics |
| **S**piritual | Sp | Religious trends·philosophical shifts·identity·meaning |

⚠️ **Spiritual domain 주의**: Standard STEEPS는 5개 domain (S·T·E·E·P). Spiritual은 비표준 6번째 domain — 전문가 vision에 따라 추가된 extension. 모든 분석에서 "(non-standard extension)" 명시.

### Step 4 — Millennium Futures Matrix 보완 적용

```bash
python3 driving_forces_utils.py futures_matrix
```

각 driving force를 Futures Matrix 6개 domain 중 하나에 매핑:
1. Demographics & Human Resources
2. Environmental Change & Biodiversity
3. Technological Capacity
4. Governance & Conflict
5. International Economics & Wealth
6. Integration / Whole Futures

### Step 5 — Coates Winnowing (결정론 카운트 검증)

```bash
python3 driving_forces_utils.py winnowing_algorithm
```

```
Stage 1 (Raw nomination):
  - 8 persona proposals union → 6-30 variables
  - python3 driving_forces_utils.py validate_count N raw

Stage 2 (Winnowing):
  - 중복 제거 (>80% 개념 중복 → merge)
  - focal issue 무관 forces 제거
  - → 6-20 variables
  - python3 driving_forces_utils.py validate_count N winnowed

Stage 3 (Final curation):
  - 중요도 + 불확실성 상위 forces 선발
  - Independence check (MITRE: "independent axes")
  - → 6-12 key driving forces
  - python3 driving_forces_utils.py validate_count N final
```

| Stage | Range | Source |
|---|---|---|
| Raw | 6-30 | Coates & Jarratt verbatim |
| Winnowed | 6-20 | Coates & Jarratt verbatim |
| Final | 6-12 | TFG convention + Schwartz axes framework |

### Step 6 — Schwartz Building Blocks 분류

```bash
python3 driving_forces_utils.py force_types
```

**분류 기준**:

| Type | 조건 | 역할 |
|---|---|---|
| **Predetermined** | 높은 중요도 + 높은 확실성 (이미 정해진 결과) | 모든 시나리오의 공통 배경 |
| **Critical Uncertainty** | 높은 중요도 + 낮은 확실성 (핵심 분기점) | 시나리오 구분 axes (MITRE verbatim) |

```
Predetermined 예시:
  - Population aging (already born)
  - Climate inertia (locked-in physical process)
  - Long lead-time infrastructure already built

Critical Uncertainty 예시:
  - AI regulatory direction
  - Technology adoption rate
  - Political decisions not yet made
  - Cultural/values shifts
  - Wild card events
```

```bash
python3 driving_forces_utils.py classify_type "Population aging demographic trend"
# → classification guidance prompt for LLM
```

### Step 7 — 다음 sub-skill 전달

→ vision-foresight-scenarios-importance-uncertainty-ranking

---

## 4. 출력 양식 (§ Driving Forces)

아래 양식 그대로 § Driving Forces 섹션 출력. 코드블록 중첩 없이 직접 작성.

---

### § Driving Forces (vision-foresight-scenarios-driving-forces-identification)

**Focal Issue**: [문제 도메인]
**Total Driving Forces**: [N curated] (raw: [M])
**STEEPS Coverage**: [checked domains]
**Futures Matrix Mapping**: ✓ 6 domains
**Predetermined vs Uncertain**: [P : U ratio]

---

#### Driving Forces Table

| ID | Driving Force | STEEPS | Futures Matrix | Type | Contributing Personas |
|---|---|---|---|---|---|
| DF01 | [Force 1] | T | Technology | Critical Uncertainty | P2+P4 |
| DF02 | [Force 2] | S | Demographics | Predetermined | P5 |
| DF03 | [Force 3] | P | Governance | Critical Uncertainty | P3+P8 |
| DF04 | [Force 4] | E | Economics | Critical Uncertainty | P6 |
| DF05 | [Force 5] | E2 | Environment | Predetermined | P7 |
| DF06 | [Force 6] | Sp* | Integration | Critical Uncertainty | P5+P8 |
| ... | ... | ... | ... | ... | ... |

*Sp = Spiritual domain (non-standard extension)

#### Coates Winnowing Log

- Raw nominated (persona union): [M] forces → `validate_count M raw`: [result]
- After winnowing: [K] forces → `validate_count K winnowed`: [result]
- Final curated: [N] forces → `validate_count N final`: [result]
- Redundancies eliminated: [list of merged items]

#### Predetermined vs Critical Uncertainty Summary

**Predetermined** (공통 배경):
- DF0X: [Force name] — [reason: why certain]
- ...

**Critical Uncertainties** (시나리오 axes 후보):
- DF0X: [Force name] — [reason: why uncertain]
- ...

---

#### 다음 sub-skill 전달

→ vision-foresight-scenarios-importance-uncertainty-ranking
  (Ranker AI Agent가 importance × uncertainty 2D ranking 수행)

---

## 5. 결정론적 유틸리티 (driving_forces_utils.py)

```bash
# 자체 검증 (ALL_PASS: true 필수)
python3 driving_forces_utils.py validate

# 주요 명령어
python3 driving_forces_utils.py verbatim KEY         # PDF verbatim 인용
python3 driving_forces_utils.py verbatim_all         # 전체 verbatim 출력
python3 driving_forces_utils.py steeps               # STEEPS 6 domains
python3 driving_forces_utils.py futures_matrix       # Futures Matrix 6 domains
python3 driving_forces_utils.py personas             # 8 고정 페르소나 + 집계 규칙
python3 driving_forces_utils.py validate_count N S   # 변수 수 검증 (raw/winnowed/final)
python3 driving_forces_utils.py classify_type FORCE  # Predetermined vs Uncertainty 가이드
python3 driving_forces_utils.py schwartz_step N      # Schwartz Step N (1-7)
python3 driving_forces_utils.py schwartz_all         # Schwartz Steps 전체
python3 driving_forces_utils.py winnowing_algorithm  # Coates winnowing 알고리즘
python3 driving_forces_utils.py force_types          # 분류 기준 정의
```

**결정론 환원 항목** (이 목록의 항목은 LLM이 자연어로 재추론 금지):

| 항목 | Python 명령 |
|---|---|
| PDF verbatim 인용 | `verbatim KEY` |
| PDF verbatim 전체 | `verbatim_all` (JSON) |
| STEEPS domains 정의 | `steeps` |
| Futures Matrix 정의 | `futures_matrix` |
| 8 페르소나 + 집계 규칙 | `personas` |
| 변수 수 범위 검증 | `validate_count N STAGE` |
| 분류 기준 정의 | `force_types` |
| Schwartz Step 2 | `schwartz_step 2` |
| Winnowing 알고리즘 | `winnowing_algorithm` |
| 8 페르소나 제안 union·dedupe | `aggregate '<JSON>'` |
| STEEPS 5 standard domain 커버 | `steeps_coverage '<JSON>'` |
| Futures Matrix 6 domain 커버 | `matrix_coverage '<JSON>' [--full]` |
| importance·certainty 점수 분류 | `classify_scores IMP CERT` |
| MITRE 독립성 (Jaccard >0.8 차단) | `independence '<JSON>'` |
| Bibliography 전체 | `bibliography` |

---

## 6. 오류 및 예외처리

| 상황 | 처리 |
|---|---|
| § Focal Issue 미입력 | 마스터에 Step 1 (Focal Issue Definition) 재실행 요청 |
| Focal Issue 불명확 | 마스터에 명확화 요청 ("어떤 의사결정을 위한 분석인가?") |
| Raw variables < 6 | 경고: "8 persona 시뮬레이션 depth 부족 — 페르소나 재시뮬레이션 또는 추가 도메인 스캔" |
| Raw variables > 30 | 경고: "과다 추출 (Coates 상한 30 초과) — 중복·무관 항목 우선 제거" + `validate_count N raw` |
| Winnowed > 20 | 경고: "winnowing 불충분 — redundancies 추가 제거 필요" + `validate_count N winnowed` |
| Final < 6 | 경고: "too few driving forces — 시나리오 공간 부족 가능성" |
| Final > 12 | 경고: "too many — 시나리오 축 과다 (관리 불가). 6-12로 우선순위 재선정" |
| STEEPS domain 미커버 | 경고: "커버되지 않은 domain: [list] — 해당 domain에서 추가 force 탐색 권장" |
| Spiritual domain 사용 시 | 항상 "(non-standard extension)" 명시 |
| Predetermined과 Critical Uncertainty가 모두 0 | 분류 재수행 필요 — `force_types` 기준 재검토 |
| Focal Issue와 무관한 forces 다수 발견 | Coates winnowing step 3 강화 — focal issue 직접 관련성 재검토 |
| Independence 위반 (두 force가 >80% 개념 중복) | Winnowing 재실행 — 중복 force 중 하나 제거 또는 병합 |

---

## 7. 마스터 협업 protocol

- 입력: § Focal Issue (vision-foresight-scenarios Step 1)
- 처리: 7-Step pipeline + 8 persona 시뮬레이션 + STEEPS + Futures Matrix + Coates winnowing
- 출력: § Driving Forces (6-12 curated)
- 다음 단계: vision-foresight-scenarios-importance-uncertainty-ranking

작업 완료 시 마스터에 § Driving Forces 반환.

---

## 8. Bibliography

```bash
python3 driving_forces_utils.py verbatim_all
```

- **Glenn J.C. & TFG (2009).** "Scenarios." In Glenn, J.C. (Ed.), *Futures Research Methodology V3.0*, Ch.19. The Millennium Project. — Primary source (Section III Schwartz Step 2 + TFG Preparation)
- **Schwartz P. (1991).** *The Art of the Long View: Planning for the Future in an Uncertain World*. Doubleday/Currency. — Driving forces methodology, building blocks concept
- **Coates J.F. & Jarratt J. (1989).** *What Futurists Believe*. Lomond Publications. — Winnowing algorithm (6-30 → 6-20)
- **Mandel T. & Wilson I.H. (1993).** *How Companies Use Scenarios: Practices and Precedents*. SRI International. — Internal + external forces framework
- **The Futures Group for MITRE Corporation.** (cited in TFG 2009) — MITRE crime environment case; independent axes concept
- **The Millennium Project.** *Futures Research Methodology V3.0*. — Futures Matrix 6 domains
