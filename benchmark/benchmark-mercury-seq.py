import requests
import time
import argparse

def get_prompts():
    prompts = [
        "Write a short story about a cat who learns to fly.",
        "Explain the theory of relativity in simple terms.",
        "Create a poem about the sea.",
        "Describe a day in the life of a space explorer.",
        "Write a dialogue between two friends discussing their favorite books.",
        "Explain how quantum computing works.",
        "Create a recipe for a new dish.",
        "Describe a futuristic city.",
        "Write a letter to your future self.",
        "Explain the importance of biodiversity."
    ]
    return prompts

def main():
    parser = argparse.ArgumentParser(description='Test OpenAI REST service.')
    parser.add_argument('--url', required=True, help='OpenAI API URL')
    parser.add_argument('--api_key', required=True, help='OpenAI API key')
    parser.add_argument('--model', required=True, help='Model name')
    parser.add_argument('--num_requests', type=int, default=10, help='Number of requests to send')

    args = parser.parse_args()

    min_wps = float('inf')
    max_wps = 0
    total_wps = 0
    valid_requests = 0

    prompts = get_prompts()

    for i in range(min(args.num_requests, len(prompts))):
        prompt = prompts[i]
        headers = {'Authorization': f'Bearer {args.api_key}'}
        data = {
            'prompt': prompt,
            'max_tokens': 100,
            'model': args.model
        }

        start_time = time.time()
        response = requests.post(args.url, headers=headers, json=data)
        end_time = time.time()

        if response.status_code == 200:
            response_text = response.json().get('choices', [{}])[0].get('text', '')
            word_count = len(response_text.split())
            time_taken = end_time - start_time
            wps = word_count / time_taken if time_taken > 0 else 0

            min_wps = min(min_wps, wps)
            max_wps = max(max_wps, wps)
            total_wps += wps
            valid_requests += 1
        else:
            print(f"Request {i+1} failed with status code: {response.status_code}")

    if valid_requests > 0:
        avg_wps = total_wps / valid_requests
    else:
        avg_wps = 0

    print(f"Minimum words per second: {min_wps:.2f}")
    print(f"Maximum words per second: {max_wps:.2f}")
    print(f"Average words per second: {avg_wps:.2f}")

if __name__ == '__main__':
    main()
