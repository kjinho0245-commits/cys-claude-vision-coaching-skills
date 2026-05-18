---
name: vision-foresight-environmental-scanning-report
description: "## TLDR — Gordon·Glenn (2009) Appendix B 양식 (Millennium Project Environmental Security 월간 보고서) 풀 구현 INTERNAL SUB-SKILL. ## Triggers — 사용자 직접 trigger 차단 (disable-model-invocation: true). 대표 스킬 Step 6·Cycle C에서 AI Report Editor Agent가 자동 호출. ## Detailed Methodology — 8 Items 양식 (Title·Summary·Implications·Sources). 사용자가 대표 스킬 Step 1-A에서 선택한 N개 Implications 도메인 (정부·기업·학계·미디어·교육·종교·금융·비영리·개인·custom) 자동 mapping. Cross-month Issue ID tracking. Body 8~15p + Appendix 5~20p 완성본."
disable-model-invocation: true
---

# Environmental Scanning Report — 정기 보고서 생성

> **출처**: Gordon, T.J. & Glenn, J.C. (2009). Environmental Scanning.
> *Futures Research Methodology V3.0*. Millennium Project. Chapter 02.
> Appendix B — Environmental Security Monthly Report (January 2009,
> all reports since 2002 at http://www.millennium-project.org/millennium/env-scanning.html)

---

## 0. 결정론 엔진 위치

**Issue ID 생성·날짜 계산·보고서 구조 검증·Sources 수량 검사·Implications 커버리지 확인은 반드시 아래 Python 스크립트를 Bash로 호출. LLM이 순번 추측·날짜 계산·검증을 자체 수행하는 것은 절대 금지.**

```bash
CALC_PY="/Users/cys/Desktop/CYSjavis/cys-claude-vision-coaching-skills/skills/vision-foresight-environmental-scanning-report/report_calc.py"
# 스킬 이동 시 이 절대 경로를 업데이트할 것.

# Issue ID 생성:
python3 "$CALC_PY" --fn generate_issue_id '{"year":2026,"month":5,"sequence":1}'
# → ISSUE-2026-05-001

# 다음 Issue ID (기존 ID 목록 기반):
python3 "$CALC_PY" --fn next_id '{"existing_ids":["ISSUE-2026-05-001",...],"year":2026,"month":5}'

# 날짜 참조 (현재·이전·다음 월):
python3 "$CALC_PY" --fn date_ref '{"year":2026,"month":5}'

# 보고서 구조 완결 검사 (Items 1-8 모두 있는지):
python3 "$CALC_PY" --fn validate_structure '{"items":{"1":"...","2":"...",...}}'

# Sources 수량 검사 (5-10 범위):
python3 "$CALC_PY" --fn validate_sources '{"item_id":"1","source_count":7}'

# Implications 도메인 커버리지 검사:
python3 "$CALC_PY" --fn validate_implications \
  '{"selected_domains":["Policy","Investment"],"item_implications":{"Policy":"...","Investment":"..."}}'
```

---

## 역할

당신은 **환경 스캐닝 보고서 시니어 editor**다. Millennium Project가 U.S. Army Environmental Policy Institute를 위해 2002년부터 매월 발행해온 *Environmental Security* 월간 보고서 형식 (Gordon-Glenn 2009 PDF Appendix B에 January 2009 보고서 풀버전 수록)을 충실히 구현하면서, 사용자(아시아미래인재연구소·금융투자) 컨텍스트에 맞춰 정기 환경 스캐닝 보고서를 생성한다.

본 스킬의 핵심 약속: *raw scanning records (vision-foresight-environmental-scanning-weak-signal-template 산출) → 의사결정자 친화적 정기 보고서*의 변환을 일관되게 facilitate.

## PDF Appendix B 보고서 출처

> "Example of an Internet scanning report on Environmental Security for the U.S. Army Environmental Policy Institute. Note: All reports since 2002 are available at http://www.millennium-project.org/millennium/env-scanning.html"

→ Millennium Project 환경 스캐닝 보고서가 *2002년부터 매월* 누적. 2009년 1월 보고서가 PDF에 풀 수록 — *연속성·표준 양식·실제 적용*이 검증된 사례.

## 표준 보고서 구조 — January 2009 사례 (PDF 풀 인용)

### Cover & Table of Contents (1 page)

```
[January 2009 Report]

Note to Readers: Pages 1-15 comprise the summary and analysis of this report.
Expanded details for some items are in the Appendix beginning on page 16.

Item 1. U.S. Policy Shift May Improve International Environmental Security ............... 1
Item 2. Green Economy a Solution for Addressing the Global Economic Crises ............ 1
Item 3. European Energy Security Strategies .......................................................... 2
Item 4. Global Plan to Address Freshwater Supplies Negotiated ............................... 3
Item 5. The Woodrow Wilson International Center Opens Synthetic Biology Project ... 3
Item 6. Technological Advances with Environmental Security Implications ................ 4
       6.1 New Process Improves Water Desalination Efficiency ............................... 4
       6.2 Another "Green" Concrete Announced .................................................... 4
       6.3 New Material Makes Biodegradable Plastic Bags ..................................... 5
       6.4 New Technique Provides Cheaper LEDs .................................................. 5
       6.5 New Detection and Cleanup Techniques ................................................. 5
              6.5.1 New Techniques for Multi-nanowire Detection Arrays ................. 5
              6.5.2 Manure Aids in Removing Hydrogen Sulfide from Biogas ............ 6
              6.5.3 New Deep Water Marine Sensors Being Developed ................... 6
Item 7. Updates on Previously Identified Issues ...................................................... 7
       7.1 New Chemicals Considered for Toxic Lists .............................................. 7
       7.2 New Jersey Ports Pushing for Toxic Diesels Ban ...................................... 7
       7.3 Chemical and Biosecurity Issues ............................................................. 8
       7.4 Arctic Security and Sovereignty Debate Continues .................................. 9
       7.5 Greenhouse Gas Observing Satellite ....................................................... 9
       7.6 India to Enact Regulation Curbing Plastic Bags Use ................................. 10
       7.7 Climate Change ................................................................................... 10
              7.7.1 Scientific Evidence and Natural Disasters ................................. 10
              7.7.2 Food and Water Security ......................................................... 11
              7.7.3 Migration ............................................................................... 11
              7.7.4 Melting Glaciers and Sea Ice ................................................... 11
              7.7.5 Rising Sea Levels .................................................................... 12
              7.7.6 Post-Kyoto Negotiations ......................................................... 12
       7.8 Nanotechnology Safety Issues ............................................................... 13
Item 8. Reports Suggested for Review ................................................................... 14
       8.1 State of the World 2009 ......................................................................... 14
       8.2 New 2009 Terminology on Disaster Risk Reduction .................................. 15
Appendix .............................................................................................................. 16
```

### Item 표준 구조

각 Item은 다음 4부 구조:

```
Item N. [Title]
[Summary 1~3 단락]

Military Implications:
[Domain별 implications — Army Environmental Policy Institute 컨텍스트]

Sources: (additional sources in the Appendix)
[5~10 source 링크]
```

### Sample Item — January 2009 Item 1

```
Item 1. U.S. Policy Shift May Improve International Environmental Security
Appointments of environmental scientists to the new U.S. administration, presidential
memoranda, and speeches all signal that the new White House will give special attention to
environmental matters from energy security to international cooperation for addressing climate
change. [See Appendix for more detail].

Military Implications:
As the military was called upon to play a key role in racial integration, it may be called upon to
play a key role in the accelerated adoption of green technology in the U.S. and around the world.
The Army Strategy for the Environment should be brought to the attention of President Obama,
as military environmental security capabilities might receive more attention from the new U.S.
Administration. International military-to-military environmental programs could receive higher
profiles. Since climate change is a new top priority, the military should identify all its resources
and programs for reducing GHGs and responding to effects of climate change, update
information continuously, forecast how it may be called upon for both mitigation and adaptation,
and perform a gap analysis in anticipation of future requests.

Sources: (additional sources in the Appendix)
Barack Obama makes history as he takes office with green agenda
http://www.unep.org/Documents.Multilingual/Default.asp?DocumentID=556&ArticleID=6040&l=en
SUBJECT: The Energy Independence and Security Act of 2007
http://www.whitehouse.gov/the_press_office/Presidential_Memorandum_fuel_economy/
[etc — 5~10 sources]
```

## 사용자 컨텍스트별 보고서 양식 — N-domain Multi Implications

### 핵심 변형 — 2가지 패턴

원전은 *Military Implications* 1개 도메인 (U.S. Army Environmental Policy Institute 컨텍스트). 본 스킬은 **사용자가 대표 스킬 Step 1-A에서 선택한 N개 도메인**(N=1~3) 또는 **Custom 컨텍스트**에 맞춘 *N개 multi-domain implications*:

#### Pattern A — Multi-domain 통합 보고서 (사용자 N개 implications)

대표 스킬에서 사용자가 선택한 1~3 도메인 모두를 한 보고서에 통합. 10개 default 옵션 중 사용자 선택:
- 정부·정책 (Policy Implications)
- 기업·경영 (Business Implications)
- 학계·연구 (Academic Implications)
- 미디어·언론 (Media Implications)
- 교육·학습 (Education Implications)
- 종교·목회 (Pastoral Implications)
- 금융·투자 (Investment Implications)
- 비영리·시민사회 (Civic / Nonprofit Implications)
- 개인·생애설계 (Personal Implications)
- Custom — 사용자 정의 영역 (예: "농업 협동조합 운영", "한국 가나안 성도 사역", "원전 해체 산업")

#### Pattern B — Single-domain 집중 보고서

사용자가 1개 도메인만 선택 시 — Military Implications 원전 모델과 동일하게 *single-domain deep* 보고서.

→ 권고: 정기 cycle 사용자에게 *3 도메인 통합 (Pattern A)* 권고 (cross-domain 통찰 우위), *단일 도메인 deep* 보고서는 분기·연말 별도.

## 사용자 N-domain 통합 보고서 표준 양식

### Cover & Table of Contents

```
[YYYY년 MM월 환경 스캐닝 보고서]
[주제] — [사용자 선택 N개 도메인 통합]

Note: Pages 1~12은 본문, pages 13~ 은 Appendix (확장 sources·background).
Implications domains: [Domain 1] · [Domain 2] · [Domain 3]

Item 1. [핵심 신규 이슈 1] ............... 1
Item 2. [핵심 신규 이슈 2] ............... 1
Item 3. [핵심 신규 이슈 3] ............... 2
Item 4. [핵심 신규 이슈 4] ............... 3
Item 5. [핵심 신규 이슈 5] ............... 4
Item 6. Technological Advances ............................................................ 5
      6.1 [신규 기술 1] ................................................................................ 5
      6.2 [신규 기술 2] ................................................................................ 5
      ... (4~8 sub-items)
Item 7. Updates on Previously Identified Issues ...................................... 7
      7.1 [이전 issue 1] (전월 대비 변화)
      7.2 [이전 issue 2]
      ... (5~10 sub-items)
Item 8. Reports Suggested for Review ................................................... 11
      8.1 [추천 보고서 1]
      8.2 [추천 보고서 2]
Appendix ............................................................................................ 13
```

### Item 표준 구조 — Generic N-domain 양식

```
Item N. [Title]
[Summary 1~3 단락 — what new, why important, current status]

[Domain 1] Implications:
[해당 도메인 사용자에게 직접 행동 가능 함의 1~2 단락]

[Domain 2] Implications:
[해당 도메인 사용자에게 직접 행동 가능 함의 1~2 단락]

[Domain 3] Implications: (사용자 선택 시)
[해당 도메인 사용자에게 직접 행동 가능 함의 1~2 단락]

Sources: (additional in Appendix)
[5~10 출처 링크]
```

→ AI Report Editor Agent가 사용자가 Step 1-A에서 선택한 N개 도메인을 *그대로* Item에 mapping. Hardcoded 3 도메인 X.

### Item 풀 사례 — 사용자 컨텍스트별 implications 시연

#### 사례 A — 사용자가 [정부·정책 + 기업·경영 + 학계·연구] 선택 시

```
Item 1. AGI 화이트칼라 침투 가속

[Summary 1~3 단락 — what new, why important, current status]

Policy Implications:
정부·정책 사용자에게 — 본 issue 응답 정책 옵션·법제 framework·정부 자문 활동 기여
지점·정책 형성 윈도우·국제 비교 reference. 1~2 단락.

Business Implications:
기업·경영 사용자에게 — 본 issue가 산업·기업 전략에 미치는 영향, 신사업 기회·
방어 시나리오·M&A·운영 모델·인력 전략. 1~2 단락.

Academic Implications:
학계·연구 사용자에게 — 본 issue 관련 연구 questions·publication 우선순위·
학제 간 협력·funding 기회·학회 발표·논문 thesis. 1~2 단락.

Sources: ...
```

#### 사례 B — 사용자가 [미디어·언론] 단일 선택 시

```
Item 1. AGI 화이트칼라 침투 가속

[Summary 1~3 단락]

Media Implications:
미디어·언론 사용자에게 — 본 issue의 보도·기획 기사·다큐멘터리 제작·논평
프레임·취재원 추천·timeline·관점 다양성 확보 방법. 2~3 단락 (single-domain
deep).

Sources: ...
```

#### 사례 C — 사용자가 [Custom: "한국 농업 협동조합 운영자"] 선택 시

```
Item 1. AGI 화이트칼라 침투 가속

[Summary]

Implications for 한국 농업 협동조합 운영자:
본 issue가 협동조합 본업·조합원 가정·농업 노동시장·식량 안보·정부 농업 정책
변동에 미치는 영향. 본 운영자가 직접 행동 가능한 권고 — 조합원 교육·신사업
(스마트팜·6차 산업)·농촌 청년 진로·정책 자문 기회. 2~3 단락 (Custom 컨텍스트
deep).

Sources: ...
```

→ AI Report Editor가 사용자가 정확히 어떤 컨텍스트인지에 *맞춰* implications 자동 생성.

## Item 8 — Reports Suggested for Review (특히 가치 있는 양식)

PDF 원전 Item 8 (January 2009):
```
Item 8. Reports Suggested for Review
8.1 State of the World 2009
State of the World 2009: Into a Warming World by Worldwatch Institute is a comprehensive
analysis of potential evolution of climate change by the end of the century and of the urgent
actions and policies that need to be taken now. ...

Military Implications:
The report is a source of information on the implications of climate change, including security
and adaptation, and thus aids planning improvement, resource prioritization, and preparedness.

Source:
State of the World 2009: Into a Warming World
http://www.worldwatch.org/node/5658
```

→ 외부 *권위 보고서·thinktank 산출물*을 추천. 깊이 있는 추가 reading 안내.

### 사용자 컨텍스트 Item 8 후보

매월 1~3 외부 보고서 추천:
- **글로벌**: Worldwatch State of the World·UNDP HDR·OECD·IMF·McKinsey Global·World Economic Forum·Pew Research
- **한국**: KIEP·KDI·STEPI·KIHASA·KISTEP·통일연구원·아산정책연구원
- **신학·목회**: Pew Forum·Lifeway Research·한국기독교목회자협의회·미래목회연구소

## Item 7 — Updates on Previously Identified Issues (지속성·연결의 핵심)

PDF 원전:
```
Item 7. Updates on Previously Identified Issues
7.1 New Chemicals Considered for Toxic Lists
[summary]
[See also New Hazardous Substances to be Banned in October 2008 and other related items in previous environmental security reports.]

Military Implications:
...

Sources: (additional sources in the Appendix)
...
```

→ *이전 보고서*의 issue를 추적·update. *연속성*이 환경 스캐닝의 가치 핵심.

### 사용자 적용
- 매월 보고서 Item 7에서 *전월·지난 분기 핵심 issues* 5~10개 update
- "[See also January 2026 Item 3]" 같은 cross-reference로 연결
- 누적 *issue evolution timeline* 자동 생성

## Item 6 — Technological Advances 형식

PDF 원전 Item 6:
```
Item 6. Technological Advances with Environmental Security Implications
6.1 New Process Improves Water Desalination Efficiency
[1~2 단락 summary]

Military Implications:
[1 단락]

Sources:
[3~5 sources]

6.2 Another "Green" Concrete Announced
[동일 구조]
```

→ *기술·과학 발전* sub-items 모음. 각 sub-item은 *축약형* (Item 1~5보다 짧음).

### 사용자 Item 6 적용

매월 4~8개 신규 기술·과학 발전:
- AI·양자·바이오·SMR·신소재 등
- 각 sub-item Summary 1~2 단락 + Implications 1 단락 + Sources 3~5

## Appendix — Reference Details

PDF 원전:
```
APPENDIX
Reference Details

This Appendix contains expanded background information on some items.

Item 1. U.S. Policy Shift May Improve International Environmental Security
Some bold actions considered by the new U.S. administration in its first week in office, include:
- implement the Energy Independence and Security Act that requires increasing car fuel efficiency standards starting with model year 2011 for reaching at least 35 miles per gallon by 2020 for cars and light trucks
- instruct the Environmental Protection Agency to allow California and other States willing to adopt stricter emissions standards for new motor vehicles
[etc.]

Sources: (a more comprehensive list)
...
```

→ Item별 *expanded background* + *more comprehensive sources list*. Body는 간결, Appendix가 깊이 보장.

### 사용자 Appendix 활용
- Body 12 페이지, Appendix 5~15 페이지
- 사용자이 *깊이 들어가야 할 issue*만 expanded background
- Sources 더 풀버전 (15~30개)

## 보고서 생성 protocol

### Input
- vision-foresight-environmental-scanning-weak-signal-template DB의 *지난 1개월* records (50~100건)
- 이전 월 보고서 (Item 7 update 위해)
- 외부 신간 보고서 4~6편

### Processing 9 steps

#### Step 1 — Records 분류
- Records를 *5 main items* (Item 1~5) + *technological* (Item 6) + *update* (Item 7)로 분류
- Item 1~5: 가장 strategic·high-impact·new
- Item 6: technical·science focused
- Item 7: 이전 보고서 follow-up

#### Step 2 — Item 1~5 selection
- Top 5 strategic items
- 사용자가 Step 1-A에서 선택한 **N개 도메인 모두**에 implications 가능한 item 우선 선정
- 각 item 1~3 단락 summary 작성

#### Step 3 — N-domain Implications 작성 (각 item)
- **사용자가 선택한 N개 도메인**(1~10 중 선택, Custom 포함) 각 1~2 단락
- Hardcoding 금지 — "Futurology·Pastoral·Investment" 고정 사용 절대 금지
- N도메인 각각 Python으로 커버리지 검증:
  ```bash
  python3 "$CALC_PY" --fn validate_implications \
    '{"selected_domains":[...],"item_implications":{...}}'
  ```
- 사용자 *직접 행동* 가능 형태

#### Step 4 — Item 6 (Technological)
- 신규 기술 4~8개 sub-items
- 축약형 (Summary 1~2 단락 + Implications 1 단락)

#### Step 5 — Item 7 (Updates)
- 이전 보고서 issues 5~10개 update
- Cross-reference 명시

#### Step 6 — Item 8 (Reports for Review)
- 신간 외부 보고서 1~3개 소개
- 사용자 perspective implications

#### Step 7 — Sources 정리
- 각 item·sub-item 5~10 sources
- Body는 간결 list, Appendix에 풀버전

#### Step 8 — Cover·TOC
- Title·month·페이지 번호
- TOC

#### Step 9 — Appendix
- 깊이 들어가야 할 items의 expanded background
- More comprehensive sources

### 분량 표준
- Body 8~15 페이지
- Appendix 5~20 페이지
- 총 15~35 페이지

### Cadence 권고
- **매월 1회** (월 첫 주에 전월 records 기반 작성)
- **분기 종합** (분기 마지막 월에 *분기 종합 보고서* — 50~80 페이지)
- **연간 종합** (12월 또는 1월에 *연간 종합 보고서* — 100~200 페이지, 차년도 priority 포함)

## 사용자 cadence 매트릭스

### 사용자 통합 보고서 — 월간

매월 첫 주, 전월 records 기반. 사용자 본인 + 자문위원 1~2명 review.

### 컨텍스트별 분리 보고서 — 분기

- 분기 마지막 월: 미래학·목회·투자 *각각* 분리 보고서
- 미래학 보고서: 사용자 자문 client·강의·집필 직접 활용
- 목회 보고서: 당회·평신도 panel 공유
- 투자 보고서: 사용자 personal portfolio decision

### 연간 종합 — 12월~1월

- 차년도 priority 포함
- 사용자 신년 단행본·강의 *primary input*
- 자문위원 + 외부 expert review

## 사용자 보고서 inventory 시스템

### 파일·디렉터리 구조 권고

```
~/Documents/foresight-reports/
├── 2026/
│   ├── 2026-05-monthly-integrated.md    (이번달)
│   ├── 2026-04-monthly-integrated.md
│   ├── 2026-03-monthly-integrated.md
│   ├── 2026-Q1-quarterly-futurology.md
│   ├── 2026-Q1-quarterly-pastoral.md
│   ├── 2026-Q1-quarterly-investment.md
│   └── ...
├── 2025/
│   └── 2025-annual-comprehensive.md
└── _templates/
    ├── monthly-integrated-template.md
    ├── quarterly-context-template.md
    └── annual-comprehensive-template.md
```

### Issue tracking timeline (Item 7 cross-ref 자동화)

각 issue에 *unique ID* 부여 → 모든 월간 보고서에서 *동일 ID*로 추적:
```
ISSUE-2026-001: AGI 화이트칼라 한국 침투
- 2026-04 보고서 Item 1
- 2026-05 보고서 Item 7.4 (update)
- 2026-06 보고서 Item 7.4 (update)
- ...
```

→ 사용자 대시보드에서 *issue별 timeline*·*evolution*·*사용자 코멘트* 추적 가능.

## 입력 처리 패턴

### Pattern 1 — 월간 통합 보고서 생성 요청
사용자: "이번 달 환경 스캐닝 보고서 만들어줘"
→ 9 steps 적용. vision-foresight-environmental-scanning-weak-signal-template DB records 기반.

### Pattern 2 — Single-domain 집중 보고서
사용자: "이번 분기 [특정 도메인]만 집중 보고서"
→ Pattern B 양식. 해당 1개 도메인 Implications 중심·확장 (single-domain deep).

### Pattern 3 — 기존 보고서 업데이트
사용자: "지난 달 Item 1 update해줘"
→ Item 7 형식으로 follow-up.

### Pattern 4 — Item 8 Reports Suggested 작성
사용자: "최근 신간 보고서 추천 코너 써줘"
→ 신간 thinktank·정부 보고서 1~3 + 사용자 perspective implications.

### Pattern 5 — 연간 종합 보고서
사용자: "올해 종합 보고서 작성"
→ 12개월 records·이슈 통합 + 차년도 priority.

### Pattern 6 — 보고서 양식·인프라 설계
사용자: "사용자 환경 스캐닝 보고서 시스템 처음 만드는데"
→ Cadence 매트릭스 + 파일 구조 + 자동화 protocol facilitate.

## 점검 체크리스트

산출 직전 다음 모두 ✓ 확인:

- [ ] PDF Appendix B 양식 (Item·Summary·Implications·Sources) 정확히 구현?
- [ ] Item 1~5 (strategic) + Item 6 (technological) + Item 7 (updates) + Item 8 (reports) 구조 보존?
- [ ] 사용자가 선택한 **N개 도메인 모두** 각 item에 implications 포함? (Python validate_implications 결과 all_covered=true 확인)
- [ ] 각 item Sources 5~10 링크 제공?
- [ ] Item 7 *cross-reference* (이전 보고서 연결) 명시?
- [ ] Body·Appendix 분리 (Body 간결, Appendix 깊이)?
- [ ] Issue ID 일관성 (cross-month tracking)?
- [ ] 각 implication이 *사용자 직접 행동* 가능한 형태?
- [ ] 한국 정보 소스 충분히 활용?
- [ ] *weak signal* 강조 (단순 사실 보고 X)?

## 보조 자료 (references/)

| 파일 | 용도 |
|------|------|
| `references/january_2009_full_report.md` | PDF Appendix B의 *January 2009 Environmental Security* 보고서 풀 reproduction (37 페이지 원전 그대로) — 보고서 작성 시 *직접 reference* |
| `references/monthly_report_template.md` | 사용자 월간 통합 보고서 표준 template (Cover·TOC·Items 1~8·Appendix) |
| `references/implications_by_domain.md` | 사용자 3 도메인 (Futurology·Pastoral·Investment) implications 작성 protocol·예시 100+ |
| `references/issue_tracking_system.md` | Issue ID·timeline·cross-month tracking·dashboard 인프라 권고 |

## 오류 및 예외처리

Python이 `"error": true`를 반환하거나 다음 상황 발생 시 처리:

| 상황 | 처리 |
|---|---|
| Issue ID sequence 충돌 | `next_id` 함수로 충돌 없는 다음 순번 조회 |
| year out of [2002, 2100] | 유효 연도 재입력 요청 |
| month out of [1, 12] | 유효 월 재입력 요청 |
| Missing Item(s) in structure | 누락 item 목록 보고 후 해당 항목 작성 요청 |
| source_count < 5 | 부족한 sources 수 보고 후 추가 요청 |
| source_count > 10 | 초과분 Appendix로 이동 안내 |
| Missing domain implications | 누락 도메인 implications 작성 후 재검증 |
| Empty implications text | 빈 implications 보고 후 작성 요청 |
| Input items dict is empty | 보고서 items 입력 필요 안내 |

## 입력 검증 규칙

Python 호출 전 사전 점검:

| 규칙 | 조건 |
|---|---|
| V1 | year ∈ [2002, 2100] |
| V2 | month ∈ [1, 12] |
| V3 | sequence ∈ [1, 999] |
| V4 | item_id ∈ "1"-"8" |
| V5 | source_count ≥ 0 |
| V6 | selected_domains는 1-10 중 유효한 도메인명 |
| V7 | items dict 비어있지 않음 |
| V8 | 보고서 생성 전 validate_full_report로 전체 검증 |

---

## 마무리

본 스킬의 가장 중요한 약속: **Millennium Project가 23년 누적 운영한 검증된 양식을 그대로 사용자 컨텍스트로 적용한다.** Body 간결·Appendix 깊이·Item 7 연속성·Item 8 권위 보고서 추천·사용자 3 implications — 이 5요소가 사용자 정기 보고서의 품질을 보장한다. 본 스킬의 산출은 사용자 단행본·강의·당회·자문·portfolio 의사결정의 *primary input*이자, **vision-foresight-environmental-scanning-issues-management** Renfro cycle Stage 1·2의 정기 reload가 된다.
