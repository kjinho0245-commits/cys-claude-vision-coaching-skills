# Glenn V3 Temporal 3D — Cone 구조 상세 + Figure 7 재현

> 출처: Glenn (2009) V3.0 06장 §VI "Frontiers of the Method" > "Version 3" + Figure 7
> 결정론 함수: `temporal_v3_engine.py ring_time_range`, `validate_temporal_anchor`

---

## 1. 원전 직접 인용 (할루시네이션 방지 — 원문 그대로)

> *"A 'Version 3 Futures Wheel' would add the dimension of historic forces, current correlations, and future implications in a cone-like fashion. This approach has the advantage of providing a space for linkages or consequences that don't always fit in Versions 1 and 2. Some people want to discuss how a trend evolved, while others want to talk about more current impacts, and still others are more future-oriented. Version 3 is more complex, requiring more time, but can capture much of the essential thinking about a trend or event into one graphic."*
>
> — Glenn (2009), §VI "Frontiers of the Method", V3.0 Ch.06

> *"A Version 3 Futures Wheel could be carried out by three different teams. One team could identify the key historical trends or events leading to the item to be studied; the second team the key contemporary impacts or correlations; and the third, the key future impacts or consequences. The results of the teams can be put into one Version 3 Futures Wheel."*
>
> — Glenn (2009), §VI, V3.0 Ch.06

> *"Unfortunately, it may be difficult to graph if confined to a two-dimensional piece of paper. If done with computer software that allows for rotation (such as computer-assisted design software) and or in hypertext software (imbedding information under terms that are not seen until requested by the user), the Version 3 Futures Wheel becomes more visually manageable."*
>
> — Glenn (2009), §VI, V3.0 Ch.06

---

## 2. Figure 7 구조 (3D Cone)

Glenn(2009) Figure 7 재현:

```
              ▲ Future Consequences
              │ (uncertainty 증가 → cone 확대)
          T+30y ●────────────● Senary (F-Sn): T+25~50y
               /              \
          T+20y ●──────────────● Quinary (F-Qn): T+20~30y
               /                \
          T+15y ●────────────────● Quaternary (F-Q): T+15~25y
               /                  \
          T+10y ●──────────────────● Tertiary (F-T): T+10~20y
               /                    \
           T+5y ●────────────────────● Secondary (F-S): T+5~10y
               /                      \
           T+1y ●──────────────────────● Primary (F-P): T+1~5y
               \                      /
    ━━━━━━━━━━━━━●━━━━━━━━━━━━━━━━━━━━  T+0 Center Oval
    ─── Current Ring ─────────────────  C1·C2·C3·... (Contemporary Team)
    ━━━━━━━━━━━━━●━━━━━━━━━━━━━━━━━━━━
               /                      \
           T-5y ●──────────────────────● Historic recent
               /                      \
          T-10y ●────────────────────● Historic mid
               /                    \
          T-20y ●──────────────────● Historic far
               /                  \
          T-30y ●────────────────● Historic deep
               /
          T-50y ●────────── Historic deepest
              ▼
              Historic Forces
```

### 시간 범위 중첩 설명 (의도적)

| Ring | 시간 범위 | 이전 Ring과 중첩 | 의미 |
|------|----------|----------------|------|
| Primary | T+1~5y | — | 가장 확실한 단기 영향 |
| Secondary | T+5~10y | Primary와 T+5 중첩 | 중기 파급 |
| Tertiary | T+10~20y | Secondary와 T+10 중첩 | 장기 파급 |
| Quaternary | T+15~25y | Tertiary와 T+15~20y 중첩 | **불확실성 확대 시작** (세옹지마 1차) |
| Quinary | T+20~30y | Quaternary와 T+20~25y 중첩 | **불확실성 중간** (세옹지마 2차) |
| Senary | T+25~50y | Quinary와 T+25~30y 중첩 | **문명 단위** (세옹지마 3차) |

**중첩은 의도적** — Glenn V3의 cone 특성: 미래로 갈수록 불확실성이 넓어져 시간 범위가 겹침.
결정론 검증: `python3 temporal_v3_engine.py ring_time_range '{"ring_num": 4}'`

---

## 3. 3D Cone vs. V1·V2 차별점

| 측면 | V1 Basic | V2 Domain | V3 Temporal |
|------|---------|-----------|-------------|
| 구조 | 동심원 ring | 도메인별 섹터 | 3D cone (historic + current + future) |
| 시간축 | 미래만 | 미래만 | **과거·현재·미래 통합** |
| Team 구성 | 1팀 | 1팀 | **3팀 (Historic · Contemporary · Future)** |
| 고유 기능 | 미래 ripple | 도메인 분류 | **Recurring pattern 탐지** |
| Glenn 원전 | §III.A | §III.B | §VI Frontiers |

---

## 4. T+0 기준 절대연도 계산 (결정론 의무)

T+0 연도를 정의하면 모든 시간 표현이 결정론으로 변환됨:

```bash
# T+0 = 2026 기준
python3 temporal_v3_engine.py temporal_year '{"T0_year": 2026, "offset": -30}'
# → {"absolute_year": 1996, "offset_label": "T-30y"}

python3 temporal_v3_engine.py temporal_year '{"T0_year": 2026, "offset": 15}'
# → {"absolute_year": 2041, "offset_label": "T+15y"}
```

**LLM이 "T-30y = 1996" 등의 연도 계산을 자연어로 추론하는 것을 구조적으로 금지.**
반드시 Python 출력을 그대로 사용.
