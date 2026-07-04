import streamlit as st
from data import GROUPS, KNOCKOUT_ROUNDS, SCORING
import json, time

st.set_page_config(
    page_title="Quiniela Mundial 2026",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.big-title { font-family: 'Bebas Neue', sans-serif; font-size: 3.5rem; letter-spacing: 3px; color: #F5C518; line-height: 1; margin: 0; }
.sub-title { color: #6b6b80; font-size: 0.85rem; letter-spacing: 3px; text-transform: uppercase; }
.group-header { font-family: 'Bebas Neue', sans-serif; font-size: 1.4rem; color: #F5C518; letter-spacing: 2px; }
div[data-testid="stMetric"] { background: #1a1a24; border: 1px solid #2e2e3e; border-radius: 10px; padding: 12px 16px; }
</style>
""", unsafe_allow_html=True)

# ── SHARED STATE via st.session_state (server-side, shared across users via storage key)
if "all_users" not in st.session_state:
    st.session_state.all_users = {}   # { user_id: {name, pin, groupPicks, knockoutPicks, points} }
if "real_results" not in st.session_state:
    st.session_state.real_results = {"groups": {}, "knockout": {}}

# Per-session user
for key in ["user_id", "user_name", "group_picks", "knockout_picks"]:
    if key not in st.session_state:
        st.session_state[key] = None if key in ["user_id","user_name"] else {}

def slugify(name):
    import re
    return re.sub(r"[^a-z0-9_]", "", name.lower().replace(" ", "_"))

def save_picks():
    uid = st.session_state.user_id
    if uid not in st.session_state.all_users:
        st.session_state.all_users[uid] = {}
    st.session_state.all_users[uid]["groupPicks"]    = st.session_state.group_picks
    st.session_state.all_users[uid]["knockoutPicks"] = st.session_state.knockout_picks
    st.session_state.all_users[uid]["points"]        = st.session_state.all_users[uid].get("points", 0)

def get_flag(team_name):
    for g in GROUPS.values():
        for t in g["teams"]:
            if t["name"] == team_name:
                return t["flag"]
    return "🏳️"

# ══ REGISTER / LOGIN ══════════════════════════════════════════════════
if not st.session_state.user_id:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown('<p class="big-title">QUINIELA<br>MUNDIAL</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-title">USA · Canadá · México 2026</p>', unsafe_allow_html=True)
        st.markdown("---")
        tab_reg, tab_log = st.tabs(["🆕 Registrarse", "🔐 Ya tengo cuenta"])

        with tab_reg:
            name = st.text_input("Tu nombre", max_chars=30, key="reg_name")
            pin  = st.text_input("PIN (opcional, 4 dígitos)", max_chars=4, type="password", key="reg_pin")
            if st.button("Entrar al Mundial →", use_container_width=True, type="primary"):
                if not name.strip():
                    st.error("Ingresa tu nombre")
                else:
                    uid = slugify(name.strip())
                    if uid in st.session_state.all_users:
                        st.error("Ese nombre ya existe. Usa la pestaña de inicio de sesión.")
                    else:
                        st.session_state.all_users[uid] = {"name": name.strip(), "pin": pin or None, "groupPicks": {}, "knockoutPicks": {}, "points": 0}
                        st.session_state.user_id   = uid
                        st.session_state.user_name = name.strip()
                        st.rerun()

        with tab_log:
            lname = st.text_input("Tu nombre", max_chars=30, key="log_name")
            lpin  = st.text_input("PIN (si pusiste uno)", max_chars=4, type="password", key="log_pin")
            if st.button("Entrar →", use_container_width=True, type="primary"):
                if not lname.strip():
                    st.error("Ingresa tu nombre")
                else:
                    uid = slugify(lname.strip())
                    if uid not in st.session_state.all_users:
                        st.error("Usuario no encontrado. Regístrate primero.")
                    else:
                        data = st.session_state.all_users[uid]
                        if data.get("pin") and data["pin"] != lpin:
                            st.error("PIN incorrecto")
                        else:
                            st.session_state.user_id        = uid
                            st.session_state.user_name      = data["name"]
                            st.session_state.group_picks    = data.get("groupPicks", {})
                            st.session_state.knockout_picks = data.get("knockoutPicks", {})
                            st.rerun()
    st.stop()

# ══ MAIN APP ══════════════════════════════════════════════════════════
c1, c2 = st.columns([6, 1])
with c1:
    st.markdown('<p class="big-title">⚽ QUINIELA 2026</p>', unsafe_allow_html=True)
with c2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Salir"):
        for k in ["user_id","user_name","group_picks","knockout_picks"]:
            st.session_state[k] = None if k in ["user_id","user_name"] else {}
        st.rerun()

st.caption(f"Sesión: **{st.session_state.user_name}**")
st.markdown("---")

tab_groups, tab_ko, tab_lb = st.tabs(["🏟️ Fase de Grupos", "🏆 Eliminatorias", "📊 Tabla General"])

# ══ TAB 1 — GRUPOS ════════════════════════════════════════════════════
with tab_groups:
    st.subheader("Fase de Grupos")
    st.caption("Selecciona el **1° y 2°** de cada grupo.")
    cols = st.columns(3)
    col_idx = 0
    for letter, group in GROUPS.items():
        with cols[col_idx % 3]:
            st.markdown(f'<p class="group-header">GRUPO {letter}</p>', unsafe_allow_html=True)
            pick   = st.session_state.group_picks.get(letter, {})
            first  = pick.get("first")
            second = pick.get("second")
            raw_names = [t["name"] for t in group["teams"]]
            st.markdown(f"**1°** `{get_flag(first)} {first}`" if first else "**1°** `—`")
            st.markdown(f"**2°** `{get_flag(second)} {second}`" if second else "**2°** `—`")
            sel = st.radio(
                f"Grupo {letter}",
                options=raw_names,
                format_func=lambda n, l=letter: (
                    f"🥇 {get_flag(n)} {n}" if n == st.session_state.group_picks.get(l, {}).get("first") else
                    f"🥈 {get_flag(n)} {n}" if n == st.session_state.group_picks.get(l, {}).get("second") else
                    f"   {get_flag(n)} {n}"
                ),
                key=f"radio_{letter}", index=None, label_visibility="collapsed",
            )
            if sel:
                p = st.session_state.group_picks.get(letter, {})
                if p.get("first") == sel:
                    st.session_state.group_picks[letter] = {"first": p.get("second"), "second": None}
                elif p.get("second") == sel:
                    st.session_state.group_picks[letter] = {"first": p.get("first"), "second": None}
                elif not p.get("first"):
                    st.session_state.group_picks[letter] = {"first": sel, "second": p.get("second")}
                else:
                    st.session_state.group_picks[letter] = {"first": p.get("first"), "second": sel}
                st.rerun()
            st.markdown("---")
        col_idx += 1

    done_count = sum(1 for l in GROUPS if st.session_state.group_picks.get(l, {}).get("first") and st.session_state.group_picks.get(l, {}).get("second"))
    st.progress(done_count / len(GROUPS), text=f"{done_count}/{len(GROUPS)} grupos completados")
    if st.button("💾 Guardar Fase de Grupos", type="primary", use_container_width=True):
        save_picks()
        st.success("✅ Fase de grupos guardada")

# ══ TAB 2 — ELIMINATORIAS ═════════════════════════════════════════════
with tab_ko:
    st.subheader("Fase Eliminatoria")
    groups_complete = all(
        st.session_state.group_picks.get(l, {}).get("first") and st.session_state.group_picks.get(l, {}).get("second")
        for l in GROUPS
    )
    if not groups_complete:
        st.warning("⚠️ Completa primero **todos** los grupos para desbloquear las eliminatorias.")
    else:
        for round_info in KNOCKOUT_ROUNDS:
            rid, rname, slots, pts = round_info["id"], round_info["name"], round_info["slots"], round_info["pts"]
            st.markdown(f"### 🏅 {rname} — {pts} pts c/acierto")
            if rid == "r32":
                pool = []
                for g in st.session_state.group_picks.values():
                    if g.get("first"):  pool.append(g["first"])
                    if g.get("second"): pool.append(g["second"])
                while len(pool) < 32: pool.append("TBD")
            else:
                prev = KNOCKOUT_ROUNDS[KNOCKOUT_ROUNDS.index(round_info) - 1]
                pool = st.session_state.knockout_picks.get(prev["id"], [])
                while len(pool) < slots: pool.append("TBD")

            match_count = len(pool) // 2
            cols = st.columns(min(match_count, 4))
            picks_this = st.session_state.knockout_picks.get(rid, [None]*match_count)
            if len(picks_this) < match_count: picks_this += [None]*(match_count-len(picks_this))
            changed = False
            for i in range(match_count):
                t1 = pool[i*2]   if i*2   < len(pool) else "TBD"
                t2 = pool[i*2+1] if i*2+1 < len(pool) else "TBD"
                with cols[i % len(cols)]:
                    st.caption(f"Partido {i+1}")
                    options = [t for t in [t1, t2] if t != "TBD"] or ["TBD"]
                    cur = picks_this[i] if picks_this[i] in options else None
                    sel = st.radio(f"P{i+1}", options=options, format_func=lambda n: f"{get_flag(n)} {n}", index=options.index(cur) if cur else None, key=f"ko_{rid}_{i}", label_visibility="collapsed")
                    if sel != picks_this[i]:
                        picks_this[i] = sel
                        changed = True
            if changed:
                st.session_state.knockout_picks[rid] = picks_this
                st.rerun()
            st.markdown("---")
        if st.button("💾 Guardar Eliminatorias", type="primary", use_container_width=True):
            save_picks()
            st.success("✅ Eliminatorias guardadas")

# ══ TAB 3 — LEADERBOARD ═══════════════════════════════════════════════
with tab_lb:
    st.subheader("Tabla de Posiciones")
    users = sorted(st.session_state.all_users.items(), key=lambda x: x[1].get("points", 0), reverse=True)
    if not users:
        st.info("Nadie registrado aún.")
    else:
        top3 = users[:3]
        labels = ["🥇 1°", "🥈 2°", "🥉 3°"]
        c1, c2, c3 = st.columns(3)
        for col, (uid, u), label in zip([c2, c1, c3], top3, labels):
            with col:
                st.metric(label=f"{label} — {u['name']}", value=f"{u.get('points',0)} pts")
        st.markdown("---")
        import pandas as pd
        rows = []
        for i, (uid, u) in enumerate(users, 1):
            medal = {1:"🥇",2:"🥈",3:"🥉"}.get(i, str(i))
            is_me = uid == st.session_state.user_id
            rows.append({"#": medal, "Participante": f"{u['name']} 👈" if is_me else u["name"], "Puntos": u.get("points", 0)})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
