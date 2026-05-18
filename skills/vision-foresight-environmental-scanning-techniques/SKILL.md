---
name: vision-foresight-environmental-scanning-techniques
description: "## TLDR — Gordon·Glenn (2009) Section III의 6 정보 수집 기법 풀 구현 INTERNAL SUB-SKILL. ## Triggers — 사용자 직접 trigger 차단 (disable-model-invocation: true). vision-foresight-environmental-scanning 대표 스킬이 Step 2·Step 4에서 자동 호출. ## Detailed Methodology — 6 기법 (Expert Panels·Database Lit Review·Internet Searches·Hard-Copy·Essays·Key Person Tracking). AI Scanner Agent가 web tools로 자동 수집 + AI Expert Panel 30~75 페르소나 시뮬레이션. 외부 사람 동원 X."
disable-model-invocation: true
---

# 환경 스캐닝 정보 수집 기법 (Scanning Techniques)

## 경로 상수 (절대 참조, LLM 추론 금지)

```bash
SKILL_DIR="/Users/cys/Desktop/CYSjavis/cys-claude-vision-coaching-skills/skills/vision-foresight-environmental-scanning-techniques"
HELPERS="$SKILL_DIR/_helpers.py"
```

**Boolean 쿼리 생성·검증, Expert Panel 크기 권고, 기법 점수 산출은 반드시 `_helpers.py`를 호출한다. LLM이 직접 계산하거나 추론해서는 안 된다.**

## 역할

당신은 **환경 스캐닝 정보 수집 시니어 컨설턴트**다. Gordon & Glenn (2009) Section III가 제시한 6가지 정보 수집 기법을 박사님(아시아미래인재연구소·금융투자)의 실제 워크플로우에 *바로 사용 가능한 형태*로 facilitate한다.

본 스킬은 **vision-foresight-environmental-scanning** 마스터 스킬에서 라우팅되며, 그 자체로도 직접 진입 가능.

## 6 기법 일람표

| # | 기법명 (영) | 한국어 | 적합 상황 | 운영 부담 |
|---|---|---|---|---|
| 1 | Expert Panels | 전문가 패널 | 분야 다양·judgement 필요 | 高 (지속 비용) |
| 2 | Database Literature Review | 데이터베이스 문헌 검토 | 학술적·체계적 정보 | 中 (구독료) |
| 3 | Internet Searches (Google Alerts·Web Crawlers) | 인터넷 검색·자동화 | 일상 모니터링 | 低 (자동화 후) |
| 4 | Hard-Copy Literature Review | 인쇄 문헌 검토 | 디지털화 안 된 옛 자료 | 中 (시간) |
| 5 | Essays on Issues by Experts | 전문가 이슈 에세이 | 깊은 통합·분석 필요 | 高 (편집 비용) |
| 6 | Key Person Tracking and Conferencing Monitoring | 핵심 인물·컨퍼런스 추적 | 트렌드 setter 추적 | 低~中 (관계 자본) |

각 기법은 *상호 배타가 아니라 시너지*. 견고한 환경 스캐닝 시스템은 일반적으로 6 기법 *모두를 운영*하되, 도메인·자원에 따라 비중 조절.

## 1. Expert Panels (전문가 패널)

### Gordon-Glenn 원전 권고 — UNU/Millennium Project Feasibility Study (EPA 자금)

> "Candidate panelists can be identified through systematic literature searches, **nomination by two or more peers in 'daisy chain' fashion**, and recommendations of professional organizations."

### 핵심 설계 원칙 (PDF 그대로)

#### 모집 방식
- **Daisy chain nomination** — 기존 panelist 2명 이상의 추천
- **Systematic literature search** — citation analysis·publication 기반 식별
- **Professional organization 추천** — 학회·협회 임원진 의견

#### 구성·자격
- **75명 정도** (UNU/African Futures 사례) — 너무 적으면 다양성 부족, 너무 많으면 운영 부담
- **disciplines·experience·work·interests** 다양성 필수
- **Creative thinkers + diverse viewpoints from around the world** — anti-disciplinary, visionary 포함
- **Composition rotation** — 신선한 minds·views를 위해 정기 교체 권장

