---
name: vision-foresight-environmental-scanning
description: "## TLDR — Theodore J. Gordon·Jerome C. Glenn (Millennium Project, *Futures Research Methodology V3.0* 02장) Environmental Scanning 풀 구현 **대표 스킬**. 환경 스캐닝의 단일 사용자 진입점. ## Triggers — 사용자가 '환경 스캐닝', '[주제] 환경 스캐닝', 'weak signal', 'horizon scanning', 'trend 모니터링', '월간 보고서', 'QUEST 워크숍', '이슈 관리 cycle', 'Renfro cycle', 'Gordon Glenn 환경 스캐닝', 'Millennium Project scanning', 'futures scanning', 'early warning system'을 명령하면 *단독으로* 발동. 5 INTERNAL sub-skill은 본 대표 스킬이 자동 orchestration. ## Detailed Methodology — Generic Futures Scanning System (Sources → Scanning → Analysis → Collective Intelligence → Management → Feedback). Aguilar/Renfro/Spies 분류·9 도메인+Spirituality·9 Cycles (A~I). 6 AI Agents 자동 작동 (Scanner·Analyst·Expert Panel 50 페르소나·Issues Committee 10 페르소나·QUEST 12~15 페르소나·Report Editor) — 외부 사람 동원 X. Step 1-A에서 Implications Domain 1회 질문 (정부·기업·학계·미디어·교육·종교·금융·비영리·개인·custom) 후 맞춤 산출. 미래학자·정책가·기업가·교수·기자·교사·목회자·투자자·NGO·창업자 누구든 본인 컨텍스트 산출물을 받음. **VRMP 8번째 절대 protocol 강제 cascade** (R·A·H mode 학습 지식 단독 금지·WebSearch·WebFetch 자동 6 계층 L1-L6 cascade·R-1·R-2·R-3 Tier 명시·할루시네이션 차단)."
---

# 환경 스캐닝 대표 스킬 — Single Entry Point

> **출처**: Gordon, T.J. & Glenn, J.C. (2009). Environmental Scanning. In Glenn, J.C. &
> Gordon, T.J. (Eds.), *Futures Research Methodology Version 3.0*.
> The Millennium Project. Chapter 02.
> Aguilar, F.J. (1967). *Scanning the Business Environment*. Macmillan.
> Renfro, W.L. (1987). Issues management in strategic planning. In *Issue Management*,
> ed. by Chase, Kiepper. Chicago: Nelson-Hall. [정식 서지: Renfro는 1983-1987년 간 다수 출판]
> Spies, P.H. (1999). Futures scanning for local governments. *Futures*, Vol. 31.

---

## 0. 결정론 엔진 위치

**Cycle 라우팅·Domain 번호 매핑·PI Chart 계산·Committee 집계는 반드시 아래 Python 스크립트를 Bash로 호출. LLM이 직접 라우팅 결정·곱셈·매핑하는 것은 절대 금지.**

```bash
CALC_PY="/Users/cys/Desktop/CYSjavis/cys-claude-vision-coaching-skills/skills/vision-foresight-environmental-scanning/env_scanning_calc.py"
# 스킬 이동 시 이 절대 경로를 업데이트할 것.

# Cycle 라우팅 (사용자 명령 → Cycle A-I):
python3 "$CALC_PY" --fn cycle_route '{"command":"<사용자 명령 전문>"}'

# Implications Domain 번호/이름 → canonical 도메인:
python3 "$CALC_PY" --fn domain_lookup '{"input":"2,7"}'

# PI Chart (Probability × Impact 계산 + 순위):
python3 "$CALC_PY" --fn pi_chart '{"issues":[{"name":"Issue A","scores":[{"p":70,"i":8},...]}]}'

# Issues Committee 집계 (median·IQR·consensus):
python3 "$CALC_PY" --fn committee_agg '{"issue":"X","p_scores":[70,80],"i_scores":[8,9]}'

# Domain 입력 검증:
python3 "$CALC_PY" --fn validate_domains '{"input":"2,7,15"}'
```

---

## 절대 원칙 (사용자 4대 기준)

본 스킬은 사용자 절대 기준 4가지를 충족하는 **유일한 환경 스캐닝 진입점**:

1. **대표 스킬 단독성**: 사용자은 *본 스킬과만 대화*. 5개 하위 스킬 (vision-foresight-environmental-scanning-techniques·vision-foresight-environmental-scanning-weak-signal-template·vision-foresight-environmental-scanning-issues-management·vision-foresight-environmental-scanning-quest-workshop·vision-foresight-environmental-scanning-report)은 사용자이 *직접 호출하지 않음*.

2. **자동 Orchestration**: 사용자 명령 → 본 스킬이 명령 분석 → 적합한 하위 스킬 자동 선택·순차 호출 → 결과 통합 → 사용자에게 산출.

3. **완전 자동화**: 사용자 1회 명령으로 전체 cycle 완료. *추가 입력 없이* 산출물 생성. 옵션·확인 질문 *최소화* (사용자 [선택 질문 자동 yes] 정책).

4. **AI 에이전트 사람 대체**: Expert Panel·QUEST 참가자·Issues Committee·Scanner·Report Editor·Peer Reviewer 등 사람 역할은 *모두 AI 페르소나 시뮬레이션*으로 대체. 사용자 외부 협력자·자문위원 *미동원*.

## 사용자 명령 → 자동 Orchestration 매트릭스

