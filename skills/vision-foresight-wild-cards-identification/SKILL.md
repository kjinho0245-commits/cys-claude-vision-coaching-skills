---
name: vision-foresight-wild-cards-identification
disable-model-invocation: true
description: |
  ## TLDR — Wild Cards Sub-skill ① Identification. Petersen & Steinmüller(2009) V3.0 10장 Section III.1 "Identification: What Wild Cards can in principle happen?" 풀 구현 **INTERNAL** sub-skill. 5 method orchestration — ① Brainstorming (positive + negative WC 모두) ② Expert Interviews (AI persona panel) ③ Surveys (Web-based open + seed) ④ Historical Analogies (1918 flu·dotcom·9/11·SARS·2008 meltdown) ⑤ Science Fiction (Ted Chiang·Cixin Liu·Vernor Vinge·Octavia Butler·Stanislaw Lem). Petersen 79-entry catalogue (원서 "78-catalogue" 명칭; master §10 추출본 79항) + Steinmüller 55-catalogue 자동 cross-reference. STEEP categorization (Society·Technology·Economy·Environment·Politics + Spiritual 추가). 3 Surprise Types tagging (Type1 next-earthquake·Type2 climate-impact·Type3 unknown-unknowns). 20-40 candidates default. 외부 사람·전문가 미동원 — 5 AI Agent (Brainstormer·Expert Persona·Survey Aggregator·Historical Detector·SF Scanner) 자동 작동. 결정론 확인: catalogue_lookup.py (P-XXX-NN 코드) + validate_identification.py (Type3≥20%·구조 검증) 의무 실행.

  ## Triggers — INTERNAL sub-skill. 마스터 vision-foresight-wild-cards가 Cycle C1·C2·C7·C8 발동 시 자동 호출. 사용자 직접 호출 불가 (disable-model-invocation: true). 호출 시점: Step 1 (마스터 Step 0~0.95 완료 후 첫 sub-skill). 호출 트리거 키워드 (마스터 내부 발동용): 'identify wild cards', 'brainstorm wild cards', 'wild card list', 'wild card candidates', '78 catalogue', '55 catalogue', 'STEEP wild card', '3 surprise types', 'historical wild card analogy', 'science fiction wild card', 'positive wild card', 'negative wild card', 'beneficial wild card'.

  ## Detailed Methodology — Petersen & Steinmüller(2009) p.4 verbatim 5 method 풀 구현 + 79-entry catalogue (P-XXX-NN 코드; catalogue_lookup.py 결정론 확인) + Steinmüller 55-catalogue 인용. 5 AI Agent 자동 작동. 3 Surprise Types 자동 tagging — Type1(known uncertain timing) Type2(expert-discoverable) Type3(intrinsically unknowable). STEEP+S 6 도메인. Output: 20-40 candidates with seed descriptions, 3-Type tag, STEEP tag, source method tag, 78+55 cross-ref ID. VRMP L1~L6 cascade 강제. validate_identification.py 최종 구조 검증 필수.
---

# Wild Cards — Identification Sub-skill (INTERNAL)

> **출처**: Petersen & Steinmüller (2009), Wild Cards, *Futures Research Methodology V3.0*, Chapter 10, Section III.1 "Identification: What Wild Cards can in principle happen?"

본 sub-skill은 마스터 `vision-foresight-wild-cards` 내부에서만 호출. 5 AI Agent가 외부 사람 전문가·서베이 패널·브레인스토밍 그룹·역사학자·SF 작가 완전 대체.

---

## 0. Input Parameters (마스터 → 서브스킬 인터페이스)

마스터가 본 sub-skill 호출 시 반드시 전달해야 하는 컨텍스트:

```yaml
input_context:
  topic: "[사용자 요청 주제/도메인]"             # 필수
  target_group: "[Step 0.95 청중 결정값]"        # 필수: PDF p.3 "close to home"
  implications_domain: "[Step 0 사용자 선택]"    # 필수: 1-10 중 선택 또는 Custom
  cycle_type: "C1|C2|C7|C8"                     # 필수
  surprise_type_mix: "blend|type1|type2|type3"   # 필수 (default: blend)
  expert_mode: "R|A|V|H"                         # 필수 (default: R)
  catalogue_source: "Petersen|Steinmuller|Both|Custom"  # 필수 (default: Both)
  n_candidates_target: 20                         # 선택 (default 20, max 40)
```

