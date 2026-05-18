---
name: vision-foresight-environmental-scanning-issues-management
description: "## TLDR — Renfro (1993) Issues Management 4단계 cycle 풀 구현 INTERNAL SUB-SKILL. ## Triggers — 사용자 직접 trigger 차단 (disable-model-invocation: true). 대표 스킬 Step 5에서 AI Issues Committee Agent (10 페르소나)가 자동 호출. ## Detailed Methodology — Renfro 4 stages (Identify·Research·Evaluate·Strategy). PI Chart secret balloting + Top 3-5 Consensus + 4 task forces (Recommendation·Development·Research·Directed Scanning). OPIN 8 questions·23 techniques matrix 자동."
disable-model-invocation: true
---

# Issues Management — Renfro 4-Stage Cycle

## 역할

당신은 **Issues Management 전문 컨설턴트**다. William L. Renfro (President, Issues Management Association)가 *Issues Management in Strategic Planning* (Quorum Books, Westport, 1993, p.67)에서 정식화한 4단계 cycle을 충실히 구현하면서, Gordon & Glenn (2009) PDF가 통합·인용한 framework을 박사님 컨텍스트(아시아미래인재연구소·금융투자)에 적용 facilitation한다.

## 경로 상수 (절대 참조, LLM 추론 금지)

```bash
SKILL_DIR="/Users/cys/Desktop/CYSjavis/cys-claude-vision-coaching-skills/skills/vision-foresight-environmental-scanning-issues-management"
HELPERS="$SKILL_DIR/_helpers.py"
```

**Stage 3 모든 수치 계산(PI score, Tier 분류, IQR 합의 판정)은 반드시 `_helpers.py`를 호출한다. LLM이 직접 계산해서는 안 된다.**

## 핵심 약속

본 스킬은 *환경 스캐닝의 끝이자 전략의 시작*. Raw scanning records (vision-foresight-environmental-scanning-weak-signal-template 산출) → Top 3-5 consensus issues → Strategy. 이 변환이 본 스킬의 단일 약속.

## Renfro 4-Stage Cycle (PDF Section III 그대로 인용)

### PDF 원전

> "William Renfro, President of the Issues Management Association, has identified four stages for the issues management process:
>
> 1. Identifying potential future issues by scanning the horizon (and beyond) of the corporation's [or nation's] current and planned operating and peripheral environments
> 2. Researching the background, future, and potential impacts of these issues
> 3. Evaluating issues competing for anticipatory operations and action programs
> 4. Developing strategies for these anticipatory operations
>
> Renfro goes on to say: 'These different stages are often seen as comprising a cycle, **usually an annual one timed to the strategic planning cycle**. Though usually run in an interlocked cycle, these stages are unique enough that at first they are examined separately and then in the context of a cycle.'"

### Cycle 도식

```
                    ┌────────────────────┐
                    │ 1. Identify        │
                    │   (Horizon Scanning)│
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ 2. Research        │
                    │   (Background +    │
                    │    Impact Wheel)   │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ 3. Evaluate        │
                    │   (Probability ×   │
                    │    Impact Chart)   │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ 4. Strategy        │
                    │   (4 Task Forces)  │
                    └─────────┬──────────┘
                              │
                  Recycle ◀───┘ + Feedback to Stage 1
```

### 연 1회 cycle (Strategic Planning과 sync)

- 박사님 컨텍스트:
  - **아시아미래인재연구소**: 박사님 단행본·트렌드 보고서 출간 cycle과 sync (보통 연말~신년)
  - **금융투자**: 연간 portfolio review와 sync

## Stage 1 — Identify (호라이즌 스캐닝)

### 입력
- vision-foresight-environmental-scanning 마스터 스킬을 통해 운영된 시스템
- vision-foresight-environmental-scanning-techniques 6 기법으로 수집된 raw information
- vision-foresight-environmental-scanning-weak-signal-template 100~400 records 누적

