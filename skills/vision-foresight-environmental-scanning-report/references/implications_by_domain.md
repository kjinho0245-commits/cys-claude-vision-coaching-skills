# Implications by Domain — 10 도메인 작성 Protocol + Generic 예시

> 사용자가 대표 스킬 Step 1-A에서 선택한 N개 Implications 도메인에 따라 Agent 6 Report Editor가 *자동* implications 생성. 본 문서는 10 도메인 default + Custom 작성 protocol.

## Implication 작성 일반 원칙 (모든 도메인 공통)

### 1. 행동 가능성 (Actionability)
- *해당 도메인 사용자가 직접 행동* 가능한 형태
- 추상적 분석 ≠ implication
- 예: "AGI가 중요하다" (X) → "정부 자문위원회 6월 하위법령 초안 직전 *AI safety 조항 강화 권고서*를 5페이지로 작성하라" (O)

### 2. 컨텍스트 specificity
- 사용자 *현재 활동·자원·우선순위* 반영
- Generic 권고 X
- 예: "마케팅 강화" (X) → "사용자가 운영하는 [기관·역할]에서 본 issue를 [구체적 channel·timeline]로 전파" (O)

### 3. Time-bound
- *언제까지·얼마나*
- 모호한 timing X

### 4. Connection to other items
- 다른 Item·Issue와의 연결 명시 (Issue ID 활용)

### 5. Confidence·uncertainty 명시
- *추정·가정* 부분 명시
- 외부 변수 의존 명시

## 10 Default 도메인 — 작성 Protocol

### Domain 1 — 정부·정책 (Policy Implications)

#### 적용 사용자 예
- 정부 부처 공무원·자문위원
- 국회의원·보좌관
- 정책 연구원 (KIEP·KDI·STEPI 등)
- 외교관
- 국제기구 (UN·OECD) 직원

#### Implication 작성 5 angle
1. **법제·규제 형성** — 본 issue 응답 입법·시행령·시행규칙
2. **정책 옵션 평가** — 다양한 정책 시나리오 비교
3. **국제 비교** — 다른 국가의 정책 reference
4. **자문 활동 기여 지점** — 사용자가 영향력 행사 가능한 정확한 시점·channel
5. **정책 형성 윈도우** — Critical timing (예: "6월 하위법령 초안 직전")

#### 사례 (AGI issue)
> 본 issue 응답 정책 옵션: ① AI Safety Framework 강화 (EU AI Act benchmark), ② 노동시장 충격 대응 universal basic income 시범, ③ 청년 진로 paradigm shift 교육 정책 개혁. 정책 형성 critical 시점: 한국 AI 기본법 6월 하위법령 초안. 사용자가 자문위원 자격으로 *외부 expert essay* 5페이지 기여 권고 (시행령 *transparency·explainability* 조항 강화). 국제 reference: EU AI Act Annex III·US Executive Order 14110.

### Domain 2 — 기업·경영 (Business Implications)

#### 적용 사용자 예
- 기업 CEO·CXO·임원
- 전략 기획 매니저
- 경영 컨설턴트 (BCG·McKinsey·Bain)
- 신사업 개발 팀
- M&A·기업 가치평가

#### Implication 작성 5 angle
1. **산업·시장 영향** — 업계 구조·경쟁 환경 변동
2. **신사업 기회** — 본 issue가 열어주는 시장
3. **방어 시나리오** — 본 issue의 위협으로부터 보호
4. **인력 전략** — 채용·교육·재배치
5. **M&A·파트너십** — 인수·합병·전략 제휴 기회

#### 사례 (AGI issue)
> 한국 SI/SW 업계 (LG CNS·삼성SDS·SK C&C) 매출·이익 모델 *근본 위협* — 인력 기반 매출이 AI agentic deployment에 침식. 신사업 기회: ① AI Native 컨설팅 transition (사람 + AI hybrid model), ② 클라이언트 기업 AI transformation 컨설팅, ③ 한국형 vertical LLM (의료·법률·금융) 개발. 인력 전략: 신입 채용 50% 축소 + 시니어 재교육 (AI 제어·prompt engineering·domain expertise). M&A: AI startup 인수 (KAIST/서울대 spin-off 우선).

### Domain 3 — 학계·연구 (Academic Implications)

#### 적용 사용자 예
- 대학 교수·연구원
- 학술 연구소 (KIST·KIAS) 연구원
- 박사·박사후 연구원
- 학술지 편집자
- 학회 임원

