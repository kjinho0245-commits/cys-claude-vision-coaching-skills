# Wiki Collaboration Template

## Source

Glenn (2009) §VI: *"Futures Wheel Wikis could be created by letting geographically dispersed people add to and/or edit the consequences via the Internet."*

## Wiki Markdown Template

```markdown
# Futures Wheel Wiki: {CENTER_ISSUE}

> **Generated**: {CURRENT_DATETIME_UTC}  ← use: python3 delphi_utils.py now_utc
> **Panel size**: {PANEL_SIZE} async panelists
> **Rounds completed**: {ROUNDS_COMPLETED} / 5
> **Status**: DRAFT | FINAL

---

## 1st Ring: Primary Impacts (Round 4 results)

### P1. {primary_impact_label} [{frequency_pct}% panel consensus — {oval_size}]
- **Added by**: {panelist_alias} (Round 3)
- **Last edited**: {edit_timestamp_utc}
- **Edit history**:
  - v1 ({timestamp}): initial submission by {alias}
  - v2 ({timestamp}): wording refined by {alias}
  - v3 ({timestamp}): time-range added by {alias}
- **Panel rating**: mean={mean}/5, std={std_dev} — {divergence_flag}
- **Discussion**:
  - {alias}: "{comment}"
  - {alias}: "{counterpoint}"

### P2. ...

---

## 2nd Ring: Secondary Impacts (Round 5 results)

### S1a. (under P1) {secondary_impact_label} [{frequency_pct}%]
- **Added by**: {panelist_alias} (Round 4)
- **Last edited**: {edit_timestamp_utc}
- **Edit history**: ...
- **Cross-links**: [→ S{n}{x} (bidirectional)] [→ P{m} (feedback loop 🔁)]

### S1b. ...
### S2a. ...

---

## Cross-Linkages (panel-suggested)

| From | To | Link Type | Suggested by |
|------|----|-----------|-------------|
| S1a | S3b | bidirectional | {alias} (Round 5) |
| P2 | P4 | feedback loop 🔁 | {alias} (Wiki phase) |
| S2a | P1 | reinforcing | {alias} (Wiki phase) |

---

## Minority Opinions Archive (divergence flag: 🚨)

### MO-1. {impact_label} [std_dev={value}]
- **Minority view**: {minority_position}
- **Majority view**: {majority_position}
- **Panelists holding minority**: {n} / {panel_size}
- **Round where divergence surfaced**: Round {n}

---

## Open Issues

- [ ] {issue_description} (surfaced Round {n}, assigned to {alias})
- [ ] Panel disagrees on time horizon for {impact}
- [ ] Cross-link between P3 and S2a needs validation

---

## Edit Policy

- Any async panelist may ADD new consequences (clearly marked as post-Round addition)
- Edits to existing entries require justification in edit history
- Contradictory entries are NOT deleted — moved to Minority Opinions Archive
- Wiki Editor agent maintains version history and flags conflicts for Round Coordinator
```

## Edit History Format

Each edit must record:
1. `version`: sequential integer starting at v1
2. `timestamp_utc`: ISO-8601 format (from `python3 delphi_utils.py now_utc`)
3. `panelist_alias`: anonymized identifier (e.g., "P-07-Economist-EU")
4. `change_type`: `ADD | EDIT | MERGE | FLAG`
5. `summary`: one sentence

## Conflict Resolution Protocol

1. **Minor wording conflict**: Wiki Editor merges, notes both versions in edit history
2. **Substantive disagreement**: Both positions preserved; flagged as ⚠️ in Open Issues
3. **Factual contradiction**: Moved to Minority Opinions Archive with full context
4. **Merge conflict (simultaneous edit)**: Later timestamp wins; earlier version archived in history

## Anonymous Panelist Alias Format

```
P-{two_digit_index}-{domain}-{geography}
```
Examples: `P-01-Technologist-NorthAmerica`, `P-15-Sociologist-EastAsia`

Aliases are consistent across all rounds and the Wiki phase.
