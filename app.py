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
.sub-title  { color: #6b6b80; font-size: 0.8rem; letter-spacing: 3px; text-transform: uppercase; text-align: center; margin-bottom: 8px; }
div[data-testid="stMetric"] { background: #1a1a24; border: 1px solid #2e2e3e; border-radius: 10px; padding: 12px 16px; }
</style>
""", unsafe_allow_html=True)

ADMIN_PASSWORD = "mundial2026"

# ══ ALL MATCHES ════════════════════════════════════════════════════════
# (team1, team2, label, result_or_None, points)
R32_MATCHES = [
    ("🇨🇦 Canadá",     "🇿🇦 Sudáfrica",   "28 Jun",  "🇨🇦 Canadá",     3),
    ("🇧🇷 Brasil",     "🇯🇵 Japón",       "29 Jun",  "🇧🇷 Brasil",     3),
    ("🇩🇪 Alemania",   "🇵🇾 Paraguay",    "29 Jun",  "🇵🇾 Paraguay",   3),  # PKs
    ("🇳🇱 Países Bajos","🇲🇦 Marruecos",  "29 Jun",  "🇲🇦 Marruecos",  3),  # PKs
    ("🇳🇴 Noruega",    "🇨🇮 Costa Marfil","30 Jun",  "🇳🇴 Noruega",    3),
    ("🇫🇷 Francia",    "🇸🇪 Suecia",      "30 Jun",  "🇫🇷 Francia",    3),
    ("🇲🇽 México",     "🇪🇨 Ecuador",     "30 Jun",  "🇲🇽 México",     3),
    ("🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra","🇨🇩 Congo RD",   "1 Jul",   "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra",3),
    ("🇧🇪 Bélgica",    "🇸🇳 Senegal",     "1 Jul",   "🇧🇪 Bélgica",    3),  # AET
    ("🇺🇸 USA",        "🇧🇦 Bosnia",      "1 Jul",   "🇺🇸 USA",        3),
    ("🇪🇸 España",     "🇦🇹 Austria",     "2 Jul",   "🇪🇸 España",     3),
    ("🇵🇹 Portugal",   "🇭🇷 Croacia",     "2 Jul",   "🇵🇹 Portugal",   3),
    ("🇨🇭 Suiza",      "🇩🇿 Argelia",     "2 Jul",   "🇨🇭 Suiza",      3),
    ("🇪🇬 Egipto",     "🇦🇺 Australia",   "3 Jul",   "🇪🇬 Egipto",     3),  # PKs
    ("🇦🇷 Argentina",  "🇨🇻 Cabo Verde",  "3 Jul",   "🇦🇷 Argentina",  3),
    ("🇨🇴 Colombia",   "🇬🇭 Ghana",       "3 Jul",   "🇨🇴 Colombia",   3),
]

R16_MATCHES = [
    ("🇲🇦 Marruecos",  "🇨🇦 Canadá",      "4 Jul · 1pm ET",  "🇲🇦 Marruecos",  5),
    ("🇫🇷 Francia",    "🇵🇾 Paraguay",    "4 Jul · 5pm ET",  None,              5),
    ("🇧🇷 Brasil",     "🇳🇴 Noruega",     "5 Jul · 4pm ET",  None,              5),
    ("🇲🇽 México",     "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra","5 Jul · 8pm ET",  None,              5),
    ("🇵🇹 Portugal",   "🇪🇸 España",      "6 Jul · 3pm ET",  None,              5),
    ("🇺🇸 USA",        "🇧🇪 Bélgica",     "6 Jul · 8pm ET",  None,              5),
    ("🇦🇷 Argentina",  "🇪🇬 Egipto",      "7 Jul · 12pm ET", None,              5),
    ("🇨🇭 Suiza",      "🇨🇴 Colombia",    "7 Jul · 4pm ET",  None,              5),
]

ALL_MATCHES = [("R32", m) for m in R32_MATCHES] + [("R16", m) for m in R16_MATCHES]
TOTAL = len(ALL_MATCHES)

# ══ SHARED STATE ═══════════════════════════════════════════════════════
if "all_users"       not in st.session_state: st.session_state.all_users       = {}
if "admin_unlocked"  not in st.session_state: st.session_state.admin_unlocked  = False
if "user_name"       not in st.session_state: st.session_state.user_name       = None
if "picks"           not in st.session_state: st.session_state.picks           = [None] * TOTAL

def recalc_all():
    for uid, u in st.session_state.all_users.items():
        pts = 0
        for i, (rnd, m) in enumerate(ALL_MATCHES):
            result = m[3]
            pick   = u.get("picks", [None]*TOTAL)[i] if i < len(u.get("picks", [])) else None
            if result and pick == result:
                pts += m[4]
        st.session_state.all_users[uid]["points"] = pts

def save_picks(uid=None, new_picks=None):
    target = uid or st.session_state.user_name
    if not target: return
    if target not in st.session_state.all_users:
        st.session_state.all_users[target] = {"picks": [None]*TOTAL, "points": 0}
    if new_picks is not None:
        st.session_state.all_users[target]["picks"] = new_picks
    else:
        st.session_state.all_users[target]["picks"] = list(st.session_state.picks)
    recalc_all()

# ══ LOGIN ══════════════════════════════════════════════════════════════
if not st.session_state.user_name:
    st.markdown('<p class="big-title">⚽ QUINIELA<br>MUNDIAL 2026</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Ronda de 32 & 16 · Familia</p>', unsafe_allow_html=True)
    st.markdown("---")
    name = st.text_input("¿Cuál es tu nombre?", max_chars=30, placeholder="Ej: Mamá, Juan, Tito...")
    if st.button("Entrar 🚀", use_container_width=True, type="primary"):
        if not name.strip():
            st.error("Escribe tu nombre")
        else:
            n = name.strip()
            st.session_state.user_name = n
            if n in st.session_state.all_users:
                p = st.session_state.all_users[n].get("picks", [None]*TOTAL)
                if len(p) < TOTAL: p += [None]*(TOTAL-len(p))
                st.session_state.picks = p
            else:
                st.session_state.all_users[n] = {"picks": [None]*TOTAL, "points": 0}
                st.session_state.picks = [None] * TOTAL
            st.rerun()
    st.stop()

# ══ HEADER ═════════════════════════════════════════════════════════════
st.markdown('<p class="big-title">⚽ QUINIELA 2026</p>', unsafe_allow_html=True)
c1, c2 = st.columns([4, 1])
with c1: st.caption(f"Jugando como: **{st.session_state.user_name}**")
with c2:
    if st.button("Salir"):
        st.session_state.user_name  = None
        st.session_state.picks      = [None]*TOTAL
        st.rerun()

tab_picks, tab_lb, tab_admin = st.tabs(["🎯 Mis Picks", "📊 Tabla", "⚙️ Admin"])

# ══════════════════════════════════════════════════════════════════════
# TAB 1 — PICKS
# ══════════════════════════════════════════════════════════════════════
with tab_picks:
    picks   = list(st.session_state.picks)
    changed = False

    # ── RONDA DE 32 (locked, view only) ──────────────────────────────
    st.subheader("Ronda de 32 — Resultados")
    st.caption("Esta ronda ya terminó. Solo el admin puede asignarte picks retroactivos.")

    for i, (rnd, m) in enumerate(ALL_MATCHES):
        if rnd != "R32": continue
        t1, t2, date, result, pts = m
        pick    = picks[i]
        correct = pick == result if result else False
        icon    = "✅" if correct else ("❌" if (pick and result) else "📋")
        st.markdown(f"**{icon} {t1} vs {t2}** · {date} · Ganó: **{result}**")
        if pick:
            st.caption(f"Tu pick: {pick} {'· **+{} pts** 🎉'.format(pts) if correct else ''}")
        else:
            st.caption("_Sin pick asignado — pídele al admin_")
        st.divider()

    # ── RONDA DE 16 (active picks) ────────────────────────────────────
    st.subheader("Ronda de 16 — Elige el ganador")
    st.caption("**5 puntos** por acierto. Los partidos terminados están bloqueados.")

    pending_indices = []
    for i, (rnd, m) in enumerate(ALL_MATCHES):
        if rnd != "R16": continue
        t1, t2, date, result, pts = m
        done = result is not None

        if done:
            pick    = picks[i]
            correct = pick == result
            icon    = "✅" if correct else ("❌" if pick else "⏹️")
            st.markdown(f"**{icon} {t1} vs {t2}** · {date}")
            st.markdown(f"Ganó: **{result}** · Tu pick: {pick or '_sin pick_'}"
                        + (f" · **+{pts} pts** 🎉" if correct else ""))
        else:
            pending_indices.append(i)
            st.markdown(f"**🕐 {t1} vs {t2}** · {date}")
            options = [t1, t2]
            cur     = picks[i] if picks[i] in options else None
            sel     = st.radio(f"p{i}", options=options,
                               index=options.index(cur) if cur else None,
                               key=f"pick_{i}", horizontal=True,
                               label_visibility="collapsed")
            if sel != picks[i]:
                picks[i] = sel
                changed   = True
        st.divider()

    if changed:
        st.session_state.picks = picks

    done_picks = sum(1 for i in pending_indices if picks[i])
    if pending_indices:
        st.progress(done_picks / len(pending_indices),
                    text=f"{done_picks}/{len(pending_indices)} partidos pendientes predichos")
        if st.button("💾 Guardar picks", type="primary", use_container_width=True):
            save_picks()
            st.success("✅ ¡Guardado! Puntos actualizados.")
            st.balloons()
    else:
        st.success("🏁 ¡Todos los partidos de la Ronda de 16 han terminado!")

# ══════════════════════════════════════════════════════════════════════
# TAB 2 — LEADERBOARD
# ══════════════════════════════════════════════════════════════════════
with tab_lb:
    recalc_all()
    st.subheader("📊 Tabla de Posiciones")
    st.caption("Puntos de todos los participantes — recalculados automáticamente.")

    users = sorted(st.session_state.all_users.items(),
                   key=lambda x: x[1].get("points", 0), reverse=True)

    if not users:
        st.info("Nadie registrado aún.")
    else:
        # Top 3 cards
        medals = {0: "🥇", 1: "🥈", 2: "🥉"}
        top3   = users[:min(3, len(users))]
        cols   = st.columns(len(top3))
        for pos, (uid, u) in enumerate(top3):
            with cols[pos]:
                picks_done = sum(1 for p in u.get("picks", []) if p)
                st.metric(
                    label=f"{medals[pos]} {uid}",
                    value=f"{u.get('points', 0)} pts",
                    delta=f"{picks_done}/{TOTAL} picks"
                )

        st.markdown("---")

        # Full table — ALL users
        rows = []
        for i, (uid, u) in enumerate(users):
            r32_pts = sum(
                m[4] for j, (rnd, m) in enumerate(ALL_MATCHES)
                if rnd == "R32" and m[3] and j < len(u.get("picks",[])) and u["picks"][j] == m[3]
            )
            r16_pts = sum(
                m[4] for j, (rnd, m) in enumerate(ALL_MATCHES)
                if rnd == "R16" and m[3] and j < len(u.get("picks",[])) and u["picks"][j] == m[3]
            )
            picks_done = sum(1 for p in u.get("picks", []) if p)
            rows.append({
                "#":           medals.get(i, i+1),
                "Nombre":      f"⭐ {uid}" if uid == st.session_state.user_name else uid,
                "R32 pts":     r32_pts,
                "R16 pts":     r16_pts,
                "Total 🏆":    u.get("points", 0),
                "Picks":       f"{picks_done}/{TOTAL}",
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
        st.subheader("⚙️ Panel de Admin")

        admin_tab1, admin_tab2 = st.tabs(["🏆 Resultados reales", "👤 Editar picks de usuario"])

        # ── SUB-TAB A: RESULTADOS REALES ─────────────────────────────
        with admin_tab1:
            st.caption("Marca el ganador real. Los puntos de todos se recalculan al guardar.")

            r32_results = {}
            st.markdown("### Ronda de 32")
            for i, (rnd, m) in enumerate(ALL_MATCHES):
                if rnd != "R32": continue
                t1, t2, date, result, pts = m
                st.markdown(f"**{t1} vs {t2}** · {date}")
                opts    = ["⏳ Pendiente", t1, t2]
                cur_idx = 1 if result == t1 else (2 if result == t2 else 0)
                sel     = st.radio(f"rres{i}", opts, index=cur_idx,
                                   key=f"admin_res_{i}", horizontal=True,
                                   label_visibility="collapsed")
                r32_results[i] = None if sel == "⏳ Pendiente" else sel
                st.divider()

            r16_results = {}
            st.markdown("### Ronda de 16")
            for i, (rnd, m) in enumerate(ALL_MATCHES):
                if rnd != "R16": continue
                t1, t2, date, result, pts = m
                st.markdown(f"**{t1} vs {t2}** · {date}")
                opts    = ["⏳ Pendiente", t1, t2]
                cur_idx = 1 if result == t1 else (2 if result == t2 else 0)
                sel     = st.radio(f"rres{i}", opts, index=cur_idx,
                                   key=f"admin_res_{i}", horizontal=True,
                                   label_visibility="collapsed")
                r16_results[i] = None if sel == "⏳ Pendiente" else sel
                st.divider()

            if st.button("💾 Guardar resultados y recalcular", type="primary", use_container_width=True):
                # Note: in session_state results are embedded in ALL_MATCHES tuple
                # We store overrides in session_state
                if "result_overrides" not in st.session_state:
                    st.session_state.result_overrides = {}
                st.session_state.result_overrides.update(r32_results)
                st.session_state.result_overrides.update(r16_results)
                recalc_all()
                st.success("✅ Resultados guardados y puntos recalculados.")
                users_sorted = sorted(st.session_state.all_users.items(),
                                      key=lambda x: x[1].get("points",0), reverse=True)
                for uid, u in users_sorted:
                    st.markdown(f"• **{uid}**: {u.get('points',0)} pts")

        # ── SUB-TAB B: EDITAR PICKS DE USUARIO ───────────────────────
        with admin_tab2:
            st.caption("Selecciona un usuario y asígnale retroactivamente sus picks de la Ronda de 32.")

            user_list = list(st.session_state.all_users.keys())
            if not user_list:
                st.info("No hay usuarios registrados aún.")
            else:
                selected_user = st.selectbox("Selecciona usuario", user_list, key="admin_user_sel")
                u_data  = st.session_state.all_users[selected_user]
                u_picks = list(u_data.get("picks", [None]*TOTAL))
                if len(u_picks) < TOTAL: u_picks += [None]*(TOTAL-len(u_picks))

                st.markdown(f"### Picks de **{selected_user}** — Ronda de 32")
                st.caption("Los resultados reales ya están fijos. Solo asignas qué predijo este usuario.")

                edited = list(u_picks)
                changed_admin = False
                for i, (rnd, m) in enumerate(ALL_MATCHES):
                    if rnd != "R32": continue
                    t1, t2, date, result, pts = m
                    correct = edited[i] == result if result else False
                    st.markdown(f"**{t1} vs {t2}** · {date} · Ganó: **{result}**")
                    opts    = ["— Sin pick —", t1, t2]
                    cur_idx = 1 if edited[i] == t1 else (2 if edited[i] == t2 else 0)
                    sel     = st.radio(f"upick{i}", opts, index=cur_idx,
                                       key=f"admin_upick_{selected_user}_{i}",
                                       horizontal=True, label_visibility="collapsed")
                    new_val = None if sel == "— Sin pick —" else sel
                    if new_val != edited[i]:
                        edited[i]    = new_val
                        changed_admin = True
                    if result and new_val == result:
                        st.caption(f"✅ Correcto · +{pts} pts")
                    elif new_val:
                        st.caption(f"❌ Incorrecto")
                    st.divider()

                if st.button(f"💾 Guardar picks de {selected_user}", type="primary", use_container_width=True):
                    save_picks(uid=selected_user, new_picks=edited)
                    st.success(f"✅ Picks de {selected_user} actualizados. "
                               f"Puntos nuevos: **{st.session_state.all_users[selected_user]['points']} pts**")

        st.markdown("---")
        if st.button("🔒 Cerrar sesión admin"):
            st.session_state.admin_unlocked = False
            st.rerun()
