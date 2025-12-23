import streamlit as st # type: ignore
import os
import requests  # Plus simple pour le streaming avec iter_content

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Mon Expert DevOps", page_icon="🤖")

######### GESTION DE LA SESSION ET DES SUJETS #########
if "messages" not in st.session_state:
    st.session_state.messages = []

######### INTERFACE PRINCIPALE #########
st.title("🤖 Mon Expert DevOps")

# Affichage des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input utilisateur
if prompt := st.chat_input("Posez votre question DevOps..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Conteneur pour l'affichage progressif
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # Appel API en mode stream
            # Note: on utilise requests ici car c'est plus direct pour st.write_stream
            with requests.post(
                f"{API_URL}/solve",
                params={"user_input": prompt},
                stream=True,
                timeout=60
            ) as r:
                # Utilisation de la fonction magique de Streamlit
                def stream_generator():
                    for chunk in r.iter_content(chunk_size=None, decode_unicode=True):
                        yield chunk
                
                # Affiche et récupère la réponse complète
                full_response = st.write_stream(stream_generator())
                
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Erreur : {e}")