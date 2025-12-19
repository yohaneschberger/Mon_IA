import streamlit as st
import httpx

########################################

# Configuration de la page
st.set_page_config(page_title="Mon Expert DevOps", page_icon="🤖")
st.title("🤖 Mon Expert DevOps")

########################################

# Historique de la discussion
if "messages" not in st.session_state:  # Initialisation de l'historique des messages
    st.session_state.messages = []

# Affichage des messages
for message in st.session_state.messages:   # Affichage de chaque message
    with st.chat_message(message["role"]):  # Rôle : user ou assistant
        st.markdown(message["content"]) # Contenu du message

# Zone de saisie
if prompt := st.chat_input("Posez votre question DevOps..."):   # Zone de saisie du chat
    st.session_state.messages.append({"role": "user", "content": prompt})   # Ajout du message utilisateur à l'historique
    with st.chat_message("user"):   # Affichage du message utilisateur
        st.markdown(prompt)

    with st.chat_message("assistant"):  # Affichage du message assistant
        with st.spinner("L'IA réfléchit..."):   # Affichage d'un spinner pendant la réflexion de l'IA
            try:
                # On appelle ton API FastAPI existante
                response = httpx.post(
                    "http://127.0.0.1:8000/solve",
                    params={"user_input": prompt},
                    timeout=60.0
                )
                answer = response.json().get("response", "Erreur de réponse")   # Récupération de la réponse de l'API
                st.markdown(answer)  # Affichage de la réponse de l'IA
                st.session_state.messages.append({"role": "assistant", "content": answer})  # Ajout de la réponse de l'IA à l'historique
            except Exception as e:  # Gestion des erreurs de connexion
                st.error(f"Erreur de connexion : {e}")