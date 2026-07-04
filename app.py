import streamlit as st
import pandas as pd
from datetime import datetime

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
.big-title { font-family: 'Bebas Neue', sans-serif; font-size: 3rem; letter-spacing: 3px; color: #F5C518; line-height: 1; margin: 0; text-align: center; }
.sub-title { color: #6b6b80; font-size: 0.8rem; letter-spacing: 3px; text-transform: uppercase; text-align: center; margin-bottom: 8px; }
.match-done { opacity: 0.55; }
div[data-testid="stMetric"] { background: #1a1a24; border: 1px solid #2e2e3e; border-radius: 10px; padding: 12px 16px; }
</style>
""", unsafe_allow_html=True)

# ══ REAL R16 MATCHES — FIFA 2026 ══════════════════════════════════════
# Format: (team1, team2, date_str, result_winner_or_None)
R16_MATCHES = [
    ("🇲🇦 Marruecos",  "🇨🇦 Canadá",      "Sáb 4 Jul · 1pm ET",   "🇲🇦 Marruecos"),  # DONE: 3-0
    ("🇫🇷 Francia",    "🇵🇾 Paraguay",     "Sáb 4 Jul · 5pm ET",   None),
    ("🇧🇷 Brasil",     "🇳🇴 Noruega",      "Dom 5 Jul · 4pm ET",   None),
    ("🇲🇽 México",     "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra", "Dom 5 Jul · 8pm ET",   None),
    ("🇵🇹 Portugal",   "🇪🇸 España",       "Lun 6 Jul · 3pm ET",   None),
    ("🇺🇸 USA",        "🇧🇪 Bélgica",      "Lun 6 Jul · 8pm ET",   None),
    ("🇦🇷 Argentina",  "🇪🇬 Egipto",       "Mar 7 Jul · 12pm ET",  None),
    ("🇨🇭 Suiza",      "🇨🇴 Colombia",     "Mar 7 Jul · 4pm ET",   None),
]

# ══ SHARED STATE ══════════════════════════════════════════════════════
if "all_users" not in st.session_state:
    st.session_state.all_users = {}
if "real_results" not in st.session_state:
    # Pre-load Morocco win
    st.session_state.real_results = ["🇲🇦 Marruecos", None, None, None, None, None, None, None]

# ══ PER-SESSION ═══════════════════════════════════════════════════════
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
        # Auto-recalc points whenever picks are saved
        recalc_points()

def recalc_points():
    real = st.session_state.real_results
    for uid, u in st.session_state.all_users.items():
        pts = sum(5 for i, w in enumerate(real) if w and i < len(u.get("picks",[])) and u["picks"][i] == w)
        st.session_state.all_users[uid]["points"] = pts

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
c1, c2 = st.columns([4,1])
with c1:
    st.caption(f"Jugando como: **{st.session_state.user_name}**")
with c2:
    if st.button("Salir"):
        st.session_state.user_name = None
        st.session_state.picks = [None] * len(R16_MATCHES)
        st.rerun()

tab_picks, tab_lb = st.tabs(["🎯 Mis Predicciones", "📊 Tabla General"])

# ══ TAB 1 — PREDICCIONES ══════════════════════════════════════════════
with tab_picks:
    st.subheader("Ronda de 16 — ¿Quién gana?")
    st.caption("**5 puntos** por cada acierto. Los partidos ya jugados están marcados.")

    picks = list(st.session_state.picks)
    changed = False

    for i, (t1, t2, date, result) in enumerate(R16_MATCHES):
        done = result is not None
        label = f"{'✅' if done else '🕐'} **Partido {i+1}** · {date}"
        if done:
            label += f" · Ganó: **{result}**"

        with st.container():
            st.markdown(label)
            if done:
                # Show locked pick
                user_pick = picks[i]
                if user_pick:
                    correct = user_pick == result
                    st.markdown(f"Tu pick: {user_pick} {'✅ +5pts' if correct else '❌'}")
                else:
                    st.markdown("_No hiciste pick en este partido_")
            else:
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

    pending = [(i, R16_MATCHES[i]) for i, r in enumerate(R16_MATCHES) if r[3] is None]
    done_picks = sum(1 for i, _ in pending if picks[i] is not None)
    total_pending = len(pending)

    if total_pending > 0:
        st.progress(done_picks / total_pending, text=f"{done_picks}/{total_pending} partidos pendientes predichos")
        if st.button("💾 Guardar mis picks", type="primary", use_container_width=True):
            save_picks()
            st.success("✅ ¡Guardado! Los puntos se actualizan automáticamente.")
            st.balloons()
    else:
        st.success("🏆 Todos los partidos han terminado. ¡Mira la tabla!")

# ══ TAB 2 — LEADERBOARD ═══════════════════════════════════════════════
with tab_lb:
    # Auto-recalc every time leaderboard is viewed
    recalc_points()

    st.subheader("Tabla de Posiciones")
    st.caption("Se actualiza automáticamente con cada resultado real.")

    # Show current results
    with st.expander("📋 Resultados reales hasta ahora"):
        for i, (t1, t2, date, result) in enumerate(R16_MATCHES):
            if result:
                st.markdown(f"✅ Partido {i+1}: **{result}** ganó")
            else:
                st.markdown(f"🕐 Partido {i+1} ({date}): pendiente")

    st.markdown("---")

    users = sorted(st.session_state.all_users.items(), key=lambda x: x[1].get("points", 0), reverse=True)

    if not users:
        st.info("Nadie registrado aún. ¡Sé el primero!")
    else:
        medals = {0: "🥇", 1: "🥈", 2: "🥉"}

        # Top 3 cards
        top3 = users[:min(3, len(users))]
        order = [1, 0, 2] if len(top3) == 3 else list(range(len(top3)))
        cols = st.columns(len(top3))
        for col_i, pos in enumerate(order[:len(top3)]):
            uid, u = top3[pos]
            with cols[col_i]:
                picks_done = sum(1 for p in u.get("picks",[]) if p)
                st.metric(
                    label=f"{medals[pos]} {uid}",
                    value=f"{u.get('points', 0)} pts",
                    delta=f"{picks_done}/8 picks"
                )

        st.markdown("---")

        rows = []
        for i, (uid, u) in enumerate(users):
            picks_done = sum(1 for p in u.get("picks",[]) if p)
            rows.append({
                "#": medals.get(i, i+1),
                "Nombre": f"⭐ {uid}" if uid == st.session_state.user_name else uid,
                "Picks": f"{picks_done}/8",
                "Puntos 🏆": u.get("points", 0),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
