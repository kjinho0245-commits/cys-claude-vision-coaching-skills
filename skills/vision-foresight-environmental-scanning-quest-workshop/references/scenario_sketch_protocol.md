# Scenario Sketch Protocol — Phase 2 Segment 4 + Phase 3 Part 2

> 박사님 *4가지 미래 가능성* (vision-four-futures 스킬) framework + GBN 2×2 매트릭스 통합

## 박사님 4가지 미래 가능성 framework (preferred)

vision-four-futures 스킬 인용:
1. **Plausible Future (기본미래)** — 51~80% 확률·논리적 충분한 미래·트렌드+계획+심층원동력+대중 이미지
2. **Possible Future (또 다른 가능성)**
3. **Wild Card / Catastrophic Future (예외 미래)**
4. **Preferred Future (희망 미래)**

이 framework이 Gordon & Glenn (2009) *Environmental Scanning, Futures Research Methodology v3.0, Millennium Project* QUEST 방법론 응용과 호환:
- Plausible = QUEST exploratory baseline scenario (탐색적·확률 할당 가능)
- Possible = QUEST exploratory alternative scenario (탐색적·확률 할당 가능)
- Wild Card = QUEST contingency/low-prob-high-impact scenario (탐색적·확률 할당 가능)
- Preferred = QUEST aspirational/normative scenario (**주의**: 탐색적 X, 규범적 희망 미래 — 확률 할당 대신 "desirability" 표시)

> **확률 할당 원칙**: 탐색적 3개 시나리오(Plausible·Possible·Wild Card)의 확률 합계 = 100%. Preferred Future는 규범적 시나리오이므로 별도 확률 비율 대신 *실현 조건*과 *no-regret moves*로 표현.
> **Python 검증**: `python3 _quest_tools.py validate_probs --probs '{"5y":[P1,P2,P3,P4]}'` (Preferred 포함 4개 합산 시 100% 확인)

## 시나리오 sketch protocol

### Step 1 — Drivers 식별 (Phase 2 Segment 3 cross-impact 결과 활용)

#### Top 2 driving forces 선정 기준
- High *influence* (다른 변수에 큰 영향)
- High *uncertainty* (어떻게 전개될지 모름)
- *Independent* (서로 dependence 적음)

#### 박사님 컨텍스트 driving forces 후보

##### 미래학 연구소
- AGI 침투 속도 (slow → fast)
- 한국 사회 적응력 (low → high)
- 박사님 글로벌 brand 진출 (no → yes)
- 박사님 본업 시간 배분 (목회·미래학·금융)

##### 교회
- 한국 기독교 인구 변화 속도 (slow decline → rapid decline)
- 디지털 사역 transformation (no → yes)
- 청년 영적 갈증 (low → high)
- 사회 종교 압박 (low → high)

##### 금융투자
- 한국 경제 path (Japan-style → recovery)
- 글로벌 환경 (US-China cold war 강도)
- 박사님 자산 active management 정도
- 통일 가능성

### Step 2 — 4 시나리오 매트릭스

#### GBN 2×2 매트릭스

```
                    Driver 2: HIGH
                          │
         ┌────────────────┼────────────────┐
         │                │                │
         │  Scenario A    │  Scenario B    │
         │  (Quadrant 1)  │  (Quadrant 2)  │
         │                │                │
   Driver 1 ───────────────┼─────────────── Driver 1
    LOW                    │                  HIGH
         │                │                │
         │  Scenario C    │  Scenario D    │
         │  (Quadrant 3)  │  (Quadrant 4)  │
         │                │                │
         └────────────────┼────────────────┘
                          │
                    Driver 2: LOW
```

#### 박사님 미래학 연구소 — 사례 매트릭스

```
                   AGI Fast (5y)
                         │
            ┌────────────┼────────────┐
            │            │            │
            │ Scenario B │ Scenario A │
            │ AGI Fast + │ AGI Fast + │
            │ Korea low  │ Korea high │
            │ adaptation │ adaptation │
   Korea low ──────────── ┼ ─────────── Korea high
                         │
            │ Scenario D │ Scenario C │
            │ AGI Slow + │ AGI Slow + │
            │ Korea low  │ Korea high │
            │ adaptation │ adaptation │
            │            │            │
            └────────────┼────────────┘
                         │
                    AGI Slow (10y+)
```

