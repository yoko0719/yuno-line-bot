from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "ユノだよ！LINE連携の準備OK！"}

# 以下、LINEからのWebhook処理などを追加していく...

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000)