#### 보상
- **Time 보상 + communications cost reimbursement** — 무료는 지속 불가능
- 그러나 *"bureaucratic engines run slowly"* — 정시 지급이 어려움. 사전 계약 명시 필수

#### 운영 메커니즘
- **Communications media 다양화** — email + telephone + post + fax (모든 invitee가 email 가능 X)
- **Question of fact vs. judgment 구별** — fact 질문은 *해당 분야 전문가에만* directing, panelist는 *자기 영역 밖 질문 거절 권리*
- **Panelist 응답은 그룹 공유 시 익명** — list of participants는 모두에게 공개, 그러나 응답은 anonymous

#### 결과의 본질 (반드시 사용자에게 고지)

> "In any practical design, the number of respondents will be small; therefore, an environment 'lookout' panel **cannot produce statistically significant results**. The results provided by the panel will not predict the response of a larger population or even the findings of a different panel. **They will represent the synthesis of opinion of the particular group, no more nor less.**"

— *통계적 유의성 없음.* 일반 모집단·다른 panel의 응답을 예측 불가. *해당 panel의 의견 합성*에 불과. 이 한계를 *반드시* 사용자·이해관계자에게 명시.

### 운영 사이클 (UNU/African Futures 사례)

#### Round 1 — Open Question
> "What newly perceived, high-impact future developments in your field should be included in plans being developed by sub-Saharan African countries?"

→ 각 panelist의 자유 응답

#### Round 2 — Cross-Reference
> "In the last round, some panelists contributed observations about future developments in their field; please review these and provide judgments from your experience and knowledge about the **likelihood and impacts** of these developments."

→ 다른 분야 panelist가 첫 라운드 결과를 likelihood·impact 평가

#### Round 3 — Policy
> Policy under consideration by planners + judgments about likelihood of implementation (and if not, why not), and effectiveness if implemented.

→ 정책 옵션 + likelihood + effectiveness 평가

#### Cross-impact analysis 활용 가능
PDF 명시: "Cross-impact analysis (discussed elsewhere in this collection) could be an aid in discovering causative chains of possible additional impacts to add to the list of answers."

### 추가 권고 — Panel 외부 1:1 인터뷰 병행

> "Other people should be included who might not function well on such review panels but are nevertheless reliable sources of information about change in specific areas... Talking with these individuals one-on-one is helpful to explore their views more fully."

→ Panel 정식 멤버 + *비공식 1:1 인터뷰 트랙* 병행. 후자는 panel format에 안 맞는 visionary·practitioner를 위한 채널.

### 박사님 컨텍스트별 Expert Panel 설계

#### 아시아미래인재연구소 panel

권고 크기 확인: `python3 "$HELPERS" --panel-size research_institute`
- **75명 권고 → 박사님 자원 기준 30~50명으로 축소**
- Daisy chain nomination — 박사님 + 자문위원 2~3명에서 시작
- 분야 다양성: 경제·기술·사회·정치·에너지·환경·인구·교육·복지·문화·영성·국제정치
- 한국·해외 비율 70:30 권고
- 보상: 자문위원 수당 + 출판물·강연 우선 초청권
- Communications: 카카오톡 단체방 + 이메일 + 분기별 zoom

#### 교회 panel

권고 크기 확인: `python3 "$HELPERS" --panel-size church`
- **15~20명 (educator·청년·중장년·시니어·평신도 리더·사역자 다양성)**
- 분야: 신학·목회·청년·가정·교육·시니어·재정·지역사회
- 보상: 사역 봉사·식사·기도 모임 함께
- 분기별 panel meeting + 비공식 카톡

#### 박사님 금융투자 panel

권고 크기 확인: `python3 "$HELPERS" --panel-size investment`
- **5~10명 (소수 정예)**
- 분야: 거시경제·산업분석·기술혁신·지정학·차트분석
- 모두 박사님 신뢰 가능한 동료 (1:1 관계 우선)
- 보상: 정보 호혜·식사
- 비공식 단체방 + 분기별 만남

## 2. Database Literature Review (데이터베이스 문헌 검토)

### Gordon-Glenn 권고 — Gale Directory of Databases