사용자가 다음 어떤 명령을 내려도 본 스킬이 단독 처리:

| 사용자 명령 패턴 | 자동 실행 워크플로우 | 활용 하위 스킬 |
|---|---|---|
| "[주제] 환경 스캐닝 해줘" | Cycle A — 풀 사이클 (수집→템플릿→패턴→평가→전략→보고서) | 5개 하위 모두 |
| "[주제] weak signal 찾아줘" | Cycle B — 정보 수집 + 템플릿화 + 패턴 분석 | 2·3 |
| "[주제] 월간 보고서" | Cycle C — Records 종합 + 보고서 자동 작성 | 3·6 |
| "[주제] QUEST 워크숍" | Cycle D — AI 페르소나 12~15명 워크숍 4 phases 시뮬레이션 | 5 |
| "[주제] 이슈 평가" | Cycle E — Renfro 4-stage cycle (식별·연구·평가·전략) | 4 |
| "[주제] horizon scanning" | Cycle F — Cycle A 단축형 (수집·패턴만) | 2·3 |
| "[주제] Top 5 issues" | Cycle G — Records 평가 + PI Chart + Top 5 + Strategy | 4 |
| "[주제] 정기 모니터링 셋업" | Cycle H — 시스템 설계·자동화 cron 구축 | 1·2·3 |
| "환경 스캐닝 시스템 처음 만들어줘" | Cycle I — Generic Futures Scanning System 전 단계 설계 | 5개 모두 |
| (모호한 환경 스캐닝 관련 명령) | Cycle A 기본 (풀 사이클) | 5개 모두 |

사용자가 *명령 모호*하게 해도 본 스킬이 *자동 추론*하여 적합 cycle 실행. 추가 질문은 *최소 1개*만 — **Implications Domain 선택** (사용자 컨텍스트 변수, 산출물 형태를 결정하는 핵심 변수).

**Cycle 라우팅은 반드시 Python 호출**:
```bash
python3 "$CALC_PY" --fn cycle_route '{"command":"<사용자 명령 전문>"}'
```
결과 `cycle` 필드 값이 실행할 Cycle. LLM이 직접 판단하지 않는다.

## Generic Futures Scanning System (Gordon-Glenn Section II 그대로)

```
[5 INPUT SOURCES] (자동 — AI Scanner agent가 web search/fetch)
 ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
 │Press·  │ │Specific│ │Keyword │ │Conf·   │ │Key     │
 │News·   │ │Websites│ │Internet│ │Seminars│ │Persons │
 │Journals│ │Monitor │ │Search  │ │Stream  │ │Tracking│
 └────┬───┘ └───┬────┘ └───┬────┘ └────┬───┘ └────┬───┘
      └─────────┴──────────┴──────────┴──────────┘
                            │
                            ▼
                   ┌────────────────┐
                   │   SCANNING     │  (vision-foresight-environmental-scanning-techniques)
                   │   AI Scanner   │
                   └───────┬────────┘
                           │
                           ▼
                   ┌────────────────┐
                   │ Analysis &     │  (vision-foresight-environmental-scanning-weak-signal-template)
                   │ Synthesis      │  AI Analyst
                   │ (10·13 field)  │
                   └───────┬────────┘
                           │
                           ▼
                   ┌────────────────┐
                   │ Collective     │  AI Expert Panel (30~75 페르소나)
                   │ Intelligence   │
                   └───────┬────────┘
                           │
                           ▼
                   ┌────────────────┐
                   │  Issues Mgmt   │  (vision-foresight-environmental-scanning-issues-management)
                   │  AI Committee  │  Renfro 4-stage
                   └───────┬────────┘
                           │
                ┌──────────┼──────────┐
                ▼          ▼          ▼
          ┌──────────┐ ┌──────┐ ┌──────────┐
          │ Strategy │ │QUEST │ │ Report   │
          │ AI 권고  │ │AI WS │ │ AI Editor│
          └──────────┘ └──────┘ └──────────┘
                           │
                Decisions·Learning·Feedback
                           │
                           └──► (loops back to Scanning)
```

본 도식의 *모든 단계*에 AI 에이전트 배치 — 사람 개입 없이 cycle 자동 완료.

## AI 에이전트 6 페르소나 (사람 작업 대체)

### Agent 1 — AI Scanner

**역할**: vision-foresight-environmental-scanning-techniques의 6 정보 수집 기법 *모두를 자동 수행*

**작업**:
- web_search·web_fetch로 글로벌·한국 sources 자동 모니터링
- 5 input sources (Press·Websites·Internet·Conferences·Key Persons) 각각 자동
- KISTI NDSL·BigKinds·KOSIS·Google Scholar·factiva 등 한국·글로벌 DB 자동 조회
- 사용자 [reference_claude_accounts]의 Gemini·Codex 계정도 활용 가능 (다중 search)
- Daily·weekly·monthly cadence 자동 (사용자 명령 없이 background)

**출력**: Raw scanning records 50~200건 (도메인 분포·sources·일자 자동)

### Agent 2 — AI Analyst

**역할**: vision-foresight-environmental-scanning-weak-signal-template의 10/13-field 템플릿화 + 패턴 분석 *자동*

**작업**:
- Raw records → 10-field KOC 또는 13-field UNDP 자동 변환
- 9 도메인 + Spirituality 자동 분류 (Primary + Secondary multi-classification)
- Leading Indicator 5 패턴 자동 추출
- Cross-field·cross-domain pattern 자동 식별
- 5가지 weak signal pattern detection 자동 적용

