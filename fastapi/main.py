from fastapi import FastAPI, Query
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/status")
def get_status():
    return {"status": "ok"}

@app.get("/echo")
def echo(text: str = Query(None, min_length=1, max_length=100)):
    return {"echo": text}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="debug")