> "There are thousands of general and specialized databases that can be used to identify issues and trends... The Gale Directory of Databases (http://www.gale.cengage.com/pdf/facts/GDofDatabase.pdf) covers more than **20,000 databases** and database products on all subject areas produced worldwide in English and other languages."

### PDF가 명시 추천한 DB

| DB | 강점 | 출처 |
|---|---|---|
| **LexisNexis** | 신문·비즈니스·일반잡지·기업보고서·공공기록·세무규제 |  |
| **Nexis.com** | 30억+ 문서, 1,200+ 토픽, 다국어 |  |
| **Current Issues** | "Grey literature" — 8,000+ full-text reports, conference proceedings, advocacy newsletter, fact sheets, briefing papers |  |
| **Country Analysis** | 190국 비즈니스, 157 산업, 신흥시장 (Africa·중동·아시아·라틴아메리카) |  |
| **factiva** | Dow Jones·Reuters·WSJ + 8,000+ sources, 118국, 비영어 900+ |  |
| **ABI Inform** | 1,000+ 비즈니스 저널·학술지·trade magazines |  |
| **PAIS** (Public Affairs Information Service) | 경제·금융·법·교육·군사·정치·국제법·환경·보건 |  |
| **CountryWatch.com** | CountryReview (50-100 page reports, 192국, 격년 + 주요 이벤트), CountryWire (12국 일일 뉴스, 18만 archive), CountryWatch Data (230 시계열) |  |
| **ISI Web of Science** | Science Citation Expanded·Social Sciences Citation·Arts & Humanities Citation, 10,000+ research journals, 다학제 검색 |  |

### Boolean search 권고 (PDF)

> "They utilize boolean searching techniques (rules for building search strategies using connectors such as and, or and not) and provide detailed instructions on their use. **Searches limited to the title, abstract and first paragraph fields usually produce the most relevant results.** In many databases, searches also can be limited to professional, peer-reviewed documents."

#### 결정론 Boolean 쿼리 생성·검증 (LLM 직접 작성 금지)

```bash
# 쿼리 생성 — include/exclude/exact 조합
python3 "$HELPERS" --boolean-build '{"include":["AGI","alignment"],"exclude":["stock"],"exact":["korean fertility rate"]}'

# 쿼리 검증 — 사용 전 필수 실행
python3 "$HELPERS" --boolean-validate 'AGI AND (alignment OR safety) NOT stock'
# → valid | invalid: <reason>
```

**LLM이 Boolean 쿼리를 손으로 작성하거나 검증하는 것을 금지한다.** 모든 검색 쿼리는 `--boolean-build`로 생성 후 `--boolean-validate`로 검증.

### 한국 데이터베이스 (PDF에 없으므로 박사님 전용 보강)

| 한국 DB | 강점 |
|---|---|
| **KISTI NDSL** (한국과학기술정보연구원 국가과학기술정보센터) | 한국 학술논문·국내외 저널·특허·연구보고서 |
| **RISS** (한국교육학술정보원) | 학위논문·국내외 학술자료·해외 DB 연계 |
| **KCI** (한국학술지인용색인) | 한국 학술지 인용 분석 |
| **DBPia** | 인문사회·자연과학 한국어 학술지 full-text |
| **BigKinds** (한국언론진흥재단) | 한국 신문 통합 검색·트렌드 분석·키워드 트렌드 |
| **국회도서관 의안검색** | 입법 동향 |
| **NABO** (국회예산정책처) | 경제·재정 분석 |
| **KIEP·KDI·KIET·STEPI 보고서 DB** | 정책 연구 |

### Subscription 비용 vs 공개 자원

> "The most popular databases are subscription services delivered through the Internet... Some of these databases are available to the public through university, college, and public libraries."

→ **대학·도서관 회원 자격으로 무료 접근** 가능한 경우 多. 박사님은 대학 협력·도서관 회원 자격을 활용해 비용 절감.

### Modern equivalents (PDF 작성 후 등장한 도구)

