import logging
import os
from fastapi import FastAPI, Request, HTTPException, Depends
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import asyncio

# Configuration des logs
logging.basicConfig(level=logging.INFO)

# Création de l'application FastAPI
app = FastAPI()

# Modèle Pydantic pour la commande
class CommandRequest(BaseModel):
    command: str

# Endpoint pour tester la connexion
@app.get("/")
def read_root():
    return {"message": "Hello from MCP Agent"}

# Endpoint /command qui accepte une commande en POST
@app.post("/command")
async def handle_command(request: CommandRequest):
    logging.info(f"Commande reçue : {request.command}")
    cmd = request.command

    # Traitement de la commande
    if cmd == "status":
        return {"message": "Commande 'status' exécutée avec succès", "status": "ok"}
    else:
        return {"message": f"Commande '{cmd}' non reconnue", "status": "error"}

# Endpoint /call pour simuler l'appel d'un module
@app.post("/call")
async def call(request: Request):
    try:
        logging.info("Requête reçue")
        data = await request.json()
        logging.info(f"Données reçues : {data}")

        module = data.get("module")
        method = data.get("method")
        args = data.get("args")

        # Exemple de gestion de l'appel au module gmail
        if module == "gmail" and method == "run":
            return {"status": "success", "message": "Gmail module executed", "data": args}

        return {"error": "Invalid module or method"}

    except Exception as e:
        logging.error(f"Erreur: {str(e)}")
        return {"error": "Internal Server Error"}

# Endpoint SSE pour envoyer des événements
@app.get("/sse")
async def sse():
    async def event_generator():
        while True:
            yield f"data: ping\n\n"
            await asyncio.sleep(1)
    return StreamingResponse(event_generator(), media_type="text/event-stream")

# Lancement de l'application avec le port dynamique
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Utilise le port spécifié par Render
    logging.info(f"Lancement du serveur sur le port {port}")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
