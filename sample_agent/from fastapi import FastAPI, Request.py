from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import time
import json

app = FastAPI()

# Exemple d'outil "math" : calcule la racine carrée (comme démonstration)
@app.get("/math")
async def math_tool(request: Request):
    async def event_stream():
        # Simule un calcul
        time.sleep(1)
        result = {"result": "5"}  # racine carrée de 25

        # Envoie le résultat au format SSE
        yield f"data: {json.dumps(result)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
