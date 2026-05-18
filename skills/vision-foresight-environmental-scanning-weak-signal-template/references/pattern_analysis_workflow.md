# Pattern Analysis Workflow — 누적 records → Weak Signal 추출

> Gordon-Glenn (2009) 핵심 약속: "additional 'weak signals' or new elements can be found within the **pattern of previously identified issues, trends, or potential future events**" — 이를 step-by-step protocol로 구현

## Workflow Overview

```
┌─────────────────────────────────────────────────────┐
│ Step 1 │ Records 누적 (분기 50~100건)             │
└────┬────────────────────────────────────────────────┘
     ▼
┌─────────────────────────────────────────────────────┐
│ Step 2 │ Field별 키워드 검색 (single-field analysis) │
└────┬────────────────────────────────────────────────┘
     ▼
┌─────────────────────────────────────────────────────┐
│ Step 3 │ Cross-field pattern 식별                  │
└────┬────────────────────────────────────────────────┘
     ▼
┌─────────────────────────────────────────────────────┐
│ Step 4 │ 5가지 weak signal 패턴 적용                │
└────┬────────────────────────────────────────────────┘
     ▼
┌─────────────────────────────────────────────────────┐
│ Step 5 │ Pattern 보고서 산출 + 평가 단계로 위임     │
└─────────────────────────────────────────────────────┘
```

## Step 1 — Records 누적

### 권고 cadence
- **분기당 50~100 records** (박사님 1인 기준)
- **연간 200~400 records** 누적

### Quality control
- 매 record 작성 시 *모든 필드* 채우려 시도 (Empty field 최소화)
- 최소 충족 조건:
  - Item, Description, Source, Date, Scanner = 100% 필수
  - Significance, Consequences, Status, Actors = ≥80% 채움
  - Leading Indicator, Misc = ≥60% 채움

### Storage 권고
- 단일 통합 DB (Notion·Airtable·markdown directory)
- 매 record id (예: `2026-05-09-001`) 부여
- Frontmatter (YAML) 또는 column으로 *검색 가능 metadata*

## Step 2 — Field별 키워드 검색 (single-field analysis)

### PDF 권고 (Section II)
> "one might search field number 7 for consequences using the word 'health' and generate a report of all items with impacts on health that have been entered"

### 5 핵심 single-field 검색 패턴

#### Pattern A — Domain 분포 분석 (KOC 필드 1 / UNDP 필드 9)

> 필드 번호 확인: `python3 validate_record.py field-number KOC domain` → 1  
> 필드 번호 확인: `python3 validate_record.py field-number UNDP classification` → 9

```
질문: "이번 분기 어느 도메인에 records가 가장 많이 누적되었나?"

결과 표:
| Domain | Q1 records | Q2 records | YoY | Trend |
|---|---|---|---|---|
| Energy | 8 | 18 | +125% | ↑↑ |
| Population | 12 | 14 | +17% | ↑ |
| AI/S&T | 25 | 22 | -12% | ↓ |
| Spirituality | 3 | 11 | +267% | ↑↑↑ ← weak signal |
| ... | | | | |

해석: Spirituality 필드의 *267% 증가*가 weak signal.
박사님 attention 필요.
```

#### Pattern B — Actors 빈도 분석 (KOC 필드 9 / UNDP 필드 7)

> 필드 번호 확인: `python3 validate_record.py field-number KOC actors` → 9  
> 필드 번호 확인: `python3 validate_record.py field-number UNDP actors` → 7

```
질문: "어떤 actor가 가장 자주 등장하는가? 새 등장 actor는?"

결과 표:
| Actor | Q1 | Q2 | 첫 등장 | 도메인 |
|---|---|---|---|---|
| Sam Altman | 8 | 12 | 2024 | AI |
| Anthropic | 5 | 11 | 2024 | AI |
| 통계청 | 6 | 8 | 2024 | Population/Economy |
| 김정은 | 2 | 7 | 2024 | Conflict ← 증가 |
| Tara Burton | 0 | 4 | 2026-Q2 | Spirituality ← 신규 |
| ...

해석: Tara Burton 신규 등장 + Spirituality 도메인 급증 = correlated weak signal.
```

#### Pattern C — Consequences 키워드 cluster (KOC 필드 7 / UNDP 필드 5)

> 필드 번호 확인: `python3 validate_record.py field-number KOC consequences` → 7  
> 필드 번호 확인: `python3 validate_record.py field-number UNDP consequences` → 5

```
질문: "Consequences 필드에서 가장 자주 나오는 키워드는?"

검색 keywords (자동 추출):
- "automation" — 18 records (AI·노동시장·생산성)
- "fertility" — 15 records (인구·경제·종교)
- "energy demand" — 12 records (AI·SMR·기후)
- "meaning" / "의미" — 11 records (정신건강·종교·청년) ← cross-domain
- "polarization" — 9 records (정치·경제·세대)
- "loneliness" / "외로움" — 8 records (인구·청년·종교) ← weak signal cluster

해석: "meaning"·"loneliness"·"fertility" 키워드가 *서로 다른 primary domains*에 동시 등장 = *cross-domain underlying dynamic* 존재 신호.
```

