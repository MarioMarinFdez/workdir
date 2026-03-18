import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Catálogo de Libros", page_icon="📖")
st.markdown("# Catálogo de Libros 📖")

API_URL = "http://fastapi:8000"

try:
    response = requests.get(f"{API_URL}/libros/")
    if response.status_code == 200:
        libros = response.json().get("libros", [])
        if libros:
            df = pd.DataFrame(libros)
            df["available"] = df["available"].map({True: "✅ Disponible", False: "❌ Prestado"})
            df.columns = ["ID", "Título", "Autor", "Disponibilidad"]
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No hay libros en el catálogo todavía.")
    else:
        st.error(f"Error al obtener libros: {response.status_code}")
except Exception as e:
    st.error(f"Error de conexión: {e}")

st.markdown("---")
st.markdown("## Añadir nuevo libro")

with st.form("add_book_form"):
    title = st.text_input("Título")
    author = st.text_input("Autor")
    isbn = st.text_input("ISBN (opcional)")
    submitted = st.form_submit_button("Añadir libro")

    if submitted:
        if not title or not author:
            st.error("El título y el autor son obligatorios.")
        else:
            try:
                response = requests.post(
                    f"{API_URL}/libros/",
                    params={"title": title, "author": author, "isbn": isbn or None}
                )
                if response.status_code == 200:
                    st.success(f"Libro '{title}' añadido correctamente.")
                    st.rerun()
                else:
                    st.error("Error al añadir el libro.")
            except Exception as e:
                st.error(f"Error de conexión: {e}")
