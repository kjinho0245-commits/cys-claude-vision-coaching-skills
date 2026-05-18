# Three Team Protocol — Historic · Contemporary · Future Team 운영 가이드

> 출처: Glenn (2009) §VI V3.0 Ch.06 + `foresight-expert-pool` 캐스팅 규칙
> 결정론 함수: `temporal_v3_engine.py validate_cone_assembly`, `validate_current_impact`

---

## 1. Team 캐스팅 원칙

각 Team은 `foresight-expert-pool` sub-skill에서 도메인·시간대에 맞는 3~5인 캐스팅.

**Glenn 원전 명시**:
> *"One team could identify the key historical trends or events leading to the item to be studied; the second team the key contemporary impacts or correlations; and the third, the key future impacts or consequences."*

---

## 2. Historic Team Panel

### 역할
T-50y ~ T-0 구간의 driving force·event·trend·correlation 식별.

### 캐스팅 (도메인별)

| 도메인 | 전문가 유형 |
|--------|-----------|
| Society·Culture | 사회학자, 인류학자, 인구학자 |
| Technology | 기술사가, 과학철학자 |
| Economy | 경제사학자, 경제학자 |
| Politics | 정치학자, 국제관계 전문가 |
| Environment | 환경사가, 생태학자 |
| Spirituality | 종교사학자, 문화철학자 |

### 산출 형식 (Phase 2)

```markdown
| Time | Historic Force/Event/Trend | 영향 방향 | ID | Tier | 출처 |
|------|---------------------------|----------|-----|------|------|
| T-30y (1996) | {force 1} | → Center | H_T30_1 | R-1 | [citation] |
| T-20y (2006) | {force 2} | → Center | H_T20_1 | R-1 | [citation] |
```

**ID 생성** (결정론 — LLM 직접 기입 금지):
```bash
python3 temporal_v3_engine.py generate_historic_id '{"T0_year": 2026, "entry_year": 1996, "seq": 1}'
# → {"node_id": "H_T30_1", "offset_label": "T-30y", "absolute_year": 1996}
```

**시간 범위 검증** (결정론):
```bash
python3 temporal_v3_engine.py historic_time_in_range \
  '{"T0_year": 2026, "past_lookback": 50, "entry_year": 1996}'
# → {"in_range": true, "valid_range": "1976~2026"}
```

### Reasoning Chain 요구 (CoER 준수)
각 historic force는 3단계 reasoning chain 필수:
- **R-1**: 역사적 사실 (검증 가능한 수치·사건) + 출처
- **R-2**: 해당 force가 center issue로 이어진 중간 연결 논리
- **H**: 이어짐의 전제(가정) 명시

---

## 3. Contemporary Team Panel

### 역할
T+0 시점의 impact·correlation·existing state 식별.

### 캐스팅

| 도메인 | 전문가 유형 |
|--------|-----------|
| Policy·Governance | 정책 분석가, 규제 전문가 |
| Market·Industry | 시장 분석가, 경영 전략가 |
| Social·Behavioral | 사회학자, 행동경제학자 |
| Technology·Data | AI·데이터 analyst |
| Environmental | 환경 컨설턴트, ESG analyst |

### 산출 형식 (Phase 3)

```markdown
| ID | Current Impact/Correlation | Type | 강도 | Tier | 출처 |
|----|---------------------------|------|-----|------|------|
| C1 | {impact} | direct_effect | 5 | R-1 | [citation] |
| C2 | {correlation} | correlation | 3 | R-2 | [citation] |
```

**강도(1-5) 척도** (결정론 조회):
```bash
python3 temporal_v3_engine.py intensity_scale '{"level": 5}'
# → {"label": "매우 강함", "description": "지배적 영향, 핵심 동인, 복수 독립 연구 확인"}
```

**유형 검증** (결정론):
```bash
python3 temporal_v3_engine.py validate_current_impact '{"impact": {
  "id": "C1", "text": "...", "type": "direct_effect", "intensity": 5, "tier": "R-1"
}}'
```

### ⚠️ 인과 vs. 상관 구별 (Glenn §endnote4 엄수)

> *"Philosophically, one cannot claim certainty of causality. ... 'What are the necessary correlations (not in the mathematical sense) with the event or trend?'"*

- `direct_effect` 유형 → 인과 주장 가능, R-1 증거 필수
- `correlation` 유형 → "인과 불명" 명시 필수, R-2 이하
- `precondition` 유형 → 선결 조건 명시

---

## 4. Future Team Panel

### 역할
T+0~T+50y 미래 primary·secondary·tertiary·quaternary·quinary·senary 식별.

### 캐스팅 (Glenn 명시 전문가)

| 역할 | 전문가 |
|------|--------|
| 마스터 퍼실리테이터 | Jerome C. Glenn (Millennium Project) |
| 시나리오 방법론 | Bishop, Futures Studies Texas State |
| 철학적 프레임 | Wendell Bell, Foundations of Futures Studies |
| 비판적 분석 | Joseph Voros, Swinburne University |
| + 도메인 전문가 2~3인 |

### 산출 형식 (Phase 4)

```markdown
| 차수 | ID | Future Consequence | 시간 | Tier | Gate | Sign |
|-----|-----|-------------------|------|------|------|------|
| Primary | F-P1 | ... | T+1~5y | R-1·R-2 | P1_Pre ✓ | 🟢 |
| Secondary | F-S1a | ... | T+5~10y | R-2 | P2_Pre ✓ | 🔴 |
```

**ID 생성** (결정론 — ⚠️ Greek α 절대 금지):
```bash
python3 temporal_v3_engine.py generate_future_id '{"ring": 6, "lineage_path": "1a1a1a"}'
# → {"node_id": "F-Sn1a1a1a"}   ← 'a' (Latin), NOT 'α' (Greek)
```

**시간 범위 조회** (결정론):
```bash
python3 temporal_v3_engine.py ring_time_range '{"ring_num": 1}'
# → {"time_range": "T+1~5y"}
```

---

## 5. Cone Assembly 완전성 검증 (결정론)

3 team 작업 완료 후 반드시 Python으로 검증:

```bash
python3 temporal_v3_engine.py validate_cone_assembly '{
  "historic_count": 6,
  "current_count": 4,
  "future_primary_count": 5,
  "future_rings_count": {"Secondary": 10, "Tertiary": 20, "Quaternary": 40, "Quinary": 80, "Senary": 160},
  "past_lookback": 50,
  "future_lookahead": 30
}'
```

→ `"valid": true, "verdict": "CONE VALID"` 확인 후 Phase 5 진행.
