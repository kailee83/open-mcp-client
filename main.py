import logging
import asyncio
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# Configuration du logging
logging.basicConfig(level=logging.INFO)

# Création de l'application FastAPI
app = FastAPI()

# Modèle de la requête pour /command
class CommandRequest(BaseModel):
    command: str

# Route GET de test
@app.get("/")
def read_root():
    return {"message": "Hello from MCP Agent"}

# Route POST pour recevoir des commandes
@app.post("/command")
async def handle_command(request: CommandRequest):
    logging.info(f"Commande reçue : {request.command}")
    cmd = request.command

    # Traitement de commandes fictives
    if cmd == "start":
        return {"status": "success", "message": "Commande start exécutée"}
    elif cmd == "stop":
        return {"status": "success", "message": "Commande stop exécutée"}
    else:
        return {"status": "error", "message": "Commande inconnue"}

# Route POST générique pour appeler un module/méthode
@app.post("/call")
async def call(request: Request):
    try:
        logging.info("Requête reçue sur /call")
        data = await request.json()
        logging.info(f"Données reçues : {data}")

        module = data.get("module")
        method = data.get("method")
        args = data.get("args")

        if module == "gmail" and method == "run":
            return {"status": "success", "message": "Gmail module executed", "data": args}

        return {"error": "Invalid module or method"}

    except Exception as e:
        logging.error(f"Erreur: {str(e)}")
        return {"error": "Internal Server Error"}

# Route GET pour le SSE (streaming)
@app.get("/sse")
async def sse():
    async def event_generator():
        while True:
            yield f"data: ping\n\n"
            await asyncio.sleep(1)
    return StreamingResponse(event_generator(), media_type="text/event-stream")

# Démarrage du serveur (à utiliser uniquement en local)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
# Trigger redeploy