**출력**: Standardized records DB + weak signals 식별 보고서

### Agent 3 — AI Expert Panel (30~75 페르소나)

**역할**: vision-foresight-environmental-scanning-techniques 1번 (Expert Panels) 75명 panel을 *AI 페르소나*로 시뮬레이션

**페르소나 카탈로그**:
- 미래학·전략 5명 (Yuval Harari·Kevin Kelly·Ray Kurzweil·Jamais Cascio·Sohail Inayatullah 페르소나)
- AI·기술 5명 (Sam Altman·Demis Hassabis·Stuart Russell·Yann LeCun·Geoffrey Hinton 페르소나)
- 거시경제 5명 (Ray Dalio·Larry Summers·Adam Tooze·Mohamed El-Erian·Nouriel Roubini 페르소나)
- 인구·사회 4명 (Phillip Longman·Jonathan Haidt·조영태·이상림 페르소나)
- 정치·국제관계 5명 (Graham Allison·Ian Bremmer·Michael Beckley·박원곤·천영우 페르소나)
- 환경·에너지 4명 (Vaclav Smil·Hannah Ritchie·조천호·KEEI 연구원 페르소나)
- 농업·식품 2명
- 통신·교통 2명
- 문화·콘텐츠 3명
- 신학·목회 5명 (N.T. Wright·Carl Trueman·Russell Moore·이원규·정재영 페르소나)
- 영성·종교 사회학 3명 (Tara Burton·David Brooks·James K.A. Smith 페르소나)
- Wild card·visionary 2명

**작업**:
- 각 페르소나가 *본인 분야 시각으로* 입력 issue·trend 평가
- Daisy chain nomination 시뮬레이션
- 3 round 응답 자동 생성:
  - Round 1: Open question (각 페르소나 분야별 응답)
  - Round 2: Cross-reference (다른 페르소나 응답에 likelihood·impact 평가)
  - Round 3: Policy options (페르소나별 정책 implementation likelihood·effectiveness)
- Anonymous response synthesis (그룹 의견 합성)
- *통계적 유의성 없음* 명시 (Gordon-Glenn 원전: "it was not possible to say whether these results were statistically significant" — Chapter 02 Expert Panel discussion)

**출력**: Expert Panel synthesis report + cross-impact insights

**페르소나 구현**: 각 페르소나는 references/ai_persona_panel_catalog.md의 *전기적·사상적·발언 양식 프로파일*을 토대로 LLM이 simulate.

### Agent 4 — AI Issues Management Committee

**역할**: vision-foresight-environmental-scanning-issues-management Renfro 4-stage cycle을 *AI Committee 5~10 페르소나*가 자동 수행

**페르소나** (Committee members):
- Senior Strategist (전략 시각)
- Devil's Advocate (반대 시각)
- Domain Expert (해당 issue 분야 전문가)
- Skeptic (가정 도전)
- Optimist (낙관 시나리오)
- Pessimist (비관 시나리오)
- Pragmatist (실행 가능성)
- Long-term Thinker (10y+ horizon)
- Wild Card Hunter (low prob × high impact)
- Korean Context Specialist (한국 컨텍스트)

**작업**:
- Stage 1 — Issues Identification: AI Analyst 산출 records에서 Top 20~50 potential issues 자동 추출
- Stage 2 — Research: 각 Top issue에 대해 OPIN 8 questions 자동 답변 + Issue Paper 작성
- Stage 3 — Evaluation: *Secret balloting 시뮬레이션* — 10 페르소나가 각자 prob·impact 점수 (3 time horizons) → median + IQR → consensus check → Top 3-5 Consensus Issues 선정
- Stage 4 — Strategy: 4 task forces 옵션 (Recommendation·Development·Research·Directed Scanning) 자동 매핑

**출력**: Renfro 4-stage cycle 풀 산출 — Top 3-5 issues + Strategy recommendations

### Agent 5 — AI QUEST Workshop Participants (12~15 페르소나)

**역할**: vision-foresight-environmental-scanning-quest-workshop QUEST 4-phase를 *AI 페르소나 12~15명*이 자동 수행

**페르소나 구성** (15명 사용자 미래학 연구소 컨텍스트):
- Lead Facilitator (사용자 페르소나)
- 미래학 동료 2명
- 기술 전문가 2명
- 경제 전문가 1명
- 신학자 1명
- 청년 미래 전문가 1명
- 글로벌 미래학자 1명 (해외 시각)
- 테크 임원 1명
- 정책 전문가 1명
- 작가·미디어 1명
- 보수 worldview 1명
- 청년 1명
- 여성 시각 1명

**작업**:
- Phase 1 (Preparation): Strategic issue 자동 정의·Notebook 자동 생성·off-premise site 시뮬레이션
- Phase 2 (Workshop all-day): 4 segments 자동 진행
  - Mission/Purposes 토의 (각 페르소나 입장)
  - Trends open-ended brainstorming (각자 5~10 trends sticky note)
  - Cross-impact analysis (페르소나 페어로 매트릭스 작성)
  - Scenarios sketch (4 페르소나 그룹이 4 시나리오)
- Phase 3 (Report): 2-section report 자동 작성
- Phase 4 (Strategic Options): Half-day workshop 시뮬레이션 + Top 5~10 strategic issues 시리즈