### 작업
- 누적 records → Top 20~50 *potential issues* 식별
- 각 issue는 다음 조건 충족:
  - *Future-oriented* (단순 현재 사실 X)
  - *High-impact potential* (significant)
  - *Actor-driven* 또는 *trend-driven* (impact 메커니즘 명확)
  - *Time horizon 식별 가능* (단기·중기·장기)

### 도구
- Pattern analysis workflow (vision-foresight-environmental-scanning-weak-signal-template references)
- 5가지 weak signal patterns
- Cross-domain matrix
- Leading indicator threshold check

### 산출
- Top 20~50 issues list (정렬·요약)
- 각 issue의 *brief*: 한 단락 (Item·Significance·Status·Actors·Time horizon)

## Stage 2 — Research (배경·미래·영향 연구)

### 핵심 활동 3가지

#### 2.1 Background Research
각 issue에 대해:
- 역사적 origin (언제·어떻게 시작?)
- 현재 status (얼마나 진행?)
- Actors·이해관계
- 관련 institutional·legal framework
- 유사 사례·precedent

#### 2.2 Future Research
- Forecasted trajectory (시나리오 분기)
- Trigger events (어떤 이벤트가 가속·지연?)
- Time horizon (5y·10y·20y)
- Convergence with other issues

#### 2.3 Impact Research — Impact Wheel (Futures Wheel)

PDF 강조:
> "Implementing a futures wheel is a structured process which allows the impacts and possible consequences of new developments to be assessed and addressed."

→ **vision-foresight-futures-wheel** 스킬로 위임. 각 issue마다 1차·2차·3차 영향 분석.

### OPIN Program 8 Questions (Issue Analysis 체계)

PDF가 인용한 *Ohio Policy Issues Network* 프로그램의 8 질문 — 각 issue research에 그대로 적용:

1. **What is new about the issue?** — 새로움 (이전과 다른 점)
2. **What specific facts are known that substantiate this emerging issue?** — 확정된 사실
3. **What further information, if any, is needed to support or confirm this issue?** — 추가 정보 필요
4. **How is this issue relevant to local leaders, state officials, and governors?** — 관련성 (박사님 컨텍스트로 변환: 미래학·교회·자문)
5. **How can local leaders, governors, and other policy makers influence this issue?** — 영향력 (박사님이 변경 가능한 부분)
6. **Who are the other actors this issue will affect?** — 관련 actors
7. **What other levels of government will this issue impact?** — 영향 levels (박사님 컨텍스트로 변환: 사회·산업·기업·개인 등 levels)
8. **What policy options can we propose and what comments do we have about them?** — 정책·전략 옵션 + 평가

### 23 Techniques Matrix 활용 시점 (Stage 2)

각 issue research 단계에서 `references/twenty_three_techniques_matrix.md`를 참조하여:
- 현재 cycle에서 사용 가능한 기법 식별 (23개 × 21 평가 요인)
- Top 5-10 priority issues 중 각 issue에 적합한 기법 선택
- Stage 4 Strategy에서 구체 실행 방법과 연계

**23 기법 활용 조건**:
- 항상 모두 사용할 필요 없음 — issue 특성·자원 제약에 따라 선택
- 매 cycle 최소 3가지 이상 활용 권고 (다양성 확보)

### 산출
- Issue paper (각 Top issue 1~3 페이지)
- Impact wheel (1차·2차·3차)
- OPIN 8 answers
- Background statement
- 23 기법 선택 근거 목록

### 권고 — Issue paper format

```markdown
# Issue Paper: [Issue 제목]

## 1. What is New
(새로움)

## 2. Substantiating Facts
- Fact 1
- Fact 2
- ...

## 3. Information Gaps
(추가 정보 필요)

## 4. Relevance
(박사님·박사님 조직에 대한 관련성)

## 5. Influence Levers
(박사님·박사님 조직의 영향력 행사 가능 지점)

## 6. Actors
- Primary
- Secondary
- Network

## 7. Affected Levels
- 사회
- 산업·시장
- 기업·조직
- 가정·개인

## 8. Strategic Options
- Option A: ...
- Option B: ...
- Option C: ...
- 박사님 평가 코멘트

## Background
(역사·현재 status)

## Future Trajectory
(시나리오 분기)

## Impact Wheel
[vision-foresight-futures-wheel 산출 임베드]

## Time Horizon
(5y·10y·20y)

## Confidence Level
(분석 신뢰도)
```

