from setuptools import setup, find_packages

setup(
    name="open_mcp_client",  # Notez le underscore au lieu du tiret
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0,<3.9.0",  # Évitez la version problématique
    ],
    entry_points={
        "console_scripts": [
            "open-mcp-client=app:main",  # Crée une commande pour lancer l'application
        ],
    },
    python_requires=">=3.8",
    description="Client MCP (Python)",
    author="Votre nom",
    author_email="votre.email@example.com",
    url="https://github.com/votre-utilisateur/open-mcp-client",
)