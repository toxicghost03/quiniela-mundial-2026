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
.big-title { font-family: 'Bebas Neue', sans-serif; font-size: 3.5rem; letter-spacing: 3px; color: #F5C518; line-height: 1; margin: 0; text-align: center; }
.sub-title { color: #6b6b80; font-size: 0.85rem; letter-spacing: 3px; text-transform: uppercase; text-align: center; }
div[data-testid="stMetric"] { background: #1a1a24; border: 1px solid #2e2e3e; border-radius: 10px; padding: 12px 16px; }
</style>
""", unsafe_allow_html=True)

# ── Round of 16 matches (FIFA 2026 — placeholder matchups, update when known)
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

# ── Shared state (all users in same server session)
if "all_users" not in st.session_state:
    st.session_state.all_users = {}
if "real_results" not in st.session_state:
    st.session_state.real_results = [None] * len(R16_MATCHES)

# ── Per-user session
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "picks" not in st.session_state:
    st.session_state.picks = [None] * len(R16_MATCHES)

def save_picks():
    uid = st.session_state.user_name
    if uid:
        if uid not in st.session_state.all_users:
            st.session_state.all_users[uid] = {"picks": [None]*len(R16_MATCHES), "points": 0}
        st.session_state.all_users[uid]["picks"] = list(st.session_state.picks)

# ══ LOGIN ══════════════════════════════════════════════════════════════
if not st.session_state.user_name:
    st.markdown('<p class="big-title">QUINIELA<br>MUNDIAL 2026</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Ronda de 16 · Familia</p>', unsafe_allow_html=True)
    st.markdown("---")
    name = st.text_input("¿Cuál es tu nombre?", max_chars=30, placeholder="Ej: Mamá, Juan, Abuela...")
    if st.button("Entrar 🚀", use_container_width=True, type="primary"):
        if not name.strip():
            st.error("Escribe tu nombre")
        else:
            n = name.strip()
            st.session_state.user_name = n
            # Load existing picks if user already registered
            if n in st.session_state.all_users:
                st.session_state.picks = list(st.session_state.all_users[n].get("picks", [None]*len(R16_MATCHES)))
            else:
                st.session_state.all_users[n] = {"picks": [None]*len(R16_MATCHES), "points": 0}
                st.session_state.picks = [None] * len(R16_MATCHES)
            st.rerun()
    st.stop()

# ══ MAIN APP ═══════════════════════════════════════════════════════════
st.markdown('<p class="big-title">⚽ QUINIELA 2026</p>', unsafe_allow_html=True)
c1, c2 = st.columns([4,1])
with c1:
    st.caption(f"Jugando como: **{st.session_state.user_name}**")
with c2:
    if st.button("Salir"):
        st.session_state.user_name = None
        st.session_state.picks = [None] * len(R16_MATCHES)
        st.rerun()

st.markdown("---")
tab_picks, tab_lb = st.tabs(["🎯 Mis Predicciones", "📊 Tabla General"])

# ══ TAB 1 — PREDICCIONES ══════════════════════════════════════════════
with tab_picks:
    st.subheader("Ronda de 16 — Elige el ganador")
    st.caption("Selecciona quién crees que gana cada partido. 5 puntos por acierto.")

    picks = list(st.session_state.picks)
    changed = False

    for i, (t1, t2) in enumerate(R16_MATCHES):
        st.markdown(f"**Partido {i+1}**")
        options = [t1, t2]
        cur = picks[i] if picks[i] in options else None
        sel = st.radio(
            f"Partido {i+1}",
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

    done = sum(1 for p in picks if p)
    st.progress(done / len(R16_MATCHES), text=f"{done}/{len(R16_MATCHES)} partidos predichos")

    if st.button("💾 Guardar mis picks", type="primary", use_container_width=True):
        save_picks()
        st.success("✅ ¡Guardado!")
        st.balloons()

# ══ TAB 2 — LEADERBOARD ═══════════════════════════════════════════════
with tab_lb:
    st.subheader("Tabla de Posiciones")

    users = sorted(st.session_state.all_users.items(), key=lambda x: x[1].get("points", 0), reverse=True)

    if not users:
        st.info("Nadie registrado aún.")
    else:
        medals = {0: "🥇", 1: "🥈", 2: "🥉"}
        top3 = users[:3]

        # Top 3 cards
        cols = st.columns(3)
        positions = [1, 0, 2]  # center = 1st
        for pos, col in zip(positions, cols):
            if pos < len(top3):
                uid, u = top3[pos]
                with col:
                    st.metric(
                        label=f"{medals[pos]} {uid}",
                        value=f"{u.get('points', 0)} pts",
                        delta=f"{sum(1 for p in u.get('picks',[]) if p)} picks hechos" if any(u.get('picks',[])) else "Sin picks"
                    )

        st.markdown("---")

        # Full table
        rows = []
        for i, (uid, u) in enumerate(users):
            rows.append({
                "#": medals.get(i, i+1),
                "Nombre": f"**{uid}**" if uid == st.session_state.user_name else uid,
                "Picks hechos": f"{sum(1 for p in u.get('picks',[]) if p)}/8",
                "Puntos": u.get("points", 0),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        st.caption("💡 Los puntos se actualizan cuando el admin cargue los resultados reales.")
