import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Quiniela Mundial 2026 🏆",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.big-title { font-family: 'Bebas Neue', sans-serif; font-size: 2.8rem; letter-spacing: 3px; color: #F5C518; line-height: 1; margin: 0; text-align: center; }
.sub-title { color: #6b6b80; font-size: 0.8rem; letter-spacing: 3px; text-transform: uppercase; text-align: center; margin-bottom: 8px; }
div[data-testid="stMetric"] { background: #1a1a24; border: 1px solid #2e2e3e; border-radius: 10px; padding: 12px 16px; }
</style>
""", unsafe_allow_html=True)

# ══ MATCHES ════════════════════════════════════════════════════════════
R16_MATCHES = [
    ("🇲🇦 Marruecos",  "🇨🇦 Canadá",       "Sáb 4 Jul · 1pm ET"),
    ("🇫🇷 Francia",    "🇵🇾 Paraguay",      "Sáb 4 Jul · 5pm ET"),
    ("🇧🇷 Brasil",     "🇳🇴 Noruega",       "Dom 5 Jul · 4pm ET"),
    ("🇲🇽 México",     "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra",  "Dom 5 Jul · 8pm ET"),
    ("🇵🇹 Portugal",   "🇪🇸 España",        "Lun 6 Jul · 3pm ET"),
    ("🇺🇸 USA",        "🇧🇪 Bélgica",       "Lun 6 Jul · 8pm ET"),
    ("🇦🇷 Argentina",  "🇪🇬 Egipto",        "Mar 7 Jul · 12pm ET"),
    ("🇨🇭 Suiza",      "🇨🇴 Colombia",      "Mar 7 Jul · 4pm ET"),
]

# ══ SHARED STATE ═══════════════════════════════════════════════════════
if "all_users" not in st.session_state:
    st.session_state.all_users = {}
if "real_results" not in st.session_state:
    st.session_state.real_results = ["🇲🇦 Marruecos", None, None, None, None, None, None, None]
if "admin_unlocked" not in st.session_state:
    st.session_state.admin_unlocked = False

# ══ PER-SESSION ════════════════════════════════════════════════════════
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "picks" not in st.session_state:
    st.session_state.picks = [None] * len(R16_MATCHES)

ADMIN_PASSWORD = "mundial2026"

def recalc_all():
    real = st.session_state.real_results
    for uid, u in st.session_state.all_users.items():
        pts = sum(
            5 for i, w in enumerate(real)
            if w and i < len(u.get("picks", [])) and u["picks"][i] == w
        )
        st.session_state.all_users[uid]["points"] = pts

def save_picks():
    uid = st.session_state.user_name
    if uid:
        if uid not in st.session_state.all_users:
            st.session_state.all_users[uid] = {"picks": [None]*len(R16_MATCHES), "points": 0}
        st.session_state.all_users[uid]["picks"] = list(st.session_state.picks)
        recalc_all()

# ══ LOGIN ══════════════════════════════════════════════════════════════
if not st.session_state.user_name:
    st.markdown('<p class="big-title">⚽ QUINIELA<br>MUNDIAL 2026</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Ronda de 16 · Familia</p>', unsafe_allow_html=True)
    st.markdown("---")
    name = st.text_input("¿Cuál es tu nombre?", max_chars=30, placeholder="Ej: Mamá, Juan, Tito...")
    if st.button("Entrar 🚀", use_container_width=True, type="primary"):
        if not name.strip():
            st.error("Escribe tu nombre")
        else:
            n = name.strip()
            st.session_state.user_name = n
            if n in st.session_state.all_users:
                st.session_state.picks = list(st.session_state.all_users[n].get("picks", [None]*len(R16_MATCHES)))
            else:
                st.session_state.all_users[n] = {"picks": [None]*len(R16_MATCHES), "points": 0}
                st.session_state.picks = [None] * len(R16_MATCHES)
            st.rerun()
    st.stop()

# ══ MAIN APP ═══════════════════════════════════════════════════════════
st.markdown('<p class="big-title">⚽ QUINIELA 2026</p>', unsafe_allow_html=True)
c1, c2 = st.columns([4, 1])
with c1:
    st.caption(f"Jugando como: **{st.session_state.user_name}**")
with c2:
    if st.button("Salir"):
        st.session_state.user_name = None
        st.session_state.picks = [None] * len(R16_MATCHES)
        st.rerun()

# ══ TABS ═══════════════════════════════════════════════════════════════
tab_picks, tab_lb, tab_admin = st.tabs(["🎯 Mis Picks", "📊 Tabla", "⚙️ Admin"])

# ══════════════════════════════════════════════════════════════════════
# TAB 1 — PICKS
# ══════════════════════════════════════════════════════════════════════
with tab_picks:
    st.subheader("Ronda de 16 — ¿Quién gana?")
    st.caption("**5 puntos** por acierto. Los partidos terminados están bloqueados.")

    picks = list(st.session_state.picks)
    changed = False

    for i, (t1, t2, date) in enumerate(R16_MATCHES):
        result = st.session_state.real_results[i]
        done   = result is not None

        if done:
            user_pick = picks[i]
            correct   = user_pick == result
            icon      = "✅" if correct else ("❌" if user_pick else "⏹️")
            st.markdown(f"**{icon} Partido {i+1}** · {date}")
            st.markdown(f"Ganó: **{result}** · Tu pick: {user_pick or '_sin pick_'} {'· **+5 pts** 🎉' if correct else ''}")
        else:
            st.markdown(f"**🕐 Partido {i+1}** · {date}")
            options = [t1, t2]
            cur = picks[i] if picks[i] in options else None
            sel = st.radio(
                f"p{i+1}",
                options=options,
                index=options.index(cur) if cur else None,
                key=f"pick_{i}",
                horizontal=True,
                label_visibility="collapsed",
            )
            if sel != picks[i]:
                picks[i] = sel
                changed = True

        st.divider()

    if changed:
        st.session_state.picks = picks

    pending = [i for i, (_, _, _) in enumerate(R16_MATCHES) if st.session_state.real_results[i] is None]
    done_picks = sum(1 for i in pending if picks[i] is not None)

    if pending:
        st.progress(done_picks / len(pending), text=f"{done_picks}/{len(pending)} partidos pendientes predichos")
        if st.button("💾 Guardar picks", type="primary", use_container_width=True):
            save_picks()
            st.success("✅ ¡Guardado! Puntos actualizados.")
            st.balloons()
    else:
        st.success("🏁 ¡Todos los partidos han terminado!")

# ══════════════════════════════════════════════════════════════════════
# TAB 2 — LEADERBOARD
# ══════════════════════════════════════════════════════════════════════
with tab_lb:
    recalc_all()
    st.subheader("Tabla de Posiciones")
    st.caption("Se recalcula automáticamente con cada resultado.")

    with st.expander("📋 Resultados hasta ahora"):
        for i, (t1, t2, date) in enumerate(R16_MATCHES):
            r = st.session_state.real_results[i]
            st.markdown(f"{'✅' if r else '🕐'} **Partido {i+1}** ({date}): {f'**{r}**' if r else 'Pendiente'}")

    st.markdown("---")
    users = sorted(st.session_state.all_users.items(), key=lambda x: x[1].get("points", 0), reverse=True)

    if not users:
        st.info("Nadie registrado aún.")
    else:
        medals = {0: "🥇", 1: "🥈", 2: "🥉"}
        top3   = users[:min(3, len(users))]
        order  = [1, 0, 2][:len(top3)]
        cols   = st.columns(len(top3))
        for col_i, pos in enumerate(order):
            uid, u = top3[pos]
            with cols[col_i]:
                st.metric(
                    label=f"{medals[pos]} {uid}",
                    value=f"{u.get('points', 0)} pts",
                    delta=f"{sum(1 for p in u.get('picks',[]) if p)}/8 picks"
                )
        st.markdown("---")
        rows = []
        for i, (uid, u) in enumerate(users):
            rows.append({
                "#":          medals.get(i, i + 1),
                "Nombre":     f"⭐ {uid}" if uid == st.session_state.user_name else uid,
                "Picks":      f"{sum(1 for p in u.get('picks',[]) if p)}/8",
                "Puntos 🏆":  u.get("points", 0),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════
# TAB 3 — ADMIN
# ══════════════════════════════════════════════════════════════════════
with tab_admin:
    if not st.session_state.admin_unlocked:
        st.subheader("🔐 Acceso Admin")
        pw = st.text_input("Contraseña", type="password", key="admin_pw")
        if st.button("Entrar", key="admin_login"):
            if pw == ADMIN_PASSWORD:
                st.session_state.admin_unlocked = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta")
    else:
        st.subheader("⚙️ Panel de Resultados")
        st.caption("Selecciona el ganador real de cada partido. Los puntos se recalculan solos al guardar.")

        results = list(st.session_state.real_results)

        for i, (t1, t2, date) in enumerate(R16_MATCHES):
            st.markdown(f"**Partido {i+1} · {date}**")
            opts    = ["⏳ Pendiente", t1, t2]
            cur_idx = 0
            if results[i] == t1: cur_idx = 1
            elif results[i] == t2: cur_idx = 2
            sel = st.radio(f"res{i}", opts, index=cur_idx, key=f"res_{i}", horizontal=True, label_visibility="collapsed")
            results[i] = None if sel == "⏳ Pendiente" else sel
            st.divider()

        if st.button("💾 Guardar resultados y recalcular puntos", type="primary", use_container_width=True):
            st.session_state.real_results = results
            recalc_all()
            st.success("✅ ¡Resultados guardados! Puntos de todos actualizados.")
            log = [f"• {uid}: **{u.get('points',0)} pts**" for uid, u in
                   sorted(st.session_state.all_users.items(), key=lambda x: x[1].get("points",0), reverse=True)]
            for line in log:
                st.markdown(line)

        st.markdown("---")
        if st.button("🔒 Cerrar sesión admin", key="admin_logout"):
            st.session_state.admin_unlocked = False
            st.rerun()
