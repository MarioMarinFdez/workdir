# 📅 DAILYS — Stand-ups Diarios

Registro de las reuniones diarias del equipo siguiendo la metodología XP.

---

## Formato

**Fecha**: DD/MM/AAAA  
**Asistentes**: nombres del equipo  
**¿Qué hice ayer?**  
**¿Qué haré hoy?**  
**¿Tengo algún bloqueo?**

---

## Sprint 1 — Arquitectura base y BD (04/03 - 14/03)

### 📆 04/03/2026
**Asistentes**: Mario  
**¿Qué hice ayer?** Kick-off del proyecto, lectura del enunciado y reparto de tareas.  
**¿Qué haré hoy?** Subir el código base del profesor al repositorio. Revisar la arquitectura inicial.  
**¿Bloqueos?** Ninguno.

### 📆 09/03/2026
**Asistentes**: Mario  
**¿Qué hice ayer?** Revisión del esqueleto inicial.  
**¿Qué haré hoy?** Configurar el `.gitignore`. Estudiar SQLAlchemy para el modelado de datos.  
**¿Bloqueos?** Dudas sobre cómo estructurar la capa de datos.

### 📆 12/03/2026
**Asistentes**: Mario  
**¿Qué hice ayer?** Configuración del entorno completada.  
**¿Qué haré hoy?** Implementar los modelos SQLAlchemy (Book, User, Loan), repositorios y loan service. Integrar FastAPI con la nueva capa de BD.  
**¿Bloqueos?** Ninguno.

---

## Sprint 2 — Calidad, tests y CI (18/03 - 13/04)

### 📆 18/03/2026
**Asistentes**: Mario  
**¿Qué hice ayer?** Capa de datos funcional con SQLAlchemy.  
**¿Qué haré hoy?** Conectar la API a la BD y construir la interfaz Streamlit con páginas de usuarios, libros y préstamos.  
**¿Bloqueos?** Ninguno.

### 📆 19/03/2026
**Asistentes**: Mario  
**¿Qué hice ayer?** Interfaz Streamlit básica funcionando.  
**¿Qué haré hoy?** Escribir tests unitarios para el loan service siguiendo TDD. Añadir búsqueda de libros.  
**¿Bloqueos?** Ninguno.

### 📆 11/04/2026
**Asistentes**: Mario  
**¿Qué hice ayer?** Tests unitarios del loan service pasando.  
**¿Qué haré hoy?** Refactorizar la API usando APIRouter, añadir logging con 3 niveles, decorador `@log_execution_time` y caché en Streamlit con `@st.cache_data`.  
**¿Bloqueos?** Ninguno.

### 📆 13/04/2026
**Asistentes**: Raúl, Marcos  
**¿Qué hice ayer?** APIRouter, logging y caché implementados por Mario.  
**¿Qué haré hoy?** Configurar GitHub Actions CI, añadir tests de routers con TestClient y BD en memoria, corregir cobertura hasta superar el 80%.  
**¿Bloqueos?** Conflictos al hacer merge de ramas main y master. Resuelto manualmente.

---

## Sprint 3 — Técnicas avanzadas y cierre (14/04 - 20/04)

### 📆 14/04/2026
**Asistentes**: Gonzalo, Raúl, Marcos  
**¿Qué hice ayer?** CI funcionando con cobertura >80%.  
**¿Qué haré hoy?** Gonzalo arregla Dockerfiles y docker-compose. Raúl y Marcos añaden comentarios de documentación y revisan el código.  
**¿Bloqueos?** El contexto de build de Docker no incluía la carpeta `data/`. Resuelto moviendo el contexto a la raíz.

### 📆 20/04/2026
**Asistentes**: Gonzalo  
**¿Qué hice ayer?** Dockerfiles corregidos, CI verde.  
**¿Qué haré hoy?** Implementar generadores (`yield`, `yield_per`) en los repositorios. Ajustar `.coveragerc` para excluir archivos auxiliares.  
**¿Bloqueos?** La carpeta `data/` estaba en el `.gitignore`. Resuelto eliminando esa línea.

---

## Resumen de participación

| Miembro | Contribuciones principales |
|---|---|
| **Mario** | Código base, SQLAlchemy+FastAPI, Streamlit, logging, APIRouter, caché, tests loan service |
| **Raúl** | Tests de routers, GitHub Actions CI, cobertura >80%, documentación (pair con Marcos) |
| **Gonzalo** | Dockerfiles, docker-compose, generadores yield, CI fixes |
| **Marcos** | Tests de routers, CI, documentación (pair programming con Raúl) |