**출력**: QUEST 4-phase 풀 산출 (1.5일 워크숍을 *수 분 내* 완료)

### Agent 6 — AI Report Editor

**역할**: vision-foresight-environmental-scanning-report Appendix B 양식 정기 보고서 *완전 자동 생성*

**작업**:
- 입력: Records DB + 이전 보고서들 + 신간 외부 보고서 monitoring
- 처리: 9 steps 자동
  1. Records 분류 (Item 1~5 strategic + Item 6 technical + Item 7 update)
  2. Top 5 strategic items 자동 선정
  3. 각 Item 3 implications 자동 생성 (Futurology·Pastoral·Investment)
  4. Item 6 신규 기술 4~8 자동
  5. Item 7 cross-month update 자동 (Issue ID 추적)
  6. Item 8 신간 보고서 추천 자동
  7. Sources 정리 자동
  8. Cover·TOC·Executive Summary 자동
  9. Appendix expanded background 자동 (Top items만)

**출력**: Body 8~15 pages + Appendix 5~20 pages 보고서. 사용자 review 없이 *완성본*.

### Agent Coordination — 본 대표 스킬의 역할

본 대표 스킬은 *6 agents의 conductor*. 사용자 명령 → 어떤 agents를 어떤 순서로 작동시킬지 결정 → 결과 통합·산출.

## 자동 Cycle 구현 — Cycle A (풀 사이클) 상세

사용자가 "[주제] 환경 스캐닝 해줘" 명령 시 자동 실행:

### Step 1 — Implications Domain 1회 질문 + Domain·Scope 자동 추론 (30~60초)

#### 1-A. Implications Domain Selection (사용자 답변 대기)
- 위 10개 옵션 표시
- 사용자 답변 수신 (1~3개 선택 또는 Custom 또는 skip)
- 사용자 컨텍스트가 메모리/CLAUDE.md에 *명확히* 있으면 자동 default 확인 모드로 단축

#### 1-B. 사용자 명령에서 자동 추출 (Implications 선택과 병행)
- Topic·도메인 (예: "AGI", "한국 인구", "한반도 통일")
- Time horizon (명시 없으면 5y 기본 + 10y·20y 보조)
- 9+1 도메인 분류 (primary + secondary)
- 지리적 범위 (국내·동아시아·전세계 — 명시 없으면 사용자 컨텍스트로 추론)

### Step 2 — AI Scanner Agent 발동 (1~3분)

자동 작업:
- 사용자 [reference_claude_accounts] 풀 활용 web_search·web_fetch
- 9+1 도메인별 keyword 매트릭스 자동 생성
- 글로벌·한국 sources 동시 (영문·국문)
- 50~200 records 자동 수집
- 각 record raw 데이터 (URL·요약·날짜·source)

### Step 3 — AI Analyst Agent 발동 (1~2분)

자동 작업:
- Raw records → 10-field KOC 자동 변환
- 9+1 도메인 multi-classification
- Cross-field·cross-domain pattern 분석
- 5가지 weak signal pattern detection
- Records DB 형태 산출

### Step 4 — AI Expert Panel 발동 (3~5분)

자동 작업:
- 30~50 페르소나 (도메인별 적정 비율) 활성화
- 입력 issue/topic에 대한 3 round 응답 자동
- Round 1: Open question — 각 페르소나 분야별 응답
- Round 2: Cross-reference — 페르소나별 likelihood·impact 평가
- Round 3: Policy options
- Synthesis report 자동 산출

### Step 5 — AI Issues Management Committee 발동 (2~3분)

자동 작업:
- Renfro 4-stage 풀 cycle
- Top 20~50 issues → Top 3-5 Consensus Issues
- Issue Paper 자동 작성 (각 Top issue, OPIN 8 questions 답변 포함)
- PI Chart 평가 (10 페르소나 secret balloting + median·IQR)
- Strategy 4 task forces 매핑

### Step 6 — AI Report Editor 발동 (2~3분)

자동 작업:
- Appendix B 양식 보고서 자동 작성
- *사용자가 Step 1-A에서 선택한 N개 Implications 도메인*에 맞춰 각 Item별 *N개 Implications 섹션* 자동 생성
- Cross-references (이전 보고서 issues — 있으면)
- Body + Appendix 풀버전
- 선택 안 된 도메인이 *cross-domain dynamic 강한* 경우만 보조 언급 (Cross-Domain Note)

### Step 7 — Final Synthesis (30초)

본 대표 스킬이:
- 6 agents 산출물 통합
- Executive summary 1 page
- 사용자 *행동 권고* 3가지 (즉시·중기·장기)
- Next cycle priorities

### 총 소요 시간: 10~15분 (구현 추정값 — Gordon-Glenn 원전 없음. 실제 소요는 LLM inference 속도에 의존)

**각 단계 시간 추정**: Step 2(1~3분), Step 3(1~2분), Step 4(3~5분), Step 5(2~3분), Step 6(2~3분) — 모두 구현 추정값, 원전 미언급.

## 사용자 입력 형식 — 최소화

### 권장 입력 형식