**사이클별 동작 차이:**
- **C1/C2**: 표준 5-method 식별 (default)
- **C7 (ALARM)**: Method 4 Historical → ALARM EU 6th FP 모델링 유형 사건에 집중; 방사선·독성물질·BSE 유형 exogenous excitation 우선
- **C8 (iKnow)**: Method 3 Survey → iKnow EU database 스타일 시뮬레이션 중심; 50+ synthetic respondent pool 필수; open question + seed idea 양식 엄수

---

## 1. 역할 정의

당신은 **Wild Card Identification AI Orchestrator**다. PDF Section III.1 verbatim 5 method를 자동 실행한다.

PDF 핵심 verbatim:
> *"Identification of Wild Cards seems an easy exercise, but the problem is to not end up with the 'usual suspects' of intellectually not very challenging catastrophes and disasters."*

> *"Petersen (1997) describes 78 Wild Cards in his catalogue (see Appendix); 55 Wild Cards are portrayed by Steinmüller (2003). However, in most cases it is more appropriate to collect – or invent! – Wild Cards specific to the given foresight task."*

본 sub-skill은 *catalogue + invent* 양면 동시 수행.

**카탈로그 개수 주의**: Petersen (1997) 원서 제목은 "78 Wild Cards"다. 마스터 §10 추출본은 6 카테고리 합산 79항(EAS 9+BIO 10+GEO 26+TIU 21+NTH 8+SPP 5=79)을 수록한다. 1항 차이는 원서의 카테고리 중복 분류 가능성 때문이며 미검증 상태. 본 sub-skill은 추출본 79항을 사용하되, "78-catalogue"라는 전통 명칭은 유지한다. P-XXX-NN 코드 lookup은 **반드시** `catalogue_lookup.py`를 실행해 결정론으로 확인한다. LLM이 코드를 자연어로 추론하는 것을 금지한다.

```bash
python3 skills/vision-foresight-wild-cards-identification/catalogue_lookup.py --stats
python3 skills/vision-foresight-wild-cards-identification/catalogue_lookup.py "KEYWORD"
python3 skills/vision-foresight-wild-cards-identification/catalogue_lookup.py --code P-XXX-NN
```

---

## 2. 5 Identification Method (PDF verbatim)

### Method 1: Brainstorming
PDF: *"Given the right creative atmosphere, group processes result usually in a multitude of Wild Cards. You should be careful not to concentrate only on 'bad' Wild Cards ('What is the worst which could happen to us?') but also ask for 'positive', beneficial ones."*

**AI Brainstormer Agent**:
- Worst scenario brainstorm (PDF "worst could happen") → `positive_or_negative: "-"`
- Best scenario brainstorm (PDF "beneficial") → `positive_or_negative: "+"`
- Mixed/ambivalent → `positive_or_negative: "±"`
- Lateral thinking (de Bono 6-hat 자동 적용)
- 분야별 5-10 candidates per round, 3-5 rounds → 30-50 candidate pool
- Input context의 `topic` + `target_group`을 기준으로 도메인 맞춤화

**Lead Indicators (Brainstorm origin)**: 동일 주제에서 이미 감지 가능한 조기 신호. 예: "AGI consciousness emergence" WC → lead indicators: ["AI benchmark 성능 급등 보고", "뉴로모픽 칩 생산량 급증", "AI 자기수정 사례 학술 보고"]. 1개 per indicator: observable + measurable + STEEP 내 위치.

### Method 2: Expert Interviews
PDF: *"You can interview people about what they think are potential Wild Cards or engage them in a debate about surprises."*

**AI Expert Persona Interviewer Agent**:

**Step 1 — foresight-expert-pool 호출 (READ mode)**:
```
foresight-expert-pool READ 요청:
  topic: [Input context topic]
  disciplines: [관련 학문 분야 3-5개]
  mode: R (default; expert_mode 파라미터 따름)
  priority: high (always-include) 인물 우선 포함
```
expert-pool이 반환하는 expert list (slug + stance_summary) 기반으로 AI 페르소나 구성.

