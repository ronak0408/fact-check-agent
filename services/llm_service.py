import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

MODEL_NAME = "openai/gpt-3.5-turbo"

def ask_llm(prompt):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


def extract_claims(text):

    prompt = f"""
    You are an advanced AI fact-checking assistant.

    Extract ALL factual claims from the text below.

    IMPORTANT:
    Focus especially on:
    - statistics
    - percentages
    - financial figures
    - dates
    - technical specifications
    - scientific claims
    - market size claims
    - growth metrics
    - company/user numbers

    DO NOT skip:
    - short claims
    - single-sentence facts
    - numerical claims

    Return ONLY valid JSON array.

    Example:
    [
    {{
        "claim": "India's internet penetration reached 95% in 2024",
        "category": "statistics"
    }},
    {{
        "claim": "OpenAI was founded in 2018",
        "category": "history"
    }}
    ]

    TEXT:
    {text[:4000]}
    """

    response = ask_llm(prompt)

    clean_json = response.replace("```json", "").replace("```", "").strip()

    extracted_claims = []

    # Try LLM extraction
    try:
        extracted_claims = json.loads(clean_json)

    except Exception:
        extracted_claims = []

    # Sentence-based fallback/merge
    sentences = text.split(".")

    for sentence in sentences:

        sentence = sentence.strip()

        if len(sentence) < 10:
            continue

        already_exists = False

        for item in extracted_claims:

            if sentence.lower() in item["claim"].lower():
                already_exists = True
                break

        if not already_exists:

            extracted_claims.append({
                "claim": sentence,
                "category": "general"
            })

    return extracted_claims[:10]


def verify_claim(claim, evidence):

    prompt = f"""
    You are a professional fact-checking AI.

    Your task is to compare a CLAIM against WEB EVIDENCE.

    You MUST classify the claim using these strict rules:

    - VERIFIED:
    The evidence clearly supports the claim.

    - INACCURATE:
    The claim contains a small factual error, outdated number/date, exaggeration, or misleading detail, but the overall topic/entity is real.

    - FALSE:
    The claim is fundamentally untrue, strongly contradicted by evidence, or unsupported by trustworthy sources.

    For numerical/statistical claims:
    - verify numbers carefully
    - outdated statistics should be marked INACCURATE
    - exaggerated metrics should NOT be VERIFIED
    - compare dates and years carefully

    IMPORTANT RULES:
    - Be strict and logical.
    - Do NOT mark incorrect claims as VERIFIED.
    - If numbers, dates, or statistics differ slightly, use INACCURATE.
    - If the entire claim is clearly wrong, use FALSE.
    - Use realistic confidence values.
    - Do NOT always return 100% confidence.
    - Confidence should usually range between 50% and 98% depending on evidence quality.

    CLAIM:
    {claim}

    EVIDENCE:
    {evidence}

    Return ONLY valid JSON in this exact format:

    {{
    "verdict": "VERIFIED",
    "explanation": "Short explanation based on evidence",
    "corrected_fact": "Provide the correct fact here",
    "confidence": "82%"
    }}
    """

    response = ask_llm(prompt)

    clean_json = response.replace("```json", "").replace("```", "").strip()

    result = json.loads(clean_json)

    # Normalize values
    verdict = result["verdict"].upper()
    explanation = result["explanation"].lower()
    corrected_fact = result["corrected_fact"].lower()
    claim_lower = claim.lower()

    # Strong contradiction detection
    if verdict == "VERIFIED":

        contradiction_keywords = [
            "incorrect",
            "wrong",
            "false",
            "inaccurate",
            "not",
            "actually",
            "however"
        ]

        contradiction_found = any(
            word in explanation for word in contradiction_keywords
        )

        # If corrected fact differs from claim
        corrected_differs = (
            corrected_fact not in ["n/a", "none", "", claim_lower]
            and corrected_fact not in claim_lower
        )

        if contradiction_found or corrected_differs:

            # Determine severity
            if any(
                word in explanation
                for word in ["false", "wrong", "not", "incorrect"]
            ):
                result["verdict"] = "FALSE"

            else:
                result["verdict"] = "INACCURATE"

    return result