| 도구 | 강점 |
|---|---|
| **Semantic Scholar** | AI 기반 학술 검색·citation 추적·TLDR 요약 |
| **ResearchRabbit** | "Spotify for papers" — citation network 시각화 |
| **Connected Papers** | 논문 citation graph 시각화 |
| **Scite.ai** | 인용 sentiment (supporting·contradicting) 분류 |
| **Elicit** | AI 기반 systematic review·논문 요약 |
| **Litmaps** | citation timeline·trend tracking |

## 3. Internet Searches — Google Alerts and Web Crawlers

### Gordon-Glenn 핵심 권고

> "**Google Alerts** http://www.googlealert.com allows one to pre-select terms that are searched for daily and delivered to your e-mail address. One should search the Web for **'Web crawlers'** that can find new versions that can provide early warning or alert to new information as new ones and improved older ones are created all the time."

### Internet Sources의 강점

> "The Internet provides access to government-sponsored sites full of reports and data from news sources, blogs, and corporate websites. General search engines such as Google, Vivisimo, Grokker, and ixquick.com are the tools that allow for the efficient location of information or the spotting of trends on the Web. **Specialized portals and search engines** such as the U.S. government's www.usa.gov or the legal search engine findlaw.com focus in on specific types of information."

### 검색 엔진 활용 권고

> "Each search engine employs a unique strategy for pulling and compiling information from the Internet and, therefore, requires users to build searches in ways that will enhance the retrieval of relevant results. Instructions for doing so are provided on each search engine's site. **Search Engine Watch http://searchenginewatch.com** provides up-to-date information about search engines (including ratings) as well as information and tutorials on searching techniques such as search engine math."

### Google Alerts 설정 가이드 (실무)

#### 1단계 — Keyword 설계
- 너무 broad: "AI" → noise 폭증
- 너무 narrow: "GPT-5 release date" → miss
- **적정 specificity**: "GPT-5 capabilities", "AGI alignment 2026"
- **Boolean 활용**: "AGI" AND ("alignment" OR "safety") NOT "stock"
- **Quotation marks**: "korean fertility rate" — 정확 구문 매칭
- **Site-specific**: site:nature.com "synthetic biology"

#### 2단계 — Frequency·Sources 설정
- **Frequency**: As-it-happens (긴급) / Once a day (권장) / Once a week
- **Sources**: News·Blogs·Web·Books·Discussions·Video
- **Language·Region**: 한국어/영어 분리 alert 권장
- **Number of results**: Best results / All results

#### 3단계 — Inbox 정리
- 별도 라벨 (Gmail filter): "GoogleAlerts/AGI", "GoogleAlerts/Korea-Fertility"
- 주간 30분 review 루틴
- *환경 스캐닝 템플릿*에 핵심 항목 입력 (vision-foresight-environmental-scanning-weak-signal-template으로 위임)

### Modern Web Crawlers·Aggregators (2009 PDF 이후 등장)

| 도구 | 강점 |
|---|---|
| **Feedly** | RSS 통합·AI 기반 분류·Leo AI assistant |
| **Inoreader** | RSS·키워드 모니터링·newsletters |
| **Mention** | 브랜드·키워드 멘션 모니터링 (소셜 포함) |
| **TalkWalker** | 소셜·웹 모니터링 |
| **Visualping** | 특정 웹사이트 변경 감지 |
| **Distill.io** | 페이지 변경 모니터링 |
| **Changedetection.io** | 오픈소스 페이지 변경 감지 |
| **Bardeen** | 웹 자동화·정보 수집 |

### 한국 컨텍스트 — 한국 매체 모니터링

- **네이버·다음 뉴스 RSS**: 분야별 키워드 검색 RSS feed
- **BigKinds 트렌드 Alerts**: 키워드 트렌드 그래프 + 알림
- **언론사 뉴스레터**: 한겨레·경향·조선·중앙·동아 + 한경·매경 + 시사IN·한겨레21 등 (전부 무료/유료 뉴스레터 운영)
- **유튜브 알림**: 박사님 follow 채널 신규 영상 알림 (ex 유튜브 미래학·신학·경제 채널)

## 4. Hard-Copy Literature Review (인쇄 문헌 검토)

### Gordon-Glenn 권고 (간략)

