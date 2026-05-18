#!/usr/bin/env python3
"""
consequence_linker_engine.py — Consequence Linker 전용 결정론 엔진.

할루시네이션 구조적 차단 대상 (LLM이 자연어로 재추론하지 못하게 봉쇄):
  - Adjacency matrix 구성 (line thickness encoding)
  - Cross-linkage 구조 탐지 (multi-parent, skip-level by in-degree)
  - Cycle detection (DFS)
  - Graph 지표 계산 (density, fan-in/out, longest path)
  - Sign reversal 카운팅 (🟢↔🔴 전이 횟수)
  - SRS aggregation (consequence-linker 전용 임계값 세트)
  - Forced reversal compliance (P→Q, Q→Qn, Qn→Sn ≥50%)
  - Excessive reversal guard (avg >3.5 → WARN)

Sign encoding (이 스킬에서 사용):
  +1 = positive/beneficial consequence (🟢)
  -1 = negative/harmful consequence (🔴)
   0 = neutral/uncertain (🟡)

CLI: python3 consequence_linker_engine.py <command> '<json_args>'

Available commands:
  adjacency_matrix        nodes, edges → matrix
  detect_cross_linkages   nodes, edges → multi-parent, skip-level
  detect_cycles           adj_dict     → cycle list
  graph_metrics           nodes, edges → density, fan_in, fan_out, longest_path
  count_reversals         sign_list    → reversal_count, positions
  linker_srs_score        lineages     → avg, classification
  linker_forced_compliance lineages   → P→Q, Q→Qn, Qn→Sn pass/fail

Source authority:
  - Glenn, J.C. (2009). "Futures Wheel." In J.C. Glenn & T.J. Gordon (Eds.),
    Futures Research Methodology, Version 3.0 (Ch. 6). Washington, DC:
    AC/UNU Millennium Project.
  - SRS threshold extensions: 박사님 2026-05-11 6차 강화 (Quaternary~Senary layers).
    These are NOT from Glenn (2009). They extend the original 3-line system
    to 6-line and add sign-reversal quality metrics beyond the original method.
"""

import json
import sys
from collections import defaultdict, deque
from typing import List, Dict, Tuple, Optional, Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

LINE_THICKNESS_VALUES: Dict[str, int] = {
    "single":    1,   # Center → Primary     (Glenn §III.B)
    "double":    2,   # Primary → Secondary  (Glenn §III.B)
    "triple":    3,   # Secondary → Tertiary (Glenn §III.B)
    "quadruple": 4,   # Tertiary → Quaternary (박사님 6차 강화)
    "quintuple": 5,   # Quaternary → Quinary  (박사님 6차 강화)
    "sextuple":  6,   # Quinary → Senary      (박사님 6차 강화)
    "feedback":  -1,  # Cycle feedback edge   (Glenn §IV)
    "cross":     0,   # Cross-domain/skip-level link (Glenn §III.B cross-linkage)
}

LINE_FROM_RING: Dict[Tuple[str, str], str] = {
    ("center",     "primary"):    "single",
    ("primary",    "secondary"):  "double",
    ("secondary",  "tertiary"):   "triple",
    ("tertiary",   "quaternary"): "quadruple",
    ("quaternary", "quinary"):    "quintuple",
    ("quinary",    "senary"):     "sextuple",
}

# SRS thresholds for consequence-linker (박사님 2026-05-11 6차 강화)
# DIFFERS from parent wheel_math.py (excellent=1.5) because 6차 extension
# requires stronger non-linearity evidence across longer causal chains.
LINKER_SRS_THRESHOLDS = {
    "excellent":   2.0,   # avg ≥ 2.0 → PASS EXCELLENT
    "good":        1.5,   # 1.5 ≤ avg < 2.0 → PASS GOOD
    "acceptable":  1.0,   # 1.0 ≤ avg < 1.5 → PASS ACCEPTABLE
    "insufficient": 0.0,  # avg < 1.0 → REJECT
    "excessive":   3.5,   # avg > 3.5 → WARN (wishful thinking)
}