### Step 3 — 박사님 4가지 framework로 매핑

매트릭스 4 quadrants → 박사님 framework:

| Quadrant | 박사님 framework | 적용 |
|---|---|---|
| 가장 likely (현재 trend 유지) | **Plausible Future** | Scenario B (AGI fast + Korea low adapt) — 박사님 분석상 가장 likely |
| 부분 likely (대안 path) | **Possible Future** | Scenario A (AGI fast + Korea high adapt) — preferred되지만 가능 |
| Low prob, high impact | **Wild Card** | Scenario D (AGI slow) — *unlikely* but possible disruption |
| Aspirational | **Preferred Future** | Scenario A 강화 버전 |

### Step 4 — 각 시나리오 sketch 작성 (1~2 페이지)

#### 표준 양식

```markdown
# Scenario [A/B/C/D]: [Defining Name]

## Defining Characteristics
- 핵심 한 줄
- 시나리오 mood·logic 1 단락

## Defining Drivers
- Driver 1 state: [HIGH/LOW]
- Driver 2 state: [HIGH/LOW]
- Other key drivers: ...

## Key Trends·Events
1. ...
2. ...
3. ...
(5~10 events)

## Timeline (10y narrative)
- 2026~2028: ...
- 2028~2030: ...
- 2030~2035: ...

## Implications for Institution
### Opportunities
- ...

### Threats
- ...

### Strategic Imperatives
- ...

## Trigger Events to Watch
- ...
- ...

## Indicators (Leading)
- ...
- ...

## Probability Estimate
- 5y: X%
- 10y: Y%
- 15y: Z%

## Robustness Check
- 어떤 변수가 변하면 이 시나리오가 깨지는가?
- 어떤 자기강화 mechanism이 있나?
```

## 풀 사례 — 미래학 연구소 4 시나리오

### Scenario A — "Korea AI Renaissance" (Plausible-Preferred 교집합)

#### Defining Characteristics
AGI가 fast (2028~2030 본격 침투)·한국 사회가 high adaptation으로 대응. 박사님 미래학 brand가 글로벌 진출 + 한국 사회 paradigm shift facilitator로 자리잡음.

#### Defining Drivers
- AGI 침투: HIGH
- Korea adaptation: HIGH

#### Key Trends·Events
1. 2027: 한국 LLM 글로벌 top tier 진입
2. 2028: 정부 AGI 적응 종합 정책 (교육·노동·복지)
3. 2029: 한국 인문·창의 산업 폭발 — AGI와 보완
4. 2030: 한국 SMR 글로벌 시장 진입
5. 2031: 박사님 영문 미래학 책 글로벌 베스트셀러
6. 2032: 한국 출산율 반등 시작 (의미·관계 추구)
7. 2033: 한국 기독교 *내적 갱신* — AGI 시대 의미 추구로 부분 회복
8. 2035: 박사님 brand 글로벌 강의 정기

#### Timeline
- 2026~2028: AGI 본격 침투 — 한국 단기 stress, 박사님 단행본 시리즈 출간
- 2028~2030: 적응 정책 + 새 산업 부상, 박사님 자문 폭증
- 2030~2035: 한국 새 paradigm 안착, 박사님 글로벌 진출

#### Implications for 미래학 연구소
**Opportunities**:
- 박사님 brand 글로벌 진출 (영문 publication)
- 정부·기업 자문 폭증
- AGI 시대 의미·영성 framework 한국 lead
- 차세대 미래학자 육성

**Threats**:
- 박사님 시간 분산
- 자문 quality 유지
- 본업 (목회) balance

**Strategic Imperatives**:
- 영문 publication 인프라 (번역·편집·배포)
- 글로벌 강연 schedule 관리
- 후계 미래학자 양성

#### Trigger Events
- 2027 한국 AGI 정책 일관성 확보
- 박사님 영문 단행본 1권 출간
- 글로벌 thinker 협업

#### Probability
- 5y: 25%
- 10y: 35%
- 15y: 30%

### Scenario B — "Korea Falls Behind" (Plausible 핵심)

#### Defining Characteristics
AGI fast·한국 low adaptation. 한국 사회가 자동화 충격에 적응 실패. 박사님은 한국 *위기 분석가*로 위치 잡지만 글로벌 영향력 제한.

