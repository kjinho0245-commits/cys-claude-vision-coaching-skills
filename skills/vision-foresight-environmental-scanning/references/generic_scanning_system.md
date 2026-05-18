# Generic Futures Scanning System — 상세 도식·운영

> Gordon & Glenn (2009) Section II + Kuwait Oil Company (KOC) Early Warning System 실제 사례

## 도식 (PDF 원본)

```
┌─────────────────────────────────────────────────────────────────┐
│              GENERIC FUTURES SCANNING SYSTEM                    │
└─────────────────────────────────────────────────────────────────┘

[Sources Layer — 5 갈래 입력]
  ┌─────────────┬───────────┬───────────┬──────────────┬──────────────┐
  │Press        │Monitor    │Key Word   │Conferences  │Key Persons   │
  │Releases     │Specific   │Internet   │Seminars     │Tracking      │
  │Newsletters  │Websites   │Searching  │             │              │
  │Journals     │           │           │             │              │
  └──────┬──────┴─────┬─────┴─────┬─────┴──────┬──────┴──────┬───────┘
         └────────────┴───────────┴────────────┴─────────────┘
                                  │
                                  ▼
                          ┌──────────────┐
                          │   SCANNING   │  (Staff layer)
                          └──────┬───────┘
                                 │
                                 ▼
                  ┌───────────────────────────────┐
                  │     Analysis & Synthesis      │
                  │ Individual ↔ Staff ↔ Mgmt     │  (3-tier)
                  └─────────────┬─────────────────┘
                                │
                                ▼
                  ┌───────────────────────────────┐
                  │   Collective Intelligence     │
                  │           System              │  (DB·SW·HW·Experts)
                  └─────────────┬─────────────────┘
                                │
                                ▼
                  ┌───────────────────────────────┐
                  │         Management            │ ──► Decisions
                  │                               │ ──► Future-oriented
                  └─────────────┬─────────────────┘     understanding
                                │                       & learning
                                │
                       Feedback & New Requirements
                                │
                                └───────► (back to Scanning)
```

## 5 Input Sources 상세

### 1. Press Releases / Newsletters / Journals
- 정부·기업·NGO 보도자료 (특정 기관 ≥10개 follow)
- 산업 trade press, 학회 newsletter
- 정기 학술 저널 (Nature, Science, NEJM 등 톱티어 + 분야별 핵심 5~10개)

### 2. Monitor Specific Websites
- "best ones for your interests" — 본인 분야의 *권위 사이트* 목록 작성
- 정부 웹사이트 (whitehouse.gov, EU Commission, UN agencies)
- 싱크탱크 (RAND, Brookings, Chatham House, Pew Research, KIEP, KDI)
- 업계 권위자 블로그·뉴스레터

### 3. Keyword Internet Searching
- **Google Alerts** (googlealert.com) — 사전 선정 keyword를 매일 검색·이메일 전송
- **Web Crawlers** — 새 버전 자동 탐지로 early warning
- 일반 검색 엔진: Google, Vivisimo, Grokker, ixquick.com
- 전문 포털: usa.gov (정부 정보), findlaw.com (법률)
- Search Engine Watch (searchenginewatch.com) — 검색 기법 자체 학습

### 4. Conferences & Seminars
- 분야별 주요 컨퍼런스 연중 일정 추적
- streaming/archived video 모니터링
- 사회자·기조연설자가 *trend setter*인 경우 별도 트래킹

### 5. Key Persons Tracking
- "Scanning the scanners is efficient" — 자기 분야 최고 trend 추적자를 한 단계 거쳐 모니터링
- 그들의 newsletter·website·SNS·논문·강연 follow
- 5개 분야 → 분야별 1~3명 key scanner 식별

## Analysis & Synthesis 3-tier

### Individual layer
- 개별 staff 또는 외부 panelist가 1차 *raw signal* 입력
- "Each piece of information or record" 형식으로 표준화 (vision-foresight-environmental-scanning-weak-signal-template로 위임)

### Staff layer
- Scanning team이 individual 입력을 cross-check, 중복 제거, 분류
- *pattern* 식별 (필드별 keyword 검색)
- "headlines for new items" 이메일로 관리자에게 푸시

### Management layer
- 의사결정자가 headline 클릭 → full item → 코멘트 추가 가능
- "should be part of the monthly meeting" / "has been countered by some other development" 같은 메타 판단

## Collective Intelligence System 운영

### 4 modes of operation (PDF Section IV에서 GEN 사례)

1. **Discussion** of important issues and associated decisions
2. **Collaboration** to produce distilled information and ratings for priority listings
3. **Identifying degree of expert consensus** — and where there is none, identifying the range of views and pending issues
4. **Linking on-call experts** for *just-in-time knowledge requirements* (실시간 의사결정 지원)

### 핵심 원칙

> "It is not a normative system, but one that could be used by others to create normative positions. It can be thought of as a federation (collection) of all (known/knowable) world views from which **social sensemaking is facilitated.**"

