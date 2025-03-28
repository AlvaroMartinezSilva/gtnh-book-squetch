import streamlit as st
from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.shelf import Shelf
from models.library import Library
from models.permission import Permission
from models.user import User
from ui.collection import CollectionUI

class ShelfUI:
    def __init__(self, library_id: int):
        self.db: Session = SessionLocal()
        self.library_id = library_id
        self.user = self.db.query(User).filter_by(username=st.session_state["user"]).first()

    def render(self):
        if not self.has_view_permission():
            st.error("🚫 You do not have permission to view this library.")
            return

        st.subheader("🗄️ Shelves")

        shelves = self.db.query(Shelf).filter(Shelf.library_id == self.library_id).all()
        shelf_names = [shelf.name for shelf in shelves]

        selected = st.selectbox("Select a shelf", shelf_names)
        if selected:
            selected_shelf = next(s for s in shelves if s.name == selected)
            CollectionUI(selected_shelf.id).render()

        if self.has_edit_permission():
            with st.expander("➕ Add new shelf"):
                name = st.text_input("Shelf name")
                if st.button("Create shelf"):
                    new_shelf = Shelf(name=name, library_id=self.library_id)
                    self.db.add(new_shelf)
                    self.db.commit()
                    st.success("Shelf created.")
                    st.rerun()
        else:
            st.info("🔒 You have read-only access to this library.")

    def has_view_permission(self) -> bool:
        if self.user.id == self.db.query(Library).get(self.library_id).owner_id:
            return True
        perm = (
            self.db.query(Permission)
            .filter_by(user_id=self.user.id, library_id=self.library_id)
            .first()
        )
        return perm.can_view if perm else False

    def has_edit_permission(self) -> bool:
        if self.user.id == self.db.query(Library).get(self.library_id).owner_id:
            return True
        perm = (
            self.db.query(Permission)
            .filter_by(user_id=self.user.id, library_id=self.library_id)
            .first()
        )
        return perm.can_edit if perm else False
