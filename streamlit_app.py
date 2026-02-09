import streamlit as st
from auth_engine import FortressSecurity
from database_manager import FortressDB
import os

st.set_page_config(page_title="DorkNet Fortress", page_icon="🏰", layout="wide")
db = FortressDB()

# Style visuel Dark Fortress
st.markdown("<style>.stApp { background-color: #050505; color: #00FF41; }</style>", unsafe_allow_html=True)

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# --- ACCÈS SÉCURISÉ ---
if not st.session_state['authenticated']:
    st.title("🛡️ ACCÈS DORKNET FORTRESS")
    master_pwd = st.text_input("Clé Maîtresse", type="password")
    if st.button("DÉVERROUILLER"):
        if master_pwd == st.secrets["MASTER_PASSWORD"]:
            st.session_state['authenticated'] = True
            st.rerun()
        else:
            st.error("ACCÈS REFUSÉ")
else:
    # --- INTERFACE PRINCIPALE ---
    st.title("🏰 DorkNet Fortress - Connecté")
    st.sidebar.info("Quota : 2 To Actif")
    
    # Initialisation du chiffrement avec la clé des secrets
    cipher = FortressSecurity.get_cipher(st.secrets["ENCRYPTION_KEY"].encode())

    # Section Upload
    with st.expander("📤 Ajouter des fichiers à la racine"):
        uploaded_files = st.file_uploader("Sélectionnez vos projets", accept_multiple_files=True)
        if st.button("Lancer la Fortification"):
            for f in uploaded_files:
                # Logique IA : Détection d'importance par extension
                importance = "HAUTE" if f.name.endswith(('.py', '.cpp', '.unity', '.sql')) else "NORMALE"
                enc_data = FortressSecurity.encrypt_data(cipher, f.getvalue())
                db.add_entry(f.name, importance, enc_data)
            st.success("Fichiers chiffrés et stockés !")
            st.rerun()

    st.divider()

    # Section Explorateur (Récupération des fichiers)
    st.subheader("📂 Vos Archives Sécurisées")
    files = db.get_all_files()
    
    if files:
        for fid, name, imp, time in files:
            col1, col2, col3, col4 = st.columns([4, 2, 2, 2])
            col1.write(f"📄 {name}")
            col2.write(f"⭐ {imp}")
            col3.write(f"📅 {time}")
            
            # Bouton de téléchargement
            encrypted_content = db.get_file_content(fid)[0]
            decrypted_data = FortressSecurity.decrypt_data(cipher, encrypted_content)
            col4.download_button(label="⬇️ Récupérer", data=decrypted_data, file_name=name, key=str(fid))
    else:
        st.write("La forteresse est vide.")
