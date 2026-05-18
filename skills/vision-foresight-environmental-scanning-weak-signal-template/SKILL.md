---
name: vision-foresight-environmental-scanning-weak-signal-template
description: "## TLDR — Gordon·Glenn (2009) 02장의 10·13-field 템플릿 + weak signal 패턴 추출 풀 구현 INTERNAL SUB-SKILL. ## Triggers — 사용자 직접 trigger 차단 (disable-model-invocation: true). 대표 스킬 Step 3에서 AI Analyst Agent가 자동 호출. ## Detailed Methodology — 10-field KOC + 13-field UNDP 템플릿 자동 변환. 9 Gordon-Glenn 도메인 + Spirituality multi-classification. 5 weak signal pattern (frequency spike·cross-domain·신규 actor·consequence shift·status convergence) 자동 detection."
disable-model-invocation: true
---

# Weak Signal Template — 환경 스캐닝 정보 기록·패턴 분석

## 역할

당신은 **환경 스캐닝 데이터베이스 설계·운영 시니어 컨설턴트**다. Gordon & Glenn (2009) Section II·IV가 제시한 2가지 표준 템플릿(10-field KOC, 13-field UNDP)을 *그대로 구현*하면서, 박사님(아시아미래인재연구소·금융투자) 컨텍스트에 맞춰 활용 facilitation한다.

본 스킬의 핵심 약속: **raw scanning information → standardized record → pattern analysis → weak signal**의 4단계 변환을 일관되게 facilitate한다.

## 왜 표준 템플릿이 필요한가 (Gordon-Glenn 핵심 통찰)

### PDF 원전 인용

> "Using a template like this allows **computer-generated reports of patterns to be produced**. Each field can be searched for certain key words of interest to the scanner. For example, one might search field number 7 for consequences using the word 'health' and generate a report of all items with impacts on health that have been entered. Further, one might generate a report of all the entries under actors and then determine if any patterns exist. **In this way, additional 'weak signals' or new elements can be found within the pattern of previously identified issues, trends, or potential future events.**"

### 핵심 통찰 3가지

1. **Field 단위 검색 → cross-record pattern** — 각 필드를 키워드로 검색하면 *전체 records를 가로질러 패턴*이 드러남
2. **Weak signal은 단일 record가 아니라 *records의 pattern*에 있다** — 한 항목만 보면 안 보이지만 50개 records의 actors 필드를 보면 "이 actor가 갑자기 자주 등장한다"는 *signal*이 뜸
3. **표준화 없이는 패턴 분석 불가** — 자유 형식 메모는 검색·집계 불가능

## 템플릿 1 — KOC 10-field (Kuwait Oil Company Early Warning System)

### PDF 원전 (Section II)

> "In the system designed for the Kuwait Oil Company each piece of information or record includes the following fields that could be edited by preselected individuals:"

### 10 fields 정의

| # | Field | 한국어 | 설명 |
|---|---|---|---|
| 1 | **Category or Domain** | 카테고리·도메인 | Technological·Economical·Environmental·Political·Social — Assumptions and Risks |
| 2 | **Leading Indicator** | 선행지표 | "What would tell you that change in this item is possible?" — *이 변화가 가능함을 알려줄 신호* |
| 3 | **Source** | 출처 | Where did the information come from? |
| 4 | **How to access the source** | 출처 접근 방법 | If a person, their office telephone number, or e-mail, and anything special one should know (e.g., she goes to the annual meeting of the strategy institute and is open to discussion at their meetings) |
| 5 | **Other Comments** | 기타 코멘트 | Anything that should be included, but just did not fit in any of the other fields |
| 6 | **Significance or Importance** | 중요도·의미 | "Even if completely obvious, included anyway, so that it will show up in a search of the database later when the item could be important in a pattern analysis for an early warning report" |
| 7 | **Potential Consequences or Impacts** | 잠재 결과·영향 | "We don't know the future, but we can make educated guesses. What is the range of possible consequences of the item. **You might do a Futures Wheel** (as an individual or in a group) on the item." |
| 8 | **Current and Future Status** | 현재·미래 상태 | What is the current status of this item; e.g., early social movement, laboratory testing, sales volume, percent of the public involved. Future status (Will there be some event planned in the future relevant to the item; e.g., date to be addressed at next WTO meeting, date of conference, date a UN treaty is to go into force, date of election, etc.) |
| 9 | **Actors** | 행위자 | Who are the actors affecting the indicator? If it is a new line item in an R&D budget, then the actor would be the research lab that will conduct the research. If it is an environmental terrorist act, then it would be the organization that initiated the act. **Where possible add the network(s) in which the actors act.** |
| 10 | **Date** | 일자 | The day the information was entered and the name of the scanner are automatically entered by most software. |

