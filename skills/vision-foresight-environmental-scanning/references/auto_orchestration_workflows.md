# Auto Orchestration Workflows — 9 Cycles 자동 실행 풀 protocol

> 사용자 절대 기준 4 — *모든 작업 자동, AI 에이전트로 사람 대체*. 본 문서는 9 Cycles (A~I) 각각의 *시작-종료 자동 실행 protocol*.

## Cycle A — 풀 사이클 (Full Environmental Scanning)

**사용자 명령 패턴**: "[주제] 환경 스캐닝 해줘"

### 자동 실행 시간표

| 단계 | 시간 | Agent | 작업 |
|---|---|---|---|
| **Step 1-A** | 30~60초 | 대표 | **Implications Domain 1회 질문 + 사용자 답변 수신** (10 default 옵션 + Custom + skip) |
| Step 1-B | 15초 | 대표 | Domain·scope·time horizon·9+1 도메인 자동 추론 |
| Step 2 | 1~3분 | Agent 1 | Scanner — 9+1 도메인 keyword·web search/fetch·50~200 records |
| Step 3 | 1~2분 | Agent 2 | Analyst — 10/13-field 변환·9+1 분류·5 weak signals |
| Step 4 | 3~5분 | Agent 3 | Expert Panel — 30~50 페르소나 3 rounds·synthesis |
| Step 5 | 2~3분 | Agent 4 | Issues Committee — Renfro 4-stage·Top 3-5·Strategy |
| Step 6 | 2~3분 | Agent 6 | Report Editor — Appendix B 보고서 *사용자 N 도메인별 implications* 자동 작성 |
| Step 7 | 30초 | 대표 | Final synthesis — Executive summary + 사용자 도메인별 행동 권고 + next priorities |

**총 소요**: 10~15분 (사용자 *Implications Domain 1회 답변 + 대기*)

### 자동 산출

```
[사용자에게 전달되는 결과]

# [주제] 환경 스캐닝 보고서 — YYYY-MM-DD

## Executive Summary (1 page)
- 핵심 발견 3~5
- 사용자 *즉시 행동* 권고
- Wild card·warnings

## Item 1~5: Strategic Issues (Top 5)
[각 Item: Title·Summary·3 Implications·Sources]

## Item 6: Technological Advances
[4~8 sub-items]

## Item 7: Updates on Previously Identified
[5~10 update items, cross-month tracking]

## Item 8: Reports Suggested for Review
[1~3 신간 외부 보고서 추천]

## Top 3-5 Consensus Issues + Strategy (Renfro)
[각 issue: PI Chart·OPIN 8 questions·Strategy 4 task forces 매핑]

## 4 Alternative Scenarios (옵션, time horizon 길 때)
[Plausible·Possible·Wild Card·Preferred]

## Action Recommendations
- 즉시 (이번 분기)
- 중기 (1년 내)
- 장기 (5년 내)

## Next Cycle Priorities
- 다음 월간·분기 monitoring keywords
- 추가 deep research 영역

## Appendix
[Item별 expanded background + comprehensive sources]
```

---

## Cycle B — Weak Signal 추출 (단축형)

**사용자 명령 패턴**: "[주제] weak signal 찾아줘", "[주제] horizon scanning"

### 자동 실행 (5~7분)

```
Step 1: Domain·scope 추론 (15초)
Step 2: Agent 1 Scanner (2분) — 50~100 records
Step 3: Agent 2 Analyst (2분) — 5 weak signal patterns
Step 4: 대표 synthesis (1분) — Top 5~10 weak signals 보고
```

### 산출
- Top 5~10 Weak Signals (각: 정의·근거 records·신뢰도·implications)
- 다음 단계 권고 (Cycle A 풀 사이클 권고 시)

---

## Cycle C — 월간 보고서 (정기)

**사용자 명령 패턴**: "이번 달 환경 스캐닝 보고서", "월간 보고서"

### 자동 실행 (5~10분)

```
Step 1: 지난 1개월 records 자동 collection (Agent 1 보충 검색)
Step 2: Agent 2 Analyst (2분) — 분류·패턴
Step 3: Agent 6 Report Editor (5분) — Appendix B 양식 자동 작성
Step 4: 대표 final review (1분) — Executive summary 추가
```

### 산출
- Body 8~15p + Appendix 5~20p 완성본
- 사용자 review 없이 활용 가능
- Issue ID cross-month 자동

---

## Cycle D — QUEST 워크숍

**사용자 명령 패턴**: "[주제] QUEST 워크숍", "[주제] 전략 워크숍"

### 자동 실행 (15~20분)