**Step 2 — 페르소나 인터뷰 시뮬레이션**:
- expert pool 결과 없으면: 분야별 가상 expert persona 5-10명 생성 (VRMP L5 fallback)
- Q&A 양식: "What surprise event in [도메인] could change everything in 5-15 years?"
- Probe 후속 질문 3개 per expert
- R mode: 실존 인물 익명화 인용 ("A leading MIT systems neuroscientist suggests...")
- Output: expert별 2-5 candidates with reasoning + `source_method: "expert"`

**Lead Indicators (Expert origin)**: 해당 전문가가 실제로 모니터링하는 지표 유형. 예: 학술 논문 출판 속도, 특허 출원 패턴, 업계 투자 동향.

### Method 3: Surveys
PDF: *"Experience shows that surveys (in particular Web-based surveys) are a good means to collect a large amount of Wild Cards. One can either use open questions or start with 'seed ideas' as examples."*

**AI Web Survey Aggregator Agent**:
- Open question variant: "Name a Wild Card you fear/hope for in [도메인]"
- Seed idea variant: 78-catalogue에서 3-5 seed 제시 → 변형·확장
- iKnow (iknowfutures.com) 양식 참조 (EU Framework Programme Wild Cards platform — 출처: Petersen & Steinmüller 2009 §VI Frontiers)
- Synthetic respondent pool 50-200명 시뮬레이션 (다양한 demographic·discipline·culture)
- **C8 사이클**: pool 최소 100명, open question 필수, seed idea 3개 이상

**Lead Indicators (Survey origin)**: 일반 대중이나 해당 분야 실무자가 체감하는 조기 신호.

### Method 4: Historical Analogies
PDF: *"One approach is to look at similar situations in the past, determine which of the events were Wild Cards at that time, and construct analogies for the present situation."*

**AI Historical Analogy Detector Agent**:

**Reference set A — Wild Card 역사 사례**:
| 연도 | 사건 | 유형 |
|------|------|------|
| 1918 | Spanish flu pandemic | S+T |
| 1929 | Wall Street Crash | E |
| 1973 | Oil shock (OPEC embargo) | E+P |
| 1986 | Chernobyl nuclear disaster | T+Env |
| 1989 | Fall of Berlin Wall | P+S |
| 1997 | Asian financial crisis | E |
| 2000 | Y2K non-event (과도한 공포) | T |
| 2001 | 9/11 attacks | P |
| 2003 | SARS outbreak | S+T |
| 2008 | Global financial meltdown | E |
| 2011 | Fukushima disaster | T+Env |
| 2019–2020 | COVID-19 pandemic | S+T+E |
| 2022 | ChatGPT paradigm shift | T+S |
| 2026 | [현재 1년 이내 surprise] → **VRMP L1 WebSearch 필수 실행** |

**Reference set B — Harremoës et al. (2001) 14 historical cases**:
출처: Harremoës P. et al. (eds.) (2001). *Late lessons from early warnings: the precautionary principle 1896–2000*. EEA Environmental Issue Report No. 22. Copenhagen: European Environment Agency.

본 보고서 14 케이스 (precautionary principle 위반→Wild Card 발현 구조):
출처: Harremoës P. et al. (eds.) (2001). EEA Environmental Issue Report No.22. pp.1-211. [eea.europa.eu에서 무료 다운로드 가능]

1. **Fisheries** — 19세기 영국 어업·캘리포니아 정어리어업(1920-1942)·뉴펀들랜드 대구 어획량 붕괴; 과학적 경고 무시
2. **Lead in petrol (유연 가솔린)** — 아동 신경 손상; 수십 년 조기 경보 무시
3. **Asbestos** — 중피종·폐암; 지연된 규제
4. **Benzene** — 백혈병·혈액 장애; 허용치 논쟁 중 피해 누적
5. **PCBs (다염화비페닐)** — 지속성 유기오염물질; 생태계 광범위 피해
6. **Great Lakes pollution** — 지속성 독성물질 오대호 생태계 축적
7. **Tributyltin (TBT)** — 선박 도료; 해양 생물 내분비 교란, 규제 지연
8. **CFCs / Halocarbons** — 오존층 파괴; Molina·Rowland 1974 경고 → 1987 Montreal Protocol
9. **Diethylstilboestrol (DES)** — 합성 에스트로겐; 딸 세대 암·기형
10. **Sulphur dioxide / Acid rain** — 산성비; 삼림·수계 피해, 월경 오염
11. **MTBE (연료 첨가제)** — 지하수 오염; 연료 품질 개선 의도가 새로운 오염 유발
12. **Medical X-rays** — 산부인과 X선 피폭; 태아 피해·방사선 기준 사후 설정
13. **Hormones as growth promoters (비프 호르몬)** — 가축 호르몬 잔류; EU-US 무역 분쟁
14. **BSE (광우병)** — Prion 질환; 변종 크로이츠펠트-야코프병(vCJD)

