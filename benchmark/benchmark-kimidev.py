import argparse
import requests
import time
import random

def main():
    parser = argparse.ArgumentParser(description="Test OpenAI REST service performance.")
    parser.add_argument("--endpoint", required=True,
                        help="Base URL of OpenAI REST service")
    parser.add_argument("--api-key", required=True,
                        help="API Key for authentication")
    parser.add_argument("--model", required=True,
                        help="Model name to use")
    parser.add_argument("--num-requests", type=int, default=10,
                        help="Number of test requests")

    args = parser.parse_args()

     # Generate realistic test prompts simulating user queries 
     action_verbs=["Explain","Describe","Compare","Analyze"]
     topics=["Artificial Intelligence","Climate Change",
             ,"Quantum Computing","Genetics",
             ,"Economics","Space Exploration",
             ,"Cybersecurity"]

     def generate_prompt():
         return f"{random.choice(action_verbs)}: What are key aspects of {random.choice(topics)}?"

     # Create N unique-ish test cases 
     prompts=[generate_prompt() for _ in range(args.num_requests)]

     total_tokens_processed=0
     cumulative_response_time_seconds=0

      # Prepare headers once outside loop 
      headers={
          'Authorization':f'Bearer {args.api_key}',
          'Content-Type':'application/json'
      }

      # Iterate through each generated prompt 
      for idx,prompt_text in enumerate(prompts):
          start_timestamp=time.time() 

          try:
              # Construct payload based on Chat Completions API format 
              payload={
                  'model':args.model,
                  'messages':[{'role':'user','content':prompt_text}],
                  # Optional parameters can go here e.g., max_token etc.
              }

              # Make POST call 
              resp=requests.post(
                  url=f"{args.endpoint}/v1/chat/completions",
                  headers=headers,
                  json=payload,
                  timeout=30   # Add timeout prevent hanging indefinitely 
              )
              
              resp.raise_for_status()   # Raise HTTPError exceptions early 

              json_response=resp.json()

              # Extract token count from usage metadata 
              usage_data=json_response.get('usage')
              if usage_data:
                  current_token_count=usage_data.get('total_tokens',0)
                  print(f"[Request {idx+1}] Processed '{prompt_text}' | Tokens Used:{current_token_count}")
                  total_tokens_processed+=current_token_count

          except Exception as e:
               print(f"[Request {idx+1}] Error occurred while processing '{prompt_text}':{str(e)}")

          finally:
               end_timestamp=time.time()
               elapsed_seconds=end_timestamp-start_timestamp 
               cumulative_response_time_seconds+=elapsed_seconds 

      avg_tps=(total_tokens_processed/cumulative_response_time_seconds) \
                if cumulative_response_time_seconds>0 else float('nan')

      print(f"\nTotal Tokens Processed:{total_tokens_processed}")
      print(f"Cumulative Response Time(s):{cumulative_response_time_seconds:.2f}s")
      print(f"Average Tokens Per Second:{avg_tps:.2f}")

if __name__ == "__main__":
   main()
