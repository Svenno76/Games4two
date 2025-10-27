import streamlit as st
import random
import time

# Page configuration
st.set_page_config(
    page_title="Memory Spiel",
    page_icon="🧠",
    layout="centered"
)

# Rennwagen-Bilder für das Memory-Spiel (Unsplash)
RACING_CAR_IMAGES = [
    "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=400&h=300&fit=crop",  # Red Formula 1
    "https://images.unsplash.com/photo-1583121274602-3e2820c69888?w=400&h=300&fit=crop",  # Blue sports car
    "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400&h=300&fit=crop",  # Yellow race car
    "https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=400&h=300&fit=crop",  # Green racing car
    "https://images.unsplash.com/photo-1542362567-b07e54358753?w=400&h=300&fit=crop",  # Orange supercar
    "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=400&h=300&fit=crop",  # White sports car
    "https://images.unsplash.com/photo-1525609004556-c46c7d6cf023?w=400&h=300&fit=crop",  # Black racing car
    "https://images.unsplash.com/photo-1563720223185-11003d516935?w=400&h=300&fit=crop",  # Pink race car
    "https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=400&h=300&fit=crop",  # Silver sports car
    "https://images.unsplash.com/photo-1514316454349-750a7fd3da3a?w=400&h=300&fit=crop",  # Classic race car
    "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?w=400&h=300&fit=crop",  # Modern supercar
    "https://images.unsplash.com/photo-1489824904134-891ab64532f1?w=400&h=300&fit=crop",  # Vintage race car
    "https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?w=400&h=300&fit=crop",  # Blue Formula car
    "https://images.unsplash.com/photo-1566023888375-f96c4d926c6b?w=400&h=300&fit=crop",  # Red supercar
    "https://images.unsplash.com/photo-1605559424843-9e4c228bf1c2?w=400&h=300&fit=crop",  # Track racing car
    "https://images.unsplash.com/photo-1541443131876-44b03de101c5?w=400&h=300&fit=crop",  # Yellow supercar
    "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=400&h=300&fit=crop",  # Classic sports car
    "https://images.unsplash.com/photo-1518672364719-c5e8bfbf7851?w=400&h=300&fit=crop",  # Rally car
    "https://images.unsplash.com/photo-1547038577-077f0e7ea3de?w=400&h=300&fit=crop",  # NASCAR style
    "https://images.unsplash.com/photo-1553440569-bcc63803a83d?w=400&h=300&fit=crop",  # GT racing car
    "https://images.unsplash.com/photo-1600712242805-5f78671b24da?w=400&h=300&fit=crop",  # Lamborghini
    "https://images.unsplash.com/photo-1616422285623-13ff0162193c?w=400&h=300&fit=crop",  # Ferrari
    "https://images.unsplash.com/photo-1603386329225-868f9b1ee6b9?w=400&h=300&fit=crop",  # Porsche race car
    "https://images.unsplash.com/photo-1565150449199-93ea0b6a83e2?w=400&h=300&fit=crop",  # McLaren
    "https://images.unsplash.com/photo-1583121274602-3e2820c69888?w=400&h=300&fit=crop&sat=10",  # Modified blue
    "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400&h=300&fit=crop&sat=10",  # Modified yellow
    "https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=400&h=300&fit=crop&sat=10",  # Modified green
    "https://images.unsplash.com/photo-1542362567-b07e54358753?w=400&h=300&fit=crop&sat=10",  # Modified orange
    "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=400&h=300&fit=crop&sat=10",  # Modified white
    "https://images.unsplash.com/photo-1525609004556-c46c7d6cf023?w=400&h=300&fit=crop&sat=10",  # Modified black
    "https://images.unsplash.com/photo-1563720223185-11003d516935?w=400&h=300&fit=crop&sat=10",  # Modified pink
    "https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=400&h=300&fit=crop&sat=10",  # Modified silver
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
    # Wähle zufällige Rennwagen-Bilder aus
    selected_images = random.sample(RACING_CAR_IMAGES, num_pairs)
    # Erstelle Paare
    cards = selected_images * 2
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

    # CSS für Bildkarten
    st.markdown("""
    <style>
    .stButton > button {
        height: 150px;
        font-size: 60px;
        padding: 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: transform 0.2s;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    .card-container {
        cursor: pointer;
        border-radius: 10px;
        overflow: hidden;
        margin: 5px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: transform 0.2s;
        background: #1a1a1a;
        aspect-ratio: 1;
        height: 150px;
    }
    .card-container:hover {
        transform: scale(1.05);
    }
    .card-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .card-matched {
        border: 4px solid #00ff00;
        opacity: 0.8;
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
                    # Zeige Bild wenn aufgedeckt oder gefunden
                    if st.session_state.revealed[card_index] or st.session_state.matched[card_index]:
                        card_class = "card-matched" if st.session_state.matched[card_index] else ""
                        st.markdown(
                            f'<div class="card-container {card_class}">'
                            f'<img src="{st.session_state.cards[card_index]}" class="card-image" />'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        # Verdeckte Karte als Button
                        if st.button("🏁", key=f"card_{card_index}", use_container_width=True):
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