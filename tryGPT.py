import openai
from Speak import speak




def ask_gpt(prompt : str , user_api_key : str , user_name : str , user_age : int):
    client = openai.OpenAI(api_key = user_api_key)
    gpt_assistant_prompt = "You are Jarvis, A personal Assistant" 
    gpt_user_prompt = prompt
    gpt_prompt = gpt_assistant_prompt, gpt_user_prompt
    #print(gpt_prompt)

    message=[   
                {"role": "assistant", "content" : f"You are Jarvis, A personal Assistant of {user_name} who is {user_age} years old."}, 
                {"role": "user", "content": gpt_user_prompt}
            ]


    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = message,
        temperature = 0.2,
        max_tokens = 400,
        frequency_penalty = 0.0
    )

    gpt_result = response.choices[0].message.content

    print(gpt_result)
    if("program" in prompt or  "code" in prompt):
        speak("Gpt Responded your answer, here is the answer.")
    else:
        speak(f"Accornig to GPT-3.5: , {gpt_result}")


if __name__ == "__main__":
    ask_gpt("define a pen in 50 words")