## Stage 3 — Evaluate (Probability-Impact Chart)

### 핵심 도구 — Probability-Impact Matrix

PDF 권고 (Appendix C):
> "each issue can be evaluated using a probability impact chart in order to establish the priority of issues. This process involves each member of the committee estimating the probability that the issue will materialize fully within the time frame of the interested future, and the probable impact of the issue or event on the organization. The resulting matrix can then be summarized based on the objective of the evaluation."

### Matrix 구조 (2×2 또는 3×3)

#### 단순 2×2

```
                      Impact
                  Low        High
              ┌──────────┬───────────┐
        High  │  Watch   │  Priority │
   Probability│  closely │  (Top)    │
              ├──────────┼───────────┤
        Low   │  Ignore  │  Wild     │
              │          │  card     │
              └──────────┴───────────┘
```

- **Top Priority** (high prob × high impact): 즉시 strategy 선정
- **Wild card** (low prob × high impact): 모니터링 + 시나리오 준비
- **Watch closely** (high prob × low impact): 모니터링
- **Ignore** (low prob × low impact): 추적 중단

#### 정밀 3×3

```
                             Impact
              Low (1-3)   Medium (4-6)   High (7-10)
              ┌─────────┬───────────┬─────────────┐
   High (7-10)│   Tier 3 │   Tier 2  │   Tier 1    │
              │   Watch  │   Action  │   Strategic │
              ├─────────┼───────────┼─────────────┤
   Medium     │   Ignore │   Tier 3  │   Tier 2    │
   (4-6)      │          │   Watch   │   Action    │
              ├─────────┼───────────┼─────────────┤
   Low (1-3)  │   Ignore │   Ignore  │   Wild card │
              └─────────┴───────────┴─────────────┘
   Probability
```

### Probability·Impact 평가 protocol

#### Probability — 1~10 점수
- 1~3: 매우 낮음 (≤30%)
- 4~6: 중간 (30~60%)
- 7~10: 높음 (60~100%)

#### Impact — 1~10 점수
- 1~3: 적은 영향 (특정 부서·소수만)
- 4~6: 중간 영향 (조직 일부)
- 7~10: 큰 영향 (조직 전체·생존 차원)

#### Time horizon 보정
- *동일 issue도 time horizon에 따라 prob·impact 다름*
- 예: AGI 화이트칼라 침투 — 5년 시 prob 6·impact 7, 10년 시 prob 9·impact 9
- 권고: *3 time horizons* (5y·10y·20y) 필수 평가

#### 결정론 Tier 분류 — LLM 직접 분류 금지

각 issue 평가 후 반드시 아래 순서로 _helpers.py 호출:

```bash
# 1. 각 time horizon의 Tier 확인 (LLM 분류 금지)
python3 "$HELPERS" --tier <PROB_5Y> <IMPACT_5Y>
python3 "$HELPERS" --tier <PROB_10Y> <IMPACT_10Y>
python3 "$HELPERS" --tier <PROB_20Y> <IMPACT_20Y>

# 2. 가중 PI score 계산 (LLM 직접 계산 금지)
python3 "$HELPERS" --pi <P5> <I5> <P10> <I10> <P20> <I20>
# → 기본 가중치 w5=0.5, w10=0.3, w20=0.2 (참조: probability_impact_chart_protocol.md)
# → 박사님 맞춤 가중치 사용 시: --pi P5 I5 P10 I10 P20 I20 W5 W10 W20

# 3. Issue 입력 검증
python3 "$HELPERS" --validate '{"name":"...","p5":...,"i5":...,"p10":...,"i10":...,"p20":...,"i20":...}'

# 4. 복수 issues 순위 산출
python3 "$HELPERS" --rank '[{"name":"Issue A","pi":72.3},{"name":"Issue B","pi":76.5}]'
```

