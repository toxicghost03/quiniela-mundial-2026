# ⚽ Quiniela Mundial 2026 — Streamlit

App de quiniela familiar con Streamlit + Firebase Firestore.  
Multi-usuario · Leaderboard en tiempo real · Fase de grupos + Eliminatorias · Panel admin

---

## 🚀 Deploy en Streamlit Cloud (gratis) — 15 min

### Paso 1 — Firebase
1. Ve a [console.firebase.google.com](https://console.firebase.google.com)
2. Crea un proyecto → Activar **Firestore Database** (modo prueba)
3. Ve a **Configuración del proyecto → Cuentas de servicio**
4. Clic en **"Generar nueva clave privada"** → descarga el JSON
5. Abre ese JSON, copia TODO el contenido

### Paso 2 — GitHub
1. Sube esta carpeta a un repositorio en GitHub (público o privado)
2. Haz push de todos los archivos

### Paso 3 — Streamlit Cloud
1. Ve a [share.streamlit.io](https://share.streamlit.io) → conecta tu GitHub
2. New app → selecciona tu repo → main file: `app.py`
3. Ve a **Advanced settings → Secrets** y pega esto:

```toml
FIREBASE_KEY = '''
{
  "type": "service_account",
  "project_id": "TU_PROYECTO",
  ... (pega aquí el JSON completo de Firebase)
}
'''
```

4. Deploy → en 2 minutos tienes tu URL pública

### Paso 4 — Cambiar contraseña admin
En `data.py`:
```python
ADMIN_PASSWORD = "pon-tu-contraseña-aqui"
```

---

## 📁 Estructura
```
quiniela-streamlit/
├── app.py              ← App principal (usuarios)
├── pages/
│   └── admin.py        ← Panel de admin
├── data.py             ← Equipos, grupos, puntuación
├── requirements.txt    ← Dependencias
├── .streamlit/
│   └── config.toml     ← Tema dark + dorado
└── README.md
```

---

## 🏆 Sistema de puntos
| Predicción | Puntos |
|---|---|
| 1° de grupo | 3 |
| 2° de grupo | 2 |
| Ronda de 32 | 5 |
| Octavos | 6 |
| Cuartos | 8 |
| Semifinal | 11 |
| 3er lugar | 10 |
| Subcampeón | 12 |
| **Campeón** | **20** |

---

## ⚠️ Actualizar equipos
El sorteo oficial del Mundial 2026 aún no se ha realizado.  
Cuando salga, edita el diccionario `GROUPS` en `data.py`.

---

Hecho para la familia · Mundial USA/Canadá/México 2026 🏆
