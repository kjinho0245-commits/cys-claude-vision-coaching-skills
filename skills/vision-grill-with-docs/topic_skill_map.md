# 주제 → 관련 vision/sermon/foresight 스킬 자동 매핑표

본 표는 `vision-grill-with-docs` Mode C(다목적 주제 인터뷰)가 사용자 주제를 받았을 때 자동 참조할 관련 스킬을 결정한다. `grill_lib.py parse_topic --text "<주제>"`가 본 표를 키워드 매칭으로 lookup.

매칭은 **부분 문자열 포함** 방식. 한 주제가 다수 스킬과 매칭되면 모두 후보로 제시하고 사용자가 선택.

---

## 매핑 형식

각 행은 다음 구조:

```
키워드 (쉼표 분리) | 관련 스킬 (쉼표 분리) | 인터뷰 초점 (한 줄)
```

`grill_lib.py`는 본 파일을 단순 텍스트 lookup으로 사용한다 (정규식 아님).

---

## 1. 진로 영역

```
진로, 직업, 직장, 이직, 전직, 커리어, 일자리, 취업 | vision-career-recommendation, vision-cys-competence-visioncoding, vision-mbti-visioncoding, vision-multipleintel-visioncoding, vision-strong-visioncoding, vision-readiness-visioncoding | 박사님 표준 사전 '소명' 정의로 시대적 부르심 응답 일치 검사 + 4 Skill Balance 강점축 확인
전공, 학과, 학교, 대학, 대학원, 부전공, 복수전공, 전과 | vision-career-recommendation, vision-cys-competence-visioncoding, vision-multipleintel-visioncoding, vision-mbti-visioncoding | 다중지능 강점축 + MBTI + STRONG 흥미 + 박사님 비전 정의 시대적 요구 cross-reference
창업, 사업, 자영업, 스타트업 | vision-career-recommendation, vision-financial-coach, vision-strategy-coach, vision-eight-training-areas | 비전 정의(가치·시대·소명) + 재정 3겹 방패 + 사역/비전 균형
은퇴, 퇴직, 이모작, 시니어 | vision-five-stages, vision-mission-frame, vision-three-realm-balance | 5단계 비전 성장 + 3영역 재균형 + 박사님 비전 정의 새로운 단계 매핑
```

## 2. 재정 영역

```
돈, 재정, 자산, 부, 자금, 자본 | vision-financial-coach, vision-financial-3shields-3windows | Dave Ramsey/Suze Orman + 박사님 3겹 방패·3창 + 재정 시뮬레이션
부채, 빚, 대출, 카드, 할부, 리볼빙 | vision-financial-coach | 스노우볼/Avalanche 결정론 시뮬레이션 + 박사님 표준 재정 코칭
투자, 주식, 부동산, 금융상품, ISA, 연금 | vision-financial-3shields-3windows, vision-financial-coach | 박사님 3창(공격·안정·균형) + 재정 위험 분석
집, 주택, 전세, 월세, 매수, 매도, 청약 | vision-financial-3shields-3windows, vision-financial-coach | 큰 재정 결정 — LDR 후보 + 5/10년 시뮬레이션
유학, 학비, 자녀교육비 | vision-financial-coach | 가족 전체 재정 시나리오 + LDR
응급자금, 비상금, 안전 | vision-financial-coach | Suze Orman 8개월 응급자금 표준
예산, 가계부, 월간 지출 | vision-financial-coach | 6단계 재정 분석 + 50/30/20
```

## 3. 관계 영역

```
결혼, 배우자, 결혼 결정, 청혼, 약혼 | vision-three-realm-balance, vision-statement-writer | LDR 자격 — 3조건 모두 충족하는 전형. 3영역 균형 검사
이혼, 별거, 관계 정리 | vision-three-realm-balance | LDR 자격 + 깊은 grill
자녀, 출산, 육아 | vision-three-realm-balance, vision-five-stages | LDR 자격 (출산) + 부모 비전 성장 단계
부모, 효도, 부양, 가족 책임 | vision-three-realm-balance | 가족과 세상 영역 + 박사님 표준 가치 검증
교회, 공동체, 소속, 멤버십 | vision-three-realm-balance, sermon-augustine-coaching, sermon-bavinck-coaching | 가족과 세상 영역 + 사역 cross-reference
인간관계, 친구, 인맥, 네트워크 | vision-cys-competence-visioncoding | 네트워킹력 비전 코드 진단
이주, 이사, 해외, 이민 | vision-three-realm-balance, vision-financial-coach | LDR 자격 + 3영역 모두 영향
```

## 4. 사역·신앙 영역

```
사역, 신앙, 봉사, 헌신, 헌금 | vision-mission-frame, sermon-augustine-coaching, sermon-bavinck-coaching, sermon-calvin-institutes | 박사님 영적 직관력 축 + 어거스틴 ordo amoris + 칼빈 vocatio
선교, 선교사, 단기선교, 장기선교 | vision-mission-frame, sermon-augustine-coaching, vision-three-realm-balance | LDR 자격 + 사역 헌신 + 3영역 검사
신학교, 안수, 목회자, 전도사 | vision-mission-frame, vision-career-recommendation, sermon-calvin-institutes | LDR 자격 — 진로 전환 + 사역 cross-reference
교회 개척, 교회 사역 전임 | vision-mission-frame, vision-three-realm-balance, vision-financial-coach | LDR 자격 + 재정 시나리오 + 3영역 + 사역
설교, 강의, 가르침 | sermon-topic-message-coach, sermon-augustine-coaching, sermon-calvin-style-insight, sermon-lloyd-jones-coaching, sermon-bavinck-coaching | 본 스킬보다 sermon 시리즈로 안내
영성, 영적 성장, 묵상, 기도 | sermon-augustine-coaching, sermon-bavinck-coaching, vision-mission-frame | 박사님 영적 직관력 축 + 어거스틴 confessio
QT, 큐티 | sermon-qt-original-text-based | 본 스킬보다 QT 전용 스킬로 안내
```