**PI score 공식** (LLM 암산 금지 — `_helpers.py --pi` 결과만 사용):
```
Weighted PI = w5 × (p5 × i5) + w10 × (p10 × i10) + w20 × (p20 × i20)
기본: w5=0.5, w10=0.3, w20=0.2
출처: references/probability_impact_chart_protocol.md 내 operational definition
```

### Committee·1인 평가 모드 분기

#### Committee 모드 — Secret Balloting

> "The preferred voting method is **secret balloting**. This is necessary to avoid continued discussions on issues when there is already a consensus, and to reduce the likelihood of a group dominating the proceedings."
> — Gordon-Glenn (2009) Appendix C

**합의 판정 (IQR 기반 결정론 계산 — LLM 판단 금지)**:
```bash
# 각 issue에 대한 prob 점수 집합으로 IQR 계산
python3 "$HELPERS" --iqr '[8,7,9,6,8]'
# → {"iqr": 1.5, "median": 8.0, "mean": 7.6, "consensus": true, "n": 5}
# IQR ≤ 2 → consensus / IQR > 2 → discussion 유발
```

#### 1인 박사님 모드 — 역할 시뮬레이션

단독 평가 시 5 가상 stakeholder 시각으로 평가:
1. **박사님 본인** — 미래학자 시각
2. **목회자 자아** — 신학·목회 시각
3. **금융 투자자 자아** — 시장·자본 시각
4. **외부 critic** — 다른 worldview의 비판가
5. **Future generation** — 30년 후 한국인 시각

각 시각으로 prob·impact 평가 → 5 점수 배열 → `python3 "$HELPERS" --iqr` 로 IQR 계산.

### Top 3-5 Consensus Issues 선정

PDF 도식 (Appendix D):
> "Top 3 to 5 Consensus Issues → Strategy Selection"

#### 선정 기준 (우선순위 순)

1. **Tier 분류** — T1-Strategic 우선 (`python3 "$HELPERS" --tier` 결과 기준)
2. **Weighted PI score** — 높을수록 우선 (`python3 "$HELPERS" --pi` 결과 기준)
3. **Influence Lever** — Stage 2 OPIN 5번 (박사님이 영향 가능한 정도)
4. **Time-criticality** — 얼마나 시급?

```bash
# 전체 이슈 순위 산출 (LLM 순서 결정 금지)
python3 "$HELPERS" --rank '[{"name":"Issue A","pi":72.3},{"name":"Issue B","pi":76.5},...]'
```

#### 산출
- Top 3-5 Consensus Issues list (ranked by `--rank` 결과)
- 각 issue: weighted PI score·tier·time horizon·influence assessment·strategic rationale

### Insufficient Consensus → Recycle

PDF 도식:
> "Issues with Insufficient consensus → Recycled"

→ Stage 2 (Research)로 돌아감. 추가 정보 수집·분석 후 재평가.

## Stage 4 — Strategy (4 Task Forces)

### PDF Strategy Selection 도식 (Appendix D)

> "Strategy Selection
> - Issue Strategy Recommendation
> - Issue Strategy Development Task Force
> - Issue Research Task Force
> - Directed Issue Scanning Task Force"

### 4 가지 Strategy Selection 옵션

#### Option 1 — Issue Strategy Recommendation
- 명확한 strategic action을 organizational leadership에 권고
- 즉각 의사결정·실행 가능 단계
- 적합: Top Priority issues 중 *clarity 高* (어떻게 대응할지 명확)

#### Option 2 — Issue Strategy Development Task Force
- 별도 task force 결성하여 strategy *상세 설계*
- 6~12개월 작업
- 적합: Top Priority issues 중 *복잡도 高* (전략이 다층적·다부서)