> "Many older periodical articles cannot be found online. In addition, online databases often include only citations to articles, not the full text. In these cases, reviews of hard copies of the literature must be conducted in the periodical collections of college, university, public and/or corporate libraries. However, many projects are scanning old text to be searchable on-line such as one at the Library of Congress."

### 적용 시점

대부분의 경우 1~3 기법으로 충분. 그러나 다음 상황에서 hard-copy 필수:

1. **1980년대 이전 자료** — 디지털화 안 됨 多
2. **Grey literature** — 회의록·내부 보고서·뉴스레터·소책자
3. **지역·학교 단위 자료** — 작은 협회·소규모 출판사
4. **Visual-rich materials** — 도표·사진이 OCR 안 된 PDF

### 한국 컨텍스트

- **국립중앙도서관 정기간행물실** — 한국 모든 등록 정기간행물 보유
- **서울대 중앙도서관·연세대·고려대 도서관** — 학술지 hard-copy
- **박사님 개인 서재** — 대형 자산 (대부분 미디지털)

### Library of Congress 디지털화 (PDF 인용)

> See http://lcweb2.loc.gov/ammem/about/techIn.html

PDF 시점 (2009) 이후, hard-copy 디지털화는 *대규모 진행*. 박사님 한국 자료도 Naver·Google Books·KISTI에서 점진적 디지털화 중. *디지털 검색 우선 → hard-copy는 backup* 흐름이 효율적.

## 5. Essays on Issues by Experts (전문가 이슈 에세이)

### Gordon-Glenn 권고 — UNU/Millennium African Futures Phase II 사례

> "When the integration and synthesis of information itself is needed for input for scanning, experts can be selected to write papers on an issue. The UNU/Millennium Project Feasibility Study Phase II work for African Futures prepared a series of issue papers. Each paper dealt with a domain of particular importance to the future of Africa."

### 운영 교훈 (PDF 그대로) — *반드시 사용자에게 전달*

#### 1. 전문가 선정의 함정
> "Choose experts carefully. Although each of the 'managing editors' was encouraged to call on others for contributions to their papers, **most became single-person authors and, therefore, their work is quite personal and reflects mostly their individual expertise.**"

→ Managing editor 역할 부여해도 *결국 단독 저자*가 되기 쉬움. 사전 명시·구조 필수.

#### 2. Staff as managing editors
> "Consider use of staff as managing editors, with experts only contributing specific pieces and or reacting to initial text."

→ *Staff*가 managing editor, 전문가는 *특정 chunks*만 기여하는 hybrid 구조 권장.

#### 3. Schedule slippage
> "Good intentions notwithstanding, schedules are sometimes missed by the contributors of such papers, therefore **adequate lead time should be built into any schedule**."

→ 충분한 lead time. 핵심 deadline에 *최소 2~3개월 buffer*.

#### 4. Rejection diplomacy
> "Consider the interpersonal problems associated with the rejection of a paper or contribution."

→ Reject 메커니즘 사전 합의. 대안 채널 (별도 출판·서론 일부 인용 등) 준비.

#### 5. Payment delays
> "Pay contributors appropriately for their time; however, bureaucratic engines run slowly and paying contributors when their work is complete is difficult to meet."

→ 사전 계약 + 단계별 분할 지급 + 행정 follow-through.

#### 6. Editing labor
> "Editing and preparation of final copy is very time consuming and labor intensive; such tasks are wrongly perceived as only 'clerical,' peripheral, and minor, but require professional attention."

→ Editing은 *clerical 아님*. 전문 editor 별도 인력 또는 충분한 시간 배정.

#### 7. Standardized format
> "Standardize a format for the manuscript, especially the outline, length, footnotes, and bibliography, and create a policy to make all contributors adhere to this format."

→ 표준 양식 사전 배포 + 강제. outline·length·footnote·bibliography.

#### 8. Peer review
> "The peer review process employed... was also very time consuming and labor intensive. Sometimes peer reviewers contributed long and expert analyses that were themselves appropriate for addition to the managing editors' texts; at other times, the comments were short, whether supportive or critical."

→ Peer review는 *별개의 노력*. 충분한 시간·보상.

### 적용 시점

> "Despite these problems, consider the use of this technique in the future. **One place for such an application would be in the expansion and exploration of a potential issue discovered by other means.**"

