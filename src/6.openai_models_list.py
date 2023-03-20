# OpenAIのPythonライブラリをインポートします。
import openai
import os
import pprint

# OpenAI APIキーを設定します。(`os.getenv`は環境変数から値を取得する関数です。)
openai.api_key = os.getenv("OPEN_AI_KEY")


# すべてのOpenAIモデルをリストする関数を定義します。
def list_all_models():
    # OpenAIのAPIを使用して、モデルリストを取得します。
    model_list = openai.Model.list()['data']
    # モデルIDのリストを作成します。
    model_ids = [x['id'] for x in model_list]
    # モデルIDをアルファベット順に並べ替えます。
    model_ids.sort()
    # pprintを使用して、整然とした形式でモデルIDリストを表示します。
    pprint.pprint(model_ids)


# モデルリスト関数を呼び出します。
list_all_models()
