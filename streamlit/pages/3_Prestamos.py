import streamlit as st
import requests

st.set_page_config(page_title="Préstamos", page_icon="✍️")
st.markdown("# Gestión de Préstamos ✍️")

API_URL = "http://fastapi:8000"

st.markdown("## Realizar un préstamo")

with st.form("loan_form"):
    user_id = st.number_input("ID del Usuario", min_value=1, step=1)
    book_id = st.number_input("ID del Libro", min_value=1, step=1)
    submitted = st.form_submit_button("Realizar Préstamo")

    if submitted:
        try:
            response = requests.post(
                f"{API_URL}/prestamos/",
                params={"user_id": user_id, "book_id": book_id}
            )
            if response.status_code == 200:
                st.success("Préstamo registrado correctamente.")
                st.json(response.json())
            else:
                st.error(f"Error: {response.json().get('detail', 'Error desconocido')}")
        except Exception as e:
            st.error(f"Error de conexión: {e}")

st.markdown("---")
st.markdown("## Devolver un préstamo")

with st.form("return_form"):
    loan_id = st.number_input("ID del Préstamo", min_value=1, step=1)
    submitted = st.form_submit_button("Devolver libro")

    if submitted:
        try:
            response = requests.post(f"{API_URL}/prestamos/{loan_id}/devolver")
            if response.status_code == 200:
                st.success("Libro devuelto correctamente.")
                st.json(response.json())
            else:
                st.error(f"Error: {response.json().get('detail', 'Error desconocido')}")
        except Exception as e:
            st.error(f"Error de conexión: {e}")
