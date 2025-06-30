import openai
import time
import os
import json
from random import randint
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Set up configuration from environment variables or command line arguments
    config = {
        'temperature': 0,
        'max_tokens': 1000,
        'n': 1,
        'api_key': os.getenv('OPENAI_API_KEY'),
    }

    # Parse command line arguments if any (optional)
    import sys
    args = sys.argv[1:]
    if len(args) > 0:
        # This is just an example; you'd need proper argument parsing here
        pass

    # Initialize counters
    total_tokens = 0
    total_time = 0

    # Number of tests to run through the service
    num_tests = int(input("Enter number of tests: ")) 

    start_time = time.time()

    try:
        openai.api_key = config['api_key']
        
        # Generate some random prompts or use fixed ones depending on your needs
        
        # Example fixed prompt setup:
        fixed_prompts = [
            "Explain quantum computing concepts.",
            "Write a short story about artificial intelligence.",
            "How does photosynthesis work?"
        ]
        
        # For more dynamic testing you can add more prompts
        
        # Start testing loop over specified number of iterations/requests
        
        success_count = 0
        
        print(f"Starting performance test with {num_tests} iterations...")
        
        while success_count < num_tests:
            start_request_time = time.time()
            
            # Select either fixed prompt or generate new randomly
            
            # For simplicity here we're cycling through fixed_prompts
            
            prompt_index = randint(0, len(fixed_prompts)-1)
            
            prompt_text = fixed_prompts[prompt_index]
            
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3",
                    messages=[{"role": "user", "content": prompt_text}],
                    temperature=config['temperature'],
                    max_tokens=config['max_tokens'],
                    n=config['n']
                )
                
                end_request_time = time.time()
                
                elapsed_time_single_request = end_request_time - start_request_time
                
                logger.info(f"Request successful after {elapsed_time_single_request:.3f}s")
                
                total_tokens += sum(r['tokens_consumed'] for r in [response])
                
                total_time += elapsed_time_single_request
                
                success_count +=1
                
                print(f"Success {success_count}/{num_tests}", end='\r')
                
            except Exception as e:
                logger.error(f"Request failed: {str(e)}")
                
            finally:
                # Optional delay between requests
                
                delay_duration=5 
                
                print(f"\nWaiting {delay_duration}s before next request...")
                
                time.sleep(delay_duration)
                
        else:
            avg_latency=total_time/num_tests
            
            throughput=total_tokens/total_time
            
            print("\nPerformance Test Results:")
            
            print(f"\tTotal successful requests: {success_count}")
            
            print(f"\tTotal Tokens Consumed: {total_tokens}")
            
            print(f"\tTotal Time Elapsed: {total_time:.3f}s")
            
            print(f"\tAverage Latency Per Request: {avg_latency:.3f}s ± stdev") 
              # Note: Standard deviation calculation not included here
            
            print(f"\tThroughput Achieved: {throughput:.3f} Tokens/sec")

    except Exception as e:
        logger.error("An error occurred during performance testing", exc_info=True)

if __name__ == "__main__":
    main()