EMOJI_TO_INT = {"🟢": +1, "🔴": -1, "🟡": 0, "+1": +1, "-1": -1, "0": 0}
INT_TO_EMOJI = {+1: "🟢", -1: "🔴", 0: "🟡"}


# ---------------------------------------------------------------------------
# 1. Adjacency Matrix
# ---------------------------------------------------------------------------

def adjacency_matrix(nodes: List[str], edges: List[Dict]) -> Dict:
    """
    Build adjacency matrix from nodes and edges.
    Cell value = LINE_THICKNESS_VALUES[line_type].
    Feedback edges stored as -1. Cross-link edges stored as 0 (no thickness).
    Returns both raw matrix and a node-indexed dict for human reading.
    """
    if not nodes:
        return {"error": "nodes list is empty"}
    n = len(nodes)
    idx = {node: i for i, node in enumerate(nodes)}
    matrix = [[None] * n for _ in range(n)]
    for i in range(n):
        matrix[i][i] = "-"  # diagonal

    edge_log = []
    for edge in edges:
        src = edge.get("from", edge.get("source", ""))
        dst = edge.get("to", edge.get("target", ""))
        line = edge.get("line", edge.get("type", "single"))
        if src not in idx or dst not in idx:
            edge_log.append({"warning": f"Node not in nodes list", "edge": edge})
            continue
        value = LINE_THICKNESS_VALUES.get(line, 0)
        r, c = idx[src], idx[dst]
        if matrix[r][c] is None:
            matrix[r][c] = value
        else:
            if matrix[r][c] != "-":
                edge_log.append({
                    "warning": f"Duplicate edge {src}→{dst}, keeping max thickness",
                    "existing": matrix[r][c], "new": value
                })
                matrix[r][c] = max(matrix[r][c], value)

    # Fill remaining None with 0
    for i in range(n):
        for j in range(n):
            if matrix[i][j] is None:
                matrix[i][j] = 0

    legend = {
        "1=single(Center→Primary)",
        "2=double(Primary→Secondary)",
        "3=triple(Secondary→Tertiary)",
        "4=quadruple(Tertiary→Quaternary)",
        "5=quintuple(Quaternary→Quinary)",
        "6=sextuple(Quinary→Senary)",
        "-1=feedback_loop",
        "0=no_edge_or_cross_link",
        "-=diagonal",
    }

    return {
        "nodes": nodes,
        "index": idx,
        "matrix": matrix,
        "legend": list(legend),
        "edge_warnings": edge_log,
    }


# ---------------------------------------------------------------------------
# 2. Cross-linkage Detection
# ---------------------------------------------------------------------------

