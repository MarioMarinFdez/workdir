import streamlit as st
import requests
from streamlit_calendar import calendar

st.set_page_config(page_title="Calendario de Préstamos", page_icon="📅")
st.markdown("# Calendario de Préstamos 📅")

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
                st.info(f"{data['usuario']} no tiene préstamos para mostrar en el calendario.")
            else:
                eventos = []
                for p in prestamos:
                    color = "#FF6B6B" if p["activo"] else "#51CF66"
                    fecha_fin = p["return_date"] or p["due_date"] or p["loan_date"]
                    eventos.append({
                        "title": p["libro"],
                        "start": p["loan_date"][:10],
                        "end": fecha_fin[:10],
                        "backgroundColor": color,
                        "borderColor": color,
                    })

                st.markdown("🔴 Préstamo activo &nbsp;&nbsp; 🟢 Devuelto")

                calendar(
                    events=eventos,
                    options={
                        "initialView": "dayGridMonth",
                        "headerToolbar": {
                            "left": "prev,next today",
                            "center": "title",
                            "right": "dayGridMonth,listMonth"
                        },
                        "height": 600,
                    }
                )
        else:
            st.error("Error al obtener los préstamos.")
    except Exception as e:
        st.error(f"Error de conexión: {e}")