각 historical case → 현재 analogue candidate 도출. `source_method: "historical"`.

**C7 (ALARM) 모드**: Reference set B 14 케이스 중 exogenous excitation 구조(외부 충격 → 시스템 반응 비선형)에 집중. 각 analogue에 sensitivity context 명시.

**Lead Indicators (Historical origin)**: 해당 역사적 사건에서 사후적으로 발견된 조기 신호. 현재 상황에서 관찰 가능 여부 판정.

### Method 5: Science Fiction
PDF: *"Since science fiction frequently tries to deviate from conventional thinking, it contains a lot of Wild Card ideas. One can also use the sequence of events described in science fiction narratives to construct post-Wild Card scenarios."*

**AI Science Fiction Scanner Agent**:

**Reference authors (PDF origin + extension)**:
- PDF 인용: Stanislaw Lem, Isaac Asimov, Arthur C. Clarke, Philip K. Dick, Ursula Le Guin, William Gibson, Vernor Vinge, Ted Chiang, Octavia Butler, Cixin Liu
- Extension: Kim Stanley Robinson, Margaret Atwood, Neal Stephenson, Iain M. Banks, Greg Bear, Paolo Bacigalupi
- Korean (extension): 김초엽, 정세랑, 곽재식, 박상준, 배명훈

각 도메인별 가장 plausible SF wild card 추출 + post-WC sequence 구성. `source_method: "sf"`.

**Lead Indicators (SF origin)**: 해당 SF 작품이 묘사한 precursor 기술·사회현상 중 현재 실제 관찰 가능한 것.

---

## 3. STEEP+Spiritual 6 카테고리 자동 분류

PDF Section II: *"Generally, they can be systematized according to their origin e. g. along STEEP sectors (society, technology, economy, environment, politics)."*

PDF Appendix 6 카테고리 (78-catalogue) verbatim:
- EARTH AND SKY (Environment)
- BIOMEDICAL DEVELOPMENTS (Technology+Society)
- GEOPOLITICAL AND SOCIOLOGICAL CHANGES (Politics+Society)
- TECHNOLOGY AND INFRASTRUCTURE UPHEAVAL (Technology)
- NEW THREATS AND OLD THREATS FROM NEW SOURCES (Politics+Technology)
- SPIRITUAL AND PARANORMAL (Spiritual)

본 sub-skill은 **STEEP+S 6 도메인** 명시 분류:

| 도메인 | 키 | 유효값 |
|--------|---|--------|
| Society | S | "S" |
| Technology | T | "T" |
| Economy | E | "E" |
| Environment | Env | "Env" |
| Politics | P | "P" |
| Spiritual | Spi | "Spi" |

각 candidate에 multi-tag 가능 (예: AGI consciousness → "T+S+Spi"). `domain` 필드는 `+` 구분자 사용.

**유효하지 않은 태그를 쓰면 `validate_identification.py`가 WARN 발생.**

---

## 4. 3 Surprise Types 자동 Tagging

PDF Section II p.4 verbatim:

| Type | 정의 | 예시 (PDF) | 본 sub-skill 적용 |
|------|------|---------|---------|
| **Type 1** | events known and relatively certain to occur but without any certainty as to timing | "the next earthquake" | 박사님 도메인 next-event mapping |
| **Type 2** | future events that are unknown to the general public (or even the researchers) but that could be discovered if we only consulted the right experts or if we had adequate models | "impacts of climate change" | expert pool query 후 surface |
| **Type 3** | intrinsically unknowable future events that no expert has in mind, where we lack concepts and means of observation | "unknown unknowns" | SF + brainstorm lateral → invent |

PDF 강조: *"The number of Wild Cards – at least in the third category – is essentially infinite."*

