import uvicorn

if __name__ == "__main__":
    uvicorn.run("agentbuddy.twin.api_v1:app", host="0.0.0.0", port=8005, workers=1)