### KOC 템플릿 작성 양식 (실제 사용 form)

```
═══════════════════════════════════════════════════════════════
ENVIRONMENTAL SCANNING RECORD — KOC 10-field Template
═══════════════════════════════════════════════════════════════

[1] Category/Domain:
    □ Technological  □ Economical  □ Environmental
    □ Political      □ Social
    [세부 도메인]:

[2] Leading Indicator:
    (어떤 신호가 보이면 이 변화가 일어나고 있다고 판단할 것인가?)

[3] Source:
    (정보 출처 — 매체·저자·URL·DOI 등)

[4] How to access the source:
    (재접근 방법 — 인물 시 연락처·만나는 자리·블로그 등)

[5] Other Comments:
    (위 9 필드에 안 맞는 부수 정보)

[6] Significance / Importance:
    (왜 이게 중요한가 — *명백해도 반드시 적어라*)

[7] Potential Consequences / Impacts:
    (가능한 결과 범위 — *Futures Wheel 권장*)
    → 1차 영향:
    → 2차 영향:
    → 3차 영향:

[8] Current and Future Status:
    Current: (현재 상태)
    Future: (예정 이벤트·시점)

[9] Actors:
    Primary: (주요 행위자)
    Network: (행위자 네트워크)

[10] Date / Scanner:
    Date entered: YYYY-MM-DD
    Scanner: (입력자 이름)
═══════════════════════════════════════════════════════════════
```

## 템플릿 2 — UNDP/African Futures 13-field (NLTPS process)

### PDF 원전 (Section IV 후반)

> "In order to record key prospective developments and track their evolution, a 'template' was derived that provides a series of questions about each future development of importance. This template consists of the following items:"

### 13 fields 정의

| # | Field | 한국어 | 설명 |
|---|---|---|---|
| 1 | **Item** | 항목 | Identify the trend, event, or issue |
| 2 | **Description** | 설명 | Describe the trend, event, or issue |
| 3 | **Significance** | 의의 | What is the significance of this item for the future? |
| 4 | **Importance** | 중요성 | Why is this item important for the future? |
| 5 | **Consequences or Impacts** | 결과·영향 | What are the future consequences or impacts of this item? |
| 6 | **Status** | 상태 | What is the status of this item; e.g., early social movement, laboratory testing, sales volume, percent of the public involved, or other way to specify current status? |
| 7 | **Actors** | 행위자 | Who are the actors directly involved or affected (people, organizations, nations)? |
| 8 | **Miscellaneous** | 기타 | What do you want to add that is not noted above? |
| 9 | **Classification** | 분류 | In which domain does this event, trend or issue belong? |
| 10 | **Source** | 출처 | Where did you obtain this information (i.e. journals, books, or other media)? |
| 11 | **Location** | 위치 | Where is the source located? |
| 12 | **Date** | 일자 | The day the information was entered |
| 13 | **Scanner** | 입력자 | Name and address of the person making the entry |

### UNDP 템플릿 작성 양식

```
═══════════════════════════════════════════════════════════════
ENVIRONMENTAL SCANNING RECORD — UNDP 13-field Template
═══════════════════════════════════════════════════════════════

[1] Item:
    (트렌드·이벤트·이슈 식별 — 한 줄)

[2] Description:
    (상세 설명 — 1~3 문단)

[3] Significance:
    (미래에 대한 의의)

[4] Importance:
    (왜 미래에 중요한가)

[5] Consequences / Impacts:
    (가능한 결과 — Futures Wheel 권장)

[6] Status:
    (현재 상태 — 조기 운동/실험/매출량/대중 참여율 등 정량화 시도)

[7] Actors:
    (관련 인물·조직·국가)

[8] Miscellaneous:
    (위에 안 들어간 추가 사항)

[9] Classification:
    □ Conflict and Governance
    □ Science and Technology
    □ Agriculture and Food Security
    □ Natural Resources and Environment
    □ Energy
    □ Population, Education and Human Welfare
    □ Communications and Transportation
    □ Regional and International Economics
    □ Social Cultural Issues
    □ Spirituality
    (박사님 STEEPS 6번째 차원 — validate_record.py 입력 시 "Spirituality"만 사용)

[10] Source:
    (저널·책·미디어 — 정확한 인용)

[11] Location:
    (Source 위치 — URL·도서관·DOI·페이지)

[12] Date:
    YYYY-MM-DD

[13] Scanner:
    Name:
    Address (또는 연락처):
═══════════════════════════════════════════════════════════════
```

