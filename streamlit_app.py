import streamlit as st
import pandas as pd
from auth_engine import FortressSecurity
from database_manager import FortressDB
from cryptography.fernet import Fernet

st.set_page_config(page_title="DorkNet Fortress", page_icon="🏰", layout="wide")
db = FortressDB()

# --- SÉCURITÉ ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

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
    st.title("🏰 DorkNet Fortress - Connecté")
    st.sidebar.success("Système 2 To Actif")

    # --- SECTION 1 : UPLOAD ---
    with st.expander("📤 Fortifier de nouveaux fichiers"):
        uploaded_files = st.file_uploader("Déposez vos fichiers ici", accept_multiple_files=True)
        if st.button("Lancer la sécurisation"):
            if uploaded_files:
                cipher = FortressSecurity.get_cipher(st.secrets["ENCRYPTION_KEY"].encode())
                for f in uploaded_files:
                    importance = "HAUTE" if f.name.endswith(('.py', '.cpp', '.unity', '.sql')) else "NORMALE"
                    enc_data = FortressSecurity.encrypt_data(cipher, f.getvalue())
                    db.add_entry(f.name, importance, len(enc_data)/1024, enc_data)
                st.success("🔒 Fichiers ajoutés à la racine de la forteresse.")
                st.rerun()

    st.divider()

    # --- SECTION 2 : EXPLORATEUR DE FICHIERS (VOTRE RACINE) ---
    st.subheader("📂 Votre Racine de Stockage")
    files_list = db.get_all_files()

    if files_list:
        # Création d'un tableau propre
        for fid, name, imp, time, size in files_list:
            col1, col2, col3, col4 = st.columns([4, 2, 2, 2])
            col1.write(f"📄 {name}")
            col2.write(f"⭐ {imp}")
            col3.write(f"📅 {time}")
            
            # Bouton de récupération
            file_info = db.get_file_content(fid)
            cipher_dec = FortressSecurity.get_cipher(st.secrets["ENCRYPTION_KEY"].encode())
            try:
                decrypted_data = cipher_dec.decrypt(file_info[1])
                col4.download_button(label="⬇️ Récupérer", data=decrypted_data, file_name=name, key=str(fid))
            except:
                col4.error("Clé invalide")
    else:
        st.info("La forteresse est vide. Commencez par uploader un fichier.")

    if st.sidebar.button("Fermer la session"):
        st.session_state['authenticated'] = False
        st.rerun()
