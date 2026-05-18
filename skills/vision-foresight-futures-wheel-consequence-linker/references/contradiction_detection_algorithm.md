# 양립 불가 짝(Contradiction) 자동 식별 알고리즘

> **Glenn 출처**: Glenn, J.C. (2009). "Futures Wheel." §IV. Figure 4 NSA Snyder.
> AC/UNU Millennium Project V3.0.

---

## 1. Glenn §IV 원전 인용

> *"The Futures Wheel can also yield contradictory impacts. For example, in the Futures Wheel on the National Security Agency (see Fig. 4), one secondary consequence on the left side of the wheel is 'more control' and another secondary consequence on the left side was 'less control.' These two impacts come from different primary consequences and, together, identify the critical issue of how management could react differently to the same event. Thus the ability to reveal contradiction may actually be a strength of the method."*

---

## 2. Contradiction 식별 기준 (3조건)

아래 3조건을 **모두** 충족해야 Contradiction으로 인정:

### 조건 1: 동일 Ring Level [결정론 검증 가능]
- 두 노드의 `type` 필드(primary/secondary/tertiary/…)가 동일해야 한다.
- Python: `node_A["type"] == node_B["type"]`

### 조건 2: 서로 다른 부모에서 파생 [결정론 검증 가능]
- 두 노드의 직접 부모(parent in adjacency)가 달라야 한다.
- Glenn NSA 사례: S-2a의 부모=P-2(increased dependency on contractors), S-2b의 부모=P-3(loss of in-house skills)
- Python: `parents(node_A) ∩ parents(node_B) == ∅` (공통 부모 없음)

### 조건 3: 텍스트 의미가 의미론적 반대 [LLM 판단 필수]
- "more control" vs "less control" — 동일 대상에 대한 반대 방향 결과
- 판단 기준: 두 텍스트를 동시에 참으로 가정하면 논리적 모순이 발생하는가?
- **출처 없는 판정은 FAIL** — 반드시 Glenn §IV 사례 또는 도메인 학계 문헌과 대조

---

## 3. 알고리즘 의사코드

```python
def find_contradictions(nodes, edges):
    """
    Step 1: Build parent lookup (결정론)
    Step 2: Group nodes by ring level (결정론)
    Step 3: For each pair in same level, check different parents (결정론)
    Step 4: LLM evaluates semantic opposition for structural candidates
    """
    # Step 1: 각 노드의 부모 집합 구축 [결정론]
    parents = defaultdict(set)
    for edge in edges:
        parents[edge["to"]].add(edge["from"])

    # Step 2: ring level별 그루핑 [결정론]
    by_level = defaultdict(list)
    for node in nodes:
        by_level[node["type"]].append(node)

    # Step 3: 구조적 후보 쌍 식별 [결정론]
    structural_candidates = []
    for level, level_nodes in by_level.items():
        for i in range(len(level_nodes)):
            for j in range(i+1, len(level_nodes)):
                A, B = level_nodes[i], level_nodes[j]
                # 서로 다른 부모 조건
                if not (parents[A["id"]] & parents[B["id"]]):
                    structural_candidates.append({
                        "A": A, "B": B, "level": level,
                        "parents_A": list(parents[A["id"]]),
                        "parents_B": list(parents[B["id"]]),
                        "needs_semantic_check": True
                    })

    # Step 4: LLM이 semantic opposition 판단 (후보만 전달)
    return structural_candidates
    # → LLM filters to actual contradictions with evidence
```

---

## 4. Sign 기반 Contradiction 보조 탐지

sign 정보가 있는 경우, 동일 ring level의 노드 쌍에서 **반대 sign**(+1 vs -1)을 자동 탐지하여 LLM semantic check의 우선 후보를 좁힐 수 있다:

```python
# 보조: 동일 ring, 다른 부모, 반대 sign 쌍 → contradiction 강력 후보
if (A["sign"] == +1 and B["sign"] == -1) or (A["sign"] == -1 and B["sign"] == +1):
    priority = "high"  # LLM semantic check 우선순위 높음
```

단, sign이 같아도 semantic contradiction일 수 있으며(예: 두 노드 모두 🔴지만 "더 많은 통제" vs "더 적은 통제"), sign 불일치는 힌트일 뿐 결정적 기준이 아니다.

---

## 5. Critical Issue 승격 기준

Glenn §IV: *"identify the critical issue of how management could react differently to the same event"*

Contradiction이 식별되면 아래 기준으로 critical issue 승격 여부 결정:

| 승격 기준 | 설명 |
|---------|------|
| 정책/전략 분기 발생 | 두 결과가 상반된 대응 전략을 요구하는가? |
| 동일 이해관계자가 영향 | 같은 집단이 상반된 결과에 노출되는가? |
| 정량적 측정 가능성 | 어느 결과가 우세한지 데이터로 확인 가능한가? |

승격된 critical issue는 `scenario-forecast` sub-skill로 escalate.

---

## 6. 출력 형식

```yaml
contradiction_analysis:
  structural_candidates: N  # Python 결정론 탐지
  confirmed_contradictions: K  # LLM semantic 확인 후

  contradictions:
    - id: CT-1
      ring_level: secondary
      A: { id: "S-2a", text: "more control", sign: "🟡", parents: ["P-2"] }
      B: { id: "S-2b", text: "less control", sign: "🟡", parents: ["P-3"] }
      structural_check: PASS  # 결정론
      semantic_check: PASS    # LLM — Glenn §IV "more control / less control" 1:1 대조
      evidence: "Glenn (2009) §IV NSA Figure 4 직접 인용"
      critical_issue: "how management could react differently to the same event"
      promote_to: scenario-forecast
      promote_reason: "상반된 대응 전략 요구 (통제 강화 vs 통제 완화)"
```

---

## 7. 할루시네이션 차단

| 검증 항목 | 방법 |
|---------|------|
| 동일 ring level 여부 | `node["type"]` 비교 [결정론] |
| 서로 다른 부모 여부 | adjacency 탐색 [결정론] |
| 의미론적 반대 여부 | LLM + Glenn §IV 사례 1:1 대조 필수 |
| Contradiction이 "strength" 임 | Glenn §IV 직접 인용 제시 필수 |
| 출처 없는 판정 | 자동 FAIL |