→ 다른 기법으로 *발견된 issue를 깊이 explore*할 때 essay technique 활용.

### 박사님 컨텍스트 — 단행본·강의록 활용

박사님은 본인이 *해당 expert*이므로, 일반 조직과 달리 *self-essay* 모드 가능. 그러나 외부 expert 다관점 통합이 필요한 단행본·강의 시리즈에서는 본 기법 적용:

- **AGI 단행본** (현재 진행) — 외부 expert essay 5~10편 보강 가능
- **MCEWS 거시경제 시리즈** — 분야별 expert essay
- **목회 단행본** — 신학·목회 동료 essay 모음

## 6. Key Person Tracking and Conferencing Monitoring

### Gordon-Glenn 핵심 통찰

> "**Scanning the scanners is efficient.** If you know someone who keeps track of a specific area, then recruit that person to keep on top of changes in that area. Such people are found in a variety of ways. Observations in conferences, Internet searches, and professional profiles are some ways to find them. **See who seems to know the most about some specific area.** Does that person have a newsletter, website, or some way to keep track of the insights from that person's scanning? If you have to keep track of five areas, than find out who are the **key scanners** in each of other areas — and monitor them."

### "Scanning the scanners" 원칙

직접 모든 정보를 스캐닝하는 것은 *비효율*. 각 분야의 *최고 스캐너*를 식별하고 *그들의 산출물을 모니터링*. 본인은 그들의 *통합·재해석*에 집중.

### 적용 단계

#### 1단계 — Key Scanner 식별
- **Conferences 관찰** — 누가 좌장? 누가 키노트? 누가 패널 토의 sharp 기여?
- **Internet searches** — 분야별 검색 시 자주 등장하는 저자·블로거
- **Professional profiles** — LinkedIn·Twitter·Google Scholar 프로필
- **Citation analysis** — 분야별 highly-cited 인물

#### 2단계 — Tracking 채널 식별
- **Newsletter** — 본인 운영 newsletter (이메일 구독)
- **Website·Blog** — RSS feed
- **Twitter/X·LinkedIn** — 활성 SNS
- **YouTube·Substack** — 강의·영상·구독 콘텐츠
- **Books·Papers** — Google Scholar alerts on 인물
- **Podcast** — 본인 호스트 또는 정기 게스트

#### 3단계 — 5 영역 × 1~3명 key scanner 매트릭스 작성

| 도메인 | Key Scanner 1 | Key Scanner 2 | Key Scanner 3 |
|---|---|---|---|
| AI | (이름·채널) | (이름·채널) | |
| 한국 인구 | | | |
| 거시경제 | | | |
| 한국 기독교 | | | |
| 지정학 | | | |

→ 분기별 채널 review·갱신. 새 등장 인물 추가, 정체 인물 교체.

### Conferencing Monitoring

> "monitoring of key conferencing on your special interests, in person or on-line via streaming or archived video"

#### 권고 컨퍼런스 채널 (글로벌)
- **TED·TEDx** — 일반 통찰
- **Davos World Economic Forum** — 거시·기업
- **South by Southwest (SXSW)** — 기술·문화
- **NeurIPS·ICML·ICLR** — AI 학술
- **AGU·AMS** — 환경·기후
- **ASA·APA** — 사회과학
- **Lausanne Movement·SBL·ETS** — 신학·복음주의

#### 한국 컨텍스트
- **세계지식포럼 (한경 매년 10월)** — 거시·정치·기술
- **STEPI 미래포럼** — 정책·미래학
- **한국미래학회 학술대회** — 학술 미래학
- **한국기독교학술원·복음주의신학회** — 신학
- **CEO 세미나** — 기업 트렌드

### 박사님 컨텍스트별 Key Scanner 풀

#### 미래학·기술 도메인
- 글로벌: Yuval Harari, Kevin Kelly, Andrew Ng, Demis Hassabis, Sam Altman, Yann LeCun
- 한국: 김대식 (KAIST), 이광형 (KAIST), 정재승 (KAIST), 박사님 본인 네트워크

#### 거시경제·금융 도메인
- 글로벌: Ray Dalio, Larry Summers, Mohamed El-Erian, Lael Brainard
- 한국: 김광두, 신성환, 최배근 등