def detect_cross_linkages(nodes: List[str], edges: List[Dict]) -> Dict:
    """
    Detect structural cross-linkage patterns (Glenn §III.B):
      - Pattern A: multi-parent (in-degree > 1 for non-center nodes)
      - Pattern B: cross-domain jump (edge skips ring level — skip-level)
      - Pattern C: cross-domain link (requires 'domain' attribute on nodes)

    NODE metadata expected:
      node dict: {"id": "P1", "type": "primary|secondary|...", "domain": "Tec|Eco|..."}

    EDGE metadata expected:
      edge dict: {"from": "P1", "to": "S1", "line": "double", "cross_link": bool}
    """
    NODE_RING_ORDER = {
        "center": 0, "primary": 1, "secondary": 2, "tertiary": 3,
        "quaternary": 4, "quinary": 5, "senary": 6
    }

    node_meta = {n["id"]: n for n in nodes if isinstance(n, dict) and "id" in n}
    if not node_meta and isinstance(nodes[0], str):
        # Plain string nodes — cannot detect domain/ring
        node_meta = {n: {"id": n, "type": "unknown", "domain": "unknown"} for n in nodes}

    # Build in-degree map
    in_degree: Dict[str, List[str]] = defaultdict(list)
    for edge in edges:
        src = edge.get("from", edge.get("source", ""))
        dst = edge.get("to", edge.get("target", ""))
        if src and dst:
            in_degree[dst].append(src)

    # Pattern A: multi-parent (in-degree > 1)
    multi_parent = []
    for node, parents in in_degree.items():
        if len(parents) > 1:
            multi_parent.append({
                "node": node,
                "parent_count": len(parents),
                "parents": parents,
                "cross_link_type": "Pattern_A_multi_parent",
                "authority": "Glenn §III.B NSA 사례 — 'increased funds required for software' appears as primary, secondary, and tertiary simultaneously"
            })

    # Pattern B: skip-level (edge skips more than one ring)
    skip_level = []
    for edge in edges:
        src = edge.get("from", "")
        dst = edge.get("to", "")
        src_type = node_meta.get(src, {}).get("type", "unknown").lower()
        dst_type = node_meta.get(dst, {}).get("type", "unknown").lower()
        src_ring = NODE_RING_ORDER.get(src_type, -1)
        dst_ring = NODE_RING_ORDER.get(dst_type, -1)
        if src_ring >= 0 and dst_ring >= 0:
            gap = dst_ring - src_ring
            if gap > 1:
                skip_level.append({
                    "edge": edge,
                    "from_ring": src_ring,
                    "to_ring": dst_ring,
                    "gap": gap,
                    "cross_link_type": "Pattern_B_skip_level",
                    "note": f"Skips {gap-1} ring level(s)"
                })

    # Pattern C: cross-domain links (same ring, different domain)
    cross_domain = []
    for edge in edges:
        src = edge.get("from", "")
        dst = edge.get("to", "")
        src_domain = node_meta.get(src, {}).get("domain", "")
        dst_domain = node_meta.get(dst, {}).get("domain", "")
        src_type = node_meta.get(src, {}).get("type", "").lower()
        dst_type = node_meta.get(dst, {}).get("type", "").lower()
        if (src_domain and dst_domain and src_domain != dst_domain
                and src_type == dst_type):
            cross_domain.append({
                "edge": edge,
                "src_domain": src_domain,
                "dst_domain": dst_domain,
                "ring_level": src_type,
                "cross_link_type": "Pattern_C_cross_domain"
            })

    return {
        "pattern_A_multi_parent": multi_parent,
        "pattern_B_skip_level": skip_level,
        "pattern_C_cross_domain": cross_domain,
        "total_cross_linkages": len(multi_parent) + len(skip_level) + len(cross_domain),
        "has_cross_linkage": (len(multi_parent) + len(skip_level) + len(cross_domain)) > 0,
    }


# ---------------------------------------------------------------------------
# 3. Cycle Detection (DFS)
# ---------------------------------------------------------------------------

def detect_cycles(adj_dict: Dict[str, List[str]]) -> Dict:
    """
    Detect all cycles in a directed graph using DFS (iterative path tracking).
    Glenn §IV: 'higher-order consequences occasionally cycle back to the original item'

    adj_dict: {"node_id": ["neighbor1", "neighbor2", ...], ...}
    Returns list of cycles (each cycle is a list of node_ids forming the loop).
    """
    visited: set = set()
    cycles: List[List[str]] = []

    def dfs(start: str) -> None:
        stack = [(start, [start], {start})]
        while stack:
            node, path, path_set = stack.pop()
            for neighbor in adj_dict.get(node, []):
                if neighbor == start and len(path) >= 2:
                    cycle = path + [neighbor]
                    # Normalize: canonical form (smallest node first)
                    min_idx = cycle.index(min(cycle[:-1]))
                    canonical = cycle[min_idx:-1] + cycle[:min_idx] + [cycle[min_idx]]
                    if canonical not in cycles:
                        cycles.append(canonical)
                elif neighbor not in path_set:
                    stack.append((neighbor, path + [neighbor], path_set | {neighbor}))

    for node in adj_dict:
        if node not in visited:
            dfs(node)
            visited.add(node)

    # Classify each cycle as positive (reinforcing) or negative (balancing)
    # Classification requires sign info — here we report structure only;
    # sign type (positive/negative feedback) must be LLM-determined.
    return {
        "cycles": cycles,
        "cycle_count": len(cycles),
        "note": "Cycle type (positive reinforcing / negative balancing) requires sign context — determined by LLM per Glenn §IV criteria."
    }


