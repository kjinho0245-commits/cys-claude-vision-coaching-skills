# NSA Snyder Cross-linkage 사례 상세 재현

> **출처**: Glenn, J.C. (2009). "Futures Wheel." In J.C. Glenn & T.J. Gordon (Eds.),
> *Futures Research Methodology*, Version 3.0 (Ch. 6, §III.B, Figure 4).
> Washington, DC: AC/UNU Millennium Project.
> Futures Wheel developed by Futurist David Snyder during consulting with the U.S. National Security Agency (reprinted with permission of the author).

---

## 1. 원전 Figure 4 구조 재현

### Center Trend

**"NSA — growing costs for and dependence on acquisition and maintenance of software"**

### Primary Consequences (single lines — Glenn §III.B 원전)

| ID | Text | 방향 |
|----|------|------|
| P-1 | Increased funds required for software | left |
| P-2 | Increased dependency on contractors | left |
| P-3 | Loss of in-house skills | left |
| P-4 | Reduced productivity | bottom |
| P-5 | More rapid software response | right |
| P-6 | Lower costs (long-term) | right |

### Secondary Consequences (double lines — Glenn §III.B 원전)

| ID | Parent | Text |
|----|--------|------|
| S-1a | P-1 | Increased costs (general) |
| S-1b | P-1 | Increased security concerns |
| S-2a | P-2 | More control | ← Glenn NSA 사례 contradiction 노드 A |
| S-2b | P-2 | Less control | ← Glenn NSA 사례 contradiction 노드 B |
| S-3a | P-3 | Impact on mission |
| S-4a | P-4 | Higher risks |
| S-5a | P-5 | Increased flexibility |

### Tertiary Consequences (triple lines — Glenn §III.B 원전)

| ID | Parent | Text | Cross-link? |
|----|--------|------|-------------|
| T-1a | S-1a | — (추가 분석 필요) | no |
| T-2a | S-2a | — (추가 분석 필요) | no |

---

## 2. Glenn 원전 인용 — Multi-level Node 현상

Glenn §III.B 직접 인용:

> *"For example, 'increased funds required for software' is a primary consequence of the National Security Agency (NSA) experiencing 'growing costs for and dependence on acquisition and maintenance of software,' a secondary consequence of 'increased dependency on contractors,' and a tertiary consequence of 'increased costs' in general."*

### 해석 (cross-linkage 구조)

동일 노드 "increased funds required for software"가 세 개의 다른 인과 사슬에서 동시에 등장:

```
Chain 1: Center ──── P: "increased funds for software"
Chain 2: Center ──── P: "increased dependency on contractors" ════ S: "increased funds for software"
Chain 3: Center ──── P: "..." ════ S: "increased costs" ━━━━━ T: "increased funds for software"
```

이것이 **Pattern A (multi-parent cross-linkage)**의 원전 근거다. tree 구조로는 표현 불가 — graph 구조 필요.

---

## 3. Contradiction 사례 (Glenn §IV)

Glenn §IV 직접 인용:

> *"one secondary consequence on the left side of the wheel is 'more control' and another secondary consequence on the left side was 'less control.' These two impacts come from different primary consequences and, together, identify the critical issue of how management could react differently to the same event."*

### 구조화

```yaml
contradiction_pair:
  A: { id: "S-2a", parent: "P-2 (Increased dependency on contractors)", text: "more control" }
  B: { id: "S-2b", parent: "P-3 (Loss of in-house skills)", text: "less control" }
  ring_level: secondary
  different_parents: true   # 결정론 검증 가능
  semantic_opposite: true   # LLM 판단 필요
  critical_issue: "how management could react differently to the same event"
  strength: "contradiction reveals a critical issue — Glenn: 'the ability to reveal contradiction may actually be a strength of the method'"
```

---

## 4. Line Thickness 시각 표현 기준

| 인과 사슬 | Glenn 기호 | 본 스킬 표현 |
|---------|-----------|------------|
| Center → Primary | single line | `─────` (1) |
| Primary → Secondary | double line | `═════` (2) |
| Secondary → Tertiary | triple line | `━━━━━` (3) |

Glenn §III.B: "*Instead of rings, one can draw single lines from the central oval to the primary impacts, double lines between the primary and secondary impacts, and triple lines between the secondary and tertiary impacts.*"

Quaternary(4차) 이상은 Glenn 원전에 없으며 박사님 2026-05-11 6차 강화 확장이다.

---

## 5. 할루시네이션 차단 포인트

| 항목 | 확인 방법 |
|------|---------|
| Multi-parent 존재 여부 | `detect_cross_linkages` Python 결정론 (in-degree > 1 탐지) |
| Contradiction 노드의 different_parents | `detect_cross_linkages` Pattern A 결과에서 확인 가능 |
| Line thickness 값 | `adjacency_matrix` Python 결정론 (1/2/3/4/5/6/-1) |
| Cycle 존재 여부 | `detect_cycles` Python 결정론 (DFS) |
