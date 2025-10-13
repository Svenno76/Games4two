import streamlit as st

st.set_page_config(page_title="Spiele Hub", page_icon="🎮", layout="centered")

st.title("🎮 Willkommen im Spiele Hub!")

st.write("### Wähle ein Spiel aus dem Menü links! 👈")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.info("""
    ### 🧮 Math Practice
    
    Übe deine Mathefähigkeiten!
    
    - Addition und Subtraktion
    - Adaptive Schwierigkeit
    - Zeitnahme und Statistiken
    - Speichert deinen Fortschritt
    """)

with col2:
    st.info("""
    ### 🧠 Memory Spiel
    
    Trainiere dein Gedächtnis!
    
    - Variabler Schwierigkeitsgrad
    - 3-32 Kartenpaare
    - Live-Statistiken
    - Effizienz-Bewertung
    """)

st.divider()

st.write("💡 **Tipp:** Nutze das Menü in der linken Sidebar, um zwischen den Spielen zu wechseln!")

st.divider()
st.caption("Built with Streamlit 🚀")