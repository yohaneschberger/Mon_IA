# 🚀 Expert DevOps IA - Instance Locale

Ce projet est un assistant intelligent spécialisé dans le diagnostic et la résolution de problèmes DevOps. Il utilise un modèle de langage (LLM) performant tournant localement pour garantir la confidentialité des données et une disponibilité totale sans frais d'API.

## 🏗️ Architecture du Projet

Le projet repose sur une architecture en micro-services conteneurisée :
* **Interface (Frontend)** : Développée avec **Streamlit** pour une interaction utilisateur fluide et intuitive.
* **Cerveau (Backend)** : Une API **FastAPI** qui orchestre la logique et formate les requêtes.
* **Moteur IA** : **Ollama** hébergeant le modèle **Llama 3**, avec accélération matérielle via GPU NVIDIA.



---

## 🛠️ Stack Technique

* **Langage** : Python 3.10+
* **Framework API** : FastAPI / Uvicorn
* **Interface Web** : Streamlit
* **Conteneurisation** : Docker & Docker-Compose
* **Modèle IA** : Llama 3 (via Ollama)
* **Accélération** : NVIDIA CUDA Support (RTX 3050)

---

## 🚀 Installation et Démarrage

### Prérequis
* Docker et Docker-Compose installés.
* NVIDIA Container Toolkit (pour l'accélération GPU).

### Lancement
1. Clonez le dépôt :
   ```bash
   git clone [https://github.com/votre-utilisateur/votre-projet.git](https://github.com/votre-utilisateur/votre-projet.git)
   cd votre-projet