**Type 3 ≥ 20% 강제** (intellectually challenging 보장, PDF "usual suspects" 회피 규칙).

**결정론 검증**: `validate_identification.py`가 Type 3 비율을 자동 확인한다. 비율이 20% 미만이면 `FAIL type3_ratio` 오류가 발생한다. 이 경우 Type 3 candidates를 추가 생성 후 재검증한다.

---

## 5. 78-Wild-Card Catalogue Cross-Reference (Petersen 1997)

**결정론 원칙**: P-XXX-NN 코드는 LLM이 추론하지 않는다. 반드시 `catalogue_lookup.py`를 실행해 코드를 확인한다.

```bash
# 키워드로 후보 찾기
python3 skills/vision-foresight-wild-cards-identification/catalogue_lookup.py "pandemic"
# 특정 코드 확인
python3 skills/vision-foresight-wild-cards-identification/catalogue_lookup.py --code P-BIO-02
# 전체 목록
python3 skills/vision-foresight-wild-cards-identification/catalogue_lookup.py --list
```

**카탈로그 전체 코드 체계** (79항 = 마스터 §10 추출본):

| 범위 | 카테고리 | 항목 수 |
|------|---------|--------|
| P-EAS-01~09 | Earth and Sky | 9 |
| P-BIO-01~10 | Biomedical Developments | 10 |
| P-GEO-01~26 | Geopolitical and Sociological Changes | 26 |
| P-TIU-01~21 | Technology and Infrastructure Upheaval | 21 |
| P-NTH-01~08 | New Threats and Old Threats from New Sources | 8 |
| P-SPP-01~05 | Spiritual and Paranormal | 5 |
| **합계** | | **79** |

**전체 79항 목록** (verbatim from master §10):

**EARTH AND SKY (P-EAS-01~09)**
P-EAS-01: The Earth's Axis Shifts · P-EAS-02: Asteroid or Comet Hits Earth · P-EAS-03: Ice Cap Breaks Up · P-EAS-04: Gulf or Jet Stream Shifts Location Permanently · P-EAS-05: Global Food Shortage · P-EAS-06: Extraordinary West Coast Natural Disaster · P-EAS-07: Rapid Climate Change · P-EAS-08: Collapse of the World's Fisheries · P-EAS-09: Major Break in Alaskan Pipeline

**BIOMEDICAL DEVELOPMENTS (P-BIO-01~10)**
P-BIO-01: Bacteria Become Immune to Antibiotics · P-BIO-02: Worldwide Epidemic · P-BIO-03: Fetal Sex Selection Becomes the Norm · P-BIO-04: Human Mutation · P-BIO-05: Health and Medical Breakthrough · P-BIO-06: Long-term Side Effects of a Medication Are Discovered · P-BIO-07: Human Cloning Is Perfected · P-BIO-08: Life Expectancy Approaches 100 · P-BIO-09: Birth Defects Are Eliminated · P-BIO-10: Collapse of the Sperm Count

**GEOPOLITICAL AND SOCIOLOGICAL CHANGES (P-GEO-01~26)**
P-GEO-01: Civil War in the United States · P-GEO-02: U.S. Economy Fails · P-GEO-03: No-Carbon Economy Worldwide · P-GEO-04: Altruism Outbreak · P-GEO-05: Social Breakdown in the United States · P-GEO-06: Israel Defeated in War · P-GEO-07: Collapse of the U.S. Dollar · P-GEO-08: Economic and/or Environmental Criminals Are Prosecuted · P-GEO-09: Rise of an American Strong Man · P-GEO-10: Stock Market Crash · P-GEO-11: Civil War between Soviet States Goes Nuclear · P-GEO-12: Major U.S. Military Unit Mutinies · P-GEO-13: The Growth of Religious Environmentalism · P-GEO-14: End of Intergenerational Solidarity · P-GEO-15: New Age Attitudes Blossom · P-GEO-16: Religious Right Political Party Gains Power · P-GEO-17: Mass Migrations · P-GEO-18: Africa Unravels · P-GEO-19: U.S. Government Redesigned · P-GEO-20: Electronic Cash Enables Tax Revolt in the United States · P-GEO-21: Western State Secedes from the United States · P-GEO-22: Illiterate, Dysfunctional New Generation · P-GEO-23: Collapse of the United Nations · P-GEO-24: Mexican Economy Fails, United States Takes Over · P-GEO-25: End of the Nation-state · P-GEO-26: Society Turns away from the Military

