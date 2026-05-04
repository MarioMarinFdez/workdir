import streamlit as st
import requests
import calendar
from datetime import datetime

st.set_page_config(page_title="Calendario de Préstamos", layout="wide", page_icon="📅")

API_BASE = "http://fastapi:8000"

st.title("Calendario de Préstamos 🗓️")


@st.cache_data(ttl=30)
def get_usuarios():
    try:
        r = requests.get(f"{API_BASE}/usuarios/", timeout=5)
        r.raise_for_status()
        return r.json().get("usuarios", []), None
    except Exception as e:
        return None, str(e)


@st.cache_data(ttl=30)
def get_prestamos(user_id=None):
    try:
        params = {}
        if user_id:
            params["user_id"] = user_id
        r = requests.get(f"{API_BASE}/prestamos/", params=params, timeout=5)
        r.raise_for_status()
        return r.json().get("prestamos", []), None
    except Exception as e:
        return None, str(e)


usuarios, err = get_usuarios()
if err:
    st.error(f"Error cargando usuarios: {err}")
    st.stop()

if not usuarios:
    st.warning("No hay usuarios registrados.")
    st.stop()

st.subheader("Selecciona un usuario")
opciones = {f"{u['name']} (ID: {u['id']})": u["id"] for u in usuarios}
seleccion = st.selectbox("", list(opciones.keys()))
user_id = opciones[seleccion]

prestamos, error = get_prestamos(user_id)
if error:
    st.error(f"Error de conexión: {error}")
    st.stop()

if not prestamos:
    st.info("Este usuario no tiene préstamos registrados.")
    st.stop()

now = datetime.now()
col1, col2 = st.columns([1, 3])
with col1:
    year = st.number_input("Año", min_value=2020, max_value=2030, value=now.year)
    month = st.selectbox(
        "Mes",
        list(range(1, 13)),
        index=now.month - 1,
        format_func=lambda m: calendar.month_name[m],
    )

cal = calendar.monthcalendar(year, month)
month_events = {}
for p in prestamos:
    for campo, etiqueta in [("loan_date", "📖"), ("due_date", "⏰"), ("return_date", "✅")]:
        if p.get(campo):
            try:
                d = datetime.fromisoformat(p[campo])
                if d.year == year and d.month == month:
                    month_events.setdefault(d.day, []).append(f"{etiqueta} {(p.get('libro') or '?')[:15]}")
            except Exception:
                pass

with col2:
    st.markdown(f"### {calendar.month_name[month]} {year}")
    header_cols = st.columns(7)
    for i, day_name in enumerate(["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]):
        header_cols[i].markdown(f"**{day_name}**")

    for week in cal:
        week_cols = st.columns(7)
        for i, day in enumerate(week):
            if day == 0:
                week_cols[i].write("")
            else:
                events = month_events.get(day, [])
                if events:
                    week_cols[i].markdown(f"**{day}**\n\n" + "\n\n".join(events))
                else:
                    week_cols[i].write(str(day))

st.markdown("---")
st.markdown("**Leyenda:** 📖 Préstamo &nbsp;&nbsp; ⏰ Fecha límite &nbsp;&nbsp; ✅ Devolución")

st.markdown("---")
st.subheader(f"Préstamos en {calendar.month_name[month]} {year}")
month_all = [
    p for p in prestamos
    if p.get("loan_date") and
    datetime.fromisoformat(p["loan_date"]).year == year and
    datetime.fromisoformat(p["loan_date"]).month == month
]
if month_all:
    import pandas as pd
    df = pd.DataFrame([{
        "Libro": p.get("libro", "-"),
        "Autor": p.get("autor", "-"),
        "Fecha préstamo": p.get("loan_date", "-")[:10] if p.get("loan_date") else "-",
        "Fecha límite": p.get("due_date", "-")[:10] if p.get("due_date") else "-",
        "Devuelto": p.get("return_date", "")[:10] if p.get("return_date") else "Activo",
        "Estado": "⚠️ Vencido" if p.get("vencido") else ("✅ Devuelto" if p.get("return_date") else "📖 Activo"),
    } for p in month_all])
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("Sin préstamos este mes.")
