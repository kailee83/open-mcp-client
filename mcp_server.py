from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import time
import json
import uvicorn  # Uvicorn est nécessaire pour démarrer le serveur

app = FastAPI()

@app.get("/math")
async def math_tool(request: Request):
    async def event_stream():
        time.sleep(1)  # Simule un délai
        result = {"result": 5}  # racine carrée de 25
        yield f"data: {json.dumps(result)}\n\n"
    
    return StreamingResponse(event_stream(), media_type="text/event-stream")

# Lancer le serveur avec uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
