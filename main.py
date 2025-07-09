from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import uvicorn
import os
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage

app = FastAPI()

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.get("/")
def read_root():
    return {"message": "ユノだよ！LINE連携の準備OKだよ🌸"}

@app.post("/callback")
async def callback(request: Request):
    body = await request.body()
    signature = request.headers.get('X-Line-Signature')

    try:
        handler.handle(body.decode(), signature)
    except Exception as e:
        return PlainTextResponse("エラー", status_code=400)

    return PlainTextResponse("OK", status_code=200)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    reply_text = "葉子、何か用？"
    line_bot_api.reply_message(event.reply_token, TextMessage(text=reply_text))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000)