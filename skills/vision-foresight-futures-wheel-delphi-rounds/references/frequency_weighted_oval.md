# Frequency-Weighted Oval Mapping Algorithm

## Source

Glenn (2009) §VI Round 4: *"the size of the oval around each primary impact could represent the frequency with which the panel identified it"*

Glenn (2009) §VI Round 5: *"again, the size of the ovals (or some other graphic device) could represent the frequency of responses"*

## Deterministic Mapping Table

| Frequency | Oval Size | Visual Representation | Glenn Basis |
|-----------|----------|-----------------------|-------------|
| ≥ 90% | XL | ⬭⬭⬭ (largest oval) | "highest frequency" — most prominent visual weight |
| 70–89% | L | ⬭⬭ | High consensus |
| 50–69% | M | ⬭ | Majority |
| 30–49% | S | ◯ | Minority plurality |
| < 30% | XS | · | Low consensus / outlier |

**All computations use `delphi_utils.py` — never LLM-estimated.**

```bash
# Compute oval size for a given frequency ratio:
python3 delphi_utils.py frequency_to_oval 0.83
# Output: {"frequency": 0.83, "oval_size": "L"}

# Compute frequencies from panel responses:
python3 delphi_utils.py count_frequencies '[[...],[...]]' <panel_size>
```

## Mermaid Edge Weight → Oval Size Mapping

| Oval Size | Mermaid Arrow Style | Node Border |
|-----------|---------------------|-------------|
| XL | `===>` (triple) | `stroke-width:5px` |
| L | `==>` (double) | `stroke-width:4px` |
| M | `-->` (single) | `stroke-width:3px` |
| S | `-.->` (dashed) | `stroke-width:2px` |
| XS | `-..->` (dotted) | `stroke-width:1px,stroke-dasharray:3` |

## Line Thickness → Linkage Strength (Phase 8 Groupware)

| Line Style | Meaning | Panel Agreement |
|-----------|---------|----------------|
| solid thick | high consensus | ≥ 70% |
| solid thin | medium consensus | 50–69% |
| dashed | low consensus | 30–49% |
| dotted | minority opinion | < 30% |

## Color Semantics (Phase 8)

| Color | Impact Type |
|-------|-------------|
| #2d6a4f (dark green) | Positive impact — majority view |
| #d62828 (red) | Negative impact — majority view |
| #f4a261 (amber) | Mixed / contested impact |
| #457b9d (blue) | Neutral / structural impact |
| #888 (gray) | Uncertain / low consensus |

## Divergence Icon Protocol

| Icon | Trigger Condition | Source |
|------|-----------------|--------|
| ⚠️ | std_dev ≥ 0.6 and < 1.2 ("moderate divergence") | computed by `aggregate_ratings()` |
| 🚨 | std_dev ≥ 1.2 ("high divergence") | computed by `aggregate_ratings()` |
| 🔁 | item appears as both cause and consequence (feedback loop) | identified by Visualizer agent |
| ⚡ | item contradicts another high-consensus item | identified by Round Coordinator |

## Frequency Thresholds — Configurable Defaults

```yaml
frequency_thresholds:
  XL: 0.90   # 90%+ panel agreement
  L:  0.70   # 70-89%
  M:  0.50   # 50-69%
  S:  0.30   # 30-49%
  XS: 0.00   # <30% (default bucket)
```

Validate with:
```bash
python3 delphi_utils.py validate_panel_size <n>
```
Custom thresholds must satisfy XL > L > M > S ≥ 0; validated by `validate_frequency_thresholds()`.
