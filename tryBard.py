import os
import requests

def get_bard_response(prompt):
    # Set your Google Bard session cookies here
    bard_cookies = {
        "__Secure-1PSID": "g.a000fwgr6H6fk_9Bs8-XRBGZQshbzaWJcNEBQpfcYF6kky77r4i2FCc6UqrQ4hDNIL-frH5TuwACgYKAeESAQASFQHGX2Mi3u3ESskQ2zu_5ZA5q2YxLRoVAUF8yKrHdJqaqrhVGoBBWsGLciLm0076.",
        "__Secure-1PSIDTS": "sidts-CjIBYfD7ZyF3E6QU9PXgBUt5vhGPurncuW_2OBZqqwRzsmpBNkrvG4L06JPX4mSXKqgJNxAA."
    }

    # Construct the API URL
    api_url = "https://bard.google.com/api/v1/quick"

    # Prepare the request headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    # Send the request to Google Bard
    response = requests.post(api_url, json={"text": prompt}, cookies=bard_cookies, headers=headers)

    # Extract the generated text from the response
    generated_text = response.json().get("text", "")

    return generated_text

if __name__ == "__main__":
    user_prompt = input("Enter your question or prompt: ")
    bard_response = get_bard_response(user_prompt)
    print("\nGoogle Bard's Response:")
    print(bard_response)
