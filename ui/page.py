import streamlit as st
import json
from sqlalchemy.orm import Session
from models.page import Page
from db.session import SessionLocal

class PageUI:
    def __init__(self, book_id: int):
        self.db: Session = SessionLocal()
        self.book_id = book_id

    def render(self):
        st.subheader("📄 Pages")

        pages = self.db.query(Page).filter(Page.book_id == self.book_id).all()

        for page in pages:
            st.markdown(f"**{page.title}** ({page.page_type})")

        with st.expander("➕ Add new page"):
            title = st.text_input("Page title")
            page_type = st.selectbox("Page type", ["text", "todo", "canvas"])
            if st.button("Create page"):
                new_page = Page(
                    title=title,
                    page_type=page_type,
                    book_id=self.book_id,
                    content=json.dumps({}),
                )
                self.db.add(new_page)
                self.db.commit()
                st.success("Page created.")
                st.rerun()