— *이념적으로 중립*, 모든 알려진/알 수 있는 세계관의 federation, social sensemaking을 facilitate.

## Management Layer

### Output 2가지

1. **Decisions** — 직접 의사결정에 활용
2. **Future-oriented understanding and learning** — 조직 학습 자체가 산출

### 의사결정 직전 워크플로우

- 관리자에게 *summary page* 제공 (헤드라인 + 한 줄 요약 by category)
- 또는 *latest scanning items* 페이지
- 또는 이메일 헤드라인 (request 시)

## Feedback & New Requirements (가장 중요)

### Gordon의 강조

> "If information just flows unidirectionally through the system, without management feedback, then the system **does not 'learn' how to perform better** and produce the most cogent knowledge, while avoiding information overload."

### 피드백 메커니즘 5가지 (구현 권고)

1. 관리자가 item에 *코멘트 추가* — "이건 우리 monthly meeting에 올려라" / "이건 X 사건으로 이미 무력화됐다"
2. 관리자가 *새 keyword 요청* — 다음 사이클부터 추가 스캔
3. 관리자가 *priority 조정* — 어떤 도메인을 더/덜 스캔할지
4. 관리자가 *false positive 표시* — 시스템 학습에 활용
5. 관리자 결정의 *결과 추적* — 실제 무엇이 일어났는지 → 시스템 정확도 평가

## KOC 실제 운영 사례 (Appendix A 요약)

### 시나리오: Heavy Crude and Microorganisms

**Step 1 — Routine scan**: KOC scanning team이 과학기술 문헌 정기 스캔 중, John Coates (Southern Illinois University) 팀의 논문 발견 — Dechloromonas 균주가 oxygen 없이 benzene 분해 가능

**Step 2 — Pattern analysis**: Scanner가 *기존 펌핑 불가 깊이의 잔류 heavy crude*에 적용 가능성 추론. Strain RCB는 perchlorate를 oxygen 대체로 사용, Strain JJ는 nitrate 사용 → 잔류 oil에 nitrate 첨가 시 생물학적 viscosity 저하 가능

**Step 3 — Manager 판단**: Scanning manager에게 보고. KPC와 조정 후 *intensified search* 승인. Patent literature 검색 — 미발급 확인. Company chemists가 insight 검증.

**Step 4 — Action**: Southern Illinois University와 technology transfer contract 협상. Funding 확정.

**Step 5 — Strategy 변경**:
- Wells previously thought depleted → potentially useful → reserves 증가
- Microorganism 대량 생산 사업 진출 가능성
- Patent licensing royalties
- PR benefit (환경친화적 기업 이미지)

### 핵심 교훈

- *Routine scan*이 *single article*에서 시작
- 그러나 *pattern recognition* (잔류 oil + 무산소 박테리아 + nitrate 풍부)이 weak signal을 *전략적 기회*로 변환
- *Feedback loop* 작동: scanner의 insight → manager → KPC → 외부 협상 → 전략 변경 → 새 scanning requirements (관련 균주·특허 추가 추적)

## 한국 컨텍스트 적용


| Layer | 한국 교회 컨텍스트 |
|---|---|
| Sources | 기독교계 매체 (국민일보·뉴스앤조이·기독신문·CTS), 신학 저널, 통계청 인구·종교 데이터, 한국 갤럽·한국기독교목회자협의회 정기조사, 외국 evangelical 트렌드 (Lifeway·Barna) |
| Scanning | 사역자 + 평신도 자원봉사 panel |
| CI | 박사님 미래학 자문 + 지역사회 데이터 |
| Management | 당회 → 결정 + 5년 사역 계획 |
| Feedback | 분기 사역 회고 → 새 스캐닝 요구사항 |

### 미래학 연구소 (아시아미래인재연구소) 환경 스캐닝 시스템

| Layer | 컨텍스트 |
|---|---|
| Sources | 글로벌 9 도메인 + 국내 KIEP·KDI·KISTI·STEPI 보고서 + 박사님 강의·자문 입력 채널 |
| Scanning | 박사님 + 연구원 + 외부 expert panel (50~75명) |
| Analysis | 박사님 + 시니어 연구원 + 자문위원 |
| CI | MCEWS·deep research workflow + 박사님 cmux 워커 시스템 |
| Management | 박사님 → 단행본·강의·자문 산출 |
| Feedback | 강의 청중 반응·자문 결과·단행본 판매·학계 수용 → 새 스캐닝 |

### 금융 투자 환경 스캐닝 시스템

| Layer | 컨텍스트 |
|---|---|
| Sources | Bloomberg·Reuters·WSJ·Financial Times + 한국경제·매경 + Federal Reserve·BOK 보고서 + 거시경제 지표 + 산업별 trade press |
| Scanning | 박사님 + 투자 자문 동료 |
| Analysis | 거시 → 산업 → 종목 3-tier |
| CI | MCEWS 시스템 + 차트 분석 + 외부 strategist 의견 |
| Management | 포트폴리오 의사결정 |
| Feedback | 실제 투자 성과 → 시스템 calibration |
