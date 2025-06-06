import streamlit as st
import google.generativeai as genai
import os

# Só carrega o .env localmente (opcional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Busca a chave da API no ambiente
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ A chave da API não foi encontrada. Defina GEMINI_API_KEY no .env (local) ou em Secrets (nuvem).")
else:
    genai.configure(api_key=api_key)

    MODEL_ID = "models/gemini-1.5-flash"

    st.set_page_config(page_title="Gerador de Início de História", page_icon="📖")
    st.title("📖 Gerador de Início de História com IA (Gemini)")

    nome_protagonista = st.text_input("Nome do Protagonista")
    genero = st.selectbox("Gênero Literário", ["Fantasia", "Ficção Científica", "Mistério", "Aventura"])
    local_inicial = st.radio(
        "Local Inicial da História",
        ["Uma floresta antiga", "Uma cidade futurista", "Um castelo assombrado", "Uma nave espacial à deriva"]
    )
    frase_desafio = st.text_area("Frase de Efeito ou Desafio Inicial", placeholder="Ex: 'E de repente, tudo ficou escuro.'")

    if st.button("Gerar Início da História"):
        if not nome_protagonista or not frase_desafio:
            st.warning("Por favor, preencha todos os campos antes de gerar a história.")
        else:
            prompt = (
                f"Crie o início de uma história no gênero '{genero}', com um protagonista chamado '{nome_protagonista}'. "
                f"A história deve começar em '{local_inicial}'. "
                f"Incorpore a seguinte frase ou desafio no início: '{frase_desafio}'. "
                f"Escreva um ou dois parágrafos envolventes e criativos."
            )
            try:
                model = genai.GenerativeModel(model_name=MODEL_ID)
                response = model.generate_content(prompt)

                st.subheader("🌟 Início da História Gerada")
                st.write(response.text)
            except Exception as e:
                st.error(f"Erro ao gerar a história: {e}")
