import os
import logging
from aiohttp import web

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def index(request):
    """Route principale de l'application"""
    logger.info("Requête reçue sur la route principale")
    return web.Response(text="Bienvenue sur open-mcp-client!")

async def health(request):
    """Point de terminaison pour les vérifications de santé"""
    return web.Response(text="OK")

def create_app():
    """Crée et configure l'application aiohttp"""
    app = web.Application()
    
    # Configuration des routes
    app.add_routes([
        web.get('/', index),
        web.get('/health', health),
    ])
    
    return app

def main():
    """Point d'entrée principal de l'application"""
    # Récupération du port depuis les variables d'environnement (important pour Render)
    port = int(os.environ.get('PORT', 8080))
    
    # Création de l'application
    app = create_app()
    
    # Affichage d'un message clair dans les logs
    logger.info(f"Démarrage du serveur sur le port {port}")
    logger.info(f"Pour accéder à l'application localement: http://localhost:{port}")
    
    # Démarrage du serveur
    web.run_app(
        app,
        host='0.0.0.0',  # Important: écouter sur toutes les interfaces
        port=port,
        access_log=logger
    )

if __name__ == '__main__':
    main()