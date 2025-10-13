import streamlit as st

st.set_page_config(page_title="Spiele Hub", page_icon="🎮", layout="centered")

st.title("🎮 Willkommen im Spiele Hub!")

st.write("### Wähle ein Spiel:")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("🧮 Math Practice")
    st.write("""
    Übe deine Mathefähigkeiten!
    
    - Addition und Subtraktion
    - Adaptive Schwierigkeit
    - Zeitnahme und Statistiken
    - Speichert deinen Fortschritt
    """)
    if st.button("Math Practice spielen →", use_container_width=True, type="primary"):
        st.switch_page("pages/0_Math_Practice.py")

with col2:
    st.subheader("🧠 Memory Spiel")
    st.write("""
    Trainiere dein Gedächtnis!
    
    - Variabler Schwierigkeitsgrad
    - 3-32 Kartenpaare
    - Live-Statistiken
    - Effizienz-Bewertung
    """)
    if st.button("Memory Spiel spielen →", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Memory_Game.py")

st.divider()

st.info("💡 **Tipp:** Du kannst auch das Menü in der linken Sidebar nutzen, um zwischen den Spielen zu wechseln!")

st.divider()
st.caption("Built with Streamlit 🚀")