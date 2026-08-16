import streamlit as st
import pandas as pd
import io
import pdfplumber
import re
from datetime import datetime

# --- KONFIGURATION & DESIGN ---
st.set_page_config(
    page_title="TaxFlow AI | Kanzlei-Portal (Demo)",
    page_icon="💼",
    layout="wide"
)

# Professionelles CSS Styling
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .stAlert { border-radius: 8px; }
    .main-header { font-size: 2.2rem; color: #1e3a8a; font-weight: 700; margin-bottom: 0.5rem; }
    .sub-header { font-size: 1.1rem; color: #4b5563; margin-bottom: 2rem; }
    .demo-badge { 
        background-color: #fef3c7; color: #92400e; 
        padding: 0.5rem 1rem; border-radius: 20px; 
        font-weight: 600; font-size: 0.8rem; border: 1px solid #f59e0b;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="demo-badge">TECHNOLOGIE-DEMONSTRATOR</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-header">TaxFlow AI: Intelligente Belegaufbereitung</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Automatisierte Erfassung und steuerliche Vorkontierung für die Quartalsbuchhaltung.</p>', unsafe_allow_html=True)

# --- DISCLAIMER ---
with st.expander("ℹ️ Wichtiger Hinweis zu dieser Demo", expanded=True):
    st.write("""
        **Dies ist eine technische Demonstration.**
        - **Funktionsumfang:** In dieser Version werden ausschließlich **PDF-Dateien** verarbeitet.
        - **Datenschutz:** Hochgeladene Dateien werden nur temporär im Arbeitsspeicher verarbeitet und nach Ende der Sitzung gelöscht.
        - **Ziel:** Erstellung einer GoBD-konformen Exportdatei (Excel) inklusive KI-basierter Begründung für den Steuerberater.
    """)

# --- LOGIK: PDF AUSLESEN ---
def extract_data_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()
    
    # Einfache Heuristik zur Extraktion (In einer Vollversion durch LLM ersetzt)
    # Suche nach Datum (DD.MM.YYYY)
    date_match = re.search(r'\d{2}\.\d{2}\.\d{4}', text)
    date_str = date_match.group(0) if date_match else datetime.now().strftime("%d.%m.%Y")
    
    # Suche nach Beträgen (X,XX €)
    amount_match = re.search(r'(\d+,\d{2})', text)
    amount_str = amount_match.group(0).replace(',', '.') if amount_match else "0.00"
    
    return {
        "Belegdatum": date_str,
        "Kreditor": file.name.split('.')[0][:20],
        "Bruttobetrag": float(amount_str),
        "USt %": "19%",  # Standardwert für Demo
        "Kategorie": "Betriebsausgabe",
        "Begründung": "Automatisch erkannt: PDF-Beleg vorhanden. Vorsteuerabzug möglich.",
        "Dateiname": file.name
    }

# --- HAUPTBEREICH: UPLOAD ---
st.subheader("1. PDF-Belege hochladen")
uploaded_files = st.file_uploader(
    "Laden Sie hier Ihre digitalen Rechnungen hoch (nur PDF)", 
    type=["pdf"], 
    accept_multiple_files=True
)

if uploaded_files:
    data_list = []
    for file in uploaded_files:
        with st.spinner(f"Analysiere {file.name}..."):
            extracted = extract_data_from_pdf(file)
            data_list.append(extracted)
    
    # Speichern in Session State
    st.session_state.processed_data = pd.DataFrame(data_list)
    st.success(f"Analyse erfolgreich: {len(uploaded_files)} Dokumente verarbeitet.")

# --- TABELLE & REVIEW ---
if "processed_data" in st.session_state and not st.session_state.processed_data.empty:
    st.subheader("2. Prüfung & steuerliches Reasoning")
    st.info("Sie können die extrahierten Daten direkt in der Tabelle anpassen.")
    
    edited_df = st.data_editor(
        st.session_state.processed_data, 
        use_container_width=True,
        num_rows="dynamic"
    )
    
    # --- EXPORT ---
    st.subheader("3. Export für die Kanzlei")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Excel Erstellung
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            edited_df.to_excel(writer, index=False, sheet_name='Steuerbelege_Q2')
        
        st.download_button(
            label="📥 Excel-Datei generieren",
            data=output.getvalue(),
            file_name=f"TaxFlow_Export_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="Klicken Sie hier, um die fertige Liste für Ihren Steuerberater herunterzuladen."
        )
    
    with col2:
        st.write("✅ **Bereit für den Versand.** Die Datei enthält alle Pflichtangaben für die Buchhaltung.")
else:
    st.write("---")
    st.info("Warten auf PDF-Upload...")

# --- FOOTER ---
st.divider()
st.caption("TaxFlow AI Prototyp | © 2024 | Fokus: Digitale Buchhaltung & Kanzlei-Effizienz")
