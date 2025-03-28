import streamlit as st
from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.db import Library,Permission,User

class LibraryUI:
    def __init__(self, username):
        self.username = username
        self.db: Session = SessionLocal()

    def render(self):
        st.header("📚 Your Libraries")

        owned = self.db.query(Library).join(User).filter(User.username == self.username).all()
        permitted = (
            self.db.query(Library)
            .join(Permission)
            .join(User)
            .filter(Permission.user.has(username=self.username))
            .all()
        )

        st.subheader("👑 Owned Libraries")
        for lib in owned:
            st.markdown(f"**{lib.name}** by {lib.author or 'Unknown'}")

        st.subheader("🔓 Shared with You")
        for lib in permitted:
            st.markdown(f"{lib.name} (by {lib.owner.username})")

        with st.expander("➕ Create new library"):
            name = st.text_input("Library name")
            author = st.text_input("Author (optional)")
            password = st.text_input("Password (optional)", type="password")
            if st.button("Create library"):
                user = self.db.query(User).filter(User.username == self.username).first()
                new_lib = Library(name=name, author=author, owner=user)
                if password:
                    new_lib.set_password(password)
                self.db.add(new_lib)
                self.db.commit()
                st.success("Library created!")
                st.rerun()