# ---------------------------------------------------------------------------
# 4. Graph Metrics
# ---------------------------------------------------------------------------

def graph_metrics(nodes: List[str], edges: List[Dict]) -> Dict:
    """
    Compute graph-level statistics:
      - total_nodes, total_edges
      - graph_density = E / (N*(N-1))
      - fan_out_max, fan_in_max
      - longest_path (DAG longest path; approximate for cyclic graphs)
      - cross_linkage_count (edges where cross_link=True or multi-parent detected)
    """
    if not nodes:
        return {"error": "Empty node list"}

    node_ids = [n["id"] if isinstance(n, dict) else n for n in nodes]
    n = len(node_ids)
    e = len(edges)

    density = round(e / (n * (n - 1)), 4) if n > 1 else 0.0

    fan_out: Dict[str, int] = defaultdict(int)
    fan_in: Dict[str, int] = defaultdict(int)
    cross_link_count = 0

    for edge in edges:
        src = edge.get("from", edge.get("source", ""))
        dst = edge.get("to", edge.get("target", ""))
        if src:
            fan_out[src] += 1
        if dst:
            fan_in[dst] += 1
        if edge.get("cross_link", False):
            cross_link_count += 1

    # Longest path (BFS topological — approximate)
    adj: Dict[str, List[str]] = defaultdict(list)
    for edge in edges:
        src = edge.get("from", "")
        dst = edge.get("to", "")
        if src and dst and edge.get("line", "") != "feedback":
            adj[src].append(dst)

    dist: Dict[str, int] = {n: 0 for n in node_ids}
    for node in node_ids:
        q = deque([node])
        visited = {node}
        depth = 0
        max_depth = 0
        while q:
            for _ in range(len(q)):
                cur = q.popleft()
                for nb in adj.get(cur, []):
                    if nb not in visited:
                        visited.add(nb)
                        q.append(nb)
                        dist[nb] = max(dist.get(nb, 0), dist.get(cur, 0) + 1)
            depth += 1
            max_depth = max(max_depth, depth)

    longest_path = max(dist.values()) if dist else 0

    by_line = defaultdict(int)
    for edge in edges:
        line = edge.get("line", "single")
        by_line[line] += 1

    return {
        "total_nodes": n,
        "total_edges": e,
        "graph_density": density,
        "fan_out_max": max(fan_out.values()) if fan_out else 0,
        "fan_in_max":  max(fan_in.values()) if fan_in else 0,
        "fan_out_distribution": dict(fan_out),
        "fan_in_distribution":  dict(fan_in),
        "longest_path_approx": longest_path,
        "cross_linkage_count": cross_link_count,
        "edges_by_line_type": dict(by_line),
    }


# ---------------------------------------------------------------------------
# 5. Sign Reversal Counting
# ---------------------------------------------------------------------------

REVERSAL_PAIRS = {(+1, -1), (-1, +1)}  # 🟢→🔴 or 🔴→🟢

