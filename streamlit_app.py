import streamlit as st
from auth_engine import FortressSecurity
from database_manager import FortressDB
import os

# Configuration visuelle
st.set_page_config(page_title="DorkNet Fortress", page_icon="🏰", layout="wide")

# Initialisation de la base de données et de la clé
db = FortressDB()
if 'enc_key' not in st.session_state:
    # En production, cette clé devrait être stockée dans st.secrets
    st.session_state['enc_key'] = FortressSecurity.generate_secure_password(32).encode()
    
cipher = FortressSecurity.get_cipher(Fernet.generate_key()) # Clé de session

# Style CSS pour l'ambiance "Fortress"
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00FF41; }
    [data-testid="stMetricValue"] { color: #00FF41; }
    </style>
    """, unsafe_allow_html=True)

# --- SYSTÈME D'ACCÈS ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.title("🛡️ ACCÈS DORKNET FORTRESS")
    with st.container():
        master_pwd = st.text_input("Clé Maîtresse", type="password")
        if st.button("DÉVERROUILLER"):
            if master_pwd == st.secrets["MASTER_PASSWORD"]:
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("ACCÈS REFUSÉ")
else:
    # --- INTERFACE PRINCIPALE ---
    st.title("🏰 DorkNet Fortress - Dashboard")
    
    # Statistiques
    col1, col2, col3 = st.columns(3)
    col1.metric("Quota", "2 To")
    col2.metric("Protection", "AES-256")
    col3.metric("Statut IA", "En veille")

    st.divider()

    # Upload et Traitement
    st.subheader("📤 Fortifier un projet")
    files = st.file_uploader("Sélectionnez vos fichiers", accept_multiple_files=True)
    
    if files:
        for f in files:
            # Calcul de l'importance (Logique IA)
            importance = "HAUTE" if f.name.endswith(('.py', '.cpp', '.unity', '.sql')) else "NORMALE"
            
            # Chiffrement
            encrypted_content = FortressSecurity.encrypt_data(cipher, f.getvalue())
            
            # Indexation
            db.add_entry(f.name, importance, f.size / 1024)
            st.success(f"🔒 {f.name} a été chiffré et indexé.")

    st.divider()

    # Affichage des fichiers
    st.subheader("📂 Archives de la Forteresse")
    history = db.get_all_files()
    if history:
        import pandas as pd
        df = pd.DataFrame(history, columns=["Nom", "Importance", "Date"])
        st.dataframe(df, use_container_width=True)
    else:
        st.write("Aucun fichier dans la forteresse pour le moment.")

    if st.sidebar.button("Fermer la Forteresse"):
        st.session_state['authenticated'] = False
        st.rerun()
      
