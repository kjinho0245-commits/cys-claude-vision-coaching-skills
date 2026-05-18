# Probability-Impact Chart 평가 — 풀버전 protocol

> Gordon-Glenn (2009) Appendix C 권고 + Renfro framework 통합

## 평가 단위

각 issue를 *time horizon별*로 평가. 단일 issue도 5y·10y·20y 시점에 따라 prob·impact 다름.

## Probability 평가 protocol

### 1~10 점수 정의

| 점수 | 정의 | 확률 범위 | 신뢰도 표현 |
|---|---|---|---|
| 1 | 거의 불가능 | ≤5% | "extremely unlikely" |
| 2~3 | 매우 낮음 | 5~25% | "unlikely" |
| 4 | 낮음 | 25~40% | "less likely than not" |
| 5 | 중립 | 40~60% | "uncertain·toss-up" |
| 6 | 약간 높음 | 60~75% | "more likely than not" |
| 7~8 | 높음 | 75~90% | "likely" |
| 9~10 | 매우 높음·확실 | ≥90% | "very likely·virtually certain" |

### Probability 평가 시 고려 요인

1. **Trend strength** — 현재 trend가 issue를 향해 가고 있는 강도
2. **Trigger event likelihood** — 가속 trigger의 확률
3. **Counter-force** — issue를 막는 force (정책·자연·resistance)
4. **Time horizon** — 시간이 길수록 일반적으로 prob 증가, 그러나 *fundamental change*가 일어날 수도
5. **Historical analogy** — 유사 사례에서 학습

### Probability 평가 함정

- **Recency bias** — 최근 사건에 과도 비중
- **Anchoring** — 첫 수치에 과도 anchor
- **Wishful thinking** — 박사님이 *원하는* 시나리오에 prob 과대평가
- **Pessimism bias** — 박사님이 *두려워하는* 시나리오에 prob 과대평가

→ 평가 후 *5 함정 체크* 권고.

## Impact 평가 protocol

### 1~10 점수 정의

| 점수 | 정의 | 영향 범위 |
|---|---|---|
| 1 | 무시 가능 | 특정 부서·소수 |
| 2~3 | 작음 | 한 fungible 기능 영향 |
| 4 | 중간 | 한 division 또는 부분 process |
| 5~6 | 상당함 | 다수 division·process |
| 7~8 | 큼 | 조직 핵심 시스템·전략 |
| 9~10 | 거대·존립 | 조직 생존·정체성 차원 |

### Impact 평가 시 고려 요인

1. **Scope** — 영향받는 stakeholder 범위
2. **Magnitude** — 영향 크기 (revenue·cost·인력·평판)
3. **Reversibility** — 회복 가능성 (revisible vs irreversible)
4. **Cascading** — 2차·3차 파급 (vision-foresight-futures-wheel)
5. **Time pressure** — 응답 시간 압박

### 박사님 컨텍스트별 Impact 정의

#### 아시아미래인재연구소 (1인 + 자문)
- 1: 박사님 연구·강의 1회분 영향
- 5: 박사님 단행본 1권·연간 자문 시즌 영향
- 10: 박사님 미래학 brand·life work 차원 영향

- 1: 부서 1개 사역 영향
- 5: 분기·연간 사역 계획 영향
- 10: 교회 존립·정체성 차원 영향

#### 금융투자
- 1: 단일 종목 5% 변동
- 5: portfolio 20% 변동
- 10: portfolio 50% 이상 변동·재구성 필요

## 평가 매트릭스

### Tier 분류 (3×3)

```
                             Impact
              Low (1-3)   Medium (4-6)   High (7-10)
              ┌─────────┬───────────┬─────────────┐
   High (7-10)│   T3    │    T2     │     T1      │
              │  Watch  │  Action   │  Strategic  │
              ├─────────┼───────────┼─────────────┤
   Medium     │ Ignore  │    T3     │     T2      │
   (4-6)      │         │  Watch    │  Action     │
              ├─────────┼───────────┼─────────────┤
   Low (1-3)  │ Ignore  │  Ignore   │ Wild card   │
              └─────────┴───────────┴─────────────┘
   Probability
```

