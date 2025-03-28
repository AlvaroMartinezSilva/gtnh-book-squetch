import streamlit as st
import os
import json
from datetime import datetime
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Config
IMG_DIR = Path("uploaded_images")
IMG_DIR.mkdir(exist_ok=True)

# SQLAlchemy setup
Base = declarative_base()
engine = create_engine("sqlite:///gtnh_library.db")
Session = sessionmaker(bind=engine)
session = Session()

class Libro(Base):
    __tablename__ = 'libros'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    estanteria = Column(String, nullable=False)
    paginas = relationship("Pagina", back_populates="libro")

class Pagina(Base):
    __tablename__ = 'paginas'
    id = Column(Integer, primary_key=True)
    libro_id = Column(Integer, ForeignKey('libros.id'))
    nombre = Column(String)
    tipo = Column(String)
    contenido = Column(Text)
    imagenes = Column(Text)
    fecha = Column(DateTime)
    libro = relationship("Libro", back_populates="paginas")

st.set_page_config(page_title="GTNH Biblioteca", layout="wide")
st.title("📘 Biblioteca de GregTech: New Horizons")

# Sidebar - estanterías
st.sidebar.header("📚 Estanterías")
estanterias = session.query(Libro.estanteria).distinct().all()
estanteria_nombres = [e[0] for e in estanterias]
selected_estanteria = st.sidebar.selectbox("Selecciona una estantería", ["+ Nueva estantería"] + estanteria_nombres)

if selected_estanteria == "+ Nueva estantería":
    with st.sidebar.form("form_estanteria"):
        nueva_estanteria = st.text_input("Nombre de la estantería")
        crear_est = st.form_submit_button("Crear")
        if crear_est and nueva_estanteria:
            st.session_state["nueva_estanteria"] = nueva_estanteria
            st.experimental_rerun()
else:
    st.sidebar.markdown("---")
    st.sidebar.subheader(f"📖 Libros en '{selected_estanteria}'")
    libros = session.query(Libro).filter_by(estanteria=selected_estanteria).all()
    libro_dict = {libro.nombre: libro.id for libro in libros}
    selected_libro = st.sidebar.selectbox("Selecciona un libro", ["+ Nuevo libro"] + list(libro_dict.keys()))

    if selected_libro == "+ Nuevo libro":
        with st.sidebar.form("form_nuevo_libro"):
            nuevo_nombre = st.text_input("Nombre del libro")
            crear_libro = st.form_submit_button("Crear libro")
            if crear_libro and nuevo_nombre:
                nuevo_libro = Libro(nombre=nuevo_nombre, estanteria=selected_estanteria)
                session.add(nuevo_libro)
                session.commit()
                st.experimental_rerun()
    else:
        libro_id = libro_dict[selected_libro]
        libro_obj = session.query(Libro).get(libro_id)
        st.sidebar.subheader("📄 Páginas")
        paginas = session.query(Pagina).filter_by(libro_id=libro_id).order_by(Pagina.fecha.desc()).all()
        pagina_nombres = [f"{p.nombre} ({p.tipo})" for p in paginas]
        selected_pagina_idx = st.sidebar.selectbox("Selecciona una página", ["+ Nueva página"] + pagina_nombres)

        if selected_pagina_idx == "+ Nueva página":
            with st.sidebar.form("form_nueva_pagina"):
                nombre_pagina = st.text_input("Nombre de la página")
                tipo_pagina = st.selectbox("Tipo de página", ["texto", "todo"])
                crear_pagina = st.form_submit_button("Crear página")
                if crear_pagina and nombre_pagina:
                    nueva = Pagina(
                        libro_id=libro_id,
                        nombre=nombre_pagina,
                        tipo=tipo_pagina,
                        contenido=json.dumps({}),
                        imagenes=json.dumps([]),
                        fecha=datetime.now()
                    )
                    session.add(nueva)
                    session.commit()
                    st.experimental_rerun()
        else:
            pagina = paginas[pagina_nombres.index(selected_pagina_idx)]
            st.subheader(f"📄 {pagina.nombre} ({pagina.tipo})")
            contenido = json.loads(pagina.contenido or '{}')
            imagenes = json.loads(pagina.imagenes or '[]')

            if pagina.tipo == "texto":
                texto = st.text_area("Contenido Markdown", value=contenido.get("texto", ""), height=300)
                if st.button("💾 Guardar texto"):
                    pagina.contenido = json.dumps({"texto": texto})
                    session.commit()
                    st.success("Texto guardado.")

            elif pagina.tipo == "todo":
                tareas = contenido.get("tareas", [])
                nuevas_tareas = []
                st.write("### Lista de tareas")
                for i, t in enumerate(tareas):
                    done = st.checkbox(t["texto"], value=t["hecho"], key=f"chk_{i}")
                    nuevas_tareas.append({"texto": t["texto"], "hecho": done})
                nueva = st.text_input("Nueva tarea")
                if st.button("➕ Añadir tarea") and nueva:
                    nuevas_tareas.append({"texto": nueva, "hecho": False})
                if st.button("💾 Guardar tareas"):
                    pagina.contenido = json.dumps({"tareas": nuevas_tareas})
                    session.commit()
                    st.success("Tareas actualizadas.")

            st.markdown("---")
            st.write("### 🖼️ Imágenes")
            uploaded_files = st.file_uploader("Sube una imagen", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
            for file in uploaded_files:
                img_path = IMG_DIR / f"{pagina.id}_{file.name}"
                with open(img_path, "wb") as f:
                    f.write(file.read())
                imagenes.append(str(img_path))
                pagina.imagenes = json.dumps(imagenes)
                session.commit()
                st.success(f"Imagen '{file.name}' guardada.")

            for img in imagenes:
                st.image(img, use_column_width=True)
