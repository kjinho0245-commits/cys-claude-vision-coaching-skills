# Panel Diversity Matrix

## Source

Glenn (2009) §VI: *"An international panel could assemble asynchronously"* — diversity across domain, geography, and perspective is structurally required for validity.

**Academic validation**: Linstone, H. A., & Turoff, M. (Eds.) (1975). *The Delphi Method: Techniques and Applications*. Addison-Wesley. (canonical reference on heterogeneous panel composition for Delphi)

## 4 Diversity Dimensions

### Dimension 1: Domain (minimum 4 of 7)

| Domain | Role in Panel |
|--------|--------------|
| Technologist | Evaluates technical feasibility and disruption pace |
| Economist | Assesses economic mechanisms and distributional effects |
| Sociologist | Analyzes behavioral and social-structure impacts |
| Policy Maker | Identifies regulatory and governance implications |
| Industry Practitioner | Grounds analysis in operational reality |
| Academia | Provides theoretical frameworks and long-horizon thinking |
| Civic Society | Surfaces equity, rights, and community-level impacts |

### Dimension 2: Geography (minimum 3 of 4)

| Region | Representation Purpose |
|--------|----------------------|
| North America | Technology leadership, regulatory standard-setting |
| Europe | Social-democratic governance, precautionary principle perspective |
| East Asia (KR/JP/CN) | Manufacturing, demographic transition, digital governance |
| Global South | Development trajectory, resource dependency, equity lens |

### Dimension 3: Perspective (minimum 3 of 4)

| Perspective | Analytical Role |
|------------|----------------|
| Optimist | Surfaces positive pathways and enabling conditions |
| Pessimist | Identifies risks, failure modes, worst-case trajectories |
| Pragmatist | Grounds discussion in current constraints and incremental change |
| Critic | Challenges assumptions, surfaces blind spots |

### Dimension 4: Age Cohort (no minimum — balance preferred)

| Cohort | Birth Range | Relevance |
|--------|------------|-----------|
| Boomer | 1946–1964 | Historical reference, institutional knowledge |
| Gen X | 1965–1980 | Bridge between analog/digital eras |
| Millennial | 1981–1996 | Digital native, early career impact horizon |
| Gen Z | 1997–2012 | Longest time horizon, climate/AI native |

## Diversity Score Formula

**All calculations performed by `delphi_utils.py` — not LLM reasoning.**

```bash
python3 delphi_utils.py diversity_score '<json_list_of_panelists>'
```

Input format:
```json
[
  {"domain": "Technologist", "geography": "North America", "perspective": "Optimist", "age_cohort": "Gen X"},
  {"domain": "Economist", "geography": "Europe", "perspective": "Pessimist", "age_cohort": "Millennial"},
  ...
]
```

Output:
```json
{
  "score": 0.72,
  "dimensions": {
    "domain": {"unique_values": [...], "count": 5, "max": 7, "coverage": 0.71},
    "geography": {"unique_values": [...], "count": 3, "max": 4, "coverage": 0.75},
    "perspective": {"unique_values": [...], "count": 4, "max": 4, "coverage": 1.0},
    "age_cohort": {"unique_values": [...], "count": 3, "max": 4, "coverage": 0.75}
  },
  "minimums_met": true,
  "minimums_required": {"domain": 4, "geography": 3, "perspective": 3}
}
```

Score interpretation:
| Score | Interpretation |
|-------|--------------|
| ≥ 0.80 | Excellent — full diversity coverage |
| 0.60–0.79 | Good — meets minimums, balanced |
| 0.40–0.59 | Acceptable — some gaps, document limitations |
| < 0.40 | Insufficient — recruit additional panelists before proceeding |

## Enforcement Protocol

1. Run diversity check **before Round 1 begins** (Phase 1)
2. If `minimums_met: false` → halt, recruit missing dimension types
3. If score < 0.40 → warn master orchestrator, request panel expansion
4. Document final diversity score in `sub_skill_output.panel_diversity_score`

## Anonymous Alias Assignment

After panel is recruited:
1. Sort panelists by domain then geography (alphabetical)
2. Assign `P-{01..30}` index
3. Full alias: `P-{index}-{domain}-{geography}` (e.g., `P-03-Economist-Europe`)
4. Aliases used consistently across all rounds and Wiki phase
