import streamlit as st
import pandas as pd
import io
from datetime import datetime

# Konfiguration
st.set_page_config(page_title="TaxFlow AI - Beleg-Prototyp", page_icon="⚖️", layout="wide")

# Styling für eine saubere Optik
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 TaxFlow AI: Beleg-Management")
st.write("Prototyp für die digitale Zusammenarbeit mit der Kanzlei.")

# Sidebar
with st.sidebar:
    st.header("Mandanten-Info")
    st.info("Zeitraum: **Q2 2024**")
    st.divider()
    st.metric("Erfasste Belege", "15")
    st.metric("Summe (Brutto)", "1.840,20 €")

# Hauptbereich: Upload
st.subheader("1. Beleg-Upload")
uploaded_files = st.file_uploader("Ziehen Sie Rechnungen (PDF/JPG) hierher", accept_multiple_files=True)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} neue Belege erkannt. KI-Analyse läuft...")
    # Simulation der Bilder-Vorschau
    cols = st.columns(min(len(uploaded_files), 3))
    for i, file in enumerate(uploaded_files[:3]):
        cols[i].image(file, caption=f"Beleg: {file.name}", use_container_width=True)

# 2. Die Tabelle (Editierbar für den Nutzer)
st.subheader("2. Automatische Analyse & Begründung")
st.caption("Die KI hat folgende Daten extrahiert. Sie können diese vor dem Export prüfen.")

if "df_data" not in st.session_state:
    st.session_state.df_data = pd.DataFrame([
        {"Datum": "2024-05-15", "Kreditor": "Apple Store", "Brutto": 849.00, "USt": "19%", "Kategorie": "GWG", "Begründung": "Laptop-Zubehör, sofort abzugsfähig (< 800€ Netto)."},
        {"Datum": "2024-05-20", "Kreditor": "Deutsche Bahn", "Brutto": 45.20, "USt": "7%", "Kategorie": "Reisekosten", "Begründung": "Fahrt zu Mandant XYZ in Berlin."},
        {"Datum": "2024-06-01", "Kreditor": "Restaurant Sonne", "Brutto": 120.00, "USt": "19%", "Kategorie": "Bewirtung", "Begründung": "Geschäftsessen mit Neukunde. 70% abzugsfähig."},
    ])

# Editor anzeigen
edited_df = st.data_editor(st.session_state.df_data, num_rows="dynamic", use_container_width=True)

# 3. Export
st.subheader("3. Finaler Export")
col1, col2 = st.columns([1, 2])

with col1:
    # Excel-Export Logik
    buffer = io.BytesIO()
    try:
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            edited_df.to_excel(writer, index=False, sheet_name='Steuerbelege')
        
        st.download_button(
            label="📥 Excel für Steuerberater herunterladen",
            data=buffer.getvalue(),
            file_name=f"TaxFlow_Export_Q2_2024.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        st.error(f"Fehler beim Erstellen der Excel: {e}")

with col2:
    st.write("💡 *Hinweis für den Steuerberater:* Diese Datei enthält bereits die GoBD-konformen Begründungen für jede Buchung.")

st.divider()
st.caption("Diese App ist ein technischer Demonstrator. Datensicherheit und Verschlüsselung sind für die Produktionsversion vorgesehen.")
