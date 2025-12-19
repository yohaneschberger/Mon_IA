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

## 🛠️ Fonctionnalités Clés

* **Inférence 100% Locale** : Confidentialité totale, aucune donnée n'est envoyée dans le cloud.
* **Accélération Hardware** : Optimisé pour les GPU NVIDIA (testé sur RTX 3050) via `nvidia-container-runtime`.
* **Réponses en Français** : Système configuré pour traduire les concepts complexes en français technique clair.
* **Haute Disponibilité** : Configuration `restart: always` pour un service opérationnel dès le démarrage du PC.
* **Persistance** : Volume Docker dédié pour conserver les modèles et éviter les retéléchargements.
---

## 🚀 Exemple de Requête & Résultat
**Utilisateur :** *"Pourquoi mon `docker-compose up` échoue avec 'port already allocated' ?"*

**Réponse de l'Expert (IA) :**
1. **Indices** : Port 8080 occupé, service Nginx en conflit.
2. **Lien** : Une instance de test tourne déjà en arrière-plan sur le même port.
3. **Solution** : `docker ps` pour identifier l'ID, puis `docker stop <ID>` ou changer le mapping de port dans le fichier YAML.

---
## 🚀 Installation et Démarrage

### Prérequis
* Docker et Docker-Compose installés.
* NVIDIA Container Toolkit (pour l'accélération GPU).


# Lancer l'infrastructure
docker-compose up -d

# Accéder à l'interface
# http://localhost:8501

### Lancement
1. Clonez le dépôt :
   ```bash
   git clone [https://github.com/votre-utilisateur/votre-projet.git](https://github.com/votre-utilisateur/votre-projet.git)
   cd votre-projet
   ```
2. Lancer l'infrastructure :
   ```bash
   docker-compose up -d
   ```
3. Télécharger le modèle d'IA (uniquement la première fois) :
   ```bash
   docker exec -it mon_ia_ollama_1 ollama pull llama3
   ```
4. Accéder à l'interface : Ouvrez votre navigateur et allez à l'adresse suivante : 👉   http://localhost:8501
