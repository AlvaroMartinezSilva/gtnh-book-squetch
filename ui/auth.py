import streamlit as st
from sqlalchemy.orm import Session
from models.db import User, Library, Permission  # 🔐 Esto resuelve las relaciones
from db.session import SessionLocal

class AuthUI:
    def __init__(self):
        if "auth_mode" not in st.session_state:
            st.session_state["auth_mode"] = "login"

    def render(self):
        if st.session_state["auth_mode"] == "login":
            self.login_form()
        else:
            self.register_form()

    def login_form(self):
        st.title("🔐 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            with SessionLocal() as db:
                user = db.query(User).filter(User.username == username).first()
                if user and user.verify_password(password):
                    st.session_state["user"] = user.username
                    st.success(f"Welcome {user.username}!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        if st.button("Don't have an account? Register"):
            st.session_state["auth_mode"] = "register"
            st.rerun()

    def register_form(self):
        st.title("🆕 Register")
        username = st.text_input("New username")
        password = st.text_input("New password", type="password")
        confirm = st.text_input("Confirm password", type="password")
        if st.button("Register"):
            if password != confirm:
                st.error("Passwords do not match")
                return
            with SessionLocal() as db:
                if db.query(User).filter(User.username == username).first():
                    st.error("Username already taken")
                    return
                new_user = User(username=username, password_hash=User.hash_password(password))
                db.add(new_user)
                db.commit()
                st.success("Account created successfully.")
                st.session_state["auth_mode"] = "login"
                st.rerun()
        if st.button("Already have an account? Login"):
            st.session_state["auth_mode"] = "login"
            st.rerun()
