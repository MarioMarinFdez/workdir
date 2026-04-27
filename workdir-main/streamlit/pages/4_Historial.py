import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Historial de Préstamos", page_icon="📋")
st.markdown("# Historial de Préstamos 📋")

API_URL = "http://fastapi:8000"

try:
    response = requests.get(f"{API_URL}/usuarios/")
    usuarios = response.json().get("usuarios", []) if response.status_code == 200 else []
except Exception:
    usuarios = []

if not usuarios:
    st.warning("No hay usuarios registrados todavía.")
else:
    opciones = {f"{u['name']} (ID: {u['id']})": u["id"] for u in usuarios}
    seleccion = st.selectbox("Selecciona un usuario", list(opciones.keys()))
    user_id = opciones[seleccion]

    try:
        response = requests.get(f"{API_URL}/prestamos/usuario/{user_id}")
        if response.status_code == 200:
            data = response.json()
            prestamos = data.get("prestamos", [])
            st.markdown(f"### Historial de **{data['usuario']}**")

            if not prestamos:
                st.info("Este usuario no tiene préstamos registrados.")
            else:
                df = pd.DataFrame(prestamos)
                df["Estado"] = df["activo"].map({True: "🟡 Activo", False: "✅ Devuelto"})
                df["Vencido"] = df["vencido"].map({True: "⚠️ Sí", False: "—"})
                df = df.rename(columns={
                    "loan_id": "ID Préstamo",
                    "book_title": "Libro",
                    "loan_date": "Fecha préstamo",
                    "due_date": "Fecha límite",
                    "return_date": "Fecha devolución",
                })
                df = df[["ID Préstamo", "Libro", "Fecha préstamo", "Fecha límite", "Fecha devolución", "Estado", "Vencido"]]
                st.dataframe(df, use_container_width=True)

                activos = df[df["Estado"] == "🟡 Activo"]
                devueltos = df[df["Estado"] == "✅ Devuelto"]
                col1, col2 = st.columns(2)
                col1.metric("Préstamos activos", len(activos))
                col2.metric("Préstamos devueltos", len(devueltos))
        else:
            st.error(f"Error: {response.json().get('detail', 'Error desconocido')}")
    except Exception as e:
        st.error(f"Error de conexión: {e}")
