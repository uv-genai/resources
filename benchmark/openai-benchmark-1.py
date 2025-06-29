# MODEL: chatgpt4-o1-mini
# Usage: python openai-benchmark-1.py <endpoint> <api_key> <model> <num_requests>
# PROMPT:Generate a Python script to test an OpenAI REST service. The script must send requests in a loop, selecting one of ten random requests each time. The number of tokens per second of each request must be timed and reported in JSON format: {"prompt": , "result": , "tokens-per-second": }. The endpoint URL, API key and number of requests must be specified on the command line.
# Add type hints
# Add command line argument to specify the model
import requests
import time
import random
import json
import argparse
from typing import List, Dict, Optional, Any

# Define five random prompts for testing
PROMPTS: List[str] = [
    "What is the capital of France?",
    "Explain the theory of relativity.",
    "What are the benefits of meditation?",
    "Generate a short story about a dragon.",
    "What is the meaning of life?",
    "Describe the process of photosynthesis.",
    "What are the latest advancements in AI?",
    "How do you make a perfect cup of coffee?",
    "List some effective time management techniques.",
    "What is the significance of the Turing Test?"
]


def call_openai_api(
    endpoint: str, api_key: str, model: str, prompt: str
) -> Optional[Dict[str, Any]]:
    headers: Dict[str, str] = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload: Dict[str, Any] = {
        "model": model,  # Use the model specified in the command line
        "prompt": prompt,
        "max_tokens": 150,  # Adjust max_tokens as needed
    }

    response = requests.post(endpoint, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return None

    return response.json()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("endpoint", help="The OpenAI API endpoint URL")
    parser.add_argument("api_key", help="Your OpenAI API key")
    parser.add_argument("model", help="Specify the model to use")
    parser.add_argument("num_requests", type=int, help="Number of requests to send")
    args = parser.parse_args()

    results: List[Dict[str, Any]] = []

    for _ in range(args.num_requests):
        prompt: str = random.choice(PROMPTS)
        start_time: float = time.time()

        response_json: Optional[Dict[str, Any]] = call_openai_api(
            args.endpoint, args.api_key, args.model, prompt
        )

        if response_json:
            end_time: float = time.time()
            # Calculate tokens per second
            tokens_per_second: float = len(
                response_json.get("choices")[0].get("text").split()
            ) / (end_time - start_time)

            result_entry: Dict[str, Any] = {
                "prompt": prompt,
                "result": response_json.get("choices")[0].get("text"),
                "tokens-per-second": tokens_per_second,
            }
            results.append(result_entry)

    print(json.dumps(results, indent=4))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
