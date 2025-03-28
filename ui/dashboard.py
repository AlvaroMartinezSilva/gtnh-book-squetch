import streamlit as st
from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.db import User,Permission,Library
from ui.shelf import ShelfUI

class DashboardUI:
    def __init__(self):
        self.db: Session = SessionLocal()
        self.username = st.session_state["user"]
        self.user = self.db.query(User).filter(User.username == self.username).first()

    def render(self):
        st.title("📚 GTNH Library Dashboard")
        st.write(f"Welcome, **{self.username}**")

        st.markdown("---")
        st.subheader("📖 Your Libraries")

        owned_libs = self.db.query(Library).filter(Library.owner == self.user).all()
        shared_libs = (
            self.db.query(Library)
            .join(Permission)
            .filter(Permission.user_id == self.user.id, Permission.can_view == True)
            .all()
        )


        options = ["+ Create new"] + [f"{lib.name} (owner)" for lib in owned_libs] + [f"{lib.name} (shared)" for lib in shared_libs]
        selected = st.selectbox("Select a library", options)

        if selected == "+ Create new":
            self._create_library()
        else:
            library = self._resolve_library(selected, owned_libs, shared_libs)
            if library:
                ShelfUI(library.id).render()

    def _create_library(self):
        with st.expander("➕ New Library"):
            name = st.text_input("Library name")
            author = st.text_input("Author (optional)", value=self.username)
            password = st.text_input("Password (optional)", type="password")
            if st.button("Create"):
                lib = Library(name=name, author=author, owner=self.user)
                if password:
                    lib.set_password(password)
                self.db.add(lib)
                self.db.commit()
                st.success("Library created.")
                st.rerun()

    def _resolve_library(self, selection, owned, shared):
        name = selection.replace(" (owner)", "").replace(" (shared)", "")
        for lib in owned + shared:
            if lib.name == name:
                return lib
        return None
