import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from data import GROUPS, KNOCKOUT_ROUNDS, SCORING, ADMIN_PASSWORD
import json

st.set_page_config(page_title="Admin — Quiniela 2026", page_icon="⚙️", layout="wide")

# ── FIREBASE ───────────────────────────────────────────────────────────
@st.cache_resource
def get_db():
    if not firebase_admin._apps:
        key_dict = json.loads(st.secrets["FIREBASE_KEY"])
        cred = credentials.Certificate(key_dict)
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = get_db()

# ── AUTH ───────────────────────────────────────────────────────────────
if "admin_ok" not in st.session_state:
    st.session_state.admin_ok = False

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

# ══════════════════════════════════════════════════════════════════════
#  ADMIN PANEL
# ══════════════════════════════════════════════════════════════════════
st.title("⚙️ Panel de Admin — Quiniela 2026")
st.caption("Ingresa los resultados reales y recalcula los puntos de todos los participantes.")

# Load saved results
@st.cache_data(ttl=60)
def load_results():
    snap = db.collection("admin").document("results").get()
    if snap.exists:
        return snap.to_dict()
    return {"groups": {}, "knockout": {}}

saved = load_results()

tab_gres, tab_kres, tab_calc = st.tabs(["📋 Resultados Grupos", "🏆 Resultados Eliminatorias", "🔄 Recalcular"])

# ── GROUP RESULTS ──────────────────────────────────────────────────────
with tab_gres:
    st.subheader("Resultados — Fase de Grupos")
    group_results = {}

    cols = st.columns(3)
    for i, (letter, group) in enumerate(GROUPS.items()):
        team_options = [""] + [t["name"] for t in group["teams"]]
        saved_g = saved.get("groups", {}).get(letter, {})

        with cols[i % 3]:
            st.markdown(f"**Grupo {letter}**")
            first = st.selectbox(
                f"1° Grupo {letter}",
                options=team_options,
                index=team_options.index(saved_g.get("first", "")) if saved_g.get("first") in team_options else 0,
                key=f"gres_{letter}_1",
                label_visibility="collapsed",
            )
            second = st.selectbox(
                f"2° Grupo {letter}",
                options=team_options,
                index=team_options.index(saved_g.get("second", "")) if saved_g.get("second") in team_options else 0,
                key=f"gres_{letter}_2",
                label_visibility="collapsed",
            )
            group_results[letter] = {"first": first or None, "second": second or None}
            st.markdown("---")

    if st.button("💾 Guardar Resultados de Grupos", type="primary"):
        db.collection("admin").document("results").set({"groups": group_results}, merge=True)
        st.cache_data.clear()
        st.success("✅ Resultados de grupos guardados")

# ── KNOCKOUT RESULTS ───────────────────────────────────────────────────
with tab_kres:
    st.subheader("Resultados — Eliminatorias")
    knockout_results = {}

    for round_info in KNOCKOUT_ROUNDS:
        rid   = round_info["id"]
        rname = round_info["name"]
        slots = round_info["slots"]
        match_count = slots // 2

        st.markdown(f"**{rname}** ({match_count} partidos)")
        saved_ko = saved.get("knockout", {}).get(rid, [None] * match_count)

        cols = st.columns(min(match_count, 4))
        winners = []
        for i in range(match_count):
            with cols[i % len(cols)]:
                val = saved_ko[i] if i < len(saved_ko) else ""
                w = st.text_input(
                    f"Ganador Partido {i+1}",
                    value=val or "",
                    key=f"ko_{rid}_{i}",
                    placeholder="Nombre del equipo",
                )
                winners.append(w or None)
        knockout_results[rid] = winners
        st.markdown("---")

    if st.button("💾 Guardar Resultados Eliminatorias", type="primary"):
        db.collection("admin").document("results").set({"knockout": knockout_results}, merge=True)
        st.cache_data.clear()
        st.success("✅ Resultados de eliminatorias guardados")

# ── RECALCULATE ────────────────────────────────────────────────────────
with tab_calc:
    st.subheader("Recalcular Puntos")
    st.info("Esto actualiza los puntos de **todos** los participantes según los resultados guardados.")

    if st.button("🔄 Recalcular ahora", type="primary", use_container_width=True):
        res_snap = db.collection("admin").document("results").get()
        if not res_snap.exists:
            st.error("No hay resultados guardados aún.")
        else:
            real = res_snap.to_dict()
            users = list(db.collection("users").stream())
            log_lines = []

            for u_doc in users:
                u  = u_doc.to_dict()
                pts = 0

                # Groups
                for letter, res in real.get("groups", {}).items():
                    pick = u.get("groupPicks", {}).get(letter, {})
                    if res.get("first")  and pick.get("first")  == res["first"]:  pts += SCORING["group_winner"]
                    if res.get("second") and pick.get("second") == res["second"]: pts += SCORING["group_runner"]

                # Knockout
                for r in KNOCKOUT_ROUNDS:
                    rid = r["id"]
                    real_w = real.get("knockout", {}).get(rid, [])
                    user_w = u.get("knockoutPicks", {}).get(rid, [])
                    if rid == "final":
                        if real_w and len(real_w) > 0 and user_w and user_w[0] == real_w[0]: pts += SCORING["final_winner"]
                        if real_w and len(real_w) > 1 and user_w and len(user_w) > 1 and user_w[1] == real_w[1]: pts += SCORING["final_runner"]
                    else:
                        for i, winner in enumerate(real_w):
                            if winner and i < len(user_w) and user_w[i] == winner:
                                pts += SCORING.get(rid, 0)

                db.collection("users").document(u_doc.id).update({"points": pts})
                log_lines.append(f"✅ {u.get('name', u_doc.id)}: {pts} pts")

            st.success(f"Recálculo completo — {len(users)} participantes actualizados")
            st.code("\n".join(log_lines), language=None)
