import streamlit as st
import random
import time

# Page configuration
st.set_page_config(
    page_title="Memory Spiel",
    page_icon="🧠",
    layout="centered"
)

# Emoji-Paare für das Memory-Spiel
EMOJI_POOL = [
    "🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼",
    "🐨", "🐯", "🦁", "🐮", "🐷", "🐸", "🐵", "🐔",
    "🐧", "🐦", "🐤", "🦆", "🦅", "🦉", "🦇", "🐺",
    "🐗", "🐴", "🦄", "🐝", "🐛", "🦋", "🐌", "🐞",
    "🍎", "🍊", "🍋", "🍌", "🍉", "🍇", "🍓", "🍒",
    "🍑", "🥝", "🍍", "🥥", "🥑", "🍆", "🥕", "🌽",
    "⚽", "🏀", "🏈", "⚾", "🎾", "🏐", "🏉", "🎱",
    "🎮", "🎯", "🎲", "🎭", "🎨", "🎬", "🎪", "🎸"
]

def init_session_state():
    """Initialisiere Session State"""
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'cards' not in st.session_state:
        st.session_state.cards = []
    if 'revealed' not in st.session_state:
        st.session_state.revealed = []
    if 'matched' not in st.session_state:
        st.session_state.matched = []
    if 'first_card' not in st.session_state:
        st.session_state.first_card = None
    if 'second_card' not in st.session_state:
        st.session_state.second_card = None
    if 'moves' not in st.session_state:
        st.session_state.moves = 0
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'game_finished' not in st.session_state:
        st.session_state.game_finished = False
    if 'total_time' not in st.session_state:
        st.session_state.total_time = 0
    if 'show_mismatch' not in st.session_state:
        st.session_state.show_mismatch = False

def create_game(num_pairs):
    """Erstelle ein neues Spiel mit der angegebenen Anzahl von Paaren"""
    # Wähle zufällige Emojis aus
    selected_emojis = random.sample(EMOJI_POOL, num_pairs)
    # Erstelle Paare
    cards = selected_emojis * 2
    # Mische die Karten
    random.shuffle(cards)
    
    st.session_state.cards = cards
    st.session_state.revealed = [False] * len(cards)
    st.session_state.matched = [False] * len(cards)
    st.session_state.first_card = None
    st.session_state.second_card = None
    st.session_state.moves = 0
    st.session_state.start_time = time.time()
    st.session_state.game_started = True
    st.session_state.game_finished = False
    st.session_state.show_mismatch = False

def card_clicked(index):
    """Behandle Kartenklick"""
    # Ignoriere Klicks auf bereits aufgedeckte oder gefundene Karten
    if st.session_state.revealed[index] or st.session_state.matched[index]:
        return
    
    # Wenn zwei Karten zum Vergleichen angezeigt werden, räume sie zuerst auf
    if st.session_state.show_mismatch:
        st.session_state.revealed[st.session_state.first_card] = False
        st.session_state.revealed[st.session_state.second_card] = False
        st.session_state.first_card = None
        st.session_state.second_card = None
        st.session_state.show_mismatch = False
    
    # Decke die Karte auf
    st.session_state.revealed[index] = True
    
    if st.session_state.first_card is None:
        # Erste Karte
        st.session_state.first_card = index
    elif st.session_state.second_card is None:
        # Zweite Karte
        st.session_state.second_card = index
        st.session_state.moves += 1
        
        # Prüfe ob die Karten übereinstimmen
        if st.session_state.cards[st.session_state.first_card] == st.session_state.cards[st.session_state.second_card]:
            # Match gefunden!
            st.session_state.matched[st.session_state.first_card] = True
            st.session_state.matched[st.session_state.second_card] = True
            st.session_state.first_card = None
            st.session_state.second_card = None
            
            # Prüfe ob das Spiel gewonnen wurde
            if all(st.session_state.matched):
                st.session_state.game_finished = True
                st.session_state.total_time = time.time() - st.session_state.start_time
        else:
            # Kein Match - zeige beide Karten kurz
            st.session_state.show_mismatch = True

def reset_game():
    """Setze das Spiel zurück"""
    st.session_state.game_started = False
    st.session_state.game_finished = False

# Initialisiere Session State
init_session_state()

# Haupttitel
st.title("🧠 Memory Spiel")

