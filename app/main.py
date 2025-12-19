from fastapi import FastAPI
import httpx

app = FastAPI()

@app.post("/solve")
async def solve_problem(user_input: str):
    # On définit la consigne pour forcer l'IA à raisonner
    prompt = f"""
    Tu es un expert DevOps. Réponds toujours en français, de manière claire et technique.
    Résous ce problème comme un jeu de piste :
    1. Liste les indices techniques.
    2. Fais un lien entre eux.
    3. Donne la solution finale.
    
    PROBLÈME : {user_input}
    """

    # On définit un timeout beaucoup plus long (ex: 60 secondes)
    # pour laisser le temps au GPU de charger le modèle
    timeout = httpx.Timeout(60.0, connect=10.0)
    
    # On envoie la demande au conteneur Ollama
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(
            "http://ollama:11434/api/generate",
            json={"model": "llama3:latest", "prompt": prompt, "stream": False}
        )
        
        return response.json()