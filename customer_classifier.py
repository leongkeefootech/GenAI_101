import os
from typing import Any, Dict, Optional
import requests
import sys
import json
import re
import time
from requests.exceptions import RequestException

attributes_metadata = """List of attributes:
        Filter attribute: Rel ID, Customer ID
        EBBS attributes: date_of_birth, age, last_name, first_name
        ICM attributes: phone_number, email, primary_address
        ECDD attributes: risk_score, credit_rating, kyc_status

        Output format:
        Rel ID = <rel_id>
        Customer ID = <customer_id>
        EBBS attribute = [<comma separated attributes>]
        ICM attribute = [<comma separated attributes>]
        ECDD attribute = [<comma separated attributes>]
        UNKNOWN attribute = [<comma separated attributes>]"""

def extract_attributes_via_llm(prompt: str,
                                *,
                                api_key: Optional[str] = None,
                                model: str = "gpt-3.5-turbo",
                                timeout: float = 10.0) -> str:
    """
    Use the LLM classifier to extract attributes according to attributes_metadata,
    returning them in the required output format. Falls back to a simple rule-based
    extractor if the LLM response is missing expected sections.
    """

    # Try LLM first
    try:
        llm_output = classify_user_prompt_via_llm(prompt, api_key=api_key, model=model, timeout=timeout)
    except Exception:
        llm_output = ""

    llm_output = (llm_output or "").strip()
    # basic validation: check presence of required headings (case-insensitive)
    required_keys = ["rel id", "customer id", "ebbs attribute", "icm attribute", "ecdd attribute", "unknown attribute"]
    if llm_output and all(k in llm_output.lower() for k in required_keys):
        # return LLM output as-is (cleaned)
        return llm_output

    # Fallback rule-based extractor
    groups = {
        "EBBS attribute": ["date_of_birth", "age", "last_name", "first_name"],
        "ICM attribute": ["phone_number", "email", "primary_address"],
        "ECDD attribute": ["risk_score", "credit_rating", "kyc_status"],
    }
    found = {k: [] for k in groups}
    unknown = set()

    # Detect rel id: patterns like "rel id 123", "rel_id=123", "relid: 123"
    rel_id = ""
    m = re.search(r"rel[\s_\-]*id[:=]?\s*([A-Za-z0-9\-\_]+)", prompt, flags=re.IGNORECASE)
    if m:
        rel_id = m.group(1)

    # Search for each known attribute by name or by common synonyms/values
    for grp, attrs in groups.items():
        for attr in attrs:
            # look for the attribute name literally
            if re.search(r"\b" + re.escape(attr) + r"\b", prompt, flags=re.IGNORECASE):
                found[grp].append(attr)

    # heuristic detections for values that imply an attribute even if name not present
    # email
    if re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", prompt):
        if "email" not in found["ICM attribute"]:
            found["ICM attribute"].append("email")
    # phone
    if re.search(r"(?:\+?\d[\d\-\s\(\)]{6,}\d)", prompt):
        if "phone_number" not in found["ICM attribute"]:
            found["ICM attribute"].append("phone_number")
    # date of birth (simple date)
    if re.search(r"\b(?:\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{2,4})\b", prompt):
        if "date_of_birth" not in found["EBBS attribute"]:
            found["EBBS attribute"].append("date_of_birth")
    # age
    if re.search(r"\b(?:age[:\s]*\d{1,3}|\b\d{1,3}\s+years?\b)", prompt, flags=re.IGNORECASE):
        if "age" not in found["EBBS attribute"]:
            found["EBBS attribute"].append("age")

    # collect unknown tokens: any attribute-like tokens that were mentioned but not matched
    # look for words with underscore or hyphen that are short and might be attribute names
    tokens = re.findall(r"\b[a-zA-Z_]{3,30}\b", prompt)
    known_attrs = {a for attrs in groups.values() for a in attrs} | {"rel", "id", "relid", "rel_id"}
    for t in tokens:
        tt = t.lower()
        if tt in known_attrs:
            continue
        # if token looks like an attribute (contains underscore) or matches common attribute words
        if "_" in tt or tt in {"kyc", "kyc_status", "credit", "rating", "risk", "primary_address"}:
            unknown.add(tt)

    # Format output exactly as required
    def fmt_list(lst):
        return "[" + ", ".join(lst) + "]" if lst else "[]"

    ebbs_list = found["EBBS attribute"]
    icm_list = found["ICM attribute"]
    ecdd_list = found["ECDD attribute"]
    unknown_list = sorted(list(unknown))

    output_lines = [
        f"Rel ID = {rel_id}" if rel_id else "Rel ID = ",
        f"EBBS attribute = {fmt_list(ebbs_list)}",
        f"ICM attribute = {fmt_list(icm_list)}",
        f"ECDD attribute = {fmt_list(ecdd_list)}",
        f"UNKNOWN attribute = {fmt_list(unknown_list)}",
    ]
    return "\n".join(output_lines)


def classify_user_prompt_via_llm(prompt: str,
                                 *,
                                 api_key: Optional[str] = None,
                                 model: str = "gpt-3.5-turbo",
                                 timeout: float = 10.0) -> str:
    """
    Call the OpenAI Chat Completions endpoint to extract attributes using the
    instructions in attributes_metadata. Returns the assistant content (raw),
    or an empty string on failure so the caller can fall back to local rules.
    """
    if not prompt or not prompt.strip():
        raise ValueError("prompt must be a non-empty string")

    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key required (pass api_key or set OPENAI_API_KEY)")

    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    system_prompt = (
        "You are a strict extractor. Follow the Output format exactly and only output "
        "the lines described (no extra explanation). Use the attribute lists provided "
        "to map tokens to each category. If you cannot map something, put it under "
        "UNKNOWN attribute. Do not invent values that are not present in the user prompt."
    )

    llm_user_prompt = attributes_metadata + "\n\nExtract attributes from this user prompt:\n\n" + prompt

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": llm_user_prompt},
        ],
        # provide enough tokens for a small structured response
        "max_tokens": 512,
        "temperature": 0.0,
    }


    # simple retry for transient rate limits
    tries = 2
    backoff = 1.0
    for attempt in range(tries):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
            resp.raise_for_status()
            j = resp.json()
            # Chat Completions: choices[*].message.content
            content = ""
            try:
                choice = (j.get("choices") or [None])[0]
                if isinstance(choice, dict):
                    # new chat response shape
                    content = choice.get("message", {}).get("content") or choice.get("text") or ""
                else:
                    content = ""
            except Exception:
                content = ""
            return (content or "").strip()
        except RequestException as e:
            # retry on rate limit or server errors once
            status = getattr(getattr(e, "response", None), "status_code", None)
            if attempt + 1 < tries and status in (429, 502, 503, 504):
                time.sleep(backoff)
                backoff *= 2
                continue
            # on any other failure return empty so caller uses rule-based fallback
            return ""

if __name__ == "__main__":
    # simple CLI for testing
    if len(sys.argv) < 2:
        print("Usage: python customer_classifier.py '<prompt>'")
        sys.exit(1)

    user_prompt = sys.argv[1]
    try:
        output = extract_attributes_via_llm(user_prompt)
        print(json.dumps(output, indent=4, ensure_ascii=False).replace('\\n', '\n'))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)