# Wenn das Spiel nicht gestartet wurde, zeige Schwierigkeitsauswahl
if not st.session_state.game_started:
    st.write("### Wähle den Schwierigkeitsgrad")
    st.write("Wie viele Kartenpaare möchtest du spielen?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🟢 Einfach\n(6 Paare)", use_container_width=True):
            create_game(6)
            st.rerun()
    
    with col2:
        if st.button("🟡 Mittel\n(12 Paare)", use_container_width=True):
            create_game(12)
            st.rerun()
    
    with col3:
        if st.button("🔴 Schwer\n(18 Paare)", use_container_width=True):
            create_game(18)
            st.rerun()
    
    st.divider()
    
    # Benutzerdefinierte Anzahl
    custom_pairs = st.slider("Oder wähle eine benutzerdefinierte Anzahl:", min_value=3, max_value=32, value=8)
    if st.button("Mit dieser Anzahl starten", use_container_width=True):
        create_game(custom_pairs)
        st.rerun()

# Wenn das Spiel läuft
elif st.session_state.game_started and not st.session_state.game_finished:
    # Spielstatistiken
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Züge", st.session_state.moves)
    with col2:
        elapsed = int(time.time() - st.session_state.start_time)
        st.metric("Zeit", f"{elapsed}s")
    with col3:
        found = sum(st.session_state.matched) // 2
        total = len(st.session_state.cards) // 2
        st.metric("Gefunden", f"{found}/{total}")
    
    st.divider()
    
    # CSS für quadratische Karten
    st.markdown("""
    <style>
    .stButton > button {
        height: 80px;
        font-size: 40px;
        padding: 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Berechne Grid-Layout basierend auf Anzahl der Karten
    num_cards = len(st.session_state.cards)
    if num_cards <= 12:
        cols_per_row = 4
    elif num_cards <= 24:
        cols_per_row = 6
    elif num_cards <= 36:
        cols_per_row = 6
    else:
        cols_per_row = 8
    
    # Zeige die Karten in mehreren Reihen
    for row_start in range(0, num_cards, cols_per_row):
        cols = st.columns(cols_per_row)
        for i, col in enumerate(cols):
            card_index = row_start + i
            if card_index < num_cards:
                with col:
                    # Zeige Emoji wenn aufgedeckt oder gefunden
                    if st.session_state.revealed[card_index] or st.session_state.matched[card_index]:
                        if st.session_state.matched[card_index]:
                            # Gefundene Karten mit grünem Hintergrund
                            st.button(
                                st.session_state.cards[card_index],
                                key=f"card_{card_index}",
                                disabled=True,
                                use_container_width=True,
                                type="primary"
                            )
                        else:
                            # Aufgedeckte Karten
                            st.button(
                                st.session_state.cards[card_index],
                                key=f"card_{card_index}",
                                disabled=True,
                                use_container_width=True
                            )
                    else:
                        # Verdeckte Karten
                        if st.button("❓", key=f"card_{card_index}", use_container_width=True):
                            card_clicked(card_index)
                            st.rerun()

# Wenn das Spiel gewonnen wurde
elif st.session_state.game_finished:
    st.balloons()
    st.success("🎉 Glückwunsch! Du hast gewonnen!")
    
    st.divider()
    
    st.write("### 📊 Deine Statistik")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Gesamtzeit", f"{st.session_state.total_time:.1f} Sekunden")
        st.metric("Anzahl Züge", st.session_state.moves)
    
    with col2:
        num_pairs = len(st.session_state.cards) // 2
        st.metric("Kartenpaare", num_pairs)
        # Berechne Effizienz (perfekt wäre Anzahl Paare = Anzahl Züge)
        efficiency = (num_pairs / st.session_state.moves) * 100 if st.session_state.moves > 0 else 0
        st.metric("Effizienz", f"{efficiency:.1f}%")
    
    st.divider()
    
    # Durchschnittliche Zeit pro Zug
    avg_time = st.session_state.total_time / st.session_state.moves if st.session_state.moves > 0 else 0
    st.info(f"⏱️ Durchschnittliche Zeit pro Zug: {avg_time:.1f} Sekunden")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Nochmal spielen", use_container_width=True):
            create_game(len(st.session_state.cards) // 2)
            st.rerun()
    with col2:
        if st.button("🏠 Zurück zum Start", use_container_width=True):
            reset_game()
            st.rerun()

# Footer
st.divider()
st.caption("Built with Streamlit 🚀")