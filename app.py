import streamlit as st
import pandas as pd

st.set_page_config(page_title="Quiniela Mundial 2026 🏆", page_icon="⚽", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.big-title { font-family:'Bebas Neue',sans-serif; font-size:2.8rem; letter-spacing:3px; color:#F5C518; line-height:1; margin:0; text-align:center; }
.sub-title  { color:#6b6b80; font-size:0.8rem; letter-spacing:3px; text-transform:uppercase; text-align:center; margin-bottom:8px; }
div[data-testid="stMetric"] { background:#1a1a24; border:1px solid #2e2e3e; border-radius:10px; padding:12px 16px; }
</style>
""", unsafe_allow_html=True)

ADMIN_PASSWORD = "admin2026"

# ══ ALL MATCHES ════════════════════════════════════════════════════════
# (team1, team2, result_or_None, points)

GD1 = [  # Jornada 1 — Jun 11-13
    ("🇲🇽 México",       "🇿🇦 Sudáfrica",    "🇲🇽 México",       2),
    ("🇰🇷 Corea del Sur","🇨🇿 Chequia",      "🇰🇷 Corea del Sur",2),
    ("🇨🇦 Canadá",       "🇧🇦 Bosnia",       "Empate",           1),
    ("🇨🇭 Suiza",        "🇶🇦 Qatar",        "Empate",           1),
    ("🇧🇷 Brasil",       "🇲🇦 Marruecos",   "Empate",           1),
    ("🏴󠁧󠁢󠁸󠁣󠁴󠁿 Escocia",    "🇭🇹 Haití",        "🏴󠁧󠁢󠁸󠁣󠁴󠁿 Escocia",    2),
    ("🇺🇸 USA",          "🇵🇾 Paraguay",    "🇺🇸 USA",          2),
    ("🇦🇺 Australia",    "🇹🇷 Turquía",      "🇦🇺 Australia",    2),
    ("🇩🇪 Alemania",     "🇨🇼 Curazao",     "🇩🇪 Alemania",     2),
    ("🇨🇮 Costa Marfil", "🇪🇨 Ecuador",     "🇨🇮 Costa Marfil", 2),
    ("🇳🇱 Países Bajos", "🇯🇵 Japón",       "Empate",           1),
    ("🇸🇪 Suecia",       "🇹🇳 Túnez",       "🇸🇪 Suecia",       2),
]
GD2 = [  # Jornada 2 — Jun 18-23
    ("🇨🇿 Chequia",      "🇿🇦 Sudáfrica",   "Empate",           1),
    ("🇲🇽 México",       "🇰🇷 Corea del Sur","🇲🇽 México",       2),
    ("🇨🇭 Suiza",        "🇧🇦 Bosnia",      "🇨🇭 Suiza",        2),
    ("🇨🇦 Canadá",       "🇶🇦 Qatar",       "🇨🇦 Canadá",       2),
    ("🏴󠁧󠁢󠁸󠁣󠁴󠁿 Escocia",    "🇲🇦 Marruecos",   "🇲🇦 Marruecos",   2),
    ("🇧🇷 Brasil",       "🇭🇹 Haití",       "🇧🇷 Brasil",       2),
    ("🇺🇸 USA",          "🇦🇺 Australia",   "🇺🇸 USA",          2),
    ("🇹🇷 Turquía",      "🇵🇾 Paraguay",    "🇵🇾 Paraguay",     2),
    ("🇩🇪 Alemania",     "🇨🇮 Costa Marfil","🇩🇪 Alemania",     2),
    ("🇪🇨 Ecuador",      "🇨🇼 Curazao",     "Empate",           1),
    ("🇳🇱 Países Bajos", "🇸🇪 Suecia",      "🇳🇱 Países Bajos", 2),
    ("🇯🇵 Japón",        "🇹🇳 Túnez",       "🇯🇵 Japón",        2),
]
GD3 = [  # Jornada 3 — Jun 24-27
    ("🇨🇿 Chequia",      "🇲🇽 México",      "🇲🇽 México",       2),
    ("🇿🇦 Sudáfrica",    "🇰🇷 Corea del Sur","🇰🇷 Corea del Sur",2),
    ("🇨🇭 Suiza",        "🇨🇦 Canadá",      "🇨🇭 Suiza",        2),
    ("🇧🇦 Bosnia",       "🇶🇦 Qatar",       "🇧🇦 Bosnia",       2),
    ("🏴󠁧󠁢󠁸󠁣󠁴󠁿 Escocia",    "🇧🇷 Brasil",       "🇧🇷 Brasil",       2),
    ("🇲🇦 Marruecos",   "🇭🇹 Haití",        "🇲🇦 Marruecos",   2),
    ("🇹🇷 Turquía",      "🇺🇸 USA",          "🇹🇷 Turquía",      2),
    ("🇵🇾 Paraguay",     "🇦🇺 Australia",   "Empate",           1),
    ("🇨🇼 Curazao",      "🇨🇮 Costa Marfil","🇨🇮 Costa Marfil", 2),
    ("🇪🇨 Ecuador",      "🇩🇪 Alemania",    "🇪🇨 Ecuador",      2),
    ("🇯🇵 Japón",        "🇸🇪 Suecia",      "Empate",           1),
    ("🇳🇱 Países Bajos", "🇹🇳 Túnez",       "🇳🇱 Países Bajos", 2),
]
R32 = [  # Ronda de 32 — Jun 28 - Jul 3
    ("🇨🇦 Canadá",      "🇿🇦 Sudáfrica",   "🇨🇦 Canadá",      3),
    ("🇧🇷 Brasil",      "🇯🇵 Japón",       "🇧🇷 Brasil",      3),
    ("🇩🇪 Alemania",    "🇵🇾 Paraguay",    "🇵🇾 Paraguay",    3),
    ("🇳🇱 Países Bajos","🇲🇦 Marruecos",  "🇲🇦 Marruecos",  3),
    ("🇳🇴 Noruega",     "🇨🇮 Costa Marfil","🇳🇴 Noruega",     3),
    ("🇫🇷 Francia",     "🇸🇪 Suecia",      "🇫🇷 Francia",     3),
    ("🇲🇽 México",      "🇪🇨 Ecuador",     "🇲🇽 México",      3),
    ("🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra","🇨🇩 Congo RD",  "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra",3),
    ("🇧🇪 Bélgica",     "🇸🇳 Senegal",     "🇧🇪 Bélgica",     3),
    ("🇺🇸 USA",         "🇧🇦 Bosnia",      "🇺🇸 USA",         3),
    ("🇪🇸 España",      "🇦🇹 Austria",     "🇪🇸 España",      3),
    ("🇵🇹 Portugal",    "🇭🇷 Croacia",     "🇵🇹 Portugal",    3),
    ("🇨🇭 Suiza",       "🇩🇿 Argelia",     "🇨🇭 Suiza",       3),
    ("🇪🇬 Egipto",      "🇦🇺 Australia",   "🇪🇬 Egipto",      3),
    ("🇦🇷 Argentina",   "🇨🇻 Cabo Verde",  "🇦🇷 Argentina",   3),
    ("🇨🇴 Colombia",    "🇬🇭 Ghana",       "🇨🇴 Colombia",    3),
]
R16 = [  # Ronda de 16 — Jul 4-7
    ("🇲🇦 Marruecos",  "🇨🇦 Canadá",      "🇲🇦 Marruecos",  5),
    ("🇫🇷 Francia",    "🇵🇾 Paraguay",    None,              5),
    ("🇧🇷 Brasil",     "🇳🇴 Noruega",     None,              5),
    ("🇲🇽 México",     "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra","None",            5),
    ("🇵🇹 Portugal",   "🇪🇸 España",      None,              5),
    ("🇺🇸 USA",        "🇧🇪 Bélgica",     None,              5),
    ("🇦🇷 Argentina",  "🇪🇬 Egipto",      None,              5),
    ("🇨🇭 Suiza",      "🇨🇴 Colombia",    None,              5),
]

# Flatten all matches with stage label
ALL_STAGES = [
    ("Jornada 1", GD1),
    ("Jornada 2", GD2),
    ("Jornada 3", GD3),
    ("Ronda de 32", R32),
    ("Ronda de 16", R16),
]
ALL_MATCHES = []
for stage, matches in ALL_STAGES:
    for m in matches:
        ALL_MATCHES.append((stage, m))
TOTAL = len(ALL_MATCHES)

# ══ SHARED STATE ═══════════════════════════════════════════════════════
if "all_users"      not in st.session_state: st.session_state.all_users      = {}
if "admin_unlocked" not in st.session_state: st.session_state.admin_unlocked = False
if "user_name"      not in st.session_state: st.session_state.user_name      = None
if "picks"          not in st.session_state: st.session_state.picks          = [None]*TOTAL

def recalc_all():
    for uid, u in st.session_state.all_users.items():
        pts = 0
        upicks = u.get("picks", [])
        for i, (stage, m) in enumerate(ALL_MATCHES):
            result = m[2]
            pick   = upicks[i] if i < len(upicks) else None
            if result and pick and pick == result:
                pts += m[3]
        st.session_state.all_users[uid]["points"] = pts

def save_my_picks():
    uid = st.session_state.user_name
    if not uid: return
    if uid not in st.session_state.all_users:
        st.session_state.all_users[uid] = {"picks":[None]*TOTAL,"points":0}
    p = list(st.session_state.picks)
    if len(p) < TOTAL: p += [None]*(TOTAL-len(p))
    st.session_state.all_users[uid]["picks"] = p
    recalc_all()

def save_user_picks(uid, new_picks):
    if uid not in st.session_state.all_users:
        st.session_state.all_users[uid] = {"picks":[None]*TOTAL,"points":0}
    p = list(new_picks)
    if len(p) < TOTAL: p += [None]*(TOTAL-len(p))
    st.session_state.all_users[uid]["picks"] = p
    recalc_all()

# ══ LOGIN ══════════════════════════════════════════════════════════════
if not st.session_state.user_name:
    st.markdown('<p class="big-title">⚽ QUINIELA<br>MUNDIAL 2026</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Fase de Grupos + Eliminatorias · Familia</p>', unsafe_allow_html=True)
    st.markdown("---")
    name = st.text_input("¿Cuál es tu nombre?", max_chars=30, placeholder="Ej: Mamá, Juan, Tito...")
    if st.button("Entrar 🚀", use_container_width=True, type="primary"):
        if not name.strip():
            st.error("Escribe tu nombre")
        else:
            n = name.strip()
            st.session_state.user_name = n
            if n in st.session_state.all_users:
                p = st.session_state.all_users[n].get("picks",[None]*TOTAL)
                if len(p) < TOTAL: p += [None]*(TOTAL-len(p))
                st.session_state.picks = p
            else:
                st.session_state.all_users[n] = {"picks":[None]*TOTAL,"points":0}
                st.session_state.picks = [None]*TOTAL
            st.rerun()
    st.stop()

# ══ HEADER ═════════════════════════════════════════════════════════════
st.markdown('<p class="big-title">⚽ QUINIELA 2026</p>', unsafe_allow_html=True)
c1, c2 = st.columns([4,1])
with c1: st.caption(f"Jugando como: **{st.session_state.user_name}**")
with c2:
    if st.button("Salir"):
        st.session_state.user_name = None
        st.session_state.picks     = [None]*TOTAL
        st.rerun()

tab_picks, tab_lb, tab_admin = st.tabs(["🎯 Mis Picks","📊 Tabla","⚙️ Admin"])

# ══════════════════════════════════════════════════════════════════════
# TAB 1 — PICKS
# ══════════════════════════════════════════════════════════════════════
with tab_picks:
    picks   = list(st.session_state.picks)
    changed = False

    for stage, matches in ALL_STAGES:
        is_r16   = stage == "Ronda de 16"
        is_past  = stage != "Ronda de 16"

        with st.expander(f"{'🟢' if is_r16 else '🔒'} {stage}", expanded=is_r16):
            if is_past:
                st.caption("Esta fase ya terminó. Solo el admin puede asignarte picks.")

            for i, (stg, m) in enumerate(ALL_MATCHES):
                if stg != stage: continue
                t1, t2, result, pts = m
                pick    = picks[i]
                correct = (pick == result) if result else False

                if is_past or result:
                    icon = "✅" if correct else ("❌" if (pick and result) else "📋")
                    st.markdown(f"**{icon} {t1} vs {t2}**" + (f" · Ganó: **{result}**" if result else ""))
                    if pick:
                        st.caption(f"Tu pick: {pick}" + (f" · **+{pts}pts** 🎉" if correct else ""))
                    else:
                        st.caption("_Sin pick — pídele al admin_")
                else:
                    options = [t1, t2]
                    cur = picks[i] if picks[i] in options else None
                    st.markdown(f"**🕐 {t1} vs {t2}**")
                    sel = st.radio(f"p{i}", options, index=options.index(cur) if cur else None,
                                   key=f"pick_{i}", horizontal=True, label_visibility="collapsed")
                    if sel != picks[i]:
                        picks[i] = sel
                        changed   = True
                st.divider()

    if changed:
        st.session_state.picks = picks

    pending = [i for i,(stg,m) in enumerate(ALL_MATCHES) if stg=="Ronda de 16" and not m[2]]
    done_n  = sum(1 for i in pending if picks[i])
    if pending:
        st.progress(done_n/len(pending), text=f"{done_n}/{len(pending)} partidos de R16 predichos")
        if st.button("💾 Guardar picks", type="primary", use_container_width=True):
            save_my_picks()
            st.success("✅ ¡Guardado!")
            st.balloons()

# ══════════════════════════════════════════════════════════════════════
# TAB 2 — LEADERBOARD
# ══════════════════════════════════════════════════════════════════════
with tab_lb:
    recalc_all()
    st.subheader("📊 Tabla de Posiciones")
    users = sorted(st.session_state.all_users.items(), key=lambda x: x[1].get("points",0), reverse=True)

    if not users:
        st.info("Nadie registrado aún.")
    else:
        medals = {0:"🥇",1:"🥈",2:"🥉"}
        top3   = users[:min(3,len(users))]
        cols   = st.columns(len(top3))
        for pos,(uid,u) in enumerate(top3):
            with cols[pos]:
                picks_done = sum(1 for p in u.get("picks",[]) if p)
                st.metric(label=f"{medals[pos]} {uid}",
                          value=f"{u.get('points',0)} pts",
                          delta=f"{picks_done}/{TOTAL} picks")
        st.markdown("---")

        rows = []
        for i,(uid,u) in enumerate(users):
            upicks = u.get("picks",[])
            def stage_pts(stg):
                return sum(m[3] for j,(s,m) in enumerate(ALL_MATCHES)
                           if s==stg and m[2] and j<len(upicks) and upicks[j]==m[2])
            rows.append({
                "#":         medals.get(i,i+1),
                "Nombre":    f"⭐ {uid}" if uid==st.session_state.user_name else uid,
                "G1":        stage_pts("Jornada 1"),
                "G2":        stage_pts("Jornada 2"),
                "G3":        stage_pts("Jornada 3"),
                "R32":       stage_pts("Ronda de 32"),
                "R16":       stage_pts("Ronda de 16"),
                "Total 🏆":  u.get("points",0),
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
        adm1, adm2 = st.tabs(["👤 Editar picks de usuario", "🏆 Resultados reales"])

        # ── EDITAR PICKS DE USUARIO ───────────────────────────────────
        with adm1:
            # Crear usuario nuevo
            with st.expander("➕ Agregar usuario nuevo"):
                new_name = st.text_input("Nombre", max_chars=30, key="admin_new_user")
                if st.button("Crear", key="admin_create"):
                    n = new_name.strip()
                    if not n:
                        st.error("Escribe un nombre")
                    elif n in st.session_state.all_users:
                        st.warning(f"{n} ya existe.")
                    else:
                        st.session_state.all_users[n] = {"picks":[None]*TOTAL,"points":0}
                        st.success(f"✅ Usuario **{n}** creado.")
                        st.rerun()

            st.markdown("---")
            user_list = list(st.session_state.all_users.keys())
            if not user_list:
                st.info("No hay usuarios aún.")
            else:
                sel_user = st.selectbox("Selecciona usuario", user_list, key="admin_user_sel")
                u_picks  = list(st.session_state.all_users[sel_user].get("picks",[None]*TOTAL))
                if len(u_picks) < TOTAL: u_picks += [None]*(TOTAL-len(u_picks))

                edited = list(u_picks)

                for stage, matches in ALL_STAGES:
                    with st.expander(f"📋 {stage}"):
                        for i,(stg,m) in enumerate(ALL_MATCHES):
                            if stg != stage: continue
                            t1, t2, result, pts = m
                            st.markdown(f"**{t1} vs {t2}**" + (f" · Ganó: **{result}**" if result else " · pendiente"))
                            opts    = ["— Sin pick —", t1, t2]
                            if result and result not in [t1, t2]:
                                opts = ["— Sin pick —", t1, t2, "Empate"]
                            elif result == "Empate":
                                opts = ["— Sin pick —", t1, t2, "Empate"]
                            cur_idx = 0
                            if edited[i] == t1: cur_idx = 1
                            elif edited[i] == t2: cur_idx = 2
                            elif edited[i] == "Empate": cur_idx = 3
                            sel = st.radio(f"up{i}", opts, index=cur_idx,
                                           key=f"adm_up_{sel_user}_{i}",
                                           horizontal=True, label_visibility="collapsed")
                            edited[i] = None if sel == "— Sin pick —" else sel
                            if result and edited[i] == result:
                                st.caption(f"✅ Correcto · +{pts}pts")
                            elif edited[i]:
                                st.caption("❌ Incorrecto")
                            st.divider()

                if st.button(f"💾 Guardar picks de {sel_user}", type="primary", use_container_width=True):
                    save_user_picks(sel_user, edited)
                    st.success(f"✅ Guardado. **{sel_user}**: {st.session_state.all_users[sel_user]['points']} pts")

        # ── RESULTADOS REALES ─────────────────────────────────────────
        with adm2:
            st.caption("Aquí puedes ver los resultados reales por jornada. Los resultados de las jornadas pasadas y R32 ya están cargados. Solo actualiza R16.")
            for stage, matches in ALL_STAGES:
                with st.expander(f"📋 {stage}"):
                    for i,(stg,m) in enumerate(ALL_MATCHES):
                        if stg != stage: continue
                        t1, t2, result, pts = m
                        icon = "✅" if result else "🕐"
                        st.markdown(f"{icon} **{t1} vs {t2}** · {f'Ganó: **{result}**' if result else 'Pendiente'}")

        st.markdown("---")
        if st.button("🔒 Cerrar sesión admin"):
            st.session_state.admin_unlocked = False
            st.rerun()
