@app.post("/callback")
async def callback(request: Request):
    body = await request.body()
    signature = request.headers.get('X-Line-Signature')

    try:
        # 非同期対応のために RequestAdapter を使う
        from linebot.exceptions import InvalidSignatureError
        from linebot.models import TextMessage, MessageEvent

        events = handler.parser.parse(body.decode(), signature)

        for event in events:
            if isinstance(event, MessageEvent) and isinstance(event.message, TextMessage):
                user_message = event.message.text

                # GPTに問い合わせ
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "あなたはユーザーの親友であり、知的で詩的なメンターのように話します。親しみやすく、感情に寄り添って、時にユーモアを交えて答えてください。"},
                        {"role": "user", "content": user_message}
                    ]
                )

                reply = response.choices[0].message.content.strip()

                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=reply)
                )

    except InvalidSignatureError:
        return PlainTextResponse("Invalid signature", status_code=400)

    return PlainTextResponse("OK", status_code=200)