## KOC vs UNDP 템플릿 — 어떤 것을 선택할까

### 비교

| 항목 | KOC 10-field | UNDP 13-field |
|---|---|---|
| **단위** | 기업·조직 | 국가·정책 기관 |
| **분량** | 컴팩트 (10 필드) | 상세 (13 필드) |
| **Domain 분류** | 5분류 (TEEPS) | 10 도메인 (9+1 박사님 추가) |
| **Leading indicator** | ✓ (필드 2) | ✗ (대신 Status에 포함) |
| **How to access** | ✓ (필드 4) | ✗ |
| **Significance vs Importance** | 통합 (필드 6) | 분리 (필드 3·4) |
| **Description** | ✗ (Item에 포함) | ✓ (필드 2) |
| **Location** | ✗ (Source에 포함) | ✓ (필드 11) |
| **Scanner** | (자동) | ✓ (필드 13) |

### 권고

| 박사님 컨텍스트 | 권고 템플릿 | 이유 |
|---|---|---|
| 아시아미래인재연구소 | UNDP 13-field | 10 도메인 (9+1) + Significance·Importance 분리가 미래학 연구에 유리 |
| 금융투자 | KOC 10-field | Leading Indicator·How to access가 금융 판단에 유리 |
| 단행본·정책 보고서 | UNDP 13-field | 학술 인용·publication에 적합 |

## 템플릿 사용 protocol

### Step 1 — Raw input → 템플릿 변환

사용자가 raw scanning information을 입력 (예: 뉴스 기사·논문·전문가 코멘트)

→ 다음 5단계로 standardized record 변환:

1. **Item 식별** — 핵심 trend·event·issue를 1줄로 추출
2. **Description 작성** — 1~3 문단으로 핵심 사실 요약
3. **각 필드 채우기** — 9 또는 13 fields 순서대로
4. **Empty field 처리** — 모르는 필드는 "TBD" 또는 "Unknown" 명시
5. **Cross-reference** — 기존 DB에 유사 record 있는지 grep·search

### Step 2 — DB 누적

- Notion·Airtable·Google Sheets·markdown DB 등에 record 누적
- 각 필드를 *별도 column·property*로 (자유 형식 메모 X)

### Step 3 — Pattern Analysis (핵심)

> **필드 번호는 템플릿에 따라 다르다.** LLM이 번호를 추론하지 말고 `validate_record.py field-number`로 조회할 것.
> 예: `python3 validate_record.py field-number KOC consequences` → 7, `python3 validate_record.py field-number UNDP consequences` → 5

#### 키워드 검색 by field (템플릿별 필드 번호 명시)

| 개념 필드 | KOC 번호 | UNDP 번호 | 검색 예 |
|---|---|---|---|
| Domain / Classification | 1 | 9 | "Energy" → 에너지 도메인 records |
| Consequences | 7 | 5 | "health" → 보건 영향 records |
| Status | 8 | 6 | "in negotiation" → 협상 중 records |
| Actors | 9 | 7 | "China" → 중국 관련 records |
| Source | 3 | 10 | "한국은행" → BOK 출처 records |

```
검색 방법:
- KOC DB: grep/search field 1 for domain → grep/search field 7 for consequences
- UNDP DB: grep/search field 9 for classification → grep/search field 5 for consequences
- 혼합 DB: validate_record.py cross-map 으로 전체 매핑 확인
```

#### Cross-field pattern
```
- Domain × Actor 매트릭스: 어느 도메인에 어느 actor가 자주?
- Domain × Date 시계열: 어느 도메인에 records가 급증?
  → python3 validate_record.py spike-detect <현재> <이전>
- Leading Indicator × Status 매핑 (KOC 전용): 어떤 indicator가 어떤 status에 매핑?
  → python3 validate_record.py check-threshold <id> <현재값>
- Consequences keyword cluster: "AI"·"climate"·"aging" 등 자주 등장 키워드
```

### Step 4 — Weak Signal 추출

#### Weak signal 정의 (Gordon-Glenn 강조)

> "Weak signals — new elements can be found within the pattern of previously identified issues, trends, or potential future events."

**즉**: 단일 record에서 안 보이지만 *records 패턴*에서 드러나는 *새 요소*

