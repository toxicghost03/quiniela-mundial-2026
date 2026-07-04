import streamlit as st
from data import ADMIN_PASSWORD

st.set_page_config(page_title="Admin — Quiniela 2026", page_icon="⚙️", layout="centered")

R16_MATCHES = [
    ("🇲🇦 Marruecos",  "🇨🇦 Canadá",      "Sáb 4 Jul"),
    ("🇫🇷 Francia",    "🇵🇾 Paraguay",     "Sáb 4 Jul"),
    ("🇧🇷 Brasil",     "🇳🇴 Noruega",      "Dom 5 Jul"),
    ("🇲🇽 México",     "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra", "Dom 5 Jul"),
    ("🇵🇹 Portugal",   "🇪🇸 España",       "Lun 6 Jul"),
    ("🇺🇸 USA",        "🇧🇪 Bélgica",      "Lun 6 Jul"),
    ("🇦🇷 Argentina",  "🇪🇬 Egipto",       "Mar 7 Jul"),
    ("🇨🇭 Suiza",      "🇨🇴 Colombia",     "Mar 7 Jul"),
]

if "admin_ok" not in st.session_state:
    st.session_state.admin_ok = False
if "all_users" not in st.session_state:
    st.session_state.all_users = {}
if "real_results" not in st.session_state:
    st.session_state.real_results = ["🇲🇦 Marruecos", None, None, None, None, None, None, None]

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
st.subheader("Cargar resultados reales")
st.caption("Cuando termine cada partido, selecciona el ganador aquí. Los puntos se recalculan automáticamente.")

results = list(st.session_state.real_results)

for i, (t1, t2, date) in enumerate(R16_MATCHES):
    st.markdown(f"**Partido {i+1} · {date}**")
    opts_with_none = ["— Pendiente —", t1, t2]
    cur_idx = 0
    if results[i] == t1: cur_idx = 1
    elif results[i] == t2: cur_idx = 2
    sel = st.radio(f"r{i+1}", opts_with_none, index=cur_idx, key=f"res_{i}", horizontal=True, label_visibility="collapsed")
    results[i] = None if sel == "— Pendiente —" else sel
    st.divider()

if st.button("💾 Guardar y recalcular puntos", type="primary", use_container_width=True):
    st.session_state.real_results = results
    # Recalc all users
    real = results
    log = []
    for uid, u in st.session_state.all_users.items():
        pts = sum(5 for i, w in enumerate(real) if w and i < len(u.get("picks",[])) and u["picks"][i] == w)
        st.session_state.all_users[uid]["points"] = pts
        log.append(f"✅ {uid}: {pts} pts")
    st.success(f"¡Listo! {len(log)} participantes actualizados.")
    if log:
        st.code("\n".join(log))

st.markdown("---")
st.subheader(f"Participantes ({len(st.session_state.all_users)})")
if st.session_state.all_users:
    users = sorted(st.session_state.all_users.items(), key=lambda x: x[1].get("points",0), reverse=True)
    for i, (uid, u) in enumerate(users):
        picks_done = sum(1 for p in u.get("picks",[]) if p)
        st.markdown(f"**{i+1}. {uid}** — {picks_done}/8 picks — **{u.get('points',0)} pts**")
else:
    st.info("Nadie registrado aún.")
