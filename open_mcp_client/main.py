
from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Définit le port à utiliser
    uvicorn.run(app, host="0.0.0.0", port=port)  # Utilise le port obtenu de l'environnement

