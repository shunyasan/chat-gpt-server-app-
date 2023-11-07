import openai
import os
from dotenv import load_dotenv

from ..schemas.chatMessage import GetChatGpt


# .envファイルから環境変数を読み込む
load_dotenv()

# OpenAI
openai.api_key = os.environ.get("OPENAI_API_KEY")


# ChatGPTへ質問する
# ひとまずcontentのみを返却。必要であれば他の値も追加する
def get_chat_gpt(get_chat_gpt:list[GetChatGpt]) -> str:
    # chatGPTへ質問
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = get_chat_gpt
    )
    return response["choices"][0]["message"]["content"]

