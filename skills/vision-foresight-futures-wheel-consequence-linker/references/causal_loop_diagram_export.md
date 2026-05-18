# DAG → CLD 표기 변환 가이드

> **Glenn 출처**: Glenn, J.C. (2009). "Futures Wheel." §IV.
> *"This sequential process is a natural way to tie the Futures Wheel into the development of a formal systems model."*
>
> **CLD 표준 출처**: Sterman, J.D. (2000). *Business Dynamics: Systems Thinking and Modeling for a Complex World*. McGraw-Hill. Ch. 5 (Causal Loop Diagrams).

---

## 1. 변환의 이론적 근거

Glenn §IV 직접 인용:

> *"The Futures Wheel can help identify positive and negative feedback loops. The higher-order consequences occasionally cycle back to the original item... This sequential process is a natural way to tie the Futures Wheel into the development of a formal systems model."*

Futures Wheel의 feedback loop는 System Dynamics의 CLD로 직접 변환 가능하다. CLD는 변수 간 인과 관계(+/-)와 피드백 구조를 시각화하는 표준 도구다.

---

## 2. CLD 표기 표준 (Sterman 2000 기준)

### 2.1 기호 체계

| Futures Wheel 요소 | CLD 기호 | 의미 |
|-------------------|---------|------|
| Node (consequence) | `[변수명]` | System variable |
| Positive causal link | `─(+)→` or `─S→` (Same direction) | A↑ → B↑ 또는 A↓ → B↓ |
| Negative causal link | `─(−)→` or `─O→` (Opposite direction) | A↑ → B↓ 또는 A↓ → B↑ |
| Feedback loop (reinforcing) | `R` 레이블 (루프 내부) | Positive loop |
| Feedback loop (balancing) | `B` 레이블 (루프 내부) | Negative loop |
| Time delay | `‖` (edge에 표시) | Delayed causal link |

### 2.2 Loop Type 판정 공식 (결정론)

```
sign_product = (-1)^(number_of_negative_edges_in_loop)

sign_product = +1  →  Reinforcing (R) loop
sign_product = -1  →  Balancing (B) loop
```

---

## 3. 변환 4단계 절차

### Step 1: Cycle 추출 [결정론]

```bash
python3 consequence_linker_engine.py detect_cycles '<adj_dict_json>'
```

→ 모든 cycle 경로 리스트 반환

### Step 2: Causal Polarity 부여 [LLM — 도메인 지식 필요]

각 edge에 대해 LLM이 판단:
- "A가 증가할 때 B가 증가하면" → `(+)`
- "A가 증가할 때 B가 감소하면" → `(−)`
- 판단 근거: 도메인 학계 문헌 또는 Glenn §IV 사례와 1:1 대조
- **출처 없는 판정은 FAIL**

### Step 3: Loop Type 계산 [결정론 환원 가능]

```python
neg_count = sum(1 for edge in loop if edge["polarity"] == "-")
loop_type = "R" if neg_count % 2 == 0 else "B"
```

### Step 4: CLD 텍스트 생성 [LLM]

표준 CLD 텍스트 포맷으로 출력:

```
[변수A] ─(+)→ [변수B]
[변수B] ─(−)→ [변수C]
[변수C] ─(+)→ [변수A]   // B loop (1 negative edge)
```

---

## 4. 변환 예시

### 4.1 Glenn highways loop

**원전**: *"more highways → more drivers → more congestion → more highways"*

```
[고속도로 건설량] ─(+)→ [도로 가용 용량]
[도로 가용 용량] ─(+)→ [신규 운전자 유입]
[신규 운전자 유입] ─(+)→ [교통 혼잡도]
[교통 혼잡도] ─(+)→ [고속도로 추가 건설 압력]
[고속도로 추가 건설 압력] ─(+)→ [고속도로 건설량]  // R loop (0 negative edges)
```

loop type = R (reinforcing / vicious cycle)

### 4.2 NSA Contractor Dependency loop

**기반**: Glenn Figure 4 NSA Snyder

```
[외주 의존도] ─(+)→ [소프트웨어 비용]
[소프트웨어 비용] ─(+)→ [예산 압박]
[예산 압박] ─(+)→ [내부 인력 감소]
[내부 인력 감소] ─(+)→ [외주 의존도]  // R loop (vicious cycle)
```

### 4.3 AI Power Cost Balancing Loop

**기반**: 박사님 2026-05-11 AGI 도입 예시 (Glenn §IV 확장 적용)

```
[AI 도입 규모] ─(+)→ [데이터센터 전력 수요]
[데이터센터 전력 수요] ─(+)→ [전기 요금]
[전기 요금] ─(−)→ [AI 운영 수익성]
[AI 운영 수익성] ─(+)→ [AI 도입 규모]  // B loop (1 negative edge → balancing)
```

---

## 5. 시간 지연(Time Delay) 처리

Futures Wheel의 ring 시간축(T+1~5y, T+5~10y 등)은 CLD의 time delay로 표현:

| Ring 전환 | 시간축 | CLD 표기 |
|---------|-------|---------|
| Center → Primary | T+1~5y | `─‖─(+)→` (단기 지연) |
| Primary → Secondary | T+5~10y | `─‖‖─(+)→` (중기 지연) |
| Secondary → Tertiary | T+10~20y | `─‖‖‖─(+)→` (장기 지연) |
| Tertiary → Quaternary | T+15~25y | `─‖‖‖‖─(+)→` (확장 지연) |
| Quaternary → Quinary | T+20~30y | `─‖‖‖‖‖─(+)→` |
| Quinary → Senary | T+25~50y | `─‖‖‖‖‖‖─(+)→` |

---

## 6. 할루시네이션 차단

| 검증 항목 | 방법 |
|---------|------|
| Cycle 존재·경로 | `detect_cycles` Python [결정론] |
| Loop type (R/B) | sign product 수식 [결정론 환원 가능] |
| Edge polarity (+/-) | LLM + 학계 문헌 1:1 대조 필수 |
| Time delay 값 | `ring_time_axis` Python (wheel_math.py) [결정론] |
| CLD 표기 준수 | Sterman (2000) Ch. 5 기준 검증 |
| "formal systems model" 연결 | Glenn §IV 직접 인용 제시 필수 |