### Tier별 strategy 자동 매핑

| Tier | Strategy Selection 권고 (Stage 4) |
|---|---|
| T1 (Strategic) | Issue Strategy Recommendation 즉시 |
| T2 (Action) | Issue Strategy Development Task Force |
| T3 (Watch) | Issue Research Task Force 또는 Directed Scanning |
| Wild card | Directed Scanning + 시나리오 준비 |
| Ignore | 추적 중단 (그러나 분기 review 시 재평가) |

## Time Horizon 보정 — 동일 issue, 다중 horizons

### 표 양식

| Issue | 5y prob | 5y impact | 10y prob | 10y impact | 20y prob | 20y impact |
|---|---|---|---|---|---|---|
| AGI 화이트칼라 | 7 | 6 | 9 | 9 | 10 | 10 |
| 한국 출산율 0.5 | 4 | 7 | 7 | 9 | 9 | 10 |
| 한국 기독교 22% | 9 | 8 | 9 | 9 | 9 | 9 |
| 한반도 통일 | 1 | 10 | 3 | 10 | 5 | 10 |

### 시계 horizon 통합 점수 — 가중평균

```
PI score = Σ (w_t × prob_t × impact_t)

박사님 권고 weights:
- 5y: 0.5 (가까운 미래에 큰 가중)
- 10y: 0.3 (중기)
- 20y: 0.2 (장기·불확실)
```

→ 박사님이 우선순위에 따라 weights 조정 가능. 5년 안에 행동해야 하는 결정은 5y weight ↑.

## Committee 평가 — Secret Balloting

### PDF 권고 (Appendix C)

> "The preferred voting method is secret balloting. This is necessary to avoid continued discussions on issues when there is already a consensus, and to reduce the likelihood of a group dominating the proceedings."

### Secret Balloting protocol

1. **각 멤버 독립 평가** — 사전 자료 review 후 *익명* 평가지 작성
2. **수집·집계** — Median + IQR (사분위) 계산
3. **Consensus check** — IQR ≤2 시 consensus, IQR >2 시 discussion 유발
4. **Discussion** — Outlier 평가자가 *justify* (그러나 익명 가능)
5. **Re-vote** — 1~3회 추가 투표 후 final

### 1인 박사님 모드 (대안)

박사님 단독 평가 시 *역할 시뮬레이션*으로 group dynamics 모사:

#### 5 가상 stakeholder 시각
1. **박사님 본인** — 미래학자 시각
2. **목회자 자아** — 신학·목회 시각
3. **금융 투자자 자아** — 시장·자본 시각
4. **외부 critic** — 박사님과 다른 worldview의 비판가 (보수·진보·세대 등)
5. **Future generation** — 30년 후 한국인 시각

각 시각으로 prob·impact 평가 → 5 점수 평균 + dispersion 확인 → IQR 큰 issue는 *재고* 권고.

## 평가 함정 — 공통 7가지

### 1. Group think (집단 사고)
- *증상*: 모두 비슷한 점수
- *대응*: Secret balloting 강화, devil's advocate 지정

### 2. Anchoring
- *증상*: 첫 평가자 점수에 anchor
- *대응*: 동시 제출, anonymous

### 3. Halo effect
- *증상*: 한 issue가 prob 높으면 impact도 높게
- *대응*: prob·impact *별도 round*로 평가

### 4. Recency·Salience
- *증상*: 최근·언론 다룬 이슈 over-rated
- *대응*: *역사적 base rate* 비교

### 5. Wishful·Pessimism bias
- *증상*: 원하는 미래 prob ↑, 두려운 미래 prob ↑ 동시 (둘 다 가능)
- *대응*: *외부 위치* 시뮬레이션 (5 stakeholder 시각)

### 6. Time horizon 무시
- *증상*: 단일 점수만 평가
- *대응*: 3 horizons (5·10·20y) 표 강제

### 7. Cross-impact 무시
- *증상*: issue를 isolated로 평가
- *대응*: vision-foresight-futures-wheel cross-impact 분석 통합