```
Pattern A — 단순 명령:
"AGI 환경 스캐닝"
"한국 인구절벽 weak signal"
"이번 분기 월간 보고서"
"기후변화 QUEST 워크숍"

Pattern B — 컨텍스트 명시:
"AGI가 한국 노동시장에 미칠 영향 환경 스캐닝, 5년 horizon"
"한국 SMR 산업 deep horizon scanning, 정부 자문 자료용"
"청년 정신건강 환경 스캐닝, 비영리·정책 양쪽 implications"

Pattern C — 풀 시스템 설계:
"우리 [기관명] 환경 스캐닝 시스템 처음 만들어줘"
```

### 본 스킬이 *자동 추론*하는 변수 vs *사용자에게 묻는* 변수

#### 자동 추론 (질문 X)
- Time horizon: 5y + 10y + 20y 기본
- 9+1 도메인 분류: 명령 키워드에서 자동
- 산출물 형식: Cycle 종류에 따라 default
- 페르소나 panel 구성: 도메인 적정 비율 자동
- 보고서 분량: Cycle별 standard

#### 사용자에게 *반드시 묻는* (Step 1-A)
- **Implications Domain Selection**: 10개 옵션 중 1~3개 또는 Custom (산출물 형태를 *근본적으로* 결정하는 변수이므로)

#### 사용자가 *명시하면* 적용
- 시급도·deadline
- 지리적 범위 (한국·동아시아·전세계)
- 보고서 분량 변경
- 특정 페르소나 강조 또는 제외

→ 사용자는 *Implications Domain 답변 1회 + 명령 1회* 이외 추가 입력 부담 없음.

## 5 하위 스킬 — 각 역할 (사용자은 직접 호출 X)

| 하위 스킬 | 본 대표가 호출하는 단계 | AI 에이전트 |
|---|---|---|
| vision-foresight-environmental-scanning-techniques | Step 2 (정보 수집) + Step 4 (Expert Panel 시뮬레이션) | Agent 1 + 3 |
| vision-foresight-environmental-scanning-weak-signal-template | Step 3 (템플릿화·패턴 분석) | Agent 2 |
| vision-foresight-environmental-scanning-issues-management | Step 5 (Renfro 4-stage cycle) | Agent 4 |
| vision-foresight-environmental-scanning-quest-workshop | Cycle D 명령 시 (QUEST workshop) | Agent 5 |
| vision-foresight-environmental-scanning-report | Step 6 (보고서 자동 작성) | Agent 6 |

사용자 명령은 *본 대표 스킬에만*. 5 하위 스킬은 *내부 sub-skill*로 본 대표 스킬이 자동 호출.

## Generic Futures Scanning System (개념·역사)

### Gordon-Glenn 핵심 명제

> "Environmental scanning systems provide early warning about important changes and detect 'weak signals' that indicate plans should be amended."

> "All futurists do environmental scanning—some are more organized and systematic, all try to distinguish among **what is constant, what changes, and what constantly changes.**"

### 명명법 진화
- 1960~70s: "Environmental Scanning"
- 환경운동 부상 후: "Futures Scanning Systems"·"Early Warning Systems"·"Futures Intelligence Systems"
- 2008+: **"Collective Intelligence"** (MIT CCI 2007 설립)

### Gordon의 Collective Intelligence 정의

> "An emergent property from synergies among data/info/knowledge, software/hardware, and human minds (experts) that **continually learns from feedback to produce 'just in time knowledge'** for better decisions than these elements acting alone."

본 대표 스킬은 *human minds*를 *AI 페르소나*로 대체하여 사용자 1인 명령에서 collective intelligence 시뮬레이션.

### 핵심 약속

> "No system will be able to eliminate all uncertainty; the objective of a scanning system is simply to **find early indications of possibly important future developments to gain as much lead-time as possible.**"

본 스킬도 *불확실성 제거 X, lead-time 확보*가 목표.

## 분류 체계 (Aguilar·Renfro·Spies)

본 대표 스킬은 *Spies (1991) Directed Scanning* 모드로 작동:
- Aguilar (1967) Formal Search
- Renfro (1983) 4 aspects 모두 *자동 결정*
- Spies *Directed* — 잘 수립된 plan·procedure 추종

사용자은 *passive·active scanning에 시간 쓰지 않음*. 본 스킬이 자동으로 *directed scanning* 수행.

## 9 도메인 + Spirituality (사용자 STEEPS)

| # | 도메인 | STEEPS 매핑 |
|---|---|---|
| 1 | Conflict and Governance | Politics |
| 2 | Science and Technology | Technology |
| 3 | Agriculture and Food Security | Environment·Economy |
| 4 | Natural Resources and Environment | Environment |
| 5 | Energy | Tech·Economy·Environment |
| 6 | Population, Education, Welfare | Society |
| 7 | Communications and Transportation | Tech·Economy |
| 8 | Regional and International Economics | Economy |
| 9 | Social Cultural Issues | Society |
| **10** | **Spirituality / Religion / Meaning** (사용자 추가) | **Spirituality** |

본 스킬 자동 산출의 모든 records·issues·implications는 **10 도메인 자동 분류**.

## Implications Domain Selection — 사용자 컨텍스트 1회 질문

본 스킬은 *고정된 implications 도메인 hardcoding 없음*. 사용자가 누구든 — 미래학자·정책가·기업가·교수·기자·교사·목회자·투자자·NGO 활동가·창업자·대학원생 — *본인 컨텍스트 산출물*을 받음.

### Cycle 시작 시 1회 질문 (필수, Step 1에서)

본 스킬이 작동 시작 시 사용자에게 *반드시* 다음 질문을 1회 제시:

```
[Implications Domain Selection]
이 환경 스캐닝의 Implications을 어떤 영역에 맞춰 산출할까요?
관심 영역을 1~3개 선택하세요 (다중 선택 가능):

  1. 정부·정책 (Policy)
     — 정부 자문·정책 수립·입법·규제
  2. 기업·경영 (Business)
     — 전략 기획·신사업·M&A·운영
  3. 학계·연구 (Academia)
     — 연구 방향·논문·학술 publication
  4. 미디어·언론 (Media)
     — 보도·논평·기획 기사·다큐멘터리
  5. 교육·학습 (Education)
     — 커리큘럼·교육 프로그램·평생학습
  6. 종교·목회 (Religious / Pastoral)
     — 사역·설교·종교적 응답
  7. 금융·투자 (Investment)
     — 포트폴리오·자산 배분·종목·리스크
  8. 비영리·시민사회 (Nonprofit / Civic)
     — NGO 활동·시민운동·공익
  9. 개인·생애설계 (Personal / Life)
     — 진로·가족·생애 의사결정
 10. Custom (사용자 정의)
     — 위 9개에 안 맞는 본인 고유 영역 (예: "농업 협동조합·원전 운영사·청소년 상담사" 등)

답변: [번호 또는 영역명, 다중은 쉼표]
예: "2, 7" 또는 "정부, 학계" 또는 "Custom: 한국 가나안 성도 사역"
```

### 사용자 답변 처리

- **명확한 답변** (예: "2, 7"): 즉시 적용
- **Custom**: 사용자가 *자유 텍스트로* 본인 컨텍스트 정의 (1~3 문장). AI Report Editor가 본 컨텍스트로 implications 자동 생성
- **무응답·skip**: *Generic universal implications* 모드로 진행 (모든 영역 공통 핵심)
- **이미 메모리/CLAUDE.md에 사용자 컨텍스트 명시**: 사용자에게 *자동 default 확인*만 하고 진행
  - 예: "이전 대화에서 [목회·미래학·금융] 컨텍스트 사용 — 동일하게? (Y/N, default Y)"
  - Y 또는 침묵 → 자동 진행
  - N → 위 10개 옵션 재제시

### Implications 산출 형식

선택된 N개 도메인별로 각 Item에 *Implications 섹션* 1~2 단락:

```
Item N. [Title]

Summary: ...

[Selected Domain 1] Implications:
[1~2 단락 — 본 도메인 사용자에게 직접 행동 가능 권고]

[Selected Domain 2] Implications:
[동일]

[Selected Domain 3] Implications: (선택 시)
[동일]

Sources: ...
```

### 도메인 외부 — Cross-domain Insights

선택된 도메인이 아니어도 *cross-domain dynamic*가 강한 경우 보조 언급:

```
Cross-Domain Note:
이 issue는 [선택 안 된 도메인]에도 직접 영향. 본 보고서는 [선택 도메인]에 초점,
원하시면 [선택 안 된 도메인] implications 별도 cycle 가능.
```

### 동일 사용자 다음 cycle

본 사용자의 *최초 선택*은 다음 cycle에서 *default*로 자동 적용. 사용자가 명시 변경 시만 갱신:
- "이번 cycle은 다른 영역으로" → 재질문
- "원래 영역으로" → 자동 적용 (질문 skip)

## Renfro 4-stage Cycle (자동 실행)

본 대표 스킬이 cycle 명령 시 자동 실행:

1. **Identify** (AI Scanner + AI Analyst) — Top 20~50 potential issues
2. **Research** (AI Issues Committee) — Issue Paper + OPIN 8 questions
3. **Evaluate** (AI Issues Committee Secret Balloting) — PI Chart + Top 3-5 Consensus
4. **Strategy** (AI Issues Committee + 본 대표 스킬) — 4 task forces 매핑

상세는 vision-foresight-environmental-scanning-issues-management 하위 스킬 자동 호출 (사용자 직접 호출 X).

## QUEST Workshop (자동 실행)

사용자이 "QUEST workshop" 명령 시 본 대표 스킬이 자동:

1. AI Workshop Participants 12~15 페르소나 활성화
2. Phase 1 — Strategic issue 정의·Notebook 자동 생성
3. Phase 2 — All-day workshop 4 segments 자동 시뮬레이션
4. Phase 3 — 2-section report 자동 작성
5. Phase 4 — Half-day strategic options workshop 자동
6. Top 5~10 Strategic Issues 시리즈 산출

상세는 vision-foresight-environmental-scanning-quest-workshop 하위 스킬 자동 호출.

## 정기 보고서 자동 (Daily·Weekly·Monthly·Quarterly·Annual)

사용자이 "정기 보고서 셋업" 또는 "[월/분기/연간] 보고서" 명령 시:

### 자동 cadence
- **Daily** (옵션, 사용자 cmux cron): 핵심 keyword alert
- **Weekly**: 누적 records review·신호 검증
- **Monthly**: 통합 보고서 (Appendix B 양식·Body 8~15p + Appendix 5~20p)
- **Quarterly**: 컨텍스트별 분리 (Futurology·Pastoral·Investment 각각)
- **Annual**: 종합 보고서 + 차년도 priority

### 자동 인프라
- 사용자 cmux 환경에서 cron 자동 실행 가능
- Markdown DB + Git version control
- Issue ID 추적 (Item 7 cross-month)
- Dashboard 자동 갱신