def count_reversals(sign_sequence: List[Any]) -> Dict:
    """
    Deterministically count sign reversals in a lineage path.

    Definition (세옹지마 전이):
      A reversal = transition +1→-1 OR -1→+1.
      Neutral (0 / 🟡) does NOT count as either +1 or -1 and is EXCLUDED
      from reversal counting (it is neither positive nor negative).

    Accepts: list of +1/-1/0 integers OR 🟢/🔴/🟡 emoji strings.

    Returns: reversal_count, reversal_positions, cleaned_sequence.
    """
    # Normalize to integers
    normalized = []
    for s in sign_sequence:
        if isinstance(s, str):
            v = EMOJI_TO_INT.get(s, None)
            if v is None:
                try:
                    v = int(s)
                except ValueError:
                    v = 0
            normalized.append(v)
        elif isinstance(s, (int, float)):
            normalized.append(int(s))
        else:
            normalized.append(0)

    count = 0
    positions = []
    for i in range(len(normalized) - 1):
        a, b = normalized[i], normalized[i + 1]
        if (a, b) in REVERSAL_PAIRS:
            count += 1
            positions.append({
                "idx": f"{i}→{i+1}",
                "transition": f"{INT_TO_EMOJI[a]}→{INT_TO_EMOJI[b]}",
                "label": "세옹지마 전이 (reversal)"
            })

    return {
        "reversal_count": count,
        "reversal_positions": positions,
        "normalized_int_sequence": normalized,
        "emoji_sequence": [INT_TO_EMOJI.get(v, "🟡") for v in normalized],
        "max_possible_reversals": len(normalized) - 1,
    }


# ---------------------------------------------------------------------------
# 6. Linker SRS Score (consequence-linker 전용 — parent wheel_math.py와 임계값 상이)
# ---------------------------------------------------------------------------

def linker_srs_score(lineages: List[List[Any]]) -> Dict:
    """
    Compute consequence-linker specific SRS from per-lineage sign sequences.

    Thresholds (박사님 2026-05-11 6차 강화 — NOT Glenn 2009):
      excellent  : avg ≥ 2.0
      good       : 1.5 ≤ avg < 2.0
      acceptable : 1.0 ≤ avg < 1.5
      insufficient: avg < 1.0 → REJECT
      excessive  : avg > 3.5 → WARN (wishful thinking)

    NOTE: Parent wheel_math.py uses excellent≥1.5. This file uses excellent≥2.0
    because consequence-linker covers 6 causal layers vs parent's 3-ring baseline.
    """
    if not lineages:
        return {"error": "No lineages provided"}

    per_lineage_results = []
    for i, lg in enumerate(lineages):
        result = count_reversals(lg)
        result["lineage_index"] = i
        per_lineage_results.append(result)

    valid = [r for r in per_lineage_results if len(r.get("normalized_int_sequence", [])) >= 2]
    if not valid:
        return {"error": "No valid lineages (each lineage needs ≥2 signs)"}

    reversals = [r["reversal_count"] for r in valid]
    avg = sum(reversals) / len(reversals)

    if avg > LINKER_SRS_THRESHOLDS["excessive"]:
        status = "WARN"
        classification = "excessive"
        verdict = f"WARN: avg={avg:.2f} > {LINKER_SRS_THRESHOLDS['excessive']} — potential wishful thinking; plausibility re-check required"
    elif avg >= LINKER_SRS_THRESHOLDS["excellent"]:
        status = "PASS"
        classification = "excellent"
        verdict = f"PASS EXCELLENT: avg={avg:.2f} ≥ {LINKER_SRS_THRESHOLDS['excellent']}"
    elif avg >= LINKER_SRS_THRESHOLDS["good"]:
        status = "PASS"
        classification = "good"
        verdict = f"PASS GOOD: avg={avg:.2f} in [{LINKER_SRS_THRESHOLDS['good']}, {LINKER_SRS_THRESHOLDS['excellent']})"
    elif avg >= LINKER_SRS_THRESHOLDS["acceptable"]:
        status = "PASS"
        classification = "acceptable"
        verdict = f"PASS ACCEPTABLE: avg={avg:.2f} in [{LINKER_SRS_THRESHOLDS['acceptable']}, {LINKER_SRS_THRESHOLDS['good']})"
    else:
        status = "REJECT"
        classification = "insufficient"
        verdict = f"REJECT: avg={avg:.2f} < {LINKER_SRS_THRESHOLDS['acceptable']} — insufficient non-linearity"

    return {
        "lineage_count": len(lineages),
        "valid_lineage_count": len(valid),
        "per_lineage_reversals": reversals,
        "avg_srs": round(avg, 4),
        "classification": classification,
        "status": status,
        "verdict": verdict,
        "thresholds": LINKER_SRS_THRESHOLDS,
        "per_lineage_details": valid,
        "export_to": "quality-control Gate 10",
    }