## 박사님 컨텍스트 사례 — 실제 평가

### 사례 — 박사님 5 issues 평가

```
Issue 1: AGI 한국 화이트칼라 침투
- 5y: prob 7, impact 8 → 56
- 10y: prob 9, impact 9 → 81
- 20y: prob 10, impact 10 → 100
- 가중 PI: 56*0.5 + 81*0.3 + 100*0.2 = 72.3 → Tier 1 (Strategic)

Issue 2: 한국 출산율 0.5 진입
- 5y: prob 4, impact 7 → 28
- 10y: prob 7, impact 9 → 63
- 20y: prob 9, impact 10 → 90
- 가중 PI: 28*0.5 + 63*0.3 + 90*0.2 = 50.9 → Tier 1·T2 경계

Issue 3: 한국 기독교 인구 22% 미만
- 5y: prob 9, impact 8 → 72
- 10y: prob 9, impact 9 → 81
- 20y: prob 9, impact 9 → 81
- 가중 PI: 72*0.5 + 81*0.3 + 81*0.2 = 76.5 → Tier 1 (Strategic)

Issue 4: 한반도 통일
- 5y: prob 1, impact 10 → 10
- 10y: prob 3, impact 10 → 30
- 20y: prob 5, impact 10 → 50
- 가중 PI: 10*0.5 + 30*0.3 + 50*0.2 = 24 → Wild card (low prob × high impact)

Issue 5: 한국 부동산·인구 동시 변곡
- 5y: prob 6, impact 7 → 42
- 10y: prob 8, impact 9 → 72
- 20y: prob 9, impact 9 → 81
- 가중 PI: 42*0.5 + 72*0.3 + 81*0.2 = 58.8 → Tier 1·T2 경계
```

### Top 3-5 Consensus Issues 선정

| Rank | Issue | Weighted PI | Tier | Strategy 권고 |
|---|---|---|---|---|
| 1 | 한국 기독교 인구 22% | 76.5 | T1 Strategic | Recommendation + Development TF (목회 컨텍스트) |
| 2 | AGI 한국 화이트칼라 | 72.3 | T1 Strategic | Recommendation (단행본·강의) |
| 3 | 한국 부동산·인구 변곡 | 58.8 | T1/T2 경계 | Development TF (금융·미래학 시나리오) |
| 4 | 한국 출산율 0.5 | 50.9 | T2 Action | Research TF + Directed Scanning |
| 5 | 한반도 통일 | 24 (Wild card) | Wild card | Directed Scanning + 시나리오 준비 |

→ 박사님 다음 단행본·자문·사역 priority의 직접 input.

## 평가 보고서 표준 양식

```markdown
# Issues Management — Stage 3 Probability-Impact Evaluation

**Cycle**: 2026 Q2
**Evaluator**: 최윤식 박사 (single + role simulation)
**Issues evaluated**: 12 (Stage 1·2 통과)
**Date**: 2026-05-09

## Summary
- Top 5 Consensus Issues 선정: [list]
- Wild card issues: [list]
- Insufficient consensus → Recycle: [list]
- Ignore (추적 중단): [list]

## Methodology
- 3×3 Tier matrix
- 3 time horizons (5·10·20y)
- 가중치: 0.5·0.3·0.2
- 5 stakeholder role simulation
- 7 함정 체크 적용

## 평가 표
| Issue | 5y P | 5y I | 10y P | 10y I | 20y P | 20y I | Weighted PI | Tier |
|---|---|---|---|---|---|---|---|---|
| ... | | | | | | | | |

## 7 함정 체크
- [ ] Group think 위험: ...
- [ ] Anchoring: ...
- [ ] Halo effect: ...
- [ ] Recency bias: ...
- [ ] Wishful bias: ...
- [ ] Time horizon: ...
- [ ] Cross-impact: ...

## Top 3-5 Consensus Issues
[상세]

## Strategy 권고 (Stage 4 입력)
[Issue별 4 strategy options 중 선택 + 근거]
```
