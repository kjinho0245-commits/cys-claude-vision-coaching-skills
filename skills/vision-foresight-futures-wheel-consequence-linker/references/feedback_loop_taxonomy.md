# Feedback Loop 분류 + System Dynamics 변환

> **Glenn 출처**: Glenn, J.C. (2009). "Futures Wheel." §IV. AC/UNU Millennium Project V3.0.
> **SD 출처**: Sterman, J.D. (2000). *Business Dynamics: Systems Thinking and Modeling for a Complex World*. McGraw-Hill. (CLD 표기 표준)

---

## 1. Glenn §IV 원전 인용

> *"The Futures Wheel can help identify positive and negative feedback loops. The higher-order consequences occasionally cycle back to the original item (e.g., more highways produce more drivers, produce more congestion, produce still more highways). This sequential process is a natural way to tie the Futures Wheel into the development of a formal systems model."*

---

## 2. Feedback Loop 분류 체계

### 2.1 Positive (Reinforcing) Loop

**정의**: 변화가 같은 방향으로 증폭되는 자기 강화 루프.

**Glenn 원전 예시**: more highways → more drivers → more congestion → more highways

**분류 규칙**:
- cycle의 모든 edge에서 sign product = +1 (양수 개수가 짝수)
- 또는 cycle 내 음수(negative) edge의 개수가 **짝수**

**세부 유형**:

| 유형 | 설명 | 예시 |
|------|------|------|
| Virtuous cycle (선순환) | 긍정적 결과가 더 긍정적 결과를 강화 | 기술 투자 → 생산성 증가 → 더 많은 투자 |
| Vicious cycle (악순환) | 부정적 결과가 더 부정적 결과를 강화 | 빈곤 → 교육 부족 → 더 깊은 빈곤 |

### 2.2 Negative (Balancing) Loop

**정의**: 변화가 반대 방향으로 조절되는 자기 균형 루프.

**분류 규칙**:
- cycle의 모든 edge에서 sign product = -1 (음수 개수가 홀수)
- 목표 추구(goal-seeking) 행동 패턴

**예시**: 온도조절 → 난방 가동 → 온도 상승 → 온도조절 감소 (음의 피드백)

### 2.3 Loop Type 판정 (Python 결정론 불가 — LLM 판단)

cycle type 판정은 edge의 sign(+/-)이 필요하며, sign 부여는 LLM이 수행.
단, 판정 기준(sign product)은 결정론으로 환원 가능.

```
loop_type = POSITIVE if (count of negative edges in cycle) % 2 == 0
loop_type = NEGATIVE if (count of negative edges in cycle) % 2 == 1
```

---

## 3. Cycle Detection 결정론 (DFS)

cycle의 **존재 여부**와 **경로**는 결정론 엔진이 탐지:

```bash
python3 consequence_linker_engine.py detect_cycles '<adj_dict_json>'
```

예시:
```json
{
  "adj": {
    "Center": ["P1"],
    "P1": ["S1"],
    "S1": ["T1"],
    "T1": ["Center"]
  }
}
```

결과: `{"cycles": [["Center","P1","S1","T1","Center"]], "cycle_count": 1}`

cycle의 **sign type** (positive/negative)은 Python 출력 후 LLM이 판정.

---

## 4. System Dynamics CLD 변환 규칙

Glenn §IV: *"a natural way to tie the Futures Wheel into the development of a formal systems model"*

### 4.1 Futures Wheel → CLD 매핑 표

| Futures Wheel 요소 | CLD 표기 | 설명 |
|-------------------|---------|------|
| Center trend | 변수 박스 `[변수명]` | 시스템의 중심 변수 |
| Primary/Secondary consequence | 변수 박스 `[변수명]` | 인과 사슬의 노드 |
| Positive feedback edge | `─(+)→` | 원인 증가 → 결과 증가 |
| Negative feedback edge | `─(−)→` | 원인 증가 → 결과 감소 |
| Feedback loop (positive) | `R` 레이블 | Reinforcing loop |
| Feedback loop (negative) | `B` 레이블 | Balancing loop |

### 4.2 변환 절차

1. graph의 feedback loop를 `detect_cycles`로 추출 [결정론]
2. loop 내 각 edge의 causal polarity를 LLM이 판단 [LLM]
3. loop type (R/B) = sign product rule [결정론 환원 가능]
4. CLD 표기 생성 [LLM — 서술 + 기호]

### 4.3 예시: AGI 도입 feedback loop

```
# R loop (reinforcing — positive feedback)
[AGI 도입 규모] ─(+)→ [화이트칼라 대체]
[화이트칼라 대체] ─(+)→ [기업 인건비 절감]
[기업 인건비 절감] ─(+)→ [AGI 추가 투자]
[AGI 추가 투자] ─(+)→ [AGI 도입 규모]   ← R 루프 완성 (4 positive edges → product = +1)

# B loop (balancing — negative feedback)
[AGI 도입 규모] ─(+)→ [전력 수요]
[전력 수요] ─(+)→ [전기 요금]
[전기 요금] ─(−)→ [AGI 운영 수익성]
[AGI 운영 수익성] ─(+)→ [AGI 도입 규모]   ← B 루프 완성 (1 negative edge → product = -1)
```

---

## 5. Glenn highways 사례 CLD 변환

Glenn 원전 (*"more highways produce more drivers, produce more congestion, produce still more highways"*):

```
[고속도로 수] ─(+)→ [운전자 수]
[운전자 수] ─(+)→ [교통 혼잡도]
[교통 혼잡도] ─(+)→ [고속도로 건설 압력]
[고속도로 건설 압력] ─(+)→ [고속도로 수]   ← R loop (reinforcing, vicious)
```

**주**: 이 루프는 외견상 positive이나 실제 사회 결과는 부정적(vicious) — loop type과 desirability는 구분됨.

---

## 6. 할루시네이션 차단

| 항목 | 결정론 처리 |
|------|-----------|
| Cycle 존재·경로 | `detect_cycles` Python |
| Edge sign product | 수식: `product = (-1)^(neg_edge_count)` |
| Loop type R/B | sign product = +1 → R, -1 → B |
| Sign 부여 | LLM 판단 + Glenn §IV 기준 1:1 대조 필수 |