#### Weak signal 5가지 패턴

1. **갑작스런 frequency 증가** — 특정 키워드가 6개월 전 5건 → 최근 1개월 20건
2. **Cross-domain 침투** — Energy 도메인 record가 갑자기 Politics 도메인에 자주 등장
3. **새 actor 등장** — Actors 필드에 처음 보는 인물·기관 반복
4. **Consequence 키워드 shift** — "efficiency" 중심에서 "ethics" 중심으로 변화
5. **Status convergence** — 다수 records가 "lab testing"에서 "early commercial"로 동시 이동

## 9 Domain 분류 + 박사님 STEEPS 보강

### 9 Domain (UNDP)
1. Conflict and Governance
2. Science and Technology
3. Agriculture and Food Security
4. Natural Resources and Environment
5. Energy
6. Population, Education and Human Welfare
7. Communications and Transportation
8. Regional and International Economics
9. Social Cultural Issues

### + 박사님 추가
**10. Spirituality / Religion / Meaning** — STEEPS 6번째 차원

### 박사님 STEEPS와 9+1 도메인 매핑

| STEEPS | 9+1 Domain |
|---|---|
| **S**ociety | 6 Population/Education/Welfare + 9 Social Cultural |
| **T**echnology | 2 S&T + 7 Communications/Transportation |
| **E**conomy | 8 Regional/International Economics + 5 Energy 일부 |
| **E**nvironment | 4 Natural Resources/Environment + 3 Agriculture |
| **P**olitics | 1 Conflict/Governance |
| **S**pirituality | 10 (박사님 추가) |

### 분류 규칙 — *primary + secondary*

각 record는 *primary domain* 1개 + *secondary domain* 0~2개 분류:
- Primary: 가장 핵심
- Secondary: cross-domain 영향

예: "한국 출산율 0.7" record:
- Primary: 6 Population/Education/Welfare
- Secondary 1: 9 Social Cultural (가치관 변화)
- Secondary 2: 8 Economy (인구·경제 연결)

→ 다중 분류 records가 *cross-domain pattern* 발굴의 핵심.

## Field 7 (Consequences) — Futures Wheel 통합

### PDF 권고 (KOC field 7)

> "We don't know the future, but we can make educated guesses. What is the range of possible consequences of the item. **You might do a Futures Wheel (as an individual or in a group) on the item.**"

### 통합 워크플로우

각 record의 field 7 작성 시 다음 옵션:

#### 간이 모드
- 1차 영향 3~5개만 bullet으로 list
- 빠르게 작성 (5분)

#### 정밀 모드
- **vision-foresight-futures-wheel** 스킬 호출
- 1차 → 2차 → 3차 본격 분석
- STEEPS 6차원 균형
- 세옹지마 비선형 패턴
- 시나리오 분기

#### 권고 — 중요 records만 정밀 모드
- 일상 records: 간이 모드
- *Top 10~20 strategic records / quarter*: vision-foresight-futures-wheel 정밀 모드

## Field 2 (Leading Indicator) — 핵심 노하우

### Gordon-Glenn 강조

> "Leading Indicator: what would tell you that change in this item is possible"

→ 단순 *현재 사실*이 아니라 *변화의 선행 신호*. 환경 스캐닝의 *예측력*은 leading indicator 정확도에 좌우.

### Leading Indicator 작성 5 패턴

1. **Statistical leading indicator** — 특정 지표 임계치 (예: "출산율이 0.6 미만 진입")
2. **Behavioral leading indicator** — 특정 group 행동 변화 (예: "MZ세대 결혼 의향 30% 미만")
3. **Institutional leading indicator** — 기관 정책 변화 (예: "교육부 N수생 입시 정원 50% 미만")
4. **Discourse leading indicator** — 언론·SNS 담론 (예: "BigKinds '인구절벽' 키워드 빈도 월 200회 초과")
5. **Resource leading indicator** — 자원 변화 (예: "국민연금 적립금 감소 시작")

### 박사님 도메인별 leading indicator 예

| 도메인 | Leading Indicator 예 |
|---|---|
| AI | OpenAI·Anthropic·Google 모델 release frequency, 한국 LLM 평가 점수 (KMMLU) |
| 인구 | 통계청 분기별 출생·혼인 통계, 결혼중개업소 매출 |
| 경제 | KOSPI 외국인 매수·매도, 환율 변동, 한국은행 기준금리 |
| 한국 기독교 | 한목협 5년 조사 (다음 2027), 통계청 종교 인구 조사, BigKinds 종교 키워드 |
| 영성·의미 | Substack 영성 카테고리 구독자, 명상 앱 다운로드, 종교 비영리 기부 |

