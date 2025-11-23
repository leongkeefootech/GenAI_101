import os
import json
import requests
from typing import List, Dict, Any, Optional
from requests.exceptions import RequestException

def _call_chat_api(messages: List[Dict[str, str]], *,
                   model: str = "gpt-3.5-turbo",
                   api_key: Optional[str] = None,
                   timeout: float = 10.0) -> str:
    """
    Send messages to the Chat Completions endpoint and return assistant content.

    Returns empty string on failure.
    """
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "ERROR: OPENAI_API_KEY not provided"

    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"model": model, "messages": messages, "max_tokens": 512, "temperature": 0.0}
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
        resp.raise_for_status()
        j = resp.json()
        choice = (j.get("choices") or [None])[0]
        if isinstance(choice, dict):
            return choice.get("message", {}).get("content", "") or ""
        return ""
    except RequestException as e:
        return f"ERROR: API request failed: {e}"

def demo_system_role_effects(user_prompt: str, *,
                             api_key: Optional[str] = None,
                             model: str = "gpt-3.5-turbo") -> str:
    """
    Demonstrate how different system role messages affect the LLM output.

    The function sends the same user prompt in three scenarios:
      - no_system: user message only
      - helpful_system: system instructs to be a helpful concise assistant
      - strict_system: system enforces a strict JSON-only response

    Returns:
        str: JSON string containing the three assistant responses under keys:
             no_system, helpful_system, strict_system
    """
    scenarios = {
        "no_system": [
            {"role": "user", "content": user_prompt}
        ],
        "helpful_system": [
            {"role": "system", "content": "You are a helpful assistant. Answer concisely."},
            {"role": "user", "content": user_prompt}
        ],
        "strict_system": [
            {"role": "system", "content": "You are a strict assistant. Respond ONLY with a JSON object: {\"answer\": <string>, \"note\": <string>} and no other text."},
            {"role": "user", "content": user_prompt}
        ],
        "chaos_system": [
            {"role": "system", "content": "You are a clown. Describe the prompt in a humorous way."},
            {"role": "user", "content": user_prompt}
        ],
        "shakespear_system": [
            {"role": "system", "content": "You are a philosopher. Answer in a thoughtful and profound manner."},
            {"role": "user", "content": user_prompt}
        ]
    }

    results: Dict[str, Any] = {}
    for name, messages in scenarios.items():
        # call API; prefer provided api_key if given
        content = _call_chat_api(messages, model=model, api_key=api_key)
        results[name] = {"messages": messages, "assistant": content}

    return json.dumps(results, indent=2, ensure_ascii=False)

# Example usage (run as script):
if __name__ == "__main__":
    sample_prompt = "Provide a short summary of: Customer John Doe, email john@example.com, age 34."
    print("Demoing system role effects...\n")
    print(demo_system_role_effects(sample_prompt))