#### Implication 작성 5 angle
1. **연구 questions** — 본 issue가 열어주는 미해결 학술 질문
2. **Publication 우선순위** — 어떤 논문·저널·학회 발표가 우위
3. **학제 간 협력** — 다른 분야와의 cross-disciplinary 가능성
4. **Funding 기회** — 정부·민간·해외 연구비 trend
5. **학회·세미나** — 발표·organize 기회

#### 사례 (AGI issue)
> 본 issue 관련 미해결 학술 questions: ① AGI labor displacement의 *macro-economic* 모델링 (Acemoglu framework 한국 적용), ② Korean 청년 22~25세 cohort *longitudinal* 추적, ③ 한국 AI Basic Act 시행 1년차 *empirical effectiveness* 평가. Publication 우선순위: *Nature Human Behaviour* (사회 영향), *Journal of Economic Perspectives* (거시), *Korea Journal of Sociology* (한국 사회). 학제 간: 경제학+사회학+공학+윤리학 4-way 협력. Funding: 과기정통부 AI 정책 R&D 신규 트랙 + NRF 학제 융합 연구.

### Domain 4 — 미디어·언론 (Media Implications)

#### 적용 사용자 예
- 신문·방송 기자
- 다큐멘터리 PD
- 칼럼니스트
- 미디어 데스크·편집장
- 유튜버·뉴스레터 작가

#### Implication 작성 5 angle
1. **보도 프레임** — 본 issue를 어떤 angle로 보도
2. **취재원 추천** — 인터뷰할 핵심 인물·기관
3. **기획 기사·다큐 시리즈** — 6~12편 시리즈 plan
4. **시각 자료** — 차트·infographic·시뮬레이션 video
5. **관점 다양성** — 한 시각만 강조 회피, multi-perspective

#### 사례 (AGI issue)
> 보도 프레임: "AGI가 한국에 *왜 다른 나라보다 먼저* 도착하는가" — 한국 디지털 인프라·영어 능력·인구 압력의 결합. 취재원: Anthropic Korea·OpenAI·KAIST 김대식·서울대 장병탁·잡코리아·한국노동연구원·청년 당사자 5명. 기획 시리즈 12편: ①AGI 시간표 ②한국 청년 첫 충격 사례 ③글로벌 비교 ④ 정책 응답 ⑤가족 경제 ⑥교육·진로 ⑦정신건강 ⑧의미 위기 ⑨에너지 인프라 ⑩통일 시나리오 ⑪한국 AI 주권 ⑫Long-term 시나리오. 관점 다양성: 기술낙관·기술회의·노동·자본·청년·세대·진보·보수.

### Domain 5 — 교육·학습 (Education Implications)

#### 적용 사용자 예
- 초·중·고등학교 교사
- 대학 교수 (교육 측면)
- 평생학습 강사
- 교육 정책 입안자
- 학원·인강 운영자
- 교육 콘텐츠 개발자

#### Implication 작성 5 angle
1. **커리큘럼 변경** — 어떤 과목·주제 추가·축소
2. **교육 program 신설** — 새 강좌·프로그램
3. **평생학습 trend** — 성인 교육 시장 응답
4. **학생 진로 가이드** — 학부모·학생에게 권고
5. **교사·강사 역량** — 본인 역량 transition

#### 사례 (AGI issue)
> 커리큘럼: 고등학교 *AI literacy* 의무 추가 + *진로 paradigm* (대졸 화이트칼라 신화 해체) 통합. 대학: AI · 인문 · 윤리 dual-major 프로그램 신설. 평생학습 trend: 30~50대 전직·재교육 시장 폭발 — *AI 협업 workflow 마스터* 코스 가치. 학생 진로: 부모와 학생에게 "기술 + 의미·관계·창의" 결합 직군 추천 (ex 정신건강·돌봄·창작·물리 장인). 교사 역량: AI를 *교사 보조*로 받아들이는 새 페다고지 마스터.

### Domain 6 — 종교·목회 (Pastoral / Religious Implications)

#### 적용 사용자 예
- 신학 교수
- 신부·승려·이맘 등
- 종교 미디어 운영자
- 종교 NGO 활동가

#### Implication 작성 5 angle
1. **설교·메시지 시리즈** — 본 issue를 신학적으로 해석
2. **사역 program** — 청년·가정·소그룹·교육 사역 응답
3. **종교 공동체 결정** — 당회·대표자 회의 안건
4. **외부 사역** — 교계·신학교·국제 협력
5. **신학적 framework** — 전통 vs 현대의 응답