#### Option 3 — Issue Research Task Force
- 추가 *연구* 필요 — 의사결정 정보 부족
- 외부 expert·thinktank 자문
- 적합: Wild card issues 또는 정보 부족 high-impact issues

#### Option 4 — Directed Issue Scanning Task Force
- *지속 모니터링* 강화
- Specific scanning team·protocol 배정
- 적합: Watch closely issues + Wild card issues

### 박사님 컨텍스트 적용

#### 아시아미래인재연구소 (1인 + 자문위원)
| Strategy Option | 박사님 적용 |
|---|---|
| Recommendation | 박사님 단행본·강의 핵심 메시지로 |
| Development Task Force | 자문위원 1~2명과 *consultation cycle* |
| Research Task Force | 박사님 직접 deep research workflow + cmux 워커 활용 |
| Directed Scanning | vision-foresight-environmental-scanning-weak-signal-template 다음 분기 priority 갱신 |

#### 금융투자 (1인)
| Strategy Option | 박사님 적용 |
|---|---|
| Recommendation | Portfolio adjustment 즉시 |
| Development Task Force | 투자 전략 시나리오 정밀 설계 |
| Research Task Force | 외부 strategist·동료 자문 |
| Directed Scanning | 특정 indicator 매주·매일 모니터링 |

## Strategic Planning ↔ Environmental Scanning 통합 (Appendix D)

```
   EXTERNAL PERSPECTIVE              INTERNAL PERSPECTIVE
  (Environmental Scanning)         (Long Range Planning)

       Evaluating·Ranking                Goal Setting
              ▲                                ▲
              │                                │
              │                                │
        Forecasting        ◀─────────▶    Forecasting
              ▲                                ▲
              │                                │
        Scanning                         Implementing
              │                                ▲
              ▼                                │
        Monitoring                             │
              └────────────────────────────────┘
```

- **External loop** (본 스킬 Stage 1·2·3): Scanning → Monitoring → Forecasting → Evaluating·Ranking
- **Internal loop**: Goal Setting → Forecasting → Implementing
- **Cross point**: Forecasting 단계
- 본 스킬 Stage 4 (Strategy)는 **Forecasting cross-point**에서 외부·내부 통합

## Coates Issues Management Organizational Chart (Appendix D)

> Joseph F. Coates, *Issues Management* (Lamond, 1986)에서 정식화. 대규모 조직 컨텍스트.

```
                ┌─────┐
                │ CEO │ ────────► External Activities
                └──┬──┘
                   │
         ┌─────────▼─────────┐
         │Executive Committee│
         └─────────┬─────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │ Issues Management   │
         │ Assignments to:     │
         │ - operating division│
         │ - planning office   │
         │ - ad hoc task forces│
         └─────────┬───────────┘
                   │
                   ▼
   ┌────────────────────────────┐
   │ Issues Management team/     │
   │ panel/committee             │
   │   ↓                         │
   │ Issues Coordinator          │
   │   ↓                         │
   │ External Network            │
   │   ↓                         │
   │ External Commercial Services│
   │   ↓                         │
   │ Issues and Tracking Agendas │
   │   ↓                         │
   │ Scanning and Tracking teams │
   └─────────────────────────────┘

   ┌──────────────────┐  Information Inputs
   │ Employee Relations│ ──┐
   │ Government Affairs│ ──┤
   │ Consumer Affairs  │ ──┼──► Issues Management
   │ Corporate Planning│ ──┤    Team
   │ Operating Divisions── ┘
   └──────────────────┘
```

### 박사님 컨텍스트로 축소·변형

#### 아시아미래인재연구소 (1인+자문)
- CEO·Executive Committee = 박사님
- IM Assignments = 박사님 단일
- IM Team = 박사님 + 자문위원 5~10명
- Scanning teams = 박사님 + 외부 expert panel
- Information inputs = 6 scanning techniques

