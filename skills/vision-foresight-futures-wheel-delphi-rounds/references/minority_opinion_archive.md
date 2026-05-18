# Minority Opinion Archive Protocol

## Purpose

Preserve dissenting panel views that diverge from the majority in any round.
High-divergence items are potential scenario bifurcation points for escalation to `foresight-scenario-forecast`.

## Divergence Classification (Deterministic)

**All classification performed by `delphi_utils.py` — not LLM estimation.**

```bash
python3 delphi_utils.py aggregate_ratings '<json>'
```

| std_dev | Flag | Action |
|---------|------|--------|
| < 0.6 | ✓ consensus | Normal processing |
| 0.6–1.19 | ⚠️ moderate divergence | Document minority view; note in Wiki |
| ≥ 1.2 | 🚨 high divergence | Full archive entry; escalate to scenario-forecast |

## Archive Entry Format

```markdown
## [MO-{sequential_id}] {impact_label}

**Round surfaced**: Round {n}
**Divergence stats**:
- Panel mean: {mean}/5
- Std dev: {std_dev}
- Flag: 🚨 high divergence

**Majority position** ({majority_pct}% of panel):
> "{majority_view_verbatim}"

**Minority position** ({minority_pct}% of panel, {n_panelists} panelists):
> "{minority_view_verbatim}"

**Minority panelist aliases**: P-{x}, P-{y}, P-{z}

**Why this matters**:
- If minority position is correct: {scenario_consequence}
- Recommended action: escalate to foresight-scenario-forecast as scenario branch

**Cross-references**:
- Related impacts: {P_or_S_id_list}
- Wiki entry: #{wiki_anchor}
```

## Escalation Protocol

When `divergence_flag == "🚨 high divergence"`:

1. Archive the item using the format above
2. Include in `sub_skill_output.divergence_flags` list
3. Master orchestrator receives flag and may call `foresight-scenario-forecast`
4. Minority view becomes the "alternative scenario" branch

## Retention Policy

- All minority opinion archive entries are permanent (not deleted)
- Updated if new evidence surfaces in later rounds
- Transferred to master orchestrator output in `minority_opinions_archive` field

## Master Orchestrator Signal

```yaml
sub_skill_output:
  divergence_flags:
    - item: "{impact_label}"
      mean: 3.2
      std_dev: 1.4
      flag: "🚨 high divergence"
      archive_id: "MO-3"
      escalate_to: "foresight-scenario-forecast"
```

## Academic Basis for Divergence Preservation

> "In Delphi, the minority view is not discarded — it is preserved as a signal of genuine uncertainty and potential alternative futures." — Linstone & Turoff (1975), p. 84.

> "High variance in expert judgment often signals a domain where multiple futures are genuinely possible." — Gordon, T. J. (1994). *The Delphi Method*. Futures Research Methodology, AC/UNU.
