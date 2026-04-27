import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Historial de Préstamos", page_icon="📋")
st.markdown("# Historial de Préstamos 📋")

API_URL = "http://fastapi:8000"

# Obtener lista de usuarios
try:
    response = requests.get(f"{API_URL}/usuarios/")
    usuarios = response.json().get("usuarios", []) if response.status_code == 200 else []
except Exception:
    usuarios = []

if not usuarios:
    st.warning("No hay usuarios registrados todavía.")
else:
    opciones = {f"{u['name']} (ID: {u['id']})": u['id'] for u in usuarios}
    seleccion = st.selectbox("Selecciona un usuario", list(opciones.keys()))
    user_id = opciones[seleccion]

    try:
        response = requests.get(f"{API_URL}/prestamos/usuario/{user_id}")
        if response.status_code == 200:
            data = response.json()
            prestamos = data.get("prestamos", [])

            if not prestamos:
                st.info(f"{data['usuario']} no tiene historial de préstamos.")
            else:
                st.markdown(f"### Historial de **{data['usuario']}**")

                activos = [p for p in prestamos if p["activo"]]
                cerrados = [p for p in prestamos if not p["activo"]]

                if activos:
                    st.markdown("#### 🟢 Préstamos activos")
                    df_activos = pd.DataFrame(activos)[["id", "libro", "loan_date", "due_date"]]
                    df_activos.columns = ["ID", "Libro", "Fecha préstamo", "Fecha límite"]
                    st.dataframe(df_activos, use_container_width=True)

                if cerrados:
                    st.markdown("#### ✅ Préstamos devueltos")
                    df_cerrados = pd.DataFrame(cerrados)[["id", "libro", "loan_date", "return_date"]]
                    df_cerrados.columns = ["ID", "Libro", "Fecha préstamo", "Fecha devolución"]
                    st.dataframe(df_cerrados, use_container_width=True)
        else:
            st.error("Error al obtener el historial.")
    except Exception as e:
        st.error(f"Error de conexión: {e}")