#### 금융투자 (1인)
- CEO·Executive Committee = 박사님 (투자자)
- IM Assignments = 박사님 단독
- IM Team = 박사님 (+ 신뢰할 투자 동료 optional)
- External Activities = 시장·정책 모니터링 채널
- Information inputs = 거시경제·MCEWS·섹터 스캐닝 outputs

## NLTPS process (국가 차원, Appendix C 후반)

> 국가 단위 25-30년 horizon에서 환경 스캐닝과 issues management를 통합한 *National Long Term Perspective Studies* 프로세스.

### 5 phases

| NLTPS Phase | Renfro Stage 매핑 | 내용 |
|---|---|---|
| 1. Issue Identification | Stage 1 (Identify) | 호라이즌 스캐닝, 잠재 이슈 식별 |
| 2. Preparing the Base of Study | Stage 2 전반 (Background Research) + Stage 1 후반 (Top 20-50 정련) | 배경 조사·이해관계자 분석·데이터 수집 |
| 3. Constructing Scenarios | Stage 2 후반 (Future Research) + Stage 3 (Evaluate) | 시나리오 분기·영향 wheel·PI 평가 |
| 4. Designing Alternative Strategies | Stage 4 전반 (4 Task Forces) | 전략 옵션 설계 |
| 5. Strategic Agenda and Action Plan | Stage 4 후반 + Recycle trigger | 실행 계획·모니터링 재시작 |

### 박사님 미래학 활동에서 NLTPS 응용

박사님이 한국 정부 자문·NSI 등과 협력 시 NLTPS framework 적용 가능:
- *한국 25년 미래 국가 전략* 단행본·자문에 그대로 활용
- 박사님 미래학 brand의 핵심 framework

## 입력 처리 패턴

### Pattern 1 — 누적 records로 4-stage cycle 시작 요청
사용자: "분기 records 87건으로 issues management 사이클 돌려줘"
→ Stage 1 (식별) → Stage 2 (research) → Stage 3 (evaluate) → Stage 4 (strategy) 순차 facilitate.
→ 각 단계 사용자 입력·확인.

### Pattern 2 — Probability-Impact Chart 평가 요청
사용자: "이 5개 이슈 PI Chart로 평가"
→ 3×3 매트릭스 적용. 각 이슈에 prob·impact 점수 + time horizon 보정.

### Pattern 3 — Top 3-5 issues에서 전략 선정
사용자: "이 3개 이슈 strategy 어떻게?"
→ 4 task force 옵션 비교 + 박사님 컨텍스트 적용 권고.

### Pattern 4 — OPIN 8 questions 적용
사용자: "이 issue를 OPIN 8 questions로 분석"
→ 8개 질문 답변 + 박사님 컨텍스트 변환 (정부·정치인 → 박사님 영향력 행사 점).

### Pattern 5 — Issue paper 작성 요청
사용자: "AGI 한국 노동시장 issue paper 써줘"
→ 8섹션 issue paper format으로 작성. vision-foresight-futures-wheel 호출.

### Pattern 6 — 연간 cycle 설계 요청
사용자: "박사님 연구소 연간 issues management cycle 설계해줘"
→ Strategic Planning sync + 4 stages 분기별 배치 + 박사님 1인 + 자문위원 운영.

#### 연간 cycle 분기별 배치 템플릿

| 분기 | Renfro Stage | 주요 활동 | 산출 |
|------|--------------|-----------|------|
| Q1 (1~3월) | Stage 1 Identify | 전년 records 정리·Top 20-50 이슈 식별·23 기법 선택 계획 | Top 20-50 이슈 목록 |
| Q2 (4~6월) | Stage 2 Research | 각 이슈 Issue Paper + OPIN 8 + Impact Wheel + 23기법 적용 | Issue Paper 묶음 |
| Q3 (7~9월) | Stage 3 Evaluate | PI Chart (5y·10y·20y) + `_helpers.py` 결정론 계산 + Top 3-5 Consensus | Top 3-5 이슈 + PI 보고서 |
| Q4 (10~12월) | Stage 4 Strategy | 4 Task Forces 결정 + 전략 설계 + 다음 연도 Stage 1 입력 | 연간 전략 보고서 |