#### Defining Drivers
- AGI: HIGH
- Korea adaptation: LOW

#### Key Trends·Events
1. 2027~2028: 한국 화이트칼라 채용 50% 감소
2. 2029: 청년 정신건강 위기 정점
3. 2030: 정치 양극화 가속 (청년 vs 기성)
4. 2031: 한국 GDP 성장률 1% 미만 정착
5. 2032: 한국 기독교 인구 ≤18%
6. 2033: 출산율 0.5 진입
7. 2035: 일본화 본격 진행

#### Probability
- 5y: 35%
- 10y: 40%
- 15y: 35%

(나머지 sections 생략, 동일 양식)

### Scenario C — "AGI Stalls, Korea Stable" (Wild Card)

#### Defining Characteristics
AGI가 기술적·규제적 stall로 slow (10y+). 한국이 high adaptation 환경에서 stable. 박사님 brand가 *전통 미래학* 기반으로 안정.

#### Defining Drivers
- AGI: LOW
- Korea adaptation: HIGH

#### Probability
- 5y: 10%
- 10y: 5%
- 15y: 5%

### Scenario D — "Slow AGI, Korea Drifts" (Wild Card)

#### Defining Characteristics
AGI slow + Korea low adaptation. 한국이 *차단적* 전통 path. 박사님 brand가 한국 보수 청중 중심.

#### Probability
- 5y: 30%   ← A(25)+B(35)+C(10)+D(30)=100% ✓
- 10y: 20%  ← A(35)+B(40)+C(5)+D(20)=100% ✓
- 15y: 30%  ← A(30)+B(35)+C(5)+D(30)=100% ✓  [수정: 이전 15% → 30%로 교정]

### Cross-Scenario Insights

#### 모든 시나리오 공통
- 박사님 brand는 어느 시나리오에서도 *어느 정도* 가치
- 한국 인구·경제 challenges는 모든 시나리오에 공존

#### "No-regret moves" — 모든 시나리오에서 후회 없는 행동
1. 박사님 영문 publication 인프라 구축
2. 후계 미래학자 양성
3. MCEWS·deep research workflow 차세대 design
4. 박사님 본업 (목회·미래학) balance

#### 시나리오별 *fork actions* (어느 시나리오에 따라 다른 행동)
- A·C 시나리오: 글로벌 진출 적극
- B·D 시나리오: 한국 위기 분석·자문 중심

## 시나리오 활용 — Phase 4 Strategic Options

각 시나리오마다 Strategic Options 도출:

| Option | A 효과 | B 효과 | C 효과 | D 효과 | Robustness |
|---|---|---|---|---|---|
| 영문 publication 강화 | ★★★★★ | ★★ | ★★★ | ★★ | High |
| AGI 단행본 시리즈 | ★★★★★ | ★★★★ | ★★ | ★★★ | High |
| 한국 인구·경제 자문 | ★★★ | ★★★★★ | ★★★ | ★★★★ | High |
| 차세대 미래학자 양성 | ★★★★ | ★★★★ | ★★★★ | ★★★★ | High |
| MCEWS 차세대 | ★★★★ | ★★★ | ★★★ | ★★★ | Medium |

→ Robustness High Options = 모든 시나리오에서 고가치 = *no-regret moves*. 우선 추진.

## Phase 3 Report에 시나리오 포함 protocol

### Part 2 구조

```markdown
# Part 2: Alternative Scenarios

## Methodology
- Driving forces 분석 (cross-impact 기반)
- 2×2 매트릭스 구조
- 박사님 4가지 미래 가능성 framework 매핑
- Probability·robustness 평가

## Scenario A: [Name]
[1~2 페이지 sketch]

## Scenario B: [Name]
[동일]

## Scenario C: [Name]
[동일]

## Scenario D: [Name]
[동일]

## Cross-Scenario Analysis
- 공통 dynamics
- 결정적 차이점
- No-regret moves
- Fork actions

## Probability Distribution
- 5y·10y·15y horizon별
- Total 100%

## Strategic Issues for Phase 4
[시나리오 분석에서 도출된 Top 5~10 strategic issues]
```

### 시나리오 작성 시간 (분기 권고)
- 각 시나리오 sketch: 4~8 시간
- Cross-scenario analysis: 4~6 시간
- Part 2 전체: 30~40 시간 (1~2주)