#### 사례 (AGI issue)
> 설교 시리즈: *Imago Dei in the Age of AGI* 8주 (시편 8·139편 + 창세기 1·2 + 요한복음 1·14). 사역 program: 청년 사역 *AI 시대 정체성·소명* 6주 + 가정 사역 *자녀 진로 paradigm shift* 워크숍 + 시니어 *AI 시대 의미* study. 당회: 5년 사역 paradigm shift 결의 — *공동체·의미·영성*이 AGI 시대 교회의 unique value. 외부 사역: 교계 협력 *한국 교회의 AGI 응답* study group + 신학교 *AI 시대 신학* 강의 contribution. 신학적: imago Dei가 *기능 (인지)*인가 *관계 (소속)*인가 — 후자 강조.

### Domain 7 — 금융·투자 (Investment Implications)

#### 적용 사용자 예
- 자산운용사 펀드매니저
- 증권사 strategist·analyst
- 개인 투자자
- VC·PE 임원
- 가족 자산 관리

#### Implication 작성 5 angle
1. **Asset allocation** — 자산 클래스별 비중
2. **섹터·종목** — 특정 산업·기업 매수·매도
3. **지역 분산** — 국내·미국·일본·유럽·신흥국
4. **Hedge·risk** — 특정 시나리오 대비
5. **Time horizon** — 단기·중기·장기 strategy 분기

#### 사례 (AGI issue)
> Asset allocation: 주식 비중 60→55%, AI infrastructure 노출 30%로 집중. 섹터·종목: NVIDIA·AMD·Broadcom·SMCI (AI chip) + Microsoft·Alphabet (AI service) + 한수원·두산에너빌리티 (SMR) + 삼성SDI·LG에너지솔루션 (배터리) + 한국 SI 업계 (LG CNS·삼성SDS) 비중 점진 축소. 지역: 미국 50%·한국 30%·일본 10%·기타 10%. Hedge: 변동성 cash 15% + 금 5%. Time horizon: 단기 (1y) 변동성 대응, 중기 (5y) AGI 가속 thesis, 장기 (10y) 인구·자동화 동시 변곡 시나리오.

### Domain 8 — 비영리·시민사회 (Civic / Nonprofit Implications)

#### 적용 사용자 예
- NGO 활동가
- 시민사회 단체 임원
- 사회적 기업가
- 자선재단 임원
- 사회운동가

#### Implication 작성 5 angle
1. **시민운동 의제** — 본 issue가 만드는 새 시민 의제
2. **NGO 활동 영역** — advocacy·교육·서비스·연대
3. **펀딩·파트너십** — 재단·기업·정부 협력
4. **국제 연대** — 유사 issue 해외 NGO와의 협력
5. **공익·취약계층 영향** — 소외 집단 대응

#### 사례 (AGI issue)
> 시민운동 의제: ① AI 노동 윤리 (자동화 충격 받는 청년·중장년 권리), ② AI 거버넌스 시민 참여 (AI 기본법 하위법령 시민의견 입력), ③ AI 디지털 격차 해소 (취약계층 AI literacy). NGO 활동: advocacy (정부 정책에 시민 input), 교육 (청년 AI literacy bootcamp), 서비스 (AI 활용 정신건강 지원). 펀딩: Google.org·OpenAI·정부 사회혁신기금 + 해외 (Open Philanthropy·Future of Life Institute). 국제 연대: AI Now Institute·Algorithm Justice League. 취약계층: 청년 무직·고령 실직자·이주민·장애인 AGI 충격 모니터링.

### Domain 9 — 개인·생애설계 (Personal / Life Implications)

#### 적용 사용자 예
- 일반 직장인 (본인·가족 미래 고민)
- 대학생·청년 (진로 고민)
- 학부모
- 은퇴 준비자
- 창업 고민 중인 개인

#### Implication 작성 5 angle
1. **진로·커리어** — 본인 직업의 future-proofing
2. **가족 의사결정** — 자녀 교육·결혼·출산
3. **재정·자산** — 본인 portfolio·소비·저축
4. **건강·정신건강** — 변화 대응 stress
5. **생애 의미·가치** — 변화 속 자기 정체성

#### 사례 (AGI issue)
> 진로: 본인 직업이 AGI 침투 high·medium·low인지 *2년 내* 평가, 침투 high면 *재교육 또는 transition*. 가족: 자녀에게 *대졸 화이트칼라 안정 일자리* 신화 해체 — 다양한 진로 (기술 + 인문, 창의, 영성, 물리 장인) 격려. 재정: 가족 emergency fund 6개월→9개월 확대 (소득 변동 대비) + 본인·배우자 *상호 보완 직군* (한 명이 AGI 노출 high면 다른 한 명은 low). 건강: 정신건강 monitoring 강화. 의미: *직업=정체성* 한국식 패러다임 의문 — *공동체·관계·창작·봉사*에서 의미 재발견.

