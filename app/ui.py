import streamlit as st
import httpx

st.set_page_config(page_title="Mon Expert DevOps", page_icon="🤖")
st.title("🤖 Mon Expert DevOps")

# Historique de la discussion
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie
if prompt := st.chat_input("Posez votre question DevOps..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("L'IA réfléchit..."):
            try:
                # On appelle ton API FastAPI existante
                response = httpx.post(
                    "http://127.0.0.1:8000/solve", 
                    params={"user_input": prompt},
                    timeout=60.0
                )
                answer = response.json().get("response", "Erreur de réponse")
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Erreur de connexion : {e}")