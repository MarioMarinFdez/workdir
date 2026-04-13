import streamlit as st
import requests

st.set_page_config(page_title="Usuarios", page_icon="👤")
st.markdown("# Gestión de Usuarios 👤")

API_URL = "http://fastapi:8000"

# Listado de usuarios
try:
    response = requests.get(f"{API_URL}/usuarios/")
    if response.status_code == 200:
        usuarios = response.json().get("usuarios", [])
        if usuarios:
            import pandas as pd
            df = pd.DataFrame(usuarios)
            df.columns = ["ID", "Nombre", "Email"]
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No hay usuarios registrados todavía.")
    else:
        st.error(f"Error: {response.status_code}")
except Exception as e:
    st.error(f"Error de conexión: {e}")

st.markdown("---")
st.markdown("## Registrar nuevo usuario")

with st.form("add_user_form"):
    name = st.text_input("Nombre")
    email = st.text_input("Email")
    submitted = st.form_submit_button("Registrar usuario")

    if submitted:
        if not name or not email:
            st.error("El nombre y el email son obligatorios.")
        else:
            try:
                response = requests.post(
                    f"{API_URL}/usuarios/",
                    params={"name": name, "email": email}
                )
                if response.status_code == 200:
                    st.success(f"Usuario '{name}' registrado correctamente.")
                    st.rerun()
                else:
                    st.error("Error al registrar el usuario.")
            except Exception as e:
                st.error(f"Error de conexión: {e}")
