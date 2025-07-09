from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Yuno LINE bot is alive!"}

@app.post("/callback")
async def callback(request: Request):
    body = await request.body()
    print("Received request body:", body)
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
