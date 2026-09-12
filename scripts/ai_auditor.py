import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def get_ai_judgment(facts):
    system_prompt = """You are a Senior Website Quality Auditor specializing in the Education Sector.
You will receive JSON data extracted from an educational website's homepage.
Your job is to:
1. Score the site 0-100 on "Professionalism, Completeness, and Business Readiness"
2. Identify missing features (based ONLY on the provided facts)
3. Provide specific, actionable recommendations (not generic advice)
4. Assign a priority level (High / Medium / Low)

STRICT RULES:
- Base every judgment ONLY on the provided facts. Do not invent data.
- Recommendations must be specific. Bad: "Improve SEO". Good: "Add a meta description tag under 160 characters summarizing the course catalog."
- Output ONLY valid JSON. No explanation text outside JSON."""

    user_prompt = f"""Here is the extracted facts for a website:

{json.dumps(facts, indent=2)}

Return a JSON object with this exact schema:
{{
  "score": <integer 0-100>,
  "score_reasoning": "<one sentence explaining the score>",
  "missing_features": ["<feature 1>", "<feature 2>"],
  "recommendations": ["<specific action 1>", "<specific action 2>"],
  "priority": "<High | Medium | Low>"
}}"""

    response = client.chat.completions.create(
model="groq/compound-mini",

       
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.3
    )

    return json.loads(response.choices[0].message.content)


def main():
    with open("data/raw_facts.json", "r", encoding="utf-8") as f:
        all_facts = json.load(f)

    print(f"Loaded {len(all_facts)} website records.\n")

    final_results = []

    for entry in all_facts:
        url = entry["url"]
        print(f"AI is judging: {url}")

        if entry["status"] != "success":
            entry["ai_judgment"] = {
                "score": None,
                "score_reasoning": "Site could not be scraped (blocked or error).",
                "missing_features": [],
                "recommendations": ["Manual review required - scraper was blocked."],
                "priority": "High"
            }
            print("   Skipped (scrape failed)\n")
            final_results.append(entry)
            continue

        try:
            judgment = get_ai_judgment(entry["data"])
            entry["ai_judgment"] = judgment
            print(f"   Score: {judgment['score']}/100")
            print(f"   Priority: {judgment['priority']}")
            print(f"   Recommendations: {len(judgment['recommendations'])}\n")
        except Exception as e:
            print(f"   AI Error: {str(e)}\n")
            entry["ai_judgment"] = {
                "score": None,
                "score_reasoning": f"AI error: {str(e)}",
                "missing_features": [],
                "recommendations": [],
                "priority": "N/A"
            }

        final_results.append(entry)

    with open("data/ai_judgments.json", "w", encoding="utf-8") as f:
        json.dump(final_results, f, indent=2, ensure_ascii=False)

    print("Done! AI judgments saved to data/ai_judgments.json")


if __name__ == "__main__":
    main()