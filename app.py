import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Hello World App",
    page_icon="👋",
    layout="centered"
)

# Main content
st.title("👋 Hello, World!")

st.write("Welcome to my Streamlit app!")

st.markdown("""
This is a simple Streamlit application deployed from GitHub.
            
### Features:
- Easy to deploy
- Interactive widgets
- Beautiful UI
""")

# Interactive element
name = st.text_input("What's your name?", "")

if name:
    st.success(f"Hello, {name}! Nice to meet you! 🎉")

# Footer
st.divider()
st.caption("Built with Streamlit 🚀")