## 5. 비전 영역 자체 (메타)

```
비전, 비전 명료화, 비전 잡기, 비전 설정 | vision-clarity-coaching, vision-mission-frame, vision-statement-writer | 비전 정의 5단계 명료화
비전이 막혀있다, 비전 모르겠다, 방향 잃었다 | vision-clarity-coaching, vision-three-realm-balance, vision-mission-frame | 인터뷰로 박사님 정의 한 자리씩 채움
미션, 비전 선언문, 비전 문장 | vision-statement-writer, vision-mission-frame | 한 문장 비전 선언문
가치, 핵심가치, 이상 | vision-values-visioncoding, vision-three-realm-balance | 가치 단어 매핑 + 3영역 검사
비전 점검, 비전 진단, 비전 검증 | vision-cys-competence-visioncoding, vision-mission-frame, vision-readiness-visioncoding | 10개 비전 코드 + 비전 프레임
강점, 약점, 재능, 능력 | vision-multipleintel-visioncoding, vision-mbti-visioncoding, vision-strong-visioncoding, vision-cys-competence-visioncoding | 다중지능 + MBTI + STRONG + CYS 통합
성격, 기질, 성품 | vision-mbti-visioncoding, vision-enneagram-visioncoding | MBTI 16유형 + 에니어그램 9유형
```

## 6. 미래 시뮬레이션 영역

```
5년 후, 10년 후, 미래 모습, 장기 계획 | vision-futures-timeline-map, vision-four-futures, vision-personal-future-research | 박사님 미래학자 본업 시나리오 4종
미래 예측, 트렌드, 변화 | vision-personal-future-research, vision-future-needs-prediction, foresight-environmental-scanning | 박사님 시대 축 + 환경 스캐닝
시나리오, 대안 미래, 가능성 | vision-four-futures, foresight-scenarios | Kahn/Glenn 시나리오 + 박사님 4미래
환경 스캐닝, weak signal, 약신호 | foresight-environmental-scanning, foresight-tech-mining | Gordon/Glenn Millennium Project
미래 약속, 약속, 헌신, 결단 | vision-future-promise-five-criteria, vision-follow-through-habits | 5기준 + 후속행동 습관
```

## 7. 실행·전략 영역

```
계획, 전략, 실행 계획, 로드맵 | vision-strategy-coach, vision-smart-five-competence, vision-eight-training-areas | SMART 5역량 + 8훈련 영역
훈련, 연습, 습관 | vision-follow-through-habits, vision-eight-training-areas | 박사님 8 훈련 영역
목표, 단기 목표, 중간 목표 | vision-goal-reframing, vision-statement-writer | 목표 재구성 + 비전 선언문
진행 점검, 회고, 리뷰 | vision-progress-review, vision-follow-through-habits | 박사님 진행 점검 표준
난관, 막혔다, 정체, 슬럼프 | vision-clarity-coaching, vision-goal-reframing, vision-three-realm-balance | 인터뷰로 막힌 가지 식별 + 재구성
```

## 8. 종합·진단 영역 (입구 스킬 후보)

```
모르겠다, 정리하고 싶다, 도와줘, 생각 정리 | vision-clarity-coaching, vision-mission-frame | 본 스킬(grill-with-docs)이 인터뷰로 정리
종합 진단, 통합 검사, 전체 점검 | vision-cys-competence-visioncoding, vision-readiness-visioncoding, vision-mission-frame | 박사님 종합 진단 도구들
어디서 시작, 어디부터 | vision-clarity-coaching | 박사님 5단계 명료화로 시작점 결정
```

---

## 매핑 로직 (`grill_lib.py parse_topic`)

1. 입력 텍스트를 공백·구두점으로 토큰화.
2. 본 파일을 라인별로 읽으며 첫 컬럼(`|` 이전)의 키워드 중 하나라도 토큰 집합에 부분 일치하면 그 라인 매칭.
3. 매칭된 라인의 스킬 후보를 모두 수집 (중복 제거).
4. 각 라인의 "인터뷰 초점" 한 줄도 수집.
5. JSON 출력:
   ```json
   {
     "topic": "<입력 원문>",
     "matched_keywords": ["진로", "전공"],
     "related_skills": ["vision-career-recommendation", "vision-mbti-visioncoding", ...],
     "interview_focus": ["다중지능 강점축 + MBTI + ...", ...]
   }
   ```

매칭 결과를 인터뷰에서 사용:

> "방금 주신 주제에서 '진로'와 '전공' 두 키워드를 잡았습니다. 관련 박사님 vision 스킬은 5개입니다 — vision-career-recommendation·vision-cys-competence·vision-multipleintel·vision-mbti·vision-strong. 이들의 산출물이 있으시면 알려주세요. 없으면 박사님 표준 사전과 본인 기질·강점만으로도 충분히 grill 가능합니다.
> 시작하겠습니다. 첫 질문 — ..."

---

## 본 파일 업데이트 절차

박사님이 새 vision/sermon/foresight 스킬을 추가하시면 본 표에도 매핑 추가. 절차:

1. 박사님이 스킬 SKILL.md 작성 → description 필드의 트리거 키워드 식별.
2. 트리거 키워드를 본 표의 영역(1~8) 중 해당 위치에 추가 또는 새 행 추가.
3. `grill_lib_test.py`의 `test_parse_topic_*` 항목 추가하여 새 키워드가 새 스킬을 매핑하는지 검증.