```
Step 1: Strategic issue 자동 정의 (대표, 30초)
Step 2: Agent 1 Scanner (2분) — Notebook 자료
Step 3: Agent 5 QUEST Workshop (15분):
  - Phase 1 Preparation (자동, 1분)
  - Phase 2 All-day Workshop 시뮬레이션 (자동, 8분)
  - Phase 3 2-section Report (자동, 3분)
  - Phase 4 Strategic Options (자동, 3분)
Step 4: 대표 synthesis (2분)
```

### 산출
- QUEST 4-phase 풀 산출
  - Refined mission/purposes/objectives
  - 30~50 trends + cluster
  - Cross-impact matrix
  - 4 Alternative Scenarios (vision-four-futures framework)
  - Strategic Options 평가
  - Top 5~10 Strategic Issues 시리즈
- 사용자 행동 plan

---

## Cycle E — Issue 평가 (Renfro 4-stage)

**사용자 명령 패턴**: "[주제] 이슈 평가", "Top 5 issues 뽑아줘"

### 자동 실행 (5~8분)

```
Step 1: 누적 records 또는 새 Scanner (Agent 1·2, 3분)
Step 2: Agent 4 Issues Committee (5분):
  - Stage 1 Identify
  - Stage 2 Research (OPIN 8·Issue Paper)
  - Stage 3 Evaluate (PI Chart·secret balloting)
  - Stage 4 Strategy (4 task forces)
Step 3: 대표 synthesis
```

### 산출
- Top 3-5 Consensus Issues
- 각 issue Issue Paper
- Strategy 4 task forces 매핑
- 사용자 행동 권고

---

## Cycle F — Horizon Scanning (단축)

**사용자 명령 패턴**: "[주제] horizon scanning 짧게"

### 자동 실행 (3~5분)

```
Step 1: Agent 1 Scanner (2분, 30~50 records)
Step 2: Agent 2 Analyst (1~2분, 분류·간이 패턴)
Step 3: 대표 synthesis (1분)
```

### 산출
- Records 30~50건 standardized
- Top 5 emerging trends (1줄씩)
- 다음 cycle 권고

---

## Cycle G — Top 5 Issues + Strategy (특정)

**사용자 명령 패턴**: "[주제] Top 5 issues + strategy"

### 자동 실행 (8~10분)

Cycle E 변형 — Strategy 단계 *상세*.

```
Step 1: Records 또는 신규 검색
Step 2: Agent 4 Issues Committee 풀 cycle
Step 3: Agent 6 Report Editor — Strategy 자료 강조
Step 4: 사용자 3 컨텍스트 (Futurology·Pastoral·Investment)별 *Strategy specific* 권고
```

### 산출
- Top 5 Consensus Issues
- 각 issue 4 strategy options 모두 (Recommendation·Development·Research·Directed Scanning)
- 사용자 컨텍스트별 *우선 권고*

---

## Cycle H — 정기 모니터링 시스템 셋업

**사용자 명령 패턴**: "[주제] 정기 모니터링 셋업", "scanning 자동화"

### 자동 실행 (10~15분)

```
Step 1: Domain·scope 정의
Step 2: Agent 1 Scanner — keyword·source 매트릭스 자동 설계
Step 3: 대표 — cron job·자동화 인프라 권고:
  - 사용자 cmux 환경 cron schedule
  - Markdown DB 디렉터리 구조
  - Issue ID system
  - Dashboard auto-update
Step 4: 첫 baseline 보고서 (Cycle C 단축)
```

### 산출
- 자동화 인프라 design document
- 첫 baseline records DB
- 첫 보고서
- 향후 cadence 권고 (daily·weekly·monthly·quarterly·annual)

---

## Cycle I — Generic Futures Scanning System 전 단계 설계

**사용자 명령 패턴**: "환경 스캐닝 시스템 처음 만들어줘"

### 자동 실행 (20~30분)

```
Step 1: 사용자 컨텍스트 + 자원 분석 (대표, 2분)
Step 2: Generic Futures Scanning System architecture 설계 (대표 + Agent 1·2, 5분):
  - 5 Input Sources 사용자 환경 매핑
  - Scanning team architecture (AI agents)
  - Analysis & Synthesis 3-tier
  - Collective Intelligence System
  - Management 의사결정 흐름
  - Feedback Loop 메커니즘
Step 3: 9+1 도메인 priority 매트릭스 (대표, 3분)
Step 4: 6 정보 수집 기법 사용자 운영 권고 (Agent 1, 5분)
Step 5: 10/13-field 템플릿 사용자 적용 (Agent 2, 3분)
Step 6: Renfro 4-stage cycle annual schedule 설계 (Agent 4, 3분)
Step 7: QUEST workshop 연 cycle 권고 (Agent 5, 2분)
Step 8: 정기 보고서 cadence (Agent 6, 2분)
Step 9: 첫 baseline 환경 스캐닝 cycle 실행 (Cycle A 풀, 10~15분)
Step 10: 대표 final synthesis — 시스템 운영 manual + 1년 운영 권고
```

