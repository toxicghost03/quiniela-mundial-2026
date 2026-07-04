import streamlit as st
import pandas as pd

st.set_page_config(page_title="Quiniela Mundial 2026 🏆", page_icon="⚽", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.big-title { font-family:'Bebas Neue',sans-serif; font-size:2.8rem; letter-spacing:3px; color:#F5C518; line-height:1; margin:0; text-align:center; }
div[data-testid="stMetric"] { background:#1a1a24; border:1px solid #2e2e3e; border-radius:10px; padding:12px 16px; }
</style>
""", unsafe_allow_html=True)

ADMIN_PASSWORD = "admin2026"

# ══ MATCH DATA ═════════════════════════════════════════════════════════
# (team1, team2, date, is_group_stage)
# Results stored separately in session_state so admin can update them

MATCHES_DEF = {
  "Jornada 1": [
    # Group A
    ("🇲🇽 México",        "🇿🇦 Sudáfrica",     "11 Jun", True),
    ("🇰🇷 Corea del Sur", "🇨🇿 Chequia",        "11 Jun", True),
    # Group B
    ("🇨🇦 Canadá",        "🇧🇦 Bosnia",         "12 Jun", True),
    ("🇶🇦 Qatar",         "🇨🇭 Suiza",          "13 Jun", True),
    # Group C
    ("🇧🇷 Brasil",        "🇲🇦 Marruecos",      "13 Jun", True),
    ("🏴󠁧󠁢󠁸󠁣󠁴󠁿 Escocia",    "🇭🇹 Haití",          "13 Jun", True),
    # Group D
    ("🇺🇸 USA",           "🇵🇾 Paraguay",       "12 Jun", True),
    ("🇦🇺 Australia",     "🇹🇷 Turquía",        "13 Jun", True),
    # Group E
    ("🇩🇪 Alemania",      "🇨🇼 Curazao",        "14 Jun", True),
    ("🇨🇮 Costa Marfil",  "🇪🇨 Ecuador",        "14 Jun", True),
    # Group F
    ("🇳🇱 Países Bajos",  "🇯🇵 Japón",          "14 Jun", True),
    ("🇸🇪 Suecia",        "🇹🇳 Túnez",          "14 Jun", True),
    # Group G
    ("🇧🇪 Bélgica",       "🇪🇬 Egipto",         "15 Jun", True),
    ("🇮🇷 Irán",          "🇳🇿 Nueva Zelanda",  "15 Jun", True),
    # Group H
    ("🇪🇸 España",        "🇨🇻 Cabo Verde",     "15 Jun", True),
    ("🇸🇦 Arabia Saudita","🇺🇾 Uruguay",        "15 Jun", True),
    # Group I
    ("🇫🇷 Francia",       "🇸🇳 Senegal",        "16 Jun", True),
    ("🇳🇴 Noruega",       "🇮🇶 Irak",           "16 Jun", True),
    # Group J
    ("🇦🇷 Argentina",     "🇩🇿 Argelia",        "16 Jun", True),
    ("🇦🇹 Austria",       "🇯🇴 Jordania",       "16 Jun", True),
    # Group K
    ("🇵🇹 Portugal",      "🇨🇩 Congo RD",       "17 Jun", True),
    ("🇺🇿 Uzbekistán",    "🇨🇴 Colombia",       "17 Jun", True),
    # Group L
    ("🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra", "🇭🇷 Croacia",        "17 Jun", True),
    ("🇬🇭 Ghana",         "🇵🇦 Panamá",         "17 Jun", True),
  ],
  "Jornada 2": [
    # Group A
    ("🇨🇿 Chequia",       "🇿🇦 Sudáfrica",     "18 Jun", True),
    ("🇲🇽 México",        "🇰🇷 Corea del Sur", "18 Jun", True),
    # Group B
    ("🇨🇭 Suiza",         "🇧🇦 Bosnia",         "18 Jun", True),
    ("🇨🇦 Canadá",        "🇶🇦 Qatar",          "18 Jun", True),
    # Group C
    ("🏴󠁧󠁢󠁸󠁣󠁴󠁿 Escocia",    "🇲🇦 Marruecos",     "19 Jun", True),
    ("🇧🇷 Brasil",        "🇭🇹 Haití",          "19 Jun", True),
    # Group D
    ("🇺🇸 USA",           "🇦🇺 Australia",      "19 Jun", True),
    ("🇹🇷 Turquía",       "🇵🇾 Paraguay",       "19 Jun", True),
    # Group E
    ("🇩🇪 Alemania",      "🇨🇮 Costa Marfil",   "20 Jun", True),
    ("🇪🇨 Ecuador",       "🇨🇼 Curazao",        "20 Jun", True),
    # Group F
    ("🇳🇱 Países Bajos",  "🇸🇪 Suecia",         "20 Jun", True),
    ("🇯🇵 Japón",         "🇹🇳 Túnez",          "20 Jun", True),
    # Group G
    ("🇧🇪 Bélgica",       "🇮🇷 Irán",           "21 Jun", True),
    ("🇪🇬 Egipto",        "🇳🇿 Nueva Zelanda",  "21 Jun", True),
    # Group H
    ("🇪🇸 España",        "🇸🇦 Arabia Saudita", "21 Jun", True),
    ("🇺🇾 Uruguay",       "🇨🇻 Cabo Verde",     "21 Jun", True),
    # Group I
    ("🇫🇷 Francia",       "🇮🇶 Irak",           "22 Jun", True),
    ("🇳🇴 Noruega",       "🇸🇳 Senegal",        "22 Jun", True),
    # Group J
    ("🇦🇷 Argentina",     "🇦🇹 Austria",        "22 Jun", True),
    ("🇯🇴 Jordania",      "🇩🇿 Argelia",        "22 Jun", True),
    # Group K
    ("🇵🇹 Portugal",      "🇺🇿 Uzbekistán",     "23 Jun", True),
    ("🇨🇴 Colombia",      "🇨🇩 Congo RD",       "23 Jun", True),
    # Group L
    ("🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra", "🇬🇭 Ghana",          "23 Jun", True),
    ("🇵🇦 Panamá",        "🇭🇷 Croacia",        "23 Jun", True),
  ],
  "Jornada 3": [
    # Group A
    ("🇨🇿 Chequia",       "🇲🇽 México",        "24 Jun", True),
    ("🇿🇦 Sudáfrica",     "🇰🇷 Corea del Sur", "24 Jun", True),
    # Group B
    ("🇨🇭 Suiza",         "🇨🇦 Canadá",        "24 Jun", True),
    ("🇧🇦 Bosnia",        "🇶🇦 Qatar",         "24 Jun", True),
    # Group C
    ("🏴󠁧󠁢󠁸󠁣󠁴󠁿 Escocia",    "🇧🇷 Brasil",        "24 Jun", True),
    ("🇲🇦 Marruecos",    "🇭🇹 Haití",         "24 Jun", True),
    # Group D
    ("🇹🇷 Turquía",       "🇺🇸 USA",           "25 Jun", True),
    ("🇵🇾 Paraguay",      "🇦🇺 Australia",     "25 Jun", True),
    # Group E
    ("🇨🇼 Curazao",       "🇨🇮 Costa Marfil",  "25 Jun", True),
    ("🇪🇨 Ecuador",       "🇩🇪 Alemania",      "25 Jun", True),
    # Group F
    ("🇯🇵 Japón",         "🇸🇪 Suecia",        "25 Jun", True),
    ("🇳🇱 Países Bajos",  "🇹🇳 Túnez",         "25 Jun", True),
    # Group G
    ("🇧🇪 Bélgica",       "🇳🇿 Nueva Zelanda", "26 Jun", True),
    ("🇪🇬 Egipto",        "🇮🇷 Irán",          "26 Jun", True),
    # Group H
    ("🇨🇻 Cabo Verde",    "🇸🇦 Arabia Saudita","26 Jun", True),
    ("🇪🇸 España",        "🇺🇾 Uruguay",       "26 Jun", True),
    # Group I
    ("🇫🇷 Francia",       "🇳🇴 Noruega",       "26 Jun", True),
    ("🇸🇳 Senegal",       "🇮🇶 Irak",          "26 Jun", True),
    # Group J
    ("🇦🇷 Argentina",     "🇯🇴 Jordania",      "27 Jun", True),
    ("🇩🇿 Argelia",       "🇦🇹 Austria",       "27 Jun", True),
    # Group K
    ("🇨🇴 Colombia",      "🇵🇹 Portugal",      "27 Jun", True),
    ("🇨🇩 Congo RD",      "🇺🇿 Uzbekistán",    "27 Jun", True),
    # Group L
    ("🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra", "🇵🇦 Panamá",        "27 Jun", True),
    ("🇭🇷 Croacia",       "🇬🇭 Ghana",         "27 Jun", True),
  ],
  "Ronda de 32": [
    ("🇨🇦 Canadá",       "🇿🇦 Sudáfrica",   "28 Jun", False),
    ("🇧🇷 Brasil",       "🇯🇵 Japón",       "29 Jun", False),
    ("🇩🇪 Alemania",     "🇵🇾 Paraguay",    "29 Jun", False),
    ("🇳🇱 Países Bajos", "🇲🇦 Marruecos",  "29 Jun", False),
    ("🇳🇴 Noruega",      "🇨🇮 Costa Marfil","30 Jun", False),
    ("🇫🇷 Francia",      "🇸🇪 Suecia",      "30 Jun", False),
    ("🇲🇽 México",       "🇪🇨 Ecuador",     "30 Jun", False),
    ("🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra","🇨🇩 Congo RD",  "1 Jul",  False),
    ("🇧🇪 Bélgica",      "🇸🇳 Senegal",     "1 Jul",  False),
    ("🇺🇸 USA",          "🇧🇦 Bosnia",      "1 Jul",  False),
    ("🇪🇸 España",       "🇦🇹 Austria",     "2 Jul",  False),
    ("🇵🇹 Portugal",     "🇭🇷 Croacia",     "2 Jul",  False),
    ("🇨🇭 Suiza",        "🇩🇿 Argelia",     "2 Jul",  False),
    ("🇪🇬 Egipto",       "🇦🇺 Australia",   "3 Jul",  False),
    ("🇦🇷 Argentina",    "🇨🇻 Cabo Verde",  "3 Jul",  False),
    ("🇨🇴 Colombia",     "🇬🇭 Ghana",       "3 Jul",  False),
  ],
  "Ronda de 16": [
    ("🇲🇦 Marruecos",   "🇨🇦 Canadá",      "4 Jul · 1pm ET",  False),
    ("🇫🇷 Francia",     "🇵🇾 Paraguay",    "4 Jul · 5pm ET",  False),
    ("🇧🇷 Brasil",      "🇳🇴 Noruega",     "5 Jul · 4pm ET",  False),
    ("🇲🇽 México",      "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra","5 Jul · 8pm ET",  False),
    ("🇵🇹 Portugal",    "🇪🇸 España",      "6 Jul · 3pm ET",  False),
    ("🇺🇸 USA",         "🇧🇪 Bélgica",     "6 Jul · 8pm ET",  False),
    ("🇦🇷 Argentina",   "🇪🇬 Egipto",      "7 Jul · 12pm ET", False),
    ("🇨🇭 Suiza",       "🇨🇴 Colombia",    "7 Jul · 4pm ET",  False),
  ],
}

# Known results — (winner or "Empate")
KNOWN_RESULTS = {
  "Jornada 1": [
    "🇲🇽 México","🇰🇷 Corea del Sur",
    "Empate","Empate",
    "Empate","🏴󠁧󠁢󠁸󠁣󠁴󠁿 Escocia",
    "🇺🇸 USA","🇦🇺 Australia",
    "🇩🇪 Alemania","🇨🇮 Costa Marfil",
    "Empate","🇸🇪 Suecia",
    "Empate","Empate",
    "Empate","Empate",
    "🇫🇷 Francia","🇳🇴 Noruega",
    "🇦🇷 Argentina","🇦🇹 Austria",
    "Empate","🇨🇴 Colombia",
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra","🇬🇭 Ghana",
  ],
  "Jornada 2": [
    "Empate","🇲🇽 México",
    "🇨🇭 Suiza","🇨🇦 Canadá",
    "🇲🇦 Marruecos","🇧🇷 Brasil",
    "🇺🇸 USA","🇵🇾 Paraguay",
    "🇩🇪 Alemania","Empate",
    "🇳🇱 Países Bajos","🇯🇵 Japón",
    "Empate","🇪🇬 Egipto",
    "🇪🇸 España","🇺🇾 Uruguay",
    "🇫🇷 Francia","🇳🇴 Noruega",
    "🇦🇷 Argentina","🇯🇴 Jordania",
    "🇵🇹 Portugal","🇨🇴 Colombia",
    "Empate","🇭🇷 Croacia",
  ],
  "Jornada 3": [
    "🇲🇽 México","🇰🇷 Corea del Sur",
    "🇨🇭 Suiza","🇧🇦 Bosnia",
    "🇧🇷 Brasil","🇲🇦 Marruecos",
    "🇹🇷 Turquía","Empate",
    "🇨🇮 Costa Marfil","🇪🇨 Ecuador",
    "Empate","🇳🇱 Países Bajos",
    "🇧🇪 Bélgica","Empate",
    "Empate","🇪🇸 España",
    "🇫🇷 Francia","🇸🇳 Senegal",
    "🇦🇷 Argentina","Empate",
    "Empate","🇨🇩 Congo RD",
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra","🇭🇷 Croacia",
  ],
  "Ronda de 32": [
    "🇨🇦 Canadá","🇧🇷 Brasil","🇵🇾 Paraguay","🇲🇦 Marruecos",
    "🇳🇴 Noruega","🇫🇷 Francia","🇲🇽 México","🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra",
    "🇧🇪 Bélgica","🇺🇸 USA","🇪🇸 España","🇵🇹 Portugal",
    "🇨🇭 Suiza","🇪🇬 Egipto","🇦🇷 Argentina","🇨🇴 Colombia",
  ],
  "Ronda de 16": [
    "🇲🇦 Marruecos", None, None, None, None, None, None, None,
  ],
}

# Build flat list
ALL_MATCHES = []
for stage, matches in MATCHES_DEF.items():
    for m in matches:
        ALL_MATCHES.append((stage, m))
TOTAL = len(ALL_MATCHES)

def get_result(stage, idx):
    """Get result from session_state override or KNOWN_RESULTS."""
    overrides = st.session_state.get("result_overrides", {})
    key = f"{stage}_{idx}"
    if key in overrides:
        return overrides[key]
    known = KNOWN_RESULTS.get(stage, [])
    return known[idx] if idx < len(known) else None

# ══ SHARED STATE ═══════════════════════════════════════════════════════
if "all_users"        not in st.session_state: st.session_state.all_users        = {}
if "admin_unlocked"   not in st.session_state: st.session_state.admin_unlocked   = False
if "result_overrides" not in st.session_state: st.session_state.result_overrides = {}
if "user_name"        not in st.session_state: st.session_state.user_name        = None
if "picks"            not in st.session_state: st.session_state.picks            = [None]*TOTAL

def recalc_all():
    stage_idx = {}
    for i,(stage,m) in enumerate(ALL_MATCHES):
        stage_idx.setdefault(stage,[]).append(i)
    for uid, u in st.session_state.all_users.items():
        pts = 0
        upicks = u.get("picks",[])
        for i,(stage,m) in enumerate(ALL_MATCHES):
            sidx = stage_idx[stage].index(i)
            result = get_result(stage, sidx)
            pick   = upicks[i] if i < len(upicks) else None
            if result and pick and pick == result:
                pts += m[3] if len(m) > 3 else (2 if m[2] else 5)
        st.session_state.all_users[uid]["points"] = pts

def get_pts(stage):
    if "Jornada" in stage: return 2
    if "32" in stage: return 3
    return 5

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
        st.session_state.picks = [None]*TOTAL
        st.rerun()

tab_picks, tab_lb, tab_admin = st.tabs(["🎯 Mis Picks","📊 Tabla","⚙️ Admin"])

# ══ TAB 1 — PICKS ══════════════════════════════════════════════════════
with tab_picks:
    picks   = list(st.session_state.picks)
    changed = False
    stage_counters = {}

    for stage, matches in MATCHES_DEF.items():
        is_r16   = stage == "Ronda de 16"
        is_group = "Jornada" in stage
        with st.expander(f"{'🟢' if is_r16 else '🔒'} {stage}", expanded=is_r16):
            if not is_r16:
                st.caption("Esta fase ya terminó. Solo el admin puede asignarte picks.")
            for i,(stg,m) in enumerate(ALL_MATCHES):
                if stg != stage: continue
                t1, t2, date, _ = m
                sidx   = stage_counters.get(stage, 0)
                stage_counters[stage] = sidx + 1
                result = get_result(stage, sidx)
                pick   = picks[i]
                correct = (pick == result) if result else False
                pts    = get_pts(stage)

                if not is_r16 or result:
                    icon = "✅" if correct else ("❌" if (pick and result) else "📋")
                    st.markdown(f"**{icon} {t1} vs {t2}** · {date}" +
                                (f" · Ganó: **{result}**" if result else ""))
                    if pick:
                        st.caption(f"Tu pick: {pick}" + (f" · **+{pts}pts** 🎉" if correct else ""))
                    else:
                        st.caption("_Sin pick — pídele al admin_")
                else:
                    options = [t1, t2]
                    cur = picks[i] if picks[i] in options else None
                    st.markdown(f"**🕐 {t1} vs {t2}** · {date}")
                    sel = st.radio(f"p{i}", options, index=options.index(cur) if cur else None,
                                   key=f"pick_{i}", horizontal=True, label_visibility="collapsed")
                    if sel != picks[i]:
                        picks[i] = sel
                        changed   = True
                st.divider()

    if changed:
        st.session_state.picks = picks

    pending = [i for i,(stg,m) in enumerate(ALL_MATCHES)
               if stg=="Ronda de 16" and not get_result("Ronda de 16", list(MATCHES_DEF["Ronda de 16"]).index(m) if m in MATCHES_DEF["Ronda de 16"] else 99)]
    done_n = sum(1 for i in pending if picks[i])
    if pending:
        st.progress(done_n/max(len(pending),1), text=f"{done_n}/{len(pending)} partidos de R16 predichos")
        if st.button("💾 Guardar picks", type="primary", use_container_width=True):
            save_my_picks()
            st.success("✅ ¡Guardado!")
            st.balloons()

# ══ TAB 2 — LEADERBOARD ════════════════════════════════════════════════
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
                st.metric(label=f"{medals[pos]} {uid}", value=f"{u.get('points',0)} pts")
        st.markdown("---")

        stage_idx_map = {}
        for i,(stage,m) in enumerate(ALL_MATCHES):
            stage_idx_map.setdefault(stage,[]).append(i)

        rows = []
        for rank,(uid,u) in enumerate(users):
            upicks = u.get("picks",[])
            def sp(stg):
                sc = {}
                total = 0
                for i,(s,m) in enumerate(ALL_MATCHES):
                    if s != stg: continue
                    sidx = stage_idx_map[stg].index(i)
                    r = get_result(stg, sidx)
                    p = upicks[i] if i < len(upicks) else None
                    if r and p and p == r:
                        total += get_pts(stg)
                return total
            rows.append({
                "#": medals.get(rank, rank+1),
                "Nombre": f"⭐ {uid}" if uid==st.session_state.user_name else uid,
                "G1": sp("Jornada 1"),
                "G2": sp("Jornada 2"),
                "G3": sp("Jornada 3"),
                "R32": sp("Ronda de 32"),
                "R16": sp("Ronda de 16"),
                "Total 🏆": u.get("points",0),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ══ TAB 3 — ADMIN ══════════════════════════════════════════════════════
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
        adm1, adm2, adm3 = st.tabs(["🏆 Poner resultados","👤 Picks de usuario","➕ Agregar usuario"])

        # ── SUB-TAB 1: RESULTADOS REALES ─────────────────────────────
        with adm1:
            st.caption("Selecciona quién ganó cada partido. Los puntos de todos se recalculan automáticamente.")

            for stage, matches in MATCHES_DEF.items():
                with st.expander(f"📋 {stage}", expanded=(stage=="Ronda de 16")):
                    is_group = "Jornada" in stage
                    changed_any = False
                    new_results = {}
                    for sidx, (t1, t2, date, _) in enumerate(matches):
                        cur_result = get_result(stage, sidx)
                        st.markdown(f"**{t1} vs {t2}** · {date}")
                        if is_group:
                            opts = ["⏳ Pendiente", t1, "Empate", t2]
                            if cur_result == t1: ci = 1
                            elif cur_result == "Empate": ci = 2
                            elif cur_result == t2: ci = 3
                            else: ci = 0
                        else:
                            opts = ["⏳ Pendiente", t1, t2]
                            if cur_result == t1: ci = 1
                            elif cur_result == t2: ci = 2
                            else: ci = 0
                        sel = st.radio(f"res_{stage}_{sidx}", opts, index=ci,
                                       key=f"admin_res_{stage}_{sidx}",
                                       horizontal=True, label_visibility="collapsed")
                        new_results[f"{stage}_{sidx}"] = None if sel == "⏳ Pendiente" else sel
                        st.divider()

                    if st.button(f"💾 Guardar {stage}", key=f"save_{stage}", type="primary", use_container_width=True):
                        st.session_state.result_overrides.update(new_results)
                        recalc_all()
                        st.success(f"✅ Resultados de {stage} guardados. Puntos recalculados.")

        # ── SUB-TAB 2: EDITAR PICKS DE USUARIO ───────────────────────
        with adm2:
            user_list = list(st.session_state.all_users.keys())
            if not user_list:
                st.info("No hay usuarios aún. Agrégalos en la pestaña ➕")
            else:
                sel_user = st.selectbox("Selecciona usuario", user_list, key="admin_user_sel")
                u_picks  = list(st.session_state.all_users[sel_user].get("picks",[None]*TOTAL))
                if len(u_picks) < TOTAL: u_picks += [None]*(TOTAL-len(u_picks))
                edited = list(u_picks)

                for stage, matches in MATCHES_DEF.items():
                    with st.expander(f"📋 {stage}"):
                        is_group = "Jornada" in stage
                        for i,(stg,m) in enumerate(ALL_MATCHES):
                            if stg != stage: continue
                            t1, t2, date, _ = m
                            sidx   = [j for j,(s,_) in enumerate(ALL_MATCHES) if s==stage].index(i)
                            result = get_result(stage, sidx)
                            pts    = get_pts(stage)
                            st.markdown(f"**{t1} vs {t2}** · {date}" +
                                        (f" · Ganó: **{result}**" if result else ""))
                            if is_group:
                                opts = ["— Sin pick —", t1, "Empate", t2]
                                if edited[i]==t1: ci=1
                                elif edited[i]=="Empate": ci=2
                                elif edited[i]==t2: ci=3
                                else: ci=0
                            else:
                                opts = ["— Sin pick —", t1, t2]
                                if edited[i]==t1: ci=1
                                elif edited[i]==t2: ci=2
                                else: ci=0
                            sel = st.radio(f"up{i}", opts, index=ci,
                                           key=f"adm_up_{sel_user}_{i}",
                                           horizontal=True, label_visibility="collapsed")
                            edited[i] = None if sel=="— Sin pick —" else sel
                            if result and edited[i]==result:
                                st.caption(f"✅ Correcto · +{pts}pts")
                            elif edited[i]:
                                st.caption("❌ Incorrecto")
                            st.divider()

                if st.button(f"💾 Guardar picks de {sel_user}", type="primary", use_container_width=True):
                    save_user_picks(sel_user, edited)
                    st.success(f"✅ Guardado. **{sel_user}**: {st.session_state.all_users[sel_user]['points']} pts")

        # ── SUB-TAB 3: AGREGAR USUARIO ────────────────────────────────
        with adm3:
            st.subheader("➕ Agregar usuario nuevo")
            new_name = st.text_input("Nombre del usuario", max_chars=30, key="admin_new_user")
            if st.button("Crear usuario", key="admin_create", type="primary"):
                n = new_name.strip()
                if not n:
                    st.error("Escribe un nombre")
                elif n in st.session_state.all_users:
                    st.warning(f"**{n}** ya existe.")
                else:
                    st.session_state.all_users[n] = {"picks":[None]*TOTAL,"points":0}
                    st.success(f"✅ Usuario **{n}** creado. Asígnale picks en la pestaña 'Picks de usuario'.")
                    st.rerun()

            st.markdown("---")
            st.subheader("👥 Usuarios registrados")
            if st.session_state.all_users:
                users_s = sorted(st.session_state.all_users.items(), key=lambda x: x[1].get("points",0), reverse=True)
                for rank,(uid,u) in enumerate(users_s):
                    picks_done = sum(1 for p in u.get("picks",[]) if p)
                    st.markdown(f"**{rank+1}. {uid}** · {picks_done}/{TOTAL} picks · **{u.get('points',0)} pts**")
            else:
                st.info("Nadie aún.")

        st.markdown("---")
        if st.button("🔒 Cerrar sesión admin"):
            st.session_state.admin_unlocked = False
            st.rerun()
