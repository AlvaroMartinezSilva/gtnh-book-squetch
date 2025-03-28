import streamlit as st
from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.collections import Collection

class CollectionUI:
    def __init__(self, shelf_id: int):
        self.db: Session = SessionLocal()
        self.shelf_id = shelf_id

    def render(self):
        st.subheader("📂 Collections")

        collections = self.db.query(Collection).filter(Collection.shelf_id == self.shelf_id).all()
        collection_names = [c.name for c in collections]
        selected = st.selectbox("Select a collection", collection_names)

        if selected:
            selected_collection = next(c for c in collections if c.name == selected)
            from ui.book import BookUI
            BookUI(selected_collection.id).render()

        with st.expander("➕ Add new collection"):
            name = st.text_input("Collection name")
            if st.button("Create collection"):
                new_collection = Collection(name=name, shelf_id=self.shelf_id)
                self.db.add(new_collection)
                self.db.commit()
                st.success("Collection created.")
                st.experimental_rerun()