상세는 vision-foresight-environmental-scanning-report 하위 스킬 자동 호출.

## AI 페르소나 실존 인물 응답 정책

Agent 3 (AI Expert Panel)은 Yuval Harari·Sam Altman·Ray Dalio 등 실존 인물 페르소나를 사용한다. 이들의 응답은 **항상** 다음 태그를 달아야 한다:

| 태그 | 적용 조건 |
|---|---|
| `[known_stance]` | 해당 인물의 출판된 저서·인터뷰·공개 발언과 일치하는 입장 |
| `[extrapolated]` | 관련 저작에서 추론한 입장 — 직접 발언 없음 |
| `[simulated]` | 도메인 전문성을 기반으로 한 AI 시뮬레이션 — 인물의 실제 견해와 다를 수 있음 |

**실존 인물 페르소나는 절대로** 검증되지 않은 특정 견해·수치·예측을 마치 해당 인물의 실제 발언인 양 태그 없이 생성하지 않는다.

## 정보 소스 접근 가용성 및 Fallback

KISTI NDSL·BigKinds·Factiva 등 구독 DB는 접근 불가 시 다음 fallback 순서를 적용한다:

1. **1차**: web_search (Google Scholar·PubMed·SSRN 등 무료 학술 검색)
2. **2차**: web_fetch (공개된 preprint·보고서·뉴스 URL 직접 조회)
3. **3차**: 학습 지식 기반 (반드시 `[학습지식·미검증]` 태그 + 날짜 명시)

Fallback 사용 시 출력에 `[Source: fallback-tier N]` 명시.

## 자동화 (cron·daily cadence) 안내

SKILL.md의 "cron 자동 실행"·"daily cadence" 기능은 **Claude Code 스케줄러 또는 외부 cron 설정 필요**. 단독 Claude Code 세션에서는 자동 실행되지 않는다. 해당 기능은 `/schedule` 스킬 또는 시스템 cron으로 별도 구성 필요.

## 오류 및 예외처리

Python이 `"error": true`를 반환하거나 예외 상황 발생 시 처리:

| 상황 | 처리 |
|---|---|
| Cycle 라우팅 fallback (A) | 사용자에게 "모호한 명령 → Cycle A 기본 실행" 공지 |
| Domain 번호 out of range [1-10] | 오류 메시지 + 유효 번호 목록 재제시 |
| Domain 이름 미인식 | 부분 일치 시도 후 없으면 재질문 |
| PI Chart p out of [0,100] | 해당 점수 제외 후 나머지로 계산, 경고 명시 |
| PI Chart i out of [0,10] | 동일 |
| Committee p_scores/i_scores 길이 불일치 | 오류 보고 + 재입력 요청 |
| 빈 issues list | Cycle 재실행 또는 수동 issue 입력 요청 |
| web_search 실패 | Fallback tier 적용 (위 정책 참조) |

## 입력 검증 규칙

Python 호출 전 사전 점검:

| 규칙 | 조건 |
|---|---|
| V1 | 사용자 명령 비어있지 않음 (최소 1자) |
| V2 | Implications Domain 번호 ∈ [1, 10] |
| V3 | PI Chart p_scores ∈ [0, 100], i_scores ∈ [0, 10] |
| V4 | committee_agg: len(p_scores) == len(i_scores) |
| V5 | issues list 비어있지 않음 |
| V6 | Cycle 라우팅 후 cycle ∈ {A,B,C,D,E,F,G,H,I} |

---

## 절대 원칙 (산출물 점검)

본 대표 스킬 산출 전 *반드시* 점검:

- [ ] 사용자 명령을 *Implications Domain 1회 질문 외에는 추가 질문 없이* 자동 처리했는가?
- [ ] **Step 1-A에서 Implications Domain Selection 질문을 *반드시* 제시**했는가? (사용자가 메모리/CLAUDE.md로 명시했거나 skip한 경우만 생략)
- [ ] 5 하위 스킬을 *사용자에게 노출 없이* 내부 호출했는가?
- [ ] AI 에이전트 6 페르소나가 *적절히 활성화*되었는가?
- [ ] **사용자가 선택한 N개 Implications 도메인에 *맞춤* implications 산출했는가?** (특정 도메인 hardcoding X)
- [ ] 10 도메인 (9 Gordon-Glenn + Spirituality) 분류 적용?
- [ ] PDF 원전 (Gordon-Glenn 2009) 충실성 보존?
- [ ] Lead-time 확보 강조 (불확실성 제거 X)?
- [ ] 본 cycle 결과가 *다음 cycle Feedback Loop*으로 환류 가능한 형태?

## 입력 처리 — 단일 명령 처리 protocol

### 단계 1 — 명령 분류 + Implications Domain 질문 (자동·30~60초)

사용자 명령 → 위 매트릭스에서 자동 매핑 → Cycle A·B·C·D·E·F·G·H·I 중 선정.
*동시에* Implications Domain Selection 질문 1회 제시 (메모리/컨텍스트로 default 가능 시 확인 모드로 단축).

### 단계 2 — 핵심 변수 자동 추론 (자동, 10초)

- Topic·도메인
- Time horizon
- 9+1 도메인 분류
- 산출 형식
- 지리적 범위

### 단계 3 — 모호 변수 1~2개만 사용자 confirm (선택)