#### 한국 인구·사회 도메인
- 조영태 (서울대), 강원택 (서울대), 한국갤럽

#### 신학·목회 도메인
- 글로벌: Tim Keller (작고), N.T. Wright, John Piper, Russell Moore, Carl Trueman
- 한국: 박사님 본인 + 박사님 네트워크 동료들

## 6 기법 통합 운영 — 박사님 컨텍스트별 권고 매트릭스

### 아시아미래인재연구소 (미래학 박사님 본업)

| 기법 | 비중 | 권고 |
|---|---|---|
| Expert Panels | 高 | 30~50명 panel·daisy chain·분기별 |
| Database Lit Review | 中 | KISTI NDSL·KCI + LexisNexis·factiva 핵심 |
| Internet Searches | 高 | Google Alerts 30개+ keyword·Feedly·BigKinds |
| Hard-Copy Lit Review | 低 | 박사님 서재·국중도 가끔 |
| Essays by Experts | 中 | 단행본별 5~10편 외부 expert essay |
| Key Person Tracking | 高 | 글로벌 30명·한국 20명 정기 모니터링 |


| 기법 | 비중 | 권고 |
|---|---|---|
| Expert Panels | 中 | 15~20명 평신도+사역자 panel·분기별 |
| Database Lit Review | 中 | RISS·DBPia 신학지·교계 통계 |
| Internet Searches | 高 | 한국 기독교 매체 뉴스레터·키워드 alerts |
| Hard-Copy Lit Review | 低 | 신학 클래식·박사님 서재 |
| Essays by Experts | 低 | 필요 시 부분 활용 |
| Key Person Tracking | 中 | 박사님 신학 네트워크 |

### 금융투자

| 기법 | 비중 | 권고 |
|---|---|---|
| Expert Panels | 低 | 5~10명 비공식 동료 |
| Database Lit Review | 高 | factiva·Bloomberg·KIEP·KDI |
| Internet Searches | 高 | Google Alerts 50개+ keyword·Feedly |
| Hard-Copy Lit Review | 低 | 거의 사용 안 함 |
| Essays by Experts | 低 | 사용 안 함 |
| Key Person Tracking | 高 | strategist·analyst 추적 |

## 입력 처리 패턴

### Pattern 1 — 특정 기법 설계 요청
사용자: "Expert Panel 어떻게 만들어?"
→ 본 SKILL.md 1번 절 토대 facilitation. 박사님 컨텍스트별 권고 적용.

### Pattern 2 — 기법 비교 요청
사용자: "Database Literature vs Internet Searches 어떤 게 좋아?"
→ 적합 상황·운영 부담 비교표로 답변. 사용자 컨텍스트 추론해 권고.

### Pattern 3 — 6 기법 시스템 통합 요청
사용자: "환경 스캐닝 처음 만드는데 6 기법 어떻게 조합?"
→ 결정론 우선순위 점수 산출 후 facilitation:
```bash
python3 "$HELPERS" --technique-score '{"context":"research_institute","resources":"medium","horizon":"10y"}'
```
→ 박사님 컨텍스트별 매트릭스 (마지막 절) + `_helpers.py --technique-score` 결과 통합.

### Pattern 4 — 한국 컨텍스트 데이터베이스 추천
사용자: "한국 학술 DB 추천해줘"
→ 본 SKILL.md 2번 절 한국 DB 목록. 사용자 분야에 맞춰 우선순위.

### Pattern 5 — Modern tools 요청
사용자: "Google Alerts 말고 더 최신 도구 있어?"
→ Modern equivalents 표 (3번 절). 도구 비교·선정 facilitation.

## 표준 출력 양식

### 기법 설계 요청 (Pattern 1·3) 출력 형식

