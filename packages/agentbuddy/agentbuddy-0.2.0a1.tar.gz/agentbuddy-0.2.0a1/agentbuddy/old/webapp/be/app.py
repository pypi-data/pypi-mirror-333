import uvicorn

if __name__ == "__main__":
    uvicorn.run("agentbuddy.webapp.be.api:app", host="0.0.0.0", port=8001, workers=1)