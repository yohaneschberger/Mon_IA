from fastapi import FastAPI # type: ignore
from fastapi.responses import StreamingResponse # type: ignore
import httpx # type: ignore
import json
import redis # type: ignore
import os


# 1. Initialisation de l'application FastAPI
app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost") # Adresse de Redis
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None) # Mot de passe Redis si nécessaire

r_db = redis.Redis(host=REDIS_HOST, port=6379, password=REDIS_PASSWORD, decode_responses=True) # Connexion à Redis

# 2. Événement de démarrage pour préparer Ollama
@app.on_event("startup")
async def startup_event():
    print("Initialisation du système...")
    # On vérifie si Ollama est prêt et on pull le modèle
    async with httpx.AsyncClient(timeout=None) as client:
        try:
            print("Vérification du modèle llama3...")
            await client.post(
                "http://ollama:11434/api/pull", 
                json={"name": "llama3"},
                timeout=None
            )
            print("Modèle prêt et chargé !")
        except Exception as e:
            print(f"Attention: Impossible de joindre Ollama : {e}")

# 3. Gestion de la mémoire avec Redis
def load_memory(user_id="default_user"):
    # On récupere l'historique depuis Redis sous forme de string JSON
    data = r_db.get(user_id)
    return json.loads(data) if data else []

def save_memory(history, user_id="default_user"):
    # On stocke l'historique en JSON dans Redis
    r_db.set(user_id, json.dumps(history))

# 4. Endpoint principal pour résoudre les problèmes DevOps
@app.post("/solve")
async def solve_problem(user_input: str, user_id: str = "default_user"):
    history = load_memory()
    
    # Construction du prompt avec consignes de style
    prompt = f"""
    Tu es un Lead DevOps senior, pédagogue et passionné. 
    Ton but est d'aider ton collègue à résoudre un problème tout en lui apprenant des choses.

    CONSIGNE DE STYLE :
    - Parle de manière naturelle mais reste très technique (utilise le jargon : pipeline, registry, runtime, etc.).
    - Ne sois pas trop formel, utilise un ton collaboratif (ex: "On va regarder ça ensemble", "Tiens, c'est curieux...").
    - Évite les listes trop scolaires, préfère un raisonnement fluide.
    
    NOUVELLE SITUATION : {user_input}

    RÉPONSE ATTENDUE (en français) :
    1. Analyse rapide de la situation (le "Pourquoi ça coince").
    2. Ton raisonnement technique (ton "jeu de piste").
    3. La solution concrète ou la commande à tester.
    """

    # Streaming de la réponse depuis Ollama
    async def event_generator():
        full_response = ""  # Pour stocker la réponse complète
        timeout = httpx.Timeout(60.0, connect=10.0) # Timeout pour la requête
        async with httpx.AsyncClient(timeout=timeout) as client:    # Connexion à Ollama
            async with client.stream(
                "POST",
                "http://ollama:11434/api/generate",
                json={"model": "llama3:latest", "prompt": prompt, "stream": True}
            ) as response:
                async for line in response.aiter_lines():   # Lecture ligne par ligne
                    if line:
                        data = json.loads(line)
                        chunk = data.get("response", "")
                        full_response += chunk
                        yield chunk # Envoie le mot à l'UI
                        
                        if data.get("done"):
                            # Sauvegarde à la toute fin
                            history.append({"u": user_input, "a": full_response})
                            save_memory(history)

    return StreamingResponse(event_generator(), media_type="text/plain")