기본값으로 진행. 정말 critical한 변수만 1회 짧게 확인.

예: "AGI 환경 스캐닝 — 5년 horizon으로 진행할까요? (Y/N, default Y)"
→ 사용자 *N 답변 시*만 변경. 침묵·Y면 진행.

### 단계 4 — 자동 cycle 실행 (10~15분)

6 AI agents 병렬·순차 작동.

### 단계 5 — 통합 산출 (자동)

사용자에게 산출:
- Executive Summary (1 page)
- 핵심 산출물 (보고서·issues·strategy)
- 사용자 *행동 권고* 3가지 (선택된 Implications 도메인별)
- Next cycle priorities

## 보조 자료 (references/)

| 파일 | 용도 |
|------|------|
| `references/generic_scanning_system.md` | Generic Futures Scanning System 5단계 + KOC 사례 풀버전 |
| `references/scanning_taxonomy_deep.md` | Aguilar/Renfro/Spies 학술 정식화 |
| `references/nine_domains_deep.md` | 10 도메인 sub-topics·정보 소스·STEEPS 매핑 |
| `references/issues_management_strategic_planning.md` | 환경 스캐닝 ↔ Issues Management ↔ Strategic Planning 통합 |
| `references/ai_agent_personas.md` | **6 AI 에이전트 + 페르소나 100+ 카탈로그·시뮬레이션 protocol** |
| `references/auto_orchestration_workflows.md` | **9 Cycles (A~I) 자동 실행 풀 protocol** |

기본 흐름은 본 SKILL.md만으로 충분. 깊이가 필요할 때만 references 추가 로드.

## 산출물 강제 양식 — Sub-skill Orchestration Trace (절대 protocol 7번)

**모든** 사용자 명령 응답은 다음 양식 *반드시* 따름. Inline 페르소나 시뮬레이션 *단독* 금지.

```markdown
# [주제] 환경 스캐닝 Report

## 0. Master 발동 + Cycle 분기
- 발동 마스터: vision-foresight-environmental-scanning
- 사용자 명령: "[원문]"
- 자동 분류 Cycle: <Cycle A~I 중>
- Implications Domain: <Step 1-A 결과>

## [Sub-skill Orchestration Trace]
호출 순서·시점:
1. vision-foresight-environmental-scanning-techniques ─ Step 2·4 ─ AI Scanner + Expert Panel
2. vision-foresight-environmental-scanning-weak-signal-template ─ Step 3 ─ AI Analyst
3. vision-foresight-environmental-scanning-issues-management ─ Step 5 ─ AI Issues Committee
4. vision-foresight-environmental-scanning-quest-workshop ─ (Cycle D 시) ─ AI QUEST Participants
5. vision-foresight-environmental-scanning-report ─ Step 6 ─ AI Report Editor

(Cycle별 일부 sub-skill 미호출 시 명시)

---

## ▶ Sub-skill 1: vision-foresight-environmental-scanning-techniques
**호출 시점**: Step 2 (정보 수집) + Step 4 (Expert Panel)
**AI Agent**: AI Scanner + AI Expert Panel (30~75 페르소나)
**Input**: 사용자 주제·Implications Domain
**작업**: 6 정보 수집 기법 + Expert Panel 시뮬레이션
**Output**: [해당 sub-skill SKILL.md Output 양식 그대로]

---

## ▶ Sub-skill 2: vision-foresight-environmental-scanning-weak-signal-template
[동일 양식]

---

## ▶ Sub-skill 3·4·5: 동일 양식 (각 호출되는 sub-skill 별도 섹션)

---

## Master Synthesis — 통합 산출
- Executive Summary
- Top issues + 사용자 행동 권고
- Next cycle priorities
- Sources [markdown hyperlinks]
```

### Trace 강제 위반 시

박사님이 *trace 없는 산출* 받으시면 즉시 trace 추가 재산출 의무.

### Inline vs Trace의 정합

박사님 [AgenticWorkflow master 패턴]:
> "master orchestrator는 inline protocol, 워커가 직접 실행. 2단 nested sub-agent 위임 영구 금지"

본 강제는 *physical inline* + *logical explicit trace*. Sub-agent spawn 금지, 그러나 호출의 *명시적 표시*는 의무.

## 마무리 — 본 대표 스킬의 4 약속

1. **사용자는 본 스킬 외 어떤 환경 스캐닝 스킬과도 대화하지 않는다.** 5 하위 스킬은 본 스킬이 자동 호출.

2. **사용자 1회 명령 + Implications Domain 1회 답변으로 전체 cycle 자동 완료.** 추가 입력·확인 최소화. 모호 변수는 본 스킬이 자동 추론·기본값.

3. **모든 사람 작업을 AI 에이전트로 대체.** 외부 협력자·자문위원·workshop 참가자·panel·committee·scanner·editor 모두 *AI 페르소나 시뮬레이션*. 사용자 1인 명령으로 환경 스캐닝 전 cycle.

4. **사용자 누구나 본인 컨텍스트로 산출물 받음.** Implications 도메인 hardcoding 없음 — 정부·기업·학계·미디어·교육·종교·금융·비영리·개인·custom 어느 영역의 사용자든 *맞춤 implications* 자동 생성.

이 4 약속으로 본 스킬은 PDF 원전 (Gordon-Glenn 2009) 충실성 + 사용자 컨텍스트 적응성을 동시에 보장.