#### Pattern D — Leading Indicator (KOC 필드 2) trigger 분석
```
질문: "어떤 leading indicators가 임계치에 가까워지고 있는가?"

표:
| Indicator | Threshold | Current | Distance |
|---|---|---|---|
| 합계출산율 | 0.7 | 0.72 | very close ← critical |
| 한국 기독교 인구 | 22% | 추정 19~21% | already crossed? |
| 가계부채/GDP | 105% | ~104% | very close |
| AGI capability index | TBD | 진행 | ??? |
| ...

해석: 다수 indicators가 동시에 임계치 접근 = *convergent inflection*.
```

#### Pattern E — Status transition 분석 (KOC 필드 8 / UNDP 필드 6)

> 필드 번호 확인: `python3 validate_record.py field-number KOC status` → 8  
> 필드 번호 확인: `python3 validate_record.py field-number UNDP status` → 6

```
질문: "Status가 'lab testing'에서 'early commercial'로 이동한 records는?"

표:
| Item | Q1 status | Q2 status | Transition |
|---|---|---|---|
| 한국 SMR | conceptual | designing | ↑ |
| Synthetic biology 산업화 | lab testing | early commercial | ↑↑ ← signal |
| AGI 화이트칼라 침투 | PoC | early deployment | ↑↑ ← signal |
| ...

해석: 다수 records가 *동시에* 한 단계 이동 = *technology cluster maturity*.
```

## Step 3 — Cross-field pattern 식별

### 5 핵심 cross-field 패턴

#### Cross 1 — Domain × Date 시계열
```
도메인별 누적 record 수의 시간 변화 그래프:

Quarter →   Q3'25  Q4'25  Q1'26  Q2'26
Energy        5      7      8     18  ←── 급증
Population   10     11     12     14
S&T          22     24     25     22
Spirituality  2      3      3     11  ←── 급증
Conflict      4      6      7     11  ←── 점진 증가
...

해석: Energy + Spirituality 동시 급증.
가설: AGI 출현 → 에너지 수요 + 의미 위기 동시 자극
```

#### Cross 2 — Domain × Actor matrix
```
도메인별 등장 actors:
| Domain | Top Actors |
|---|---|
| AI/S&T | Altman·Amodei·Hassabis·KAIST AI |
| Energy | 한수원·두산·BloombergNEF·EIA |
| Population | 통계청·KIHASA·조영태 |
| Spirituality | Burton·Brooks·Smith·정재영·박사님 |

질문: 어떤 actor가 *2개 이상 도메인*에 등장? → cross-domain leader
박사님: AI·미래학·금융·신학 4개 도메인 등장 (=박사님 본인이 cross-domain)
```

#### Cross 3 — Leading Indicator × Status convergence
```
서로 다른 records의 Leading indicator + Status:
- 출산율 0.7 → "convergent" (이미 임계 통과)
- AGI 화이트칼라 → "convergent" (early deployment)
- 한국 기독교 22% → "convergent" (cross 직전)
- 부동산 PIR 17 → "convergent"

해석: 4개 다른 도메인의 indicator가 *동시 임계 통과* → *2026~2028 한국 다중 변곡점*
```

#### Cross 4 — Consequences keyword × Domain
```
"meaning" 키워드 등장 records:
- AI 출현 (S&T) → "직업 정체성 의미 위기"
- 청년 정신건강 (Population) → "삶 의미 추구"
- 한국 기독교 감소 (Spirituality) → "종교 외 의미 추구"
- 출산율 (Population/Economy) → "결혼·출산 의미 회의"

해석: 4개 도메인이 *공통 underlying* 변수 (의미 위기)에 의해 묶임.
박사님 단행본 후보 토픽: *AI 시대 한국의 의미 위기*
```

#### Cross 5 — Source × Direction (긍정·부정·중립)
```
기관별 보고서 sentiment:
| Source | Records | 긍정·기회 | 부정·위협 | 중립 |
|---|---|---|---|---|
| BloombergNEF | 12 | 9 | 1 | 2 |
| KIEP | 8 | 3 | 4 | 1 |
| KINU | 6 | 1 | 4 | 1 |
| Wilson Center | 5 | 3 | 1 | 1 |

해석: 한국 정책 기관 (KIEP·KINU) 보고서가 *부정* 비중 높음 = 한국 기관의 *cautious bias*.
박사님 균형 위해 글로벌 thinktank 보고서 보강 권고.
```

## Step 4 — 5가지 weak signal 패턴 적용

