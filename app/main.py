from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import httpx
import json
import os

app = FastAPI()

MEMORY_DIR = "/app/memory"
MEMORY_FILE = os.path.join(MEMORY_DIR, "chat_history.json")

if not os.path.exists(MEMORY_DIR):
    os.makedirs(MEMORY_DIR)

def load_memory():
    try:
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r") as f:
                content = f.read()
                return json.loads(content) if content else []
    except Exception as e:
        print(f"Erreur mémoire : {e}")
    return []

def save_memory(history):
    with open(MEMORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

@app.post("/solve")
async def solve_problem(user_input: str):
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

    async def event_generator():
        full_response = ""
        timeout = httpx.Timeout(60.0, connect=10.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            async with client.stream(
                "POST",
                "http://ollama:11434/api/generate",
                json={"model": "llama3:latest", "prompt": prompt, "stream": True}
            ) as response:
                async for line in response.aiter_lines():
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