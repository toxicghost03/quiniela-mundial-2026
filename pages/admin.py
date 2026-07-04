import streamlit as st
from data import GROUPS, KNOCKOUT_ROUNDS, SCORING, ADMIN_PASSWORD

st.set_page_config(page_title="Admin — Quiniela 2026", page_icon="⚙️", layout="wide")

if "admin_ok" not in st.session_state:
    st.session_state.admin_ok = False
if "all_users" not in st.session_state:
    st.session_state.all_users = {}
if "real_results" not in st.session_state:
    st.session_state.real_results = {"groups": {}, "knockout": {}}

if not st.session_state.admin_ok:
    st.title("⚙️ Admin — Quiniela 2026")
    pw = st.text_input("Contraseña de admin", type="password")
    if st.button("Entrar"):
        if pw == ADMIN_PASSWORD:
            st.session_state.admin_ok = True
            st.rerun()
        else:
            st.error("Contraseña incorrecta")
    st.stop()

st.title("⚙️ Panel de Admin — Quiniela 2026")
tab_gres, tab_kres, tab_calc = st.tabs(["📋 Resultados Grupos", "🏆 Resultados Eliminatorias", "🔄 Recalcular"])

with tab_gres:
    st.subheader("Resultados — Fase de Grupos")
    group_results = {}
    cols = st.columns(3)
    for i, (letter, group) in enumerate(GROUPS.items()):
        opts = [""] + [t["name"] for t in group["teams"]]
        saved = st.session_state.real_results.get("groups", {}).get(letter, {})
        with cols[i % 3]:
            st.markdown(f"**Grupo {letter}**")
            f = st.selectbox(f"1° {letter}", opts, index=opts.index(saved.get("first","")) if saved.get("first") in opts else 0, key=f"gr_{letter}_1", label_visibility="collapsed")
            s = st.selectbox(f"2° {letter}", opts, index=opts.index(saved.get("second","")) if saved.get("second") in opts else 0, key=f"gr_{letter}_2", label_visibility="collapsed")
            group_results[letter] = {"first": f or None, "second": s or None}
            st.markdown("---")
    if st.button("💾 Guardar Grupos", type="primary"):
        st.session_state.real_results["groups"] = group_results
        st.success("✅ Guardado")

with tab_kres:
    st.subheader("Resultados — Eliminatorias")
    ko_results = {}
    for r in KNOCKOUT_ROUNDS:
        rid, rname, slots = r["id"], r["name"], r["slots"]
        mc = slots // 2
        st.markdown(f"**{rname}**")
        saved_ko = st.session_state.real_results.get("knockout", {}).get(rid, [""]*mc)
        cols = st.columns(min(mc, 4))
        winners = []
        for i in range(mc):
            with cols[i % len(cols)]:
                v = saved_ko[i] if i < len(saved_ko) else ""
                w = st.text_input(f"Ganador {i+1}", value=v or "", key=f"ko_{rid}_{i}", placeholder="Equipo ganador")
                winners.append(w or None)
        ko_results[rid] = winners
        st.markdown("---")
    if st.button("💾 Guardar Eliminatorias", type="primary"):
        st.session_state.real_results["knockout"] = ko_results
        st.success("✅ Guardado")

with tab_calc:
    st.subheader("Recalcular Puntos")
    if st.button("🔄 Recalcular ahora", type="primary", use_container_width=True):
        real = st.session_state.real_results
        log = []
        for uid, u in st.session_state.all_users.items():
            pts = 0
            for letter, res in real.get("groups", {}).items():
                pick = u.get("groupPicks", {}).get(letter, {})
                if res.get("first") and pick.get("first") == res["first"]: pts += SCORING["group_winner"]
                if res.get("second") and pick.get("second") == res["second"]: pts += SCORING["group_runner"]
            for r in KNOCKOUT_ROUNDS:
                rid = r["id"]
                rw = real.get("knockout", {}).get(rid, [])
                uw = u.get("knockoutPicks", {}).get(rid, [])
                if rid == "final":
                    if rw and uw and len(uw) > 0 and uw[0] == rw[0]: pts += SCORING["final_winner"]
                    if rw and len(rw) > 1 and uw and len(uw) > 1 and uw[1] == rw[1]: pts += SCORING["final_runner"]
                else:
                    for i, w in enumerate(rw):
                        if w and i < len(uw) and uw[i] == w: pts += SCORING.get(rid, 0)
            st.session_state.all_users[uid]["points"] = pts
            log.append(f"✅ {u['name']}: {pts} pts")
        st.success(f"Recálculo completo — {len(log)} participantes")
        st.code("\n".join(log) if log else "No hay participantes aún.", language=None)