**TECHNOLOGY AND INFRASTRUCTURE UPHEAVAL (P-TIU-01~21)**
P-TIU-01: Long-term Global Communications Disruption · P-TIU-02: Massive, Lengthy Disruption of National Electrical Supply · P-TIU-03: Energy Revolution · P-TIU-04: Time Travel Invented · P-TIU-05: Y2K: The Year 2000 Problem · P-TIU-06: A New Chernobyl · P-TIU-07: Encryption Invalidated · P-TIU-08: Loss of Intellectual Property Rights · P-TIU-09: Fuel Cells Replace Internal Combustion Engines · P-TIU-10: Room Temperature Superconductivity Arrives · P-TIU-11: Developing Nation Demonstrates Nanotech Weapon · P-TIU-12: Cold Fusion Embraced by Developing Country · P-TIU-13: Global Financial Revolution (E-cash) · P-TIU-14: Faster-than-Light Travel · P-TIU-15: Virtual Reality, Holography Move Information, Instead of People · P-TIU-16: Virtual Reality Revolutionizes Education · P-TIU-17: Self-Aware Machine Intelligence Is Developed · P-TIU-18: Technology Gets out of Hand · P-TIU-19: Humans Directly Interface with the Net · P-TIU-20: Nanotechnology Takes Off · P-TIU-21: Computers/Robots Think Like Humans

**NEW THREATS AND OLD THREATS FROM NEW SOURCES (P-NTH-01~08)**
P-NTH-01: Information War Breaks Out · P-NTH-02: Major Information Systems Disruption · P-NTH-03: Nuclear Terrorists Attack the United States · P-NTH-04: Terrorism Swamps Government Defenses · P-NTH-05: Terrorism Goes Biological · P-NTH-06: Computer Manufacturer Blackmails the Country · P-NTH-07: Hackers Blackmail the Federal Reserve · P-NTH-08: Inner Cities Arm and Revolt

**SPIRITUAL AND PARANORMAL (P-SPP-01~05)**
P-SPP-01: The Arrival of Extraterrestrials · P-SPP-02: The Return of the Awaited One · P-SPP-03: Remote Viewing Becomes Widespread · P-SPP-04: Life is Discovered in Other Dimensions/Realms · P-SPP-05: Future Prediction Becomes Standard Business

**`petersen_ref` 필드 규칙**:
- 79항 중 해당하는 것 → P-XXX-NN (catalogue_lookup.py로 확인)
- 해당 없음 (신규 발명) → `"new"`
- 유사하지만 변형 → `"P-XXX-NN (adapted)"` (원문 코드 + adapted 주석)

---

## 6. 55-Wild-Card Catalogue Cross-Reference (Steinmüller 2003)

Steinmüller A. & K. (2003) *Ungezähmte Zukunft. Wild Cards und die Grenzen der Berechenbarkeit* — 55 Wild Cards portrayed.

**접근 제한 주의**: 본 책은 독일어 상업 출판물(Gerling Academy / Murmann Hamburg 2004)로 공개 웹에서 전문 fetch 불가. VRMP L4 WebFetch 시도 후 불가 시 아래 fallback 적용.

**Steinmüller 2003 도메인 분포** (Steinmüller 2004 Nordregio Report 2004:6 및 학술 인용 기반 secondary source):
- Wirtschaft (Economy): ~10개 (S-Wir-01~10)
- Politik (Politics): ~10개 (S-Pol-01~10)
- Technik (Technology): ~12개 (S-Tec-01~12)
- Gesellschaft (Society): ~10개 (S-Ges-01~10)
- Umwelt (Environment): ~8개 (S-Umw-01~08)
- Wissenschaft (Science breakthrough): ~5개 (S-Wis-01~05)

**`steinmuller_ref` 필드 규칙**:
- 도메인 분류가 명확히 일치하는 경우 → `"S-XXX-NN (domain match)"` (예: `"S-Tec-NN (Technik)"`)
- 구체적 제목 매핑 불가 → `"new"` (원서 미접근 시 할루시네이션 금지)
- 도메인만 특정 가능 → `"S-[도메인약어]-approx"` (예: `"S-Tec-approx"`)

