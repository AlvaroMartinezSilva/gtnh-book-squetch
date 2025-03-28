import streamlit as st
from sqlalchemy.orm import Session
from models.book import Book
from models.collections import Collection
from db.session import SessionLocal

class BookUI:
    def __init__(self, collection_id: int):
        self.db: Session = SessionLocal()
        self.collection_id = collection_id

    def render(self):
        st.subheader("📘 Books")

        books = self.db.query(Book).filter(Book.collection_id == self.collection_id).all()

        for book in books:
            st.markdown(f"- **{book.title}** — Tags: {book.tags or '—'}")

        with st.expander("➕ Add new book"):
            title = st.text_input("Title")
            tags = st.text_input("Tags (comma-separated)")
            if st.button("Add book"):
                new_book = Book(title=title, tags=tags, collection_id=self.collection_id)
                self.db.add(new_book)
                self.db.commit()
                st.success("Book added.")
                st.rerun()