# ---------------------------------------------------------------------------
# 7. Forced Reversal Compliance (P→Q, Q→Qn, Qn→Sn ≥50%)
# ---------------------------------------------------------------------------

def linker_forced_compliance(lineages: List[List[Any]]) -> Dict:
    """
    Check forced reversal compliance for Quaternary/Quinary/Senary transitions.
    박사님 2026-05-11 6차 강화 rule (NOT Glenn 2009):
      - P→Q (ring 3→4, index 2→3): ≥50% of lineages must reverse sign
      - Q→Qn (ring 4→5, index 3→4): ≥50% of lineages must reverse sign
      - Qn→Sn (ring 5→6, index 4→5): ≥50% of lineages must reverse sign

    Rationale: 세옹지마 구조상 T+15~50y 구간에서 한 번 이상의 반전이
    일어나야 직선적 단정(linear extrapolation)에서 벗어난 것으로 인정한다.
    """
    FORCED_TRANSITIONS = [
        {"name": "P→Q (Tertiary→Quaternary)", "from_idx": 2, "to_idx": 3},
        {"name": "Q→Qn (Quaternary→Quinary)", "from_idx": 3, "to_idx": 4},
        {"name": "Qn→Sn (Quinary→Senary)",    "from_idx": 4, "to_idx": 5},
    ]

    # Normalize all lineages to int
    normalized_lgs = []
    for lg in lineages:
        result = count_reversals(lg)
        normalized_lgs.append(result["normalized_int_sequence"])

    compliance_results = {}
    overall_pass = True

    for trans in FORCED_TRANSITIONS:
        fname = trans["name"]
        fi, ti = trans["from_idx"], trans["to_idx"]
        eligible = 0
        reversed_count = 0
        for lg in normalized_lgs:
            if len(lg) > ti:
                eligible += 1
                a, b = lg[fi], lg[ti]
                if (a, b) in REVERSAL_PAIRS:
                    reversed_count += 1
        rate = reversed_count / eligible if eligible > 0 else 0.0
        passed = rate >= 0.50
        if not passed:
            overall_pass = False
        compliance_results[fname] = {
            "eligible_lineages": eligible,
            "reversed": reversed_count,
            "rate": round(rate, 4),
            "required": 0.50,
            "status": "PASS" if passed else "FAIL",
        }

    return {
        "forced_reversal_compliance": compliance_results,
        "overall_pass": overall_pass,
        "verdict": "PASS" if overall_pass else "FAIL — one or more forced reversal transitions < 50%",
        "authority": "박사님 2026-05-11 6차 강화 (consequence-linker 전용 규칙; NOT from Glenn 2009)",
    }


# ---------------------------------------------------------------------------
# CLI dispatch
# ---------------------------------------------------------------------------

_COMMANDS = {
    "adjacency_matrix":        lambda a: adjacency_matrix(a["nodes"], a["edges"]),
    "detect_cross_linkages":   lambda a: detect_cross_linkages(a["nodes"], a["edges"]),
    "detect_cycles":           lambda a: detect_cycles(a["adj"]),
    "graph_metrics":           lambda a: graph_metrics(a["nodes"], a["edges"]),
    "count_reversals":         lambda a: count_reversals(a["signs"]),
    "linker_srs_score":        lambda a: linker_srs_score(a["lineages"]),
    "linker_forced_compliance": lambda a: linker_forced_compliance(a["lineages"]),
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        print("\nAvailable commands:", list(_COMMANDS.keys()))
        sys.exit(0)

    command = sys.argv[1]
    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}

    if command not in _COMMANDS:
        result = {"error": f"Unknown command: {command!r}", "available": list(_COMMANDS.keys())}
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)

    try:
        result = _COMMANDS[command](args)
    except Exception as e:
        result = {"error": str(e), "command": command, "args": args}
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
