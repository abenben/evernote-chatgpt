import openai
import os
import requests
import json
import time

# OpenAI APIキーを設定する
openai.api_key = os.getenv("OPEN_AI_KEY")

# OpenAIのGPT-3を使用して、応答を生成する関数
def generate_response(message):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=message,
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text.strip()

# OpenWeatherMap APIキーを設定する
weather_api_key = os.getenv("WEATHER_API_KEY")

# 都市名から天気情報を取得する関数
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
    response = requests.get(url)
    data = json.loads(response.text)
    return data['weather'][0]['description'], data['main']['temp'], data['main']['humidity']

# チャットアシスタントのクラス
class ChatAssistant:
    def __init__(self):
        self.previous_message = None

    # チャットを開始する関数
    def start_chat(self):
        print("こんにちは！AIアシスタントです。何かお手伝いできることはありますか？")
        while True:
            message = input("ユーザー：")
            if message == "さようなら":
                print("AIアシスタント：さようなら！またお会いしましょう。")
                break

            if self.previous_message == "今日の天気は？":
                weather_city = message
                weather_desc, weather_temp, weather_humidity = get_weather(weather_city)
                response = f"{weather_city}の天気は{weather_desc}、気温は{weather_temp}℃、湿度は{weather_humidity}%です。"
                self.previous_message = None
            else:
                response = generate_response(message)
                if "天気" in response:
                    self.previous_message = "今日の天気は？"
                else:
                    self.previous_message = None

            print("AIアシスタント：" + response)

# チャットアシスタントを作成し、チャットを開始する
assistant = ChatAssistant()
assistant.start_chat()