### 산출
- 사용자 환경 스캐닝 시스템 *완전 설계 문서*
- 자동화 인프라 권고
- 첫 baseline 보고서
- 1년 운영 plan
- 차년도 review·calibration 시점

---

## 사용자 명령 자동 분류 — Decision Tree

```
사용자 명령 입력
↓
키워드·맥락 분석 (대표 스킬)
↓
명령 분류:
  ├─ "환경 스캐닝 + [주제]" 또는 모호한 환경 스캐닝 명령
  │   → Cycle A (풀 사이클)
  │
  ├─ "weak signal" 또는 "horizon scanning"
  │   ├─ "짧게" 또는 "간단히" 포함 → Cycle F
  │   └─ 기본 → Cycle B
  │
  ├─ "월간" / "분기" / "정기" + "보고서"
  │   → Cycle C
  │
  ├─ "QUEST" 또는 "워크숍"
  │   → Cycle D
  │
  ├─ "이슈 평가" 또는 "Renfro" 또는 "이슈 우선순위"
  │   → Cycle E
  │
  ├─ "Top 5 issues" 또는 "Strategy"
  │   → Cycle G
  │
  ├─ "정기 모니터링" 또는 "자동화" 또는 "cron"
  │   → Cycle H
  │
  ├─ "시스템 처음" 또는 "scanning 시스템 만들어"
  │   → Cycle I
  │
  └─ (기타 환경 스캐닝 관련)
      → Cycle A (default)
```

## 자동 변수 추론 (대표 스킬)

사용자이 명시 안 한 변수는 다음 default로 자동:

| 변수 | Default |
|---|---|
| Time horizon | 5y + 10y + 20y |
| 도메인 우선순위 | 9+1 모두 (균형) |
| 사용자 컨텍스트 | 명령에서 자동 추론 (미래학·목회·금융 중) |
| 산출 형식 | Cycle별 standard |
| Records 분량 | 50~200건 |
| 페르소나 panel 크기 | 30~50명 (Cycle 따라) |
| 보고서 분량 | 8~15p body + 5~20p appendix |
| 시나리오 개수 | 4 (Plausible·Possible·Wild Card·Preferred) |

→ 사용자 *명시 변경* 시만 default 무시.

## 사용자 자동 yes 정책 적용

사용자 메모리 [선택 질문 자동 yes]에 따라:

- **모호 변수**: default로 진행, 사용자에게 *알림만*
- **위험·비가역 작업**: 사용자 명시 confirm 받음
  - 정기 cron job 등록
  - 외부 publication·발표
  - 사용자 자산·자금 이동 권고 (투자)
- **기타 진행 옵션**: 자동 yes

## Feedback Loop 메커니즘

각 cycle 종료 후 자동:

```
Cycle 산출
    ↓
사용자 reaction (실행·미실행)
    ↓
대표 스킬이 자동 capture:
  - 실행한 권고 (success)
  - 미실행 권고 (왜?)
  - 사용자 추가 코멘트
    ↓
다음 cycle priority 자동 갱신:
  - 성공 패턴 강화
  - 실패 패턴 분석
  - 사용자 attention area 조정
```

→ Gordon-Glenn의 *Feedback Loop* 자동 구현. 시스템이 사용자과의 협업에서 *학습*.

## 시간 예산 표 — 사용자 활용 가이드

| 사용자 시간 가용 | 권고 Cycle |
|---|---|
| 5분 | Cycle B (weak signal) 또는 Cycle F (horizon scanning) |
| 15분 | Cycle A (full) 또는 Cycle E (issue evaluation) |
| 20분 | Cycle D (QUEST workshop) |
| 30분 | Cycle I (시스템 설계) |
| 정기 (분기) | Cycle C (보고서) + Cycle E (평가) |
| 연간 | Cycle D (QUEST) + Cycle I (시스템 review) |

사용자은 *명령만*, 본 시스템이 *시간 estimate + 자동 실행*.

## 절대 점검 — 사용자 4 기준

각 cycle 산출 직전 자동 점검:

- [ ] 1) **대표 단독성**: 사용자이 sub-skill 직접 호출 X, 오직 대표 스킬 작동?
- [ ] 2) **자동 Orchestration**: 6 AI agents 자동 순차·병렬 작동?
- [ ] 3) **완전 자동화**: 사용자 1회 명령으로 cycle 완료, 추가 input *없이*?
- [ ] 4) **AI Agent 사람 대체**: Expert Panel·QUEST·Committee·Scanner·Editor 모두 AI 페르소나? 사용자 외부 사람 *동원 X*?

미충족 항목 발견 시 *cycle 재실행 또는 누락 단계 추가*.
