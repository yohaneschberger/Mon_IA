#!/bin/bash

echo "Vérification du modèle Llama3..."
# On attend que Ollama soit prêt
sleep 5 

# On télécharge le modèle
ollama pull llama3

echo "Modèle prêt !"