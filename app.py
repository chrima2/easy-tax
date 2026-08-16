import streamlit as st
import pandas as pd
import io
from datetime import datetime

# Seiten-Konfiguration
st.set_page_config(page_title="TaxFlow Prototyp", layout="wide")

st.title("📊 TaxFlow AI: Beleg-Analyse")
st.info("Dieser Prototyp zeigt, wie Belege automatisch für die Kanzlei aufbereitet werden.")

# Sidebar für Status
st.sidebar.header("Status: Q2 2024")
st.sidebar.metric("Erfasste Belege", "12")
st.sidebar.metric("Gesamtsumme (Brutto)", "1.450,50 €")

# 1. Upload Bereich
st.subheader("1. Neue Belege hochladen")
uploaded_files = st.file_uploader("Bilder oder PDFs auswählen", accept_multiple_files=True)

if uploaded_files:
    st.success(f"{len(uploaded_files)} Beleg(e) erfolgreich hochgeladen und analysiert!")

# 2. Mock-Daten für die Demonstration
# Hier zeigen wir dem Steuerberater, wie das Ergebnis aussieht
if "data" not in st.session_state:
    st.session_state.data = [
        {"Datum": "2024-05-15", "Kreditor": "Apple Store", "Brutto": 849.00, "USt": "19%", "Kategorie": "GWG", "Begründung": "Hardware-Anschaffung (MacBook Zubehör), sofort abzugsfähig da < 800€ Netto."},
        {"Datum": "2024-05-20", "Kreditor": "Deutsche Bahn", "Brutto": 45.20, "USt": "7%", "Kategorie": "Reisekosten", "Begründung": "Fahrt zum Mandantentermin in Berlin."},
        {"Datum": "2024-06-01", "Kreditor": "Restaurant Le Buffet", "Brutto": 120.00, "USt": "19%", "Kategorie": "Bewirtung", "Begründung": "Geschäftsessen mit Projektpartner. 70% abzugsfähig."},
    ]

df = pd.DataFrame(st.session_state.data)

# 3. Anzeige der Analyse-Tabelle
st.subheader("2. Analysierte Belege (Vorschau)")
edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

# 4. Export Funktion
st.subheader("3. Export für Steuerberater")

# Excel-Buffer erstellen
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    edited_df.to_excel(writer, index=False, sheet_name='Quartalsübersicht')
    
st.download_button(
    label="📥 Excel-Datei für Kanzlei generieren",
    data=buffer,
    file_name=f"TaxFlow_Export_{datetime.now().strftime('%Y-%m-%d')}.xlsx",
    mime="application/vnd.ms-excel"
)

st.divider()
st.caption("TaxFlow AI Prototyp - Sicherer Datentransfer wird in der Vollversion via SSL und OAuth2 gewährleistet.")