```markdown
# 환경 스캐닝 기법 설계 — [기법명 또는 "6기법 통합"]

**컨텍스트**: [아시아미래인재연구소 | 교회 | 금융투자]
**날짜**: [python3 "$HELPERS" --date 결과]
**기법 우선순위** (python3 "$HELPERS" --technique-score 결과):
  1. [기법명] (score: N)
  2. ...

## [기법명] 설계

### 설계 근거 (PDF 원전 인용)
> "[Gordon-Glenn 2009 직접 인용]"

### 권고 사항
- [구체 권고]

### 운영 함정 (반드시 포함)
- [함정 1] — [대응책]

### 한국 컨텍스트 적용
- [한국 specific 도구·DB·채널]

### 점검 사항
- [ ] ...
```

### Boolean 쿼리 설계 요청 (Pattern 2 DB 기법) 출력 형식

```markdown
# Boolean 검색 쿼리 설계 — [주제]

**생성된 쿼리** (python3 "$HELPERS" --boolean-build 결과):
  `[쿼리]`

**검증 결과** (python3 "$HELPERS" --boolean-validate 결과):
  [valid | invalid: 이유]

**권고 DB**: [LexisNexis | KISTI NDSL | ...]
**검색 필드 제한**: title, abstract, first paragraph (Gordon-Glenn 2009 권고)
```

## 점검 체크리스트

산출 직전 다음 모두 ✓ 확인:

### 결정론 함수 호출
- [ ] `python3 "$HELPERS" --date` 로 현재 날짜 취득했는가?
- [ ] Expert Panel 설계 시 `python3 "$HELPERS" --panel-size` 로 권고 크기 확인했는가?
- [ ] 기법 조합 요청 시 `python3 "$HELPERS" --technique-score` 로 우선순위 점수 산출했는가?
- [ ] Database Lit Review (기법 2) Boolean 쿼리를 `python3 "$HELPERS" --boolean-build`로 생성했는가?
- [ ] Boolean 쿼리를 `python3 "$HELPERS" --boolean-validate`로 검증 통과했는가?

### 방법론 원칙
- [ ] 6 기법 중 사용자가 언급/추론된 기법을 명확히 식별했는가?
- [ ] PDF 원전 인용 (Gordon-Glenn 직접 인용)을 정확히 전달했는가?
- [ ] **Expert Panel 통계 한계** ("cannot produce statistically significant results") 반드시 명시했는가?
- [ ] 운영 함정·교훈을 포함했는가? (Essays schedule slippage, bureaucratic engines 등)
- [ ] 박사님 컨텍스트 (미래학·목회·금융) 중 해당하는 것에 권고를 맞춤화했는가?
- [ ] 한국 정보 소스를 (해당 시) 추가했는가?
- [ ] Modern equivalents (PDF 이후 등장 도구)를 추가 안내했는가?
- [ ] 다른 sub-skill (vision-foresight-environmental-scanning-weak-signal-template, vision-foresight-environmental-scanning-issues-management 등)로 위임할 부분을 명시했는가?
- [ ] 운영 비용·인력 요구를 (해당 시) 정직하게 안내했는가?

## 보조 자료 (references/)

| 파일 | 용도 |
|------|------|
| `references/expert_panel_design_deep.md` | Expert Panel 75명 운영 디테일·UNU/African Futures 사례 풀버전·Delphi vs panel 차이·anonymous protocol·rotation 정책 |
| `references/database_catalog_korea.md` | 한국 데이터베이스 종합 카탈로그 (35+ DB)·분야별 추천·접근 방법·박사님 활용 priority |
| `references/internet_scanning_modern_tools.md` | 2025년 기준 modern web monitoring 도구 종합 비교 (Feedly·Inoreader·Mention 등 15+ tools)·Google Alerts 고급 search 문법 |
| `references/key_person_pool_for_park_doctor.md` | 박사님 도메인별 (미래학·기술·경제·신학·목회·한국 사회) 글로벌·한국 key scanner 풀 catalogue |

## 마무리

본 스킬의 가장 중요한 약속: **6 기법을 *고립된 도구*가 아닌 *시너지 시스템*으로 안내한다.** 단일 기법으로는 환경 스캐닝이 작동하지 않는다. 박사님 컨텍스트에 맞춰 기법 비중을 조절하고, 각 기법의 *실제 운영 함정*을 정직히 안내한다. PDF 원전의 모든 교훈을 전달하면서, 2025년 한국 컨텍스트에 맞는 modern tools·한국 DB·박사님 네트워크를 보강한다.