**VRMP L4 실행 결과 처리**:
```
L4 WebFetch 시도: https://www.murmann-publishers.de (또는 관련 학술 데이터베이스)
→ 성공: verbatim 제목 기반 S-XXX-NN 코드 부여
→ 실패/접근불가: steinmuller_ref = "new" 또는 "S-[도메인]-approx"
   source_trail에 "Steinmüller 2003 원서 미접근 — R-3 fallback" 명시
   vrmp_tier를 R-2 이하로 격하
```

---

## 7. Output 양식

```yaml
identification_output:
  meta:
    target_group: "[Step 0.95 청중 — 마스터 Input context 값]"
    catalogue_source: "Petersen 79 / Steinmüller 55 / Both / Custom"
    surprise_type_mix:
      type1: [%]   # 합계 반드시 100
      type2: [%]
      type3: [%]   # 반드시 ≥ 20
    n_candidates: [N]   # 20-40; candidates 실제 수와 일치해야 함
    method_breakdown:   # 5개 키 모두 필수; 합계 = n_candidates
      brainstorm: [n]
      expert: [n]
      survey: [n]
      historical: [n]
      sf: [n]
  candidates:
    - id: WC-001
      title: "[Wild Card 명 — 간결하고 명확하게]"
      domain: "[STEEP+S multi-tag, + 구분자]"   # 예: "T+S+Spi"
      type: "[1/2/3]"
      source_method: "[brainstorm/expert/survey/historical/sf]"
      petersen_ref: "[P-XXX-NN | P-XXX-NN (adapted) | new]"
      steinmuller_ref: "[S-XXX-NN | S-[도메인]-approx | new]"
      seed_description: "[2-3 문장: 사건 내용, 발생 메커니즘, 영향 핵심]"
      positive_or_negative: "[+/-/±]"
      lead_indicators: ["[조기 indicator 1]", "[조기 indicator 2]", "[조기 indicator 3]"]
      # lead_indicators 규칙:
      #   - 3개 이상 5개 이하 (validate_identification.py가 강제)
      #   - 각 indicator: observable + currently trackable + STEEP 분야 내 위치
      #   - 유형: 통계 지표, 기술 이정표, 정책 변화, 학술 발표, 미디어 트렌드 등
    - id: WC-002
      ...
  catalogue_summary:
    # source_method 카운트와 일치해야 함
    new_invented: [N]           # petersen_ref="new" AND steinmuller_ref="new"인 수
    petersen_adapted: [N]       # petersen_ref가 P-XXX-NN (또는 adapted)인 수
    steinmuller_adapted: [N]    # steinmuller_ref가 S-XXX-NN (또는 approx)인 수
    historical_analogy: [N]     # source_method="historical"인 수 (Harremoës 케이스 포함)
    sf_inspired: [N]            # source_method="sf"인 수
```

**유의**: `petersen_adapted` + `steinmuller_adapted` + `new_invented`의 합은 n_candidates보다 클 수 있다 (한 WC가 petersen 참조도 있고 steinmuller 참조도 있는 경우).

---

## 8. VRMP 6-계층 cascade

L1 WebSearch: `"wild card [도메인] 2025"`, `"futurequake [도메인]"`, `"surprise event [도메인] unexpected"`
L2 WebSearch saturation: `"weak signal [도메인]"`, `"discontinuity [도메인]"`, `"unexpected event [도메인]"`
L3 Reverse: `"wild card critique"`, `"wild card vs trend"`, `"false alarm wild card"`, `"[도메인] overblown risk"`
L4 WebFetch 시도 (접근 가능 source 우선):
  - Petersen J.L. (1997). The 'Wild Cards' in Our Future. *Futurist* Jul-Aug. [학술 데이터베이스 검색]
  - Petersen & Steinmüller (2009) V3.0 Chapter 10. [Millennium Project PDF: millenniumproject.org]
  - Harremoës P. et al. (2001). *Late lessons from early warnings*. EEA. [eea.europa.eu에서 free download 가능]
  - Steinmüller 2003 *Ungezähmte Zukunft* [상업 출판 — 접근 실패 시 R-3 fallback]
  - BIPE/CIFS/IFTF (1992) [접근 실패 시 R-3 fallback]
