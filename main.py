import streamlit as st
from ui.auth import AuthUI
from ui.dashboard import DashboardUI
from db.session import SessionLocal
from models.user import User

def load_user_info():
    if "user" in st.session_state and "user_id" not in st.session_state:
        with SessionLocal() as db:
            user = db.query(User).filter_by(username=st.session_state["user"]).first()
            if user:
                st.session_state["user_id"] = user.id

def logout():
    if st.sidebar.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()


def main():
    st.set_page_config(page_title="GTNH Library", layout="wide")
    load_user_info()

    if "user" not in st.session_state:
        AuthUI().render()
    else:
        st.sidebar.markdown(f"👤 **{st.session_state['user']}**")
        logout()
        DashboardUI().render()

if __name__ == "__main__":
    main()
