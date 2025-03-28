import streamlit as st
from ui.auth import auth_ui
from ui.dashboard import show_dashboard

def main():
    if "user" not in st.session_state:
        auth_ui()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()