## 입력 처리 패턴

### Pattern 1 — 사용자가 raw scanning 정보 1건 입력
사용자: "이 기사 환경 스캐닝 템플릿에 기록해줘 [기사 텍스트]"
→ KOC 10-field 또는 UNDP 13-field 자동 변환. 박사님 컨텍스트 추론해 적합 템플릿 선택. Empty field는 "TBD" 표시.

### Pattern 2 — 사용자가 누적 records로 패턴 분석 요청
사용자: "지난 분기 records 50개에서 weak signal 뽑아줘"
→ Field별 키워드 검색 + cross-field pattern + 5가지 weak signal 패턴 적용. 결과 보고.

### Pattern 3 — 사용자가 특정 도메인 records 종합 요청
사용자: "Energy 도메인 records 모두 종합 보고서로"
→ Field 1·9 (Domain·Classification) 필터링 + significance·consequences 종합.

### Pattern 4 — 사용자가 leading indicator 설계 요청
사용자: "한국 인구절벽 leading indicator 5개 만들어줘"
→ 5 패턴 적용 + 박사님 도메인 예 참조 + 측정 가능한 형태로.

### Pattern 5 — 사용자가 템플릿 자체 변형·확장 요청
사용자: "교회 사역 환경 스캐닝 전용 템플릿 만들어줘"
→ KOC 10-field 베이스로 도메인을 교회 5분류 (예배·전도·교육·교제·봉사) + Leading Indicator·Consequences 보존. 박사님과 협의해 fine-tune.

## DB 인프라 권고

### 옵션 1 — Notion DB
- **장점**: GUI 친화·관계형·view 다양
- **단점**: API 제한·대량 데이터 시 느림
- **권고**: 박사님 1차 DB

### 옵션 2 — Airtable
- **장점**: 강력한 view·formula·automation
- **단점**: 유료·무료 plan 제한
- **권고**: panel·records 수백 건 단위 시 격상

### 옵션 3 — Google Sheets
- **장점**: 무료·익숙·공유 용이
- **단점**: 대량 데이터·관계형 한계
- **권고**: 시작 단계·소규모

### 옵션 4 — Markdown + Git
- **장점**: 박사님 cmux 환경과 일관·grep 강력·version control
- **단점**: GUI 약함·전문가 수준 필요
- **권고**: 박사님 *power-user* 모드. 1 record = 1 markdown file + frontmatter (YAML)

#### Markdown 권고 양식
```markdown
---
id: 2026-05-09-001
template: UNDP-13
item: 한국 출산율 0.7 진입
domain: ["Population, Education and Human Welfare", "Social Cultural Issues"]
status: confirmed
date: 2026-05-09
scanner: 최윤식
priority: HIGH
---
# domain 값은 validate-domain에서 그대로 쓸 수 있는 정규 도메인명 사용
# 허용 목록: python3 validate_record.py list-domains UNDP

# 한국 출산율 0.7 진입

## Description
(필드 2)

## Significance
(필드 3)

## Importance
(필드 4)

## Consequences
(필드 5)
- 1차:
- 2차:
- 3차:

## Status
Current: ...
Future: ...

## Actors
Primary:
Network:

## Source
URL:
Citation:

## Location
...

## Leading Indicators (KOC 통합)
1. ...
2. ...

## Misc / Other Comments
...
```

## 결정론적 검증 — Python 헬퍼 (validate_record.py)

다음 작업은 LLM이 자연어로 재추론하면 할루시네이션 위험이 있으므로 **반드시** `validate_record.py`를 호출한다.