### Domain 10 — Custom (사용자 정의)

#### 적용
사용자가 위 9개에 안 맞는 *본인 고유 영역* 정의:
- "한국 농업 협동조합 운영자"
- "원전 운영사 안전 관리자"
- "청소년 상담사"
- "한국 가나안 성도 사역자"
- "K-pop 아이돌 매니지먼트"
- "한국 스타트업 창업자 모임 (Y Combinator 동문)"
- "지방자치단체 미래 전략실"
- 등 무제한

#### 작성 protocol
사용자가 입력한 컨텍스트 1~3 문장에서 다음 자동 추출:
1. **사용자의 *역할·직위·기관*** (예: 운영자·관리자·상담사·사역자)
2. ***책임·미션*** (예: 조합원 이익·사고 방지·청소년 정신건강)
3. **사용자의 *의사결정 권한 범위*** (조합 사업 선택·안전 protocol·상담 program 등)
4. **사용자의 *제약·자원*** (예산·인력·시간·관계망)

→ 이 4 변수를 토대로 *해당 컨텍스트에 정확히 맞춘* implications 생성.

#### 사례 (Custom: "한국 농업 협동조합 운영자" + AGI issue)
> 본 issue가 농업 협동조합 운영에 미치는 영향: ① 조합원 가정의 자녀 (도시 화이트칼라 진로) 진로 paradigm shift → 조합원 가족이 *농업 후계*에 다시 관심 가능성, ② 농업 자체가 AGI 시대 *AI 침투 어려운 영역* (물리 + 자연 의존)으로 가치 재평가, ③ 스마트팜 기술이 AGI agentic 능력으로 더 진화. 운영자 행동 권고: ① 조합원·청년 농업 후계자 program 강화 (도시 청년 *역귀촌* trend 흡수), ② 협동조합 6차 산업 (스마트팜 + 가공 + 콘텐츠) 신사업, ③ 정부 농업 정책에 AI 시대 농업 가치 *advocacy*, ④ 조합원 정신건강·세대 전환 cohort 지원.

## Generic Universal Implications (사용자 skip 시 fallback)

대표 스킬 Step 1-A에서 사용자가 *skip*한 경우 — 어떤 사용자에게도 보편적 의미가 있는 3 implications:

### Decision-makers Implications
- 본 issue가 *어떤 결정*을 *언제까지* 요구하는가
- 의사결정의 *비용·이익·리스크* 비교
- *No-regret moves* — 어떤 시나리오에서도 후회 없는 행동

### Stakeholders Implications
- 본 issue로 영향 받는 *주요 stakeholder들*
- 각 stakeholder의 *입장·이해관계*
- Stakeholder 간 *갈등·협력 가능성*

### Long-term Watchers Implications
- 본 issue의 *5y·10y·20y* trajectory
- *Trigger events* — 시나리오 변경 신호
- *Wild cards* — Low prob × high impact 가능성

→ Generic universal implications는 *모든 사용자에게 의미*는 있지만, *깊이는 도메인 특화 implications보다 낮음*. 사용자는 *명시적 도메인 선택* 권고.

## Multi-domain 통합 패턴

### Pattern 1 — Cross-domain *공통* implications
한 issue가 N개 도메인 모두에 implications. 예: AGI는 정부+기업+학계+미디어+교육+종교+금융+비영리+개인 모두에 영향. → AI Report Editor가 *각 도메인별 implications 작성하면서 공통 underlying dynamic 식별*.

### Pattern 2 — *상충* implications
한 issue가 도메인별로 *상반된* 응답 요구. 예: AI 거버넌스 — 정부 (강한 규제) vs 기업 (혁신 우위) vs 학계 (연구 자유) vs 시민사회 (안전·평등). → AI Report Editor가 *상충 명시 + 사용자가 어떤 도메인 우위로 결정할지 자료* 제공.

### Pattern 3 — *시너지* implications
한 도메인 응답이 다른 도메인을 강화. 예: 정부 정책 강화 → 기업 적응 → 학계 연구 활성화 → 미디어 보도 확장 → 시민 인식 격상. → AI Report Editor가 *cascade 시너지 chain 자동 visualization*.

### Pattern 4 — *Time-staggered* implications
도메인별로 *다른 timing*. 예: AGI — 미디어 (즉시 보도), 정부 (6개월 정책), 기업 (1년 전략), 학계 (3년 연구), 교육 (5년 커리큘럼), 종교 (10년 신학 정립). → AI Report Editor가 *timing 매트릭스* 자동 생성.

→ 사용자가 N개 도메인 동시 선택 시 위 4 패턴 자동 적용으로 cross-pattern 식별 가치.
