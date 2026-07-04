import streamlit as st
from data import ADMIN_PASSWORD

st.set_page_config(page_title="Admin — Quiniela 2026", page_icon="⚙️", layout="centered")

R16_MATCHES = [
    ("Estados Unidos 🇺🇸",   "México 🇲🇽"),
    ("España 🇪🇸",           "Marruecos 🇲🇦"),
    ("Francia 🇫🇷",          "Brasil 🇧🇷"),
    ("Argentina 🇦🇷",        "Portugal 🇵🇹"),
    ("Inglaterra 🏴󠁧󠁢󠁥󠁮󠁧󠁿",       "Países Bajos 🇳🇱"),
    ("Alemania 🇩🇪",         "Colombia 🇨🇴"),
    ("Japón 🇯🇵",            "Croacia 🇭🇷"),
    ("Italia 🇮🇹",           "Suiza 🇨🇭"),
]

if "admin_ok" not in st.session_state:
    st.session_state.admin_ok = False
if "all_users" not in st.session_state:
    st.session_state.all_users = {}
if "real_results" not in st.session_state:
    st.session_state.real_results = [None] * len(R16_MATCHES)

if not st.session_state.admin_ok:
    st.title("⚙️ Admin")
    pw = st.text_input("Contraseña", type="password")
    if st.button("Entrar"):
        if pw == ADMIN_PASSWORD:
            st.session_state.admin_ok = True
            st.rerun()
        else:
            st.error("Incorrecta")
    st.stop()

st.title("⚙️ Admin — Quiniela 2026")
st.subheader("Resultados Reales — Ronda de 16")
st.caption("Selecciona el ganador real de cada partido para calcular los puntos.")

results = list(st.session_state.real_results)
for i, (t1, t2) in enumerate(R16_MATCHES):
    st.markdown(f"**Partido {i+1}**")
    opts = [t1, t2]
    cur = results[i] if results[i] in opts else None
    sel = st.radio(f"R{i+1}", opts, index=opts.index(cur) if cur else None, key=f"res_{i}", horizontal=True, label_visibility="collapsed")
    results[i] = sel
    st.divider()

col1, col2 = st.columns(2)
with col1:
    if st.button("💾 Guardar resultados", type="primary", use_container_width=True):
        st.session_state.real_results = results
        st.success("✅ Resultados guardados")

with col2:
    if st.button("🔄 Recalcular puntos", use_container_width=True):
        real = st.session_state.real_results
        log = []
        for uid, u in st.session_state.all_users.items():
            pts = sum(5 for i, w in enumerate(real) if w and i < len(u.get("picks",[])) and u["picks"][i] == w)
            st.session_state.all_users[uid]["points"] = pts
            log.append(f"✅ {uid}: {pts} pts")
        st.success("Puntos actualizados")
        if log:
            st.code("\n".join(log))

st.markdown("---")
st.subheader("Participantes registrados")
if st.session_state.all_users:
    for uid, u in st.session_state.all_users.items():
        st.write(f"**{uid}** — {sum(1 for p in u.get('picks',[]) if p)}/8 picks — {u.get('points',0)} pts")
else:
    st.info("Nadie registrado aún.")
