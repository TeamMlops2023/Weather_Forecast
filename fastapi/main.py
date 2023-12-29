# lancement du script start_server.py (fastapi)
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="debug")