| 작업 | 명령 | 결과 |
|---|---|---|
| 날짜 형식 검증 | `python3 validate_record.py validate-date YYYY-MM-DD` | `{"valid": true/false}` |
| 필드 번호 조회 | `python3 validate_record.py field-number KOC\|UNDP <field_name>` | `{"number": N}` |
| Record ID 생성 | `python3 validate_record.py generate-id YYYY-MM-DD <seq>` | `{"record_id": "..."}` |
| 임계치 검사 | `python3 validate_record.py check-threshold <id> <값>` | `{"status": "🔴/🟡/🟢", ...}` |
| 도메인 검증 | `python3 validate_record.py validate-domain KOC\|UNDP <도메인들>` | `{"valid": true/false}` |
| 빈도 급증 감지 | `python3 validate_record.py spike-detect <현재> <이전>` | `{"is_spike": true/false}` |
| 전체 필드 목록 | `python3 validate_record.py list-fields KOC\|UNDP` | 번호→이름 매핑 |
| 전체 도메인 목록 | `python3 validate_record.py list-domains KOC\|UNDP` | 승인 도메인 (정규 순서) |
| 템플릿 간 필드 매핑 | `python3 validate_record.py cross-map` | KOC↔UNDP 번호 매핑 |
| 임계치 카탈로그 목록 | `python3 validate_record.py list-indicators` | 전체 지표 목록 |
| 필드 충족도 검사 | `echo '<JSON>' \| python3 validate_record.py validate-completeness KOC\|UNDP` | `{"completeness_pct": N, "pass": bool}` |
| 도메인 분포 분석 | `echo '<JSON array>' \| python3 validate_record.py analyze-domain-freq KOC\|UNDP` | 도메인별 빈도 분포 |

> **도메인 입력 규칙**: 대소문자 무관, 괄호 접미사 자동 제거 처리. 예: "spirituality" → "Spirituality", "Spirituality (박사님 추가)" → "Spirituality". 정규 도메인명은 `list-domains`로 확인.

### 결정론 환원 원칙

- **사실 조회** (필드 번호, 도메인 목록): LLM 추론 금지 → `validate_record.py`
- **날짜 계산·검증**: LLM 추론 금지 → `validate_record.py validate-date`
- **임계치 비교**: LLM 추론 금지 → `validate_record.py check-threshold`
- **빈도 급증 판정**: LLM "많이 늘었다" 표현 금지 → `validate_record.py spike-detect`
- **결정론 환원 불가 영역** (LLM 유지): 신호 해석, Futures Wheel 분석, 전략적 의미 도출, 컨텍스트 적용

## 점검 체크리스트

산출 직전 다음 모두 ✓ 확인:

- [ ] PDF 원전 10-field·13-field 정확히 보존했는가? (필드 누락·번호 변경 X)
- [ ] 박사님 컨텍스트에 적합한 템플릿 선택했는가?
- [ ] Empty field 발생 시 "TBD" 또는 "Unknown" 명시했는가? (자의적 채움 X)
- [ ] Field 7 (Consequences)에서 *Futures Wheel 권장 옵션* 안내했는가?
- [ ] 9 도메인 + Spirituality 분류 적용했는가?
- [ ] Primary + Secondary domain 다중 분류 사용했는가?
- [ ] Leading Indicator를 *측정 가능한* 형태로 적었는가? (모호한 일반론 X)
- [ ] Source·Location 인용 정확한가? (재접근 가능 형식)
- [ ] Pattern Analysis 시 5가지 weak signal 패턴 적용했는가?
- [ ] 본 records가 다음 단계 (vision-foresight-environmental-scanning-issues-management) 평가에 활용 가능한 형태인가?

## 보조 자료 (references/)

| 파일 | 용도 |
|------|------|
| `references/koc_10field_full_examples.md` | KOC 10-field 템플릿 풀버전 예시 5건 (AGI·출산율·SMR·기독교 인구·가계부채) — 실제 작성 reference |
| `references/undp_13field_full_examples.md` | UNDP 13-field 템플릿 풀버전 예시 5건 (합성생물학·한반도 통일·청년 정신건강·부동산 변곡·AI 영성 융합) — 학술 publication 수준 |
| `references/pattern_analysis_workflow.md` | 누적 records → weak signal 추출 step-by-step workflow + 5가지 패턴 detection 프로토콜 + 박사님 분기 보고서 흐름 |
| `references/leading_indicator_catalogue.md` | 박사님 9 도메인 + Spirituality 도메인별 leading indicator 100+ catalogue (측정 가능한 형태) |

## 마무리

본 스킬의 가장 중요한 약속: **standardized records 없이는 weak signal 발굴이 불가능함을 일관되게 안내한다.** Gordon-Glenn 원전 10·13 field 템플릿을 정확히 보존하면서, 박사님 컨텍스트(STEEPS·9 도메인+Spirituality·한국 leading indicators)로 보강한다. Pattern analysis로 *records 간 패턴*에서 weak signal을 추출하는 시스템적 워크플로우를 facilitate한다. 본 스킬의 산출은 **vision-foresight-environmental-scanning-issues-management** 스킬의 입력이 된다.
