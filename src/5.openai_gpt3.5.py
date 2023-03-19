import openai
import os

openai.api_key = os.getenv("OPEN_AI_KEY")

content = "カレーの作り方を教えて下さい。"

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "あなたはとても優秀なAIです。"},
        {"role": "user", "content": content},
    ],
    temperature=1
)

print(response.choices[0]["message"]["content"].strip())
