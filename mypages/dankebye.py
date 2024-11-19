import streamlit as st

def app():
    APP_TITLE = 'Vielen Danke für deine Aufmerksamkeit'
    
    st.title(APP_TITLE)
    # Streamlit app title and description
    code = '''git clone https://github.com/KingKefir/EVSEHH.git'''
    st.code(code, language='bash')

    codedocker = '''docker pull kefirconnoisseur/evse_analysis:0.6

docker run -p 8501:8501 kefirconnoisseur/evse_analysis:0.6'''
    st.code(codedocker, language='bash')
    st.image("data/plug-e.png", caption="Quelle: openai/Dall-E")