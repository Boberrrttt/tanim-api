from fastapi import FastAPI
import sys

print("BOOT", sys.version)

app = FastAPI()

@app.get("/")
def root():
    print("ROOT accessed")
    return {"status": "ok"}
