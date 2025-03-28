import streamlit as st
from sqlalchemy.orm import Session
from models.db import Collection, Book, Page
from db.session import SessionLocal
from datetime import datetime

class BookUI:
    def __init__(self, collection_id: int):
        self.db: Session = SessionLocal()
        self.collection_id = collection_id

    def render(self):
        st.subheader("📘 Books")

        books = self.db.query(Book).filter(Book.collection_id == self.collection_id).all()

        for book in books:
            with st.expander(f"📖 {book.title} — Tags: {book.tags or '—'}"):
                pages = self.db.query(Page).filter(Page.book_id == book.id).all()
                for page in pages:
                    st.markdown(f"• **{page.title or '(Untitled Page)'}** — {page.page_type or 'text'}")

                with st.form(f"add_page_form_{book.id}"):
                    st.markdown("➕ Add page to this book")
                    title = st.text_input("Page title", key=f"title_{book.id}")
                    page_type = st.selectbox("Page type", ["text", "todo", "canvas"], key=f"type_{book.id}")
                    content = st.text_area("Content", key=f"content_{book.id}")
                    if st.form_submit_button("Add page"):
                        page = Page(
                            title=title,
                            page_type=page_type,
                            content=content,
                            book_id=book.id,
                            created_at=datetime.utcnow()
                        )
                        self.db.add(page)
                        self.db.commit()
                        st.success("✅ Page added.")
                        st.rerun()

        with st.expander("➕ Add new book"):
            title = st.text_input("Title")
            tags = st.text_input("Tags (comma-separated)")
            if st.button("Add book"):
                new_book = Book(title=title, tags=tags, collection_id=self.collection_id)
                self.db.add(new_book)
                self.db.commit()
                st.success("✅ Book added.")
                st.rerun()
