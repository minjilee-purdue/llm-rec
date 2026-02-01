import json
import os
from anthropic import Anthropic

# --- Config ---
DATA_PATH = "data/preference.json"
PROMPT_PATH = "prompts/recommend.txt"
OUTPUT_DIR = "outputs"
MODEL = "claude-sonnet-4-20250514"

client = Anthropic()


def load_prompt(prompt_path: str) -> str:
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()


def split_prompt(prompt_text: str) -> tuple[str, str]:
    """[SYSTEM]과 [USER WATCH PROFILE] 기준으로 system / user 분리"""
    system_section = prompt_text.split("[USER WATCH PROFILE]")[0].replace("[SYSTEM]", "").strip()
    user_section = "[USER WATCH PROFILE]" + prompt_text.split("[USER WATCH PROFILE]")[1]
    return system_section, user_section


def get_recommendations(system_prompt: str, user_prompt: str) -> list[dict]:
    response = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )

    raw = response.content[0].text.strip()

    # JSON array parsing
    parsed = json.loads(raw)
    return parsed


def save_output(recommendations: list[dict], output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)

    # time-stamp generation
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(output_dir, f"recommendations_{timestamp}.json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(recommendations, f, ensure_ascii=False, indent=2)

    return out_path


def main():
    # 1. prompt load 
    prompt_text = load_prompt(PROMPT_PATH)
    system_prompt, user_prompt = split_prompt(prompt_text)

    print("=== System Prompt ===")
    print(system_prompt[:200] + "...\n")

    print("=== Sending to Claude API ===\n")

    # 2. API call
    recommendations = get_recommendations(system_prompt, user_prompt)

    # 3. print the result
    print("=== Recommendations ===")
    print(json.dumps(recommendations, ensure_ascii=False, indent=2))

    # 4. save
    out_path = save_output(recommendations, OUTPUT_DIR)
    print(f"\n=== Saved to {out_path} ===")


if __name__ == "__main__":
    main()
