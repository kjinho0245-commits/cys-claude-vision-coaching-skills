#!/usr/bin/env python3
"""결정론적 Jaccard 비유사도 계산 — LLM 판단 대체.

Usage:
    python3 calculate_divergence.py --input <path_to_json>

Input JSON format:
    {
      "scenarios": [
        ["feature1", "feature2", "feature3"],   // scenario 0
        ["feature2", "feature4", "feature5"],   // scenario 1
        ...
      ]
    }

Output JSON:
    {
      "pairwise_scores": [...],
      "overall_divergence_score": 0.xxxx,
      "interpretation": "..."
    }

Exit codes:
    0 = success
    1 = error
"""
import json
import sys
import argparse
from itertools import combinations


def normalize_feature(f: str) -> str:
    """feature 정규화: 소문자, 앞뒤 공백 제거, 하이픈/언더스코어를 공백으로 통일."""
    return str(f).strip().lower().replace("-", " ").replace("_", " ")


def jaccard_dissimilarity(set_a: set, set_b: set) -> float:
    """
    Jaccard 비유사도 공식: score = 1 - |A ∩ B| / |A ∪ B|
    결과 범위: 0.0 (완전 동일) ~ 1.0 (완전 상이)
    두 집합 모두 비어있으면 0.0 반환.
    """
    if not set_a and not set_b:
        return 0.0
    union_size = len(set_a | set_b)
    if union_size == 0:
        return 0.0
    intersection_size = len(set_a & set_b)
    return round(1.0 - intersection_size / union_size, 4)


def interpret_score(score: float) -> str:
    if score < 0:
        return "calculation error"
    if score < 0.2:
        return "near-identical (scenarios converge)"
    if score < 0.4:
        return "low divergence"
    if score < 0.6:
        return "moderate divergence"
    if score < 0.8:
        return "high divergence (critical branch — escalate to master)"
    return "extreme divergence"


def calculate_overall_divergence(scenarios_features: list) -> dict:
    """
    입력: 각 시나리오의 features 리스트의 리스트 (list of list of str)
    출력: pairwise Jaccard scores + overall_divergence_score

    overall_divergence_score = 모든 pair Jaccard 비유사도의 산술 평균
    """
    if not isinstance(scenarios_features, list):
        return {"error": "scenarios must be a list", "overall_divergence_score": -1}

    if len(scenarios_features) < 2:
        return {
            "error": "at least 2 scenarios required for divergence calculation",
            "overall_divergence_score": -1,
        }

    # 정규화된 feature 집합 생성
    sets = []
    for i, feats in enumerate(scenarios_features):
        if not isinstance(feats, list):
            return {
                "error": f"scenarios[{i}] must be a list of strings",
                "overall_divergence_score": -1,
            }
        sets.append(set(normalize_feature(f) for f in feats if f))

    # Pairwise 계산
    pairwise = []
    for i, j in combinations(range(len(sets)), 2):
        score = jaccard_dissimilarity(sets[i], sets[j])
        intersection = sorted(sets[i] & sets[j])
        union = sorted(sets[i] | sets[j])
        pairwise.append({
            "scenario_i": i,
            "scenario_j": j,
            "jaccard_dissimilarity": score,
            "shared_features": intersection,
            "shared_count": len(intersection),
            "union_count": len(union),
        })

    # Overall score = 모든 pair 평균
    overall = round(
        sum(p["jaccard_dissimilarity"] for p in pairwise) / len(pairwise), 4
    )

    return {
        "pairwise_scores": pairwise,
        "overall_divergence_score": overall,
        "interpretation": interpret_score(overall),
        "num_scenarios": len(sets),
        "num_pairs": len(pairwise),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Deterministic Jaccard divergence score for scenario feature sets"
    )
    parser.add_argument(
        "--input",
        required=True,
        help='Path to JSON file: {"scenarios": [[feat1,...], [feat1,...], ...]}',
    )
    args = parser.parse_args()

    try:
        with open(args.input, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(json.dumps({"error": f"File not found: {args.input}", "overall_divergence_score": -1}))
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"JSON parse error: {e}", "overall_divergence_score": -1}))
        sys.exit(1)

    if "scenarios" not in data:
        print(json.dumps({"error": "JSON must contain 'scenarios' key", "overall_divergence_score": -1}))
        sys.exit(1)

    result = calculate_overall_divergence(data["scenarios"])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result.get("overall_divergence_score", -1) >= 0 else 1)


if __name__ == "__main__":
    main()
