import streamlit as st
import os

# Importation sécurisée pour éviter le crash au chargement
try:
    from auth_engine import FortressSecurity
    from database_manager import FortressDB
    from cryptography.fernet import Fernet
except ModuleNotFoundError:
    st.error("⚠️ Erreur : Les bibliothèques nécessaires ne sont pas encore installées sur le serveur.")
    st.stop()

# Configuration de la page
st.set_page_config(page_title="DorkNet Fortress", page_icon="🏰", layout="wide")

# Initialisation de la base de données
db = FortressDB()

# Logique de sécurité de session
if 'enc_key' not in st.session_state:
    st.session_state['enc_key'] = Fernet.generate_key()

cipher = FortressSecurity.get_cipher(st.session_state['enc_key'])

# --- INTERFACE ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.title("🛡️ ACCÈS DORKNET FORTRESS")
    master_pwd = st.text_input("Clé Maîtresse", type="password")
    if st.button("DÉVERROUILLER"):
        # Vérification via les secrets Streamlit
        if master_pwd == st.secrets["MASTER_PASSWORD"]:
            st.session_state['authenticated'] = True
            st.rerun()
        else:
            st.error("ACCÈS REFUSÉ")
else:
    st.title("🏰 DorkNet Fortress - Connecté")
    st.success("Système de stockage 2 To actif et sécurisé.")
    
    # Upload
    uploaded_file = st.file_uploader("Fortifier un fichier", type=None)
    if uploaded_file:
        file_bytes = uploaded_file.getvalue()
        encrypted = FortressSecurity.encrypt_data(cipher, file_bytes)
        # Logique d'importance simplifiée
        importance = "HAUTE" if uploaded_file.name.endswith(('.py', '.cpp', '.sql')) else "NORMALE"
        db.add_entry(uploaded_file.name, importance, len(file_bytes)/1024)
        st.info(f"🔒 {uploaded_file.name} chiffré et indexé dans la base.")

    if st.sidebar.button("Déconnexion"):
        st.session_state['authenticated'] = False
        st.rerun()