### Weak Signal Pattern 1 — 갑작스런 frequency 증가
- Records 빈도가 6개월 전 5건 → 최근 1개월 20건
- 통계적 *2 sigma* 이상 spike
- 예: Spirituality 도메인 Q1 3건 → Q2 11건 (267%)

### Weak Signal Pattern 2 — Cross-domain 침투
- 한 도메인의 record가 갑자기 다른 도메인에 자주 등장
- 예: AI (S&T) records가 Spirituality 필드에 점차 등장 ("AI 시대 의미 위기")
- 예: Energy records가 Politics 필드에 등장 (지정학적 에너지 안보)

### Weak Signal Pattern 3 — 새 actor 등장
- Actors 필드에 처음 보는 인물·기관이 *반복* 등장
- 예: Tara Isabella Burton — 2026 Q2 처음 등장 후 4번 재등장 = *thinker가 박사님 분야 진입*

### Weak Signal Pattern 4 — Consequences 키워드 shift
- 같은 도메인의 consequences 키워드가 시간에 따라 변화
- 예: AI 도메인 — 2024 "efficiency"·"productivity" 중심 → 2026 "meaning"·"identity"·"values" 중심
- *논의 무게중심*이 기능 → 가치로 이동

### Weak Signal Pattern 5 — Status convergence
- 다수 records가 *비슷한 시기*에 status transition
- 예: 2026 Q2에 다수 record가 "lab testing" → "early commercial"
- *기술 군집의 동시 성숙*

## Step 5 — Pattern Report 산출

### 권고 보고서 구조

```markdown
# 환경 스캐닝 분기 패턴 분석 보고서
**분기**: 2026 Q2
**기간**: 2026-04-01 ~ 2026-06-30
**Scanner**: 최윤식 박사
**Records 분석**: 87건 (Q1 73건 → +19%)

## Executive Summary
3대 weak signals 식별:
1. Spirituality 도메인 records 267% 급증 — AI 시대 의미 위기
2. 다중 한국 indicators 동시 임계 접근 (2026~2028 변곡)
3. "Meaning" 키워드 cross-domain (AI·청년·종교·출산) 등장

## 1. Records 누적 현황
| Domain | Records | YoY | Status |
|---|---|---|---|
| ... | | | |

## 2. Single-field 분석 결과
### 2.1 Domain 분포
### 2.2 Actor 빈도
### 2.3 Consequences 키워드 cluster
### 2.4 Leading Indicator 임계치 분석
### 2.5 Status transitions

## 3. Cross-field 패턴
### 3.1 Domain × Date 시계열
### 3.2 Domain × Actor matrix
### 3.3 LI × Status convergence
### 3.4 Consequences × Domain ("meaning" cluster)
### 3.5 Source × Sentiment

## 4. Weak Signals 식별
### Signal 1: AI·영성 융합 (cross-domain dynamic)
- 근거: ...
- 함의: ...
- 추가 모니터링: ...

### Signal 2: 한국 다중 변곡점 (2026~2028)
### Signal 3: ...

## 5. 다음 단계
- vision-foresight-environmental-scanning-issues-management 단계로 위임
- Top 3~5 issues 평가 권고
- 분기 사이클 다음 회차 priority 갱신

## 6. Limitations
- N=87 records로는 통계적 유의성 X
- 박사님 1인 scanner의 cognitive bias 가능
- Source bias (한국 기관 보고서 비중 高)
```

## 박사님 분기 사이클 권고

### 매 분기 (3개월) 사이클

#### Week 1~10: Records 누적
- 일상 환경 스캐닝 → records DB 입력
- 주간 30분 review 루틴

#### Week 11: Pattern analysis
- 본 workflow Step 2~4 적용
- ChatGPT·Claude·Notion AI 등으로 자동 키워드 추출 보조

#### Week 12: Pattern report 산출 + Issues Management 평가 단계로 위임
- 위 보고서 구조로 산출
- Top 3~5 weak signals 식별
- **vision-foresight-environmental-scanning-issues-management** 스킬로 위임 → Renfro 4-stage cycle Stage 2~3 진행

#### Year-end: 4 분기 통합 review
- 연간 weak signals trend
- 박사님 단행본·강의 priority 갱신
- 차년도 scanning priority 조정 (feedback loop)

## 자동화 권고 (박사님 cmux 환경)

### 자동화 가능 영역
- Records DB grep 검색 → 키워드 빈도
- Domain 분류 (LLM 자동)
- Sentiment analysis (positive·negative·neutral)
- Cross-domain matrix 생성

### 자동화 어려운 영역
- *판단력*이 필요한 patten 해석 (박사님 통찰)
- Weak signal 신뢰도 평가
- 박사님 컨텍스트 (목회·미래학·금융) 적용

→ **반자동화 권고**: 자동 산출 → 박사님 review·해석
