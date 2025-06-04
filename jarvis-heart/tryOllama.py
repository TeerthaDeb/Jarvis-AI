import requests
import torch
import json

OLLAMA_API = "http://localhost:11434/api/generate"
MODEL_NAME = "llama2"

def direct_ollama_request(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": True,
        "options": {
            "num_gpu": 1 if torch.cuda.is_available() else 0,
            "temperature": 0.7,
            "repeat_penalty": 1.1,
            "stop": ["</s>", "Human:", "Assistant:"]
        }
    }
   
    print("payload:", payload)
    

    response = requests.post(
        "http://localhost:11434/api/generate",
        json=payload,
        timeout=15,
        stream=True  # This enables streaming
    )

    for line in response.iter_lines():
        if line:
            try:
                json_response = json.loads(line.decode('utf-8'))
                
                if 'response' in json_response:
                    token = json_response['response']
                    full_response += token
                    print(token, end='', flush=True)  # Print token immediately
                
                if json_response.get('done', False):
                    print("\n\n--- Response complete ---")
                    break
                    
            except json.JSONDecodeError as e:
                print(f"\nError parsing JSON: {e}")
                continue
    
    return full_response

if __name__ == "__main__":
    while True:
        try:
            prompt = input("\nEnter your prompt: ")
            if prompt.lower() in ['quit', 'exit', 'q']:
                break
                
            print("\nOllama response:")
            full_response = direct_ollama_request(prompt)
            print(f"\n\nFull response: {full_response}")
            
        except Exception as e:
            print("Exception " + str(e) + " occurred..")