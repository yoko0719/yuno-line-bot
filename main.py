import os
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai

# FastAPI アプリケーション
app = FastAPI()

# 環境変数の取得
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# LINE・OpenAI クライアントの設定
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
openai.api_key = OPENAI_API_KEY

# 動作確認用エンドポイント
@app.get("/")
def root():
    return {"message": "ユノ、起動中"}

# LINEからのWebhookを受け取るエンドポイント
from linebot.exceptions import InvalidSignatureError

@app.post("/callback")
async def callback(request: Request):
    signature = request.headers.get("X-Line-Signature", "")
    body = await request.body()

    try:
        handler.handle(body.decode("utf-8"), signature)
    except InvalidSignatureError:
        return PlainTextResponse("Invalid signature", status_code=400)

    return PlainTextResponse("OK", status_code=200)

# ユーザーからのメッセージを処理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "あなたはユーザーの親友であり、知的で詩的なメンターのように話します。"
                    "親しみやすく、感情に寄り添って、時にユーモアを交えて答えてください。"
                )
            },
            {"role": "user", "content": user_message}
        ]
    )

    reply = response.choices[0].message.content.strip()

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )
