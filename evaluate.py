import json
import os
import glob
from datetime import datetime

OUTPUT_DIR = "outputs"
RATING_ORDER = ["very_liked", "liked", "okay_neutral", "disliked"]


def load_latest_recommendation() -> tuple[str, list[dict]]:
    """Load the most recent recommendation file from outputs/"""
    files = glob.glob(os.path.join(OUTPUT_DIR, "recommendations_*.json"))
    if not files:
        raise FileNotFoundError("No recommendation files found in outputs/")

    latest = sorted(files)[-1]
    with open(latest, "r", encoding="utf-8") as f:
        data = json.load(f)

    return latest, data


def prompt_actual_ratings(recommendations: list[dict]) -> list[dict]:
    """Prompt the user to input their actual rating for each recommendation"""
    print("\n=== Rate each recommendation ===")
    print("Options: very_liked / liked / okay_neutral / disliked / skip\n")

    for i, item in enumerate(recommendations):
        print(f"[{i+1}] {item['title']}")
        print(f"    Predicted: {item['predicted_rating']}")
        print(f"    Reasoning: {item.get('reasoning', 'N/A')}")

        while True:
            raw = input("    Your rating: ").strip().lower()
            if raw in RATING_ORDER or raw == "skip":
                break
            print(f"    Invalid. Choose from: {', '.join(RATING_ORDER)}, skip")

        if raw == "skip":
            item["actual_rating"] = None
        else:
            item["actual_rating"] = raw

        print()

    return recommendations


def evaluate(recommendations: list[dict]) -> dict:
    """Compare predicted vs actual ratings and generate a summary"""
    evaluated = [r for r in recommendations if r.get("actual_rating") is not None]

    if not evaluated:
        return {"error": "No items were rated."}

    correct = sum(1 for r in evaluated if r["predicted_rating"] == r["actual_rating"])
    total = len(evaluated)

    # Measure the gap between predicted and actual as level differences
    # e.g. very_liked -> liked = 1 level off
    diffs = []
    for r in evaluated:
        pred_idx = RATING_ORDER.index(r["predicted_rating"])
        actual_idx = RATING_ORDER.index(r["actual_rating"])
        diffs.append(abs(pred_idx - actual_idx))

    summary = {
        "total_rated": total,
        "exact_match": correct,
        "exact_match_rate": f"{correct / total * 100:.1f}%",
        "avg_level_diff": f"{sum(diffs) / len(diffs):.2f}",  # 0 = perfect, 1 = 1 level off, ...
        "details": [
            {
                "title": r["title"],
                "predicted": r["predicted_rating"],
                "actual": r["actual_rating"],
                # positive = over-predicted, negative = under-predicted
                "level_diff": RATING_ORDER.index(r["predicted_rating"]) - RATING_ORDER.index(r["actual_rating"])
            }
            for r in evaluated
        ]
    }

    return summary


def save_evaluated(recommendations: list[dict], summary: dict, source_file: str) -> str:
    """Save the evaluation results to outputs/"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(OUTPUT_DIR, f"evaluated_{timestamp}.json")

    output = {
        "source": os.path.basename(source_file),
        "evaluated_at": timestamp,
        "summary": summary,
        "recommendations": recommendations
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    return out_path


def main():
    # 1. Load the latest recommendation output
    source_file, recommendations = load_latest_recommendation()
    print(f"Loaded: {source_file} ({len(recommendations)} items)")

    # 2. Collect actual ratings from user
    recommendations = prompt_actual_ratings(recommendations)

    # 3. Run evaluation
    summary = evaluate(recommendations)

    # 4. Print results
    print("=== Evaluation Summary ===")
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    # 5. Save to outputs/
    out_path = save_evaluated(recommendations, summary, source_file)
    print(f"\n=== Saved to {out_path} ===")


if __name__ == "__main__":
    main()
