# Recurring Pattern Catalog — 5종 Recurring Pattern 식별 알고리즘

> 출처: Glenn (2009) §VI V3.0 Ch.06 + 장기 역사 패턴 연구
> 결정론 함수: `temporal_v3_engine.py classify_pattern`, `validate_ct_chain`
> V3 고유 기능 — V1·V2로는 발견 불가

---

## 1. Recurring Pattern이 V3의 고유 가치인 이유

Glenn 원전:
> *"Version 3 is more complex, requiring more time, but can capture much of the essential thinking about a trend or event into one graphic."*

V3의 고유 기능 = **과거·현재·미래를 하나의 cone에 통합**하므로 역사적 반복 패턴이 시각적으로 드러남.

---

## 2. 5종 Recurring Pattern (Section 6 표준)

### 1. Cycle Pattern (사이클 패턴)

**정의**: 일정 주기로 반복되는 역사적 패턴.

**학술 근거**:
- Kondratiev 장파 (K-파동, 40~60년 기술-경제 사이클): Kondratieff, N. (1925). The Major Economic Cycles. Voprosy Konjunktury.
- Huntington (1991). The Third Wave: 민주화-권위주의 주기.
- 쿠즈네츠 사이클 (15~25년 인프라 투자 사이클): Kuznets, S. (1930). Secular Movements in Production and Prices.

**탐지 알고리즘**:
```
1. Historic cone에서 최소 2회 이상 반복 이벤트 식별
2. 반복 주기 계산: interval_1, interval_2, ...
3. 주기 편차 검사: abs(interval_n - avg_interval) / avg_interval < 0.30 (30% 이내)
4. 다음 cycle 예측: T+0 + avg_interval
```

**결정론 분류**:
```bash
python3 temporal_v3_engine.py classify_pattern '{"pattern_type": "cycle"}'
# → Cycle Pattern 정의·탐지방법·미래함의 반환
```

**예시**: 20년 경제위기 사이클 (1997→2008→2027?), K-파동 4차(2010~2040?).

---

### 2. Echo Pattern (에코 패턴)

**정의**: 과거 한 사건의 영향이 N년 후 재반향.

**학술 근거**:
- Strauss & Howe (1991). Generations: 4세대 역사 주기 이론 (사로브린 → 에코).
- Schumpeter (1942). Capitalism, Socialism and Democracy: 창조적 파괴 → 재건 echo.

**탐지 알고리즘**:
```
1. 원사건(Source Event) 식별: T-N년의 주요 충격
2. Echo 기간 추정: 역사적 유사 사례에서 echo lag 측정
3. 현재(T+0) 상태에서 echo 진행 여부 확인
4. 미래 cone에서 echo peak 시점 추정
```

**예시**: 2차 대전(1945) → 베이비붐 → 베이비붐 퇴직 파동(2010~2030), 1997 외환위기 → 20년 후 가계부채 위기.

---

### 3. Compound Advantage (복리 우위 패턴)

**정의**: 과거 투자→현재 dominance→미래 confirmed 우위. 누적 이점 강화.

**학술 근거**:
- Arthur, W.B. (1994). Increasing Returns and Path Dependence in the Economy: 경로 의존성·수확체증.
- Gladwell, M. (2008). Outliers: 10,000시간 법칙 = 누적 우위의 사회적 구조.

**탐지 알고리즘**:
```
1. Historic → Current → Future 각 시간대에서 우위 지표 추적
2. 우위 지표 상승 추세 확인 (선형 또는 지수적)
3. 현재 dominant position 정량 측정
4. 미래 cone에서 우위 유지/강화 probability 추정
```

**예시**: 한국 IT 인프라 투자(1990s)→현재 디지털 5위→미래 AI 경쟁력 기반.

---

### 4. Reversal Pattern (역전 패턴)

**정의**: 과거 trend가 임계점에서 역방향 전환. 세옹지마 효과 역사적 버전.

**학술 근거**:
- Gladwell, M. (2000). The Tipping Point: 임계질량 → 역전.
- Taleb, N.N. (2007). The Black Swan: 비선형 역전.
- Gladwell (2000) p.12: "The moment of critical mass, the threshold, the boiling point."

**탐지 알고리즘**:
```
1. Historic cone에서 trend 방향 매핑 (+ or -)
2. 임계점(tipping point) 식별: sign 변화 시점
3. 역전 이후 신규 trend 형성 확인
4. 현재 trend에서 유사 임계점 접근 여부 판단
5. 미래 cone ring 4~6에 역전 가능성 반영 (세옹지마)
```

**예시**: 세계화 trend(1990~2016)→임계점(2016 브렉시트·트럼프)→보호무역 역전.

---

### 5. Phase Transition (상전이 패턴)

**정의**: 양적 누적이 질적 도약으로 전환. 임계 질량 도달 후 비선형 변화.

**학술 근거**:
- Prigogine, I. (1984). Order out of Chaos: 산일 구조·비평형 상전이.
- Gladwell (2000). The Tipping Point: S-커브 상의 급격한 전환.
- Rogers, E.M. (1962). Diffusion of Innovations: S-커브와 임계 보급률(16%).

**탐지 알고리즘**:
```
1. Historic cone에서 누적 지표 S-커브 매핑
2. 변곡점(inflection point) 식별: 2차 미분 최대 지점
3. 현재(T+0)의 S-커브 위치 확인 (초기·가속·포화 중 어느 단계?)
4. 다음 변곡점(전환점) 추정 시점 → 미래 Primary~Tertiary ring 배치
```

**예시**: 스마트폰 보급(0→50%)의 사회 상전이, AI 채택의 상전이 예상.

---

## 3. SKILL.md Phase 6 표현 → Section 6 표준 매핑

| Phase 6 예시 표현 | Section 6 표준 분류 | 매핑 근거 |
|-----------------|---------------------|---------|
| "linear amplification" | Cycle Pattern | 사이클 강화 국면의 선형 증폭 |
| "compound advantage" | Compound Advantage | 직접 일치 |
| "recurring 20y cycle" | Cycle Pattern | 20년 주기 반복 |
| "echo" | Echo Pattern | 직접 일치 |
| "reversal" | Reversal Pattern | 직접 일치 |
| "phase transition" | Phase Transition | 직접 일치 |
| "tipping point" | Phase Transition | 티핑포인트 = 상전이 임계점 |

결정론 매핑:
```bash
python3 temporal_v3_engine.py classify_pattern '{"pattern_type": "linear amplification"}'
# → {"standard_key": "cycle", "matched": true}
```

---

## 4. Recurring Pattern 탐지 체크리스트

```
□ Historic cone에서 최소 2회 반복 확인 (Cycle / Echo)
□ 각 반복의 주기·규모·맥락 기록
□ 현재(T+0) 상태가 과거 패턴의 어느 단계에 해당하는지 명시
□ 미래 cone에서 다음 반복/역전/전환 시점 추정
□ 예측 근거: 인과 메커니즘 or 통계적 주기성 중 어느 것인지 명시
□ classify_pattern Python 호출로 패턴 유형 공식화
```
