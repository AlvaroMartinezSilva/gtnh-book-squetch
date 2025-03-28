import streamlit as st

class DashboardUI:
    def render(self):
        st.title("📚 GTNH Library Dashboard")
        st.write(f"Welcome, {st.session_state['user']}!")

        # Aquí podrías importar e instanciar otras clases (LibraryUI, BookUI, etc.)
