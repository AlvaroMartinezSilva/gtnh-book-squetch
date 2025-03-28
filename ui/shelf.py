import streamlit as st
from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.shelf import Shelf
from models.library import Library

class ShelfUI:
    def __init__(self, library_id: int):
        self.db: Session = SessionLocal()
        self.library_id = library_id

    def render(self):
        st.subheader("🗄️ Shelves")

        shelves = self.db.query(Shelf).filter(Shelf.library_id == self.library_id).all()
        shelf_names = [shelf.name for shelf in shelves]
        selected = st.selectbox("Select a shelf", shelf_names)

        if selected:
            selected_shelf = next(s for s in shelves if s.name == selected)
            from ui.collection import CollectionUI
            CollectionUI(selected_shelf.id).render()

        with st.expander("➕ Add new shelf"):
            name = st.text_input("Shelf name")
            if st.button("Create shelf"):
                new_shelf = Shelf(name=name, library_id=self.library_id)
                self.db.add(new_shelf)
                self.db.commit()
                st.success("Shelf created.")
                st.experimental_rerun()