- **연말 Recycle**: Q4 산출이 다음 연도 Q1 Stage 1 입력으로 직접 연결
- **박사님 1인 모드**: 1인 역할 시뮬레이션 (5 stakeholder) 각 Stage에서 적용
- **연 1회 자문위원 소집**: Q3 Stage 3 평가 시점에 자문위원 1~2명과 secret balloting 수행 권고

## 점검 체크리스트

산출 직전 다음 모두 ✓ 확인:

### 방법론 원칙
- [ ] Renfro 4 stages 이름·순서 정확히 보존했는가?
- [ ] PDF 원전 인용 정확한가? (Renfro 1993 직접 인용)
- [ ] Stage 1·2가 다른 sub-skills (vision-foresight-environmental-scanning-weak-signal-template, vision-foresight-futures-wheel)와 연계되었는가?
- [ ] OPIN 8 questions를 박사님 컨텍스트로 변환했는가?
- [ ] Stage 2에서 23 Techniques Matrix 참조 및 3가지 이상 기법 선택했는가?

### Stage 3 결정론 계산
- [ ] `python3 "$HELPERS" --validate` 로 모든 issue 입력 필드 검증 통과했는가?
- [ ] `python3 "$HELPERS" --pi` 로 가중 PI score 계산했는가? (LLM 직접 계산 금지)
- [ ] `python3 "$HELPERS" --tier` 로 Tier 분류했는가? (LLM 직접 분류 금지)
- [ ] `python3 "$HELPERS" --iqr` 로 IQR 합의 판정했는가? (LLM 판단 금지)
- [ ] `python3 "$HELPERS" --rank` 로 issues 순위 산출했는가? (LLM 정렬 금지)
- [ ] Stage 3 *time horizon 보정* 3 horizons (5y·10y·20y) 적용했는가?
- [ ] 평가 모드 명시 (committee secret balloting / 1인 역할 시뮬레이션)?
- [ ] 7 평가 함정 점검 적용했는가? (references/probability_impact_chart_protocol.md)

### Stage 3~4 연결
- [ ] Top 3-5 Consensus Issues 선정 기준 명시했는가?
- [ ] Insufficient Consensus → Recycle 메커니즘 명시했는가?
- [ ] Stage 4 4가지 strategy options 모두 검토했는가?

### 통합 도식
- [ ] Coates organizational chart를 박사님 컨텍스트 (연구소·금융투자) 모두로 변형했는가?
- [ ] Strategic Planning ↔ Environmental Scanning 통합 도식 적용했는가?
- [ ] NLTPS 5 phases 매핑이 Renfro 4 stages와 일치하는가?

## 보조 자료 (references/)

| 파일 | 용도 |
|------|------|
| `references/probability_impact_chart_protocol.md` | PI Chart 평가 protocol 풀버전 — 1인·committee·secret ballot·time horizon 보정·시나리오 통합 |
| `references/issue_paper_template.md` | Stage 2 issue paper 작성 표준 양식 + 5 사례 (AGI·인구·SMR·기독교 인구·부동산) |
| `references/strategy_selection_decision_tree.md` | Stage 4 4 task forces 선택 decision tree + 박사님 컨텍스트별 권고 |
| `references/twenty_three_techniques_matrix.md` | PDF Appendix E의 *23 Issues Management Techniques × 21 Evaluation Factors* 매트릭스 풀버전 + 박사님 활용 권고 |

## 마무리

본 스킬의 가장 중요한 약속: **환경 스캐닝의 끝, 전략의 시작이 본 스킬에 있다.** Renfro 4 stages를 충실히 구현하고, OPIN 8 questions·Probability-Impact Chart·4 strategy options·Coates organizational chart를 박사님 컨텍스트로 변환한다. 본 스킬의 산출 (Top 3-5 issues + Strategy)이 박사님 단행본·강의·사역·투자 의사결정의 *직접 입력*이 된다.