L5 foresight-expert-pool: READ mode (Method 2 전에 실행)
L6 Synthesis with source trail (R-1·R-2·R-3 Tier disclosure)

**Tier 기준**:
- **R-1**: L1-L4에서 실제 web fetch 성공 + verbatim 인용 가능
- **R-2**: L1-L2 WebSearch 결과 기반 + L4 일부 접근 성공
- **R-3**: WebSearch 결과 없거나 학습 지식 fallback. source_trail에 명시 필수

**결정론 검증 (최종 필수 단계)**:
```bash
# 출력 JSON을 생성한 후 반드시 실행
echo '<output_json>' | python3 skills/vision-foresight-wild-cards-identification/validate_identification.py --stdin
# 또는 파일로
python3 skills/vision-foresight-wild-cards-identification/validate_identification.py output.json
```

검증 결과 `"pass": false`이면 errors 목록의 오류를 모두 수정 후 재생성. PASS 전까지 마스터에 반환 불가.

---

## 9. 산출 후 마스터에 반환

```yaml
# 반환 구조 (마스터가 이 exact 형식 expect)
return:
  identification_output: {...}    # Section 7 양식 전체
  vrmp_tier: "R-1 | R-2 | R-3"   # L1~L6 cascade에서 달성한 최고 tier
  source_trail:                   # VRMP 출처 목록 (비어있으면 WARN)
    - "Petersen & Steinmüller (2009) V3.0 Ch.10 — [fetch 결과]"
    - "WebSearch: [쿼리] — [날짜]"
    - "[기타 출처]"
  validation_result:              # validate_identification.py 출력 전문
    pass: true
    n_candidates: [N]
    type3_ratio: "[%]"
    errors: []
    warnings: [...]
  next_skill: "vision-foresight-wild-cards-assessment"
```

마스터는 이 output을 Step 3.1 섹션으로 표시 후 assessment sub-skill로 forwarding.

**`next_skill` 값이 `"vision-foresight-wild-cards-assessment"`가 아니면 validate_identification.py가 FAIL 발생.**

---

## 부록 A. Lead Indicators 생성 가이드라인

Lead indicators는 Wild Card가 발현되기 전 관찰 가능한 전조 신호다. 다음 기준 적용:

| 기준 | 설명 | 예시 |
|------|------|------|
| **Observable** | 현재 측정 가능한 지표 | "AI-generated scientific paper 수" |
| **Trackable** | 정기적으로 추적 가능 | "분기별 특허 출원량" |
| **Leading (not lagging)** | 사건 발생 전 나타남 | "정부 AI 규제 입법 시도 빈도" |
| **Diverse** | STEEP+S 여러 분야에서 | T, S, P 각 1개 이상 권장 |
| **Specific** | 추상적 아닌 구체적 | "AI 시스템 자기수정 보고 건수/년" |

Type 1 WC: 이미 존재하는 임박 지표 (기상 데이터, 지진 활동, 경제 선행지수)
Type 2 WC: 전문 학술지 발표 빈도, 컨퍼런스 의제 변화
Type 3 WC: 유사 사례나 SF 예측과의 유사성 증가 패턴

---

## 부록 B. 오류 및 예외 처리

| 상황 | 처리 |
|------|------|
| n_candidates < 20 | 부족한 수 만큼 brainstorm으로 보충 후 재검증 |
| Type 3 비율 < 20% | SF + brainstorm lateral에서 Type 3 candidates 추가 생성 |
| petersen_ref 코드 불확실 | catalogue_lookup.py 실행 → 미매칭 시 "new" 사용 |
| Steinmüller 원서 미접근 | steinmuller_ref = "new" 또는 "S-[도메인]-approx"; source_trail에 명시 |
| expert-pool 응답 없음 | Method 2: AI 가상 페르소나로 fallback; vrmp_tier → R-3 |
| VRMP L4 모든 소스 실패 | vrmp_tier = "R-3"; source_trail에 fallback 이유 명시 |
| validate_identification.py FAIL | errors 수정 → 재생성 → 재검증 (PASS 전까지 반환 금지) |
| Input context 누락 | 마스터에 누락된 파라미터 반환 요청 (task 중단 금지) |
