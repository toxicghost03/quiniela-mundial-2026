import streamlit as st
import pandas as pd
import json, urllib.request, urllib.error, base64
from datetime import datetime, timezone, timedelta

st.set_page_config(page_title="Quiniela Mundial 2026 🏆", page_icon="⚽", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.big-title { font-family:'Bebas Neue',sans-serif; font-size:2.8rem; letter-spacing:3px; color:#F5C518; line-height:1; margin:0; text-align:center; }
.countdown { font-family:'Bebas Neue',sans-serif; font-size:2rem; color:#ff4d6d; text-align:center; letter-spacing:2px; }
.locked-banner { background:#1a1a24; border:2px solid #ff4d6d; border-radius:10px; padding:16px; text-align:center; color:#ff4d6d; font-weight:700; font-size:1.1rem; margin-bottom:16px; }
.open-banner { background:#1a1a24; border:2px solid #00d97e; border-radius:10px; padding:16px; text-align:center; color:#00d97e; font-weight:700; font-size:1rem; margin-bottom:16px; }
div[data-testid="stMetric"] { background:#1a1a24; border:1px solid #2e2e3e; border-radius:10px; padding:12px 16px; }
</style>
""", unsafe_allow_html=True)

ADMIN_PASSWORD = "admin2026"
GH_TOKEN  = st.secrets["GH_TOKEN"]
GH_REPO   = "toxicghost03/quiniela-mundial-2026"
GH_FILE   = "data.json"
GH_API    = f"https://api.github.com/repos/{GH_REPO}/contents/{GH_FILE}"

DEADLINE_UTC = datetime(2026, 7, 6, 3, 0, 0, tzinfo=timezone.utc)

def now_utc():
    return datetime.now(timezone.utc)

def is_locked():
    return now_utc() >= DEADLINE_UTC

def time_remaining():
    delta = DEADLINE_UTC - now_utc()
    if delta.total_seconds() <= 0: return None
    h, rem = divmod(int(delta.total_seconds()), 3600)
    m, s   = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

# ── GitHub persistence ─────────────────────────────────────────────────
def gh_load():
    try:
        req = urllib.request.Request(GH_API,
            headers={"Authorization": f"token {GH_TOKEN}", "Accept": "application/vnd.github+json"})
        with urllib.request.urlopen(req) as r:
            resp = json.loads(r.read())
            content = base64.b64decode(resp["content"]).decode()
            data = json.loads(content)
            data["_sha"] = resp["sha"]
            return data
    except:
        return {"users": {}, "results": {}, "_sha": ""}

def gh_save():
    data = {"users": st.session_state.all_users, "results": st.session_state.result_overrides}
    sha  = st.session_state.get("_gh_sha", "")
    body = json.dumps({"message": "Auto-save", "content": base64.b64encode(
        json.dumps(data, ensure_ascii=False, indent=2).encode()).decode(),
        "sha": sha}, ensure_ascii=False).encode()
    try:
        req = urllib.request.Request(GH_API, data=body, method="PUT",
            headers={"Authorization": f"token {GH_TOKEN}",
                     "Accept": "application/vnd.github+json",
                     "Content-Type": "application/json"})
        with urllib.request.urlopen(req) as r:
            resp = json.loads(r.read())
            st.session_state._gh_sha = resp.get("content", {}).get("sha", sha)
    except Exception as e:
        st.warning(f"⚠️ No se pudo guardar en GitHub: {e}")

# ══ MATCH DATA ═════════════════════════════════════════════════════════
MATCHES_DEF = {
  "Jornada 1": [
    ("🇲🇽 México","🇿🇦 Sudáfrica","11 Jun",True),("🇰🇷 Corea del Sur","🇨🇿 Chequia","11 Jun",True),
    ("🇨🇦 Canadá","🇧🇦 Bosnia","12 Jun",True),("🇶🇦 Qatar","🇨🇭 Suiza","13 Jun",True),
    ("🇧🇷 Brasil","🇲🇦 Marruecos","13 Jun",True),("🏴󠁧󠁢󠁸󠁣󠁴󠁿 Escocia","🇭🇹 Haití","13 Jun",True),
    ("🇺🇸 USA","🇵🇾 Paraguay","12 Jun",True),("🇦🇺 Australia","🇹🇷 Turquía","13 Jun",True),
    ("🇩🇪 Alemania","🇨🇼 Curazao","14 Jun",True),("🇨🇮 Costa Marfil","🇪🇨 Ecuador","14 Jun",True),
    ("🇳🇱 Países Bajos","🇯🇵 Japón","14 Jun",True),("🇸🇪 Suecia","🇹🇳 Túnez","14 Jun",True),
    ("🇧🇪 Bélgica","🇪🇬 Egipto","15 Jun",True),("🇮🇷 Irán","🇳🇿 Nueva Zelanda","15 Jun",True),
    ("🇪🇸 España","🇨🇻 Cabo Verde","15 Jun",True),("🇸🇦 Arabia Saudita","🇺🇾 Uruguay","15 Jun",True),
    ("🇫🇷 Francia","🇸🇳 Senegal","16 Jun",True),("🇳🇴 Noruega","🇮🇶 Irak","16 Jun",True),
    ("🇦🇷 Argentina","🇩🇿 Argelia","16 Jun",True),("🇦🇹 Austria","🇯🇴 Jordania","16 Jun",True),
    ("🇵🇹 Portugal","🇨🇩 Congo RD","17 Jun",True),("🇺🇿 Uzbekistán","🇨🇴 Colombia","17 Jun",True),
    ("🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra","🇭🇷 Croacia","17 Jun",True),("🇬🇭 Ghana","🇵🇦 Panamá","17 Jun",True),
  ],
  "Jornada 2": [
    ("🇨🇿 Chequia","🇿🇦 Sudáfrica","18 Jun",True),("🇲🇽 México","🇰🇷 Corea del Sur","18 Jun",True),
    ("🇨🇭 Suiza","🇧🇦 Bosnia","18 Jun",True),("🇨🇦 Canadá","🇶🇦 Qatar","18 Jun",True),
    ("🏴󠁧󠁢󠁸󠁣󠁴󠁿 Escocia","🇲🇦 Marruecos","19 Jun",True),("🇧🇷 Brasil","🇭🇹 Haití","19 Jun",True),
    ("🇺🇸 USA","🇦🇺 Australia","19 Jun",True),("🇹🇷 Turquía","🇵🇾 Paraguay","19 Jun",True),
    ("🇩🇪 Alemania","🇨🇮 Costa Marfil","20 Jun",True),("🇪🇨 Ecuador","🇨🇼 Curazao","20 Jun",True),
    ("🇳🇱 Países Bajos","🇸🇪 Suecia","20 Jun",True),("🇯🇵 Japón","🇹🇳 Túnez","20 Jun",True),
    ("🇧🇪 Bélgica","🇮🇷 Irán","21 Jun",True),("🇪🇬 Egipto","🇳🇿 Nueva Zelanda","21 Jun",True),
    ("🇪🇸 España","🇸🇦 Arabia Saudita","21 Jun",True),("🇺🇾 Uruguay","🇨🇻 Cabo Verde","21 Jun",True),
    ("🇫🇷 Francia","🇮🇶 Irak","22 Jun",True),("🇳🇴 Noruega","🇸🇳 Senegal","22 Jun",True),
    ("🇦🇷 Argentina","🇦🇹 Austria","22 Jun",True),("🇯🇴 Jordania","🇩🇿 Argelia","22 Jun",True),
    ("🇵🇹 Portugal","🇺🇿 Uzbekistán","23 Jun",True),("🇨🇴 Colombia","🇨🇩 Congo RD","23 Jun",True),
    ("🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra","🇬🇭 Ghana","23 Jun",True),("🇵🇦 Panamá","🇭🇷 Croacia","23 Jun",True),
  ],
  "Jornada 3": [
    ("🇨🇿 Chequia","🇲🇽 México","24 Jun",True),("🇿🇦 Sudáfrica","🇰🇷 Corea del Sur","24 Jun",True),
    ("🇨🇭 Suiza","🇨🇦 Canadá","24 Jun",True),("🇧🇦 Bosnia","🇶🇦 Qatar","24 Jun",True),
    ("🏴󠁧󠁢󠁸󠁣󠁴󠁿 Escocia","🇧🇷 Brasil","24 Jun",True),("🇲🇦 Marruecos","🇭🇹 Haití","24 Jun",True),
    ("🇹🇷 Turquía","🇺🇸 USA","25 Jun",True),("🇵🇾 Paraguay","🇦🇺 Australia","25 Jun",True),
    ("🇨🇼 Curazao","🇨🇮 Costa Marfil","25 Jun",True),("🇪🇨 Ecuador","🇩🇪 Alemania","25 Jun",True),
    ("🇯🇵 Japón","🇸🇪 Suecia","25 Jun",True),("🇳🇱 Países Bajos","🇹🇳 Túnez","25 Jun",True),
    ("🇧🇪 Bélgica","🇳🇿 Nueva Zelanda","26 Jun",True),("🇪🇬 Egipto","🇮🇷 Irán","26 Jun",True),
    ("🇨🇻 Cabo Verde","🇸🇦 Arabia Saudita","26 Jun",True),("🇪🇸 España","🇺🇾 Uruguay","26 Jun",True),
    ("🇫🇷 Francia","🇳🇴 Noruega","26 Jun",True),("🇸🇳 Senegal","🇮🇶 Irak","26 Jun",True),
    ("🇦🇷 Argentina","🇯🇴 Jordania","27 Jun",True),("🇩🇿 Argelia","🇦🇹 Austria","27 Jun",True),
    ("🇨🇴 Colombia","🇵🇹 Portugal","27 Jun",True),("🇨🇩 Congo RD","🇺🇿 Uzbekistán","27 Jun",True),
    ("🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra","🇵🇦 Panamá","27 Jun",True),("🇭🇷 Croacia","🇬🇭 Ghana","27 Jun",True),
  ],
  "Ronda de 32": [
    ("🇨🇦 Canadá","🇿🇦 Sudáfrica","28 Jun",False),("🇧🇷 Brasil","🇯🇵 Japón","29 Jun",False),
    ("🇩🇪 Alemania","🇵🇾 Paraguay","29 Jun",False),("🇳🇱 Países Bajos","🇲🇦 Marruecos","29 Jun",False),
    ("🇳🇴 Noruega","🇨🇮 Costa Marfil","30 Jun",False),("🇫🇷 Francia","🇸🇪 Suecia","30 Jun",False),
    ("🇲🇽 México","🇪🇨 Ecuador","30 Jun",False),("🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra","🇨🇩 Congo RD","1 Jul",False),
    ("🇧🇪 Bélgica","🇸🇳 Senegal","1 Jul",False),("🇺🇸 USA","🇧🇦 Bosnia","1 Jul",False),
    ("🇪🇸 España","🇦🇹 Austria","2 Jul",False),("🇵🇹 Portugal","🇭🇷 Croacia","2 Jul",False),
    ("🇨🇭 Suiza","🇩🇿 Argelia","2 Jul",False),("🇪🇬 Egipto","🇦🇺 Australia","3 Jul",False),
    ("🇦🇷 Argentina","🇨🇻 Cabo Verde","3 Jul",False),("🇨🇴 Colombia","🇬🇭 Ghana","3 Jul",False),
  ],
  "Ronda de 16": [
    ("🇲🇦 Marruecos","🇨🇦 Canadá","4 Jul · 1pm ET",False),
    ("🇫🇷 Francia","🇵🇾 Paraguay","4 Jul · 5pm ET",False),
    ("🇧🇷 Brasil","🇳🇴 Noruega","5 Jul · 4pm ET",False),
    ("🇲🇽 México","🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra","5 Jul · 8pm ET",False),
    ("🇵🇹 Portugal","🇪🇸 España","6 Jul · 3pm ET",False),
    ("🇺🇸 USA","🇧🇪 Bélgica","6 Jul · 8pm ET",False),
    ("🇦🇷 Argentina","🇪🇬 Egipto","7 Jul · 12pm ET",False),
    ("🇨🇭 Suiza","🇨🇴 Colombia","7 Jul · 4pm ET",False),
  ],
}

KNOWN_RESULTS = {
  "Jornada 1":   ["🇲🇽 México","🇰🇷 Corea del Sur","Empate","Empate","Empate","🏴󠁧󠁢󠁸󠁣󠁴󠁿 Escocia","🇺🇸 USA","🇦🇺 Australia","🇩🇪 Alemania","🇨🇮 Costa Marfil","Empate","🇸🇪 Suecia","Empate","Empate","Empate","Empate","🇫🇷 Francia","🇳🇴 Noruega","🇦🇷 Argentina","🇦🇹 Austria","Empate","🇨🇴 Colombia","🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra","🇬🇭 Ghana"],
  "Jornada 2":   ["Empate","🇲🇽 México","🇨🇭 Suiza","🇨🇦 Canadá","🇲🇦 Marruecos","🇧🇷 Brasil","🇺🇸 USA","🇵🇾 Paraguay","🇩🇪 Alemania","Empate","🇳🇱 Países Bajos","🇯🇵 Japón","Empate","🇪🇬 Egipto","🇪🇸 España","🇺🇾 Uruguay","🇫🇷 Francia","🇳🇴 Noruega","🇦🇷 Argentina","🇯🇴 Jordania","🇵🇹 Portugal","🇨🇴 Colombia","Empate","🇭🇷 Croacia"],
  "Jornada 3":   ["🇲🇽 México","🇰🇷 Corea del Sur","🇨🇭 Suiza","🇧🇦 Bosnia","🇧🇷 Brasil","🇲🇦 Marruecos","🇹🇷 Turquía","Empate","🇨🇮 Costa Marfil","🇪🇨 Ecuador","Empate","🇳🇱 Países Bajos","🇧🇪 Bélgica","Empate","Empate","🇪🇸 España","🇫🇷 Francia","🇸🇳 Senegal","🇦🇷 Argentina","Empate","Empate","🇨🇩 Congo RD","🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra","🇭🇷 Croacia"],
  "Ronda de 32": ["🇨🇦 Canadá","🇧🇷 Brasil","🇵🇾 Paraguay","🇲🇦 Marruecos","🇳🇴 Noruega","🇫🇷 Francia","🇲🇽 México","🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra","🇧🇪 Bélgica","🇺🇸 USA","🇪🇸 España","🇵🇹 Portugal","🇨🇭 Suiza","🇪🇬 Egipto","🇦🇷 Argentina","🇨🇴 Colombia"],
  "Ronda de 16": ["🇲🇦 Marruecos",None,None,None,None,None,None,None],
}

ALL_MATCHES = [(stage, m) for stage, matches in MATCHES_DEF.items() for m in matches]
TOTAL = len(ALL_MATCHES)

def get_pts(stage):
    if "Jornada" in stage: return 2
    if "32" in stage: return 3
    return 5

def get_result(stage, sidx):
    key = f"{stage}_{sidx}"
    if key in st.session_state.result_overrides:
        return st.session_state.result_overrides[key]
    known = KNOWN_RESULTS.get(stage, [])
    return known[sidx] if sidx < len(known) else None

# ── Load from GitHub once per session ─────────────────────────────────
if "data_loaded" not in st.session_state:
    with st.spinner("Cargando datos..."):
        d = gh_load()
    st.session_state.all_users        = d.get("users", {})
    st.session_state.result_overrides = d.get("results", {})
    st.session_state._gh_sha          = d.get("_sha", "")
    st.session_state.data_loaded      = True

if "admin_unlocked" not in st.session_state: st.session_state.admin_unlocked = False
if "user_name"      not in st.session_state: st.session_state.user_name      = None
if "picks"          not in st.session_state: st.session_state.picks          = [None]*TOTAL

def recalc_all():
    sl = {}
    for i,(stage,m) in enumerate(ALL_MATCHES): sl.setdefault(stage,[]).append(i)
    for uid,u in st.session_state.all_users.items():
        pts=0; upicks=u.get("picks",[])
        for i,(stage,m) in enumerate(ALL_MATCHES):
            sidx=sl[stage].index(i); result=get_result(stage,sidx)
            pick=upicks[i] if i<len(upicks) else None
            if result and pick and pick==result: pts+=get_pts(stage)
        st.session_state.all_users[uid]["points"]=pts

def save_my_picks():
    uid=st.session_state.user_name
    if not uid: return
    p=list(st.session_state.picks)
    if len(p)<TOTAL: p+=[None]*(TOTAL-len(p))
    if uid not in st.session_state.all_users:
        st.session_state.all_users[uid]={"picks":[None]*TOTAL,"points":0,"submitted":False}
    st.session_state.all_users[uid]["picks"]=p
    st.session_state.all_users[uid]["submitted"]=True
    recalc_all(); gh_save()

def save_user_picks(uid, new_picks):
    p=list(new_picks)
    if len(p)<TOTAL: p+=[None]*(TOTAL-len(p))
    if uid not in st.session_state.all_users:
        st.session_state.all_users[uid]={"picks":[None]*TOTAL,"points":0,"submitted":False}
    st.session_state.all_users[uid]["picks"]=p
    recalc_all(); gh_save()

def user_submitted():
    return st.session_state.all_users.get(st.session_state.user_name,{}).get("submitted",False)

# ══ LOGIN PAGE ══════════════════════════════════════════════════════════
if not st.session_state.user_name:
    st.markdown('<p class="big-title">⚽ QUINIELA<br>MUNDIAL 2026</p>', unsafe_allow_html=True)
    remaining=time_remaining()
    if remaining:
        st.markdown(f'<p class="countdown">⏳ Cierra en: {remaining}</p>', unsafe_allow_html=True)
        st.caption("📅 Deadline: Domingo 5 Jul · 9pm Costa Rica")
    else:
        st.markdown('<div class="locked-banner">🔒 La quiniela está cerrada</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Live leaderboard on landing
    recalc_all()
    users_lb=sorted(st.session_state.all_users.items(),key=lambda x:x[1].get("points",0),reverse=True)
    if users_lb:
        medals={0:"🥇",1:"🥈",2:"🥉"}
        st.markdown("### 📊 Tabla en vivo")
        rows_l=[]
        for rank,(uid,u) in enumerate(users_lb):
            rows_l.append({"#":medals.get(rank,rank+1),"Nombre":uid,
                           "Enviado":"✅" if u.get("submitted") else "⏳",
                           "Puntos 🏆":u.get("points",0)})
        st.dataframe(pd.DataFrame(rows_l),use_container_width=True,hide_index=True)
        st.markdown("---")

    name=st.text_input("¿Cuál es tu nombre?",max_chars=30,placeholder="Ej: Mamá, Juan, Tito...")
    if st.button("Entrar 🚀",use_container_width=True,type="primary"):
        if not name.strip(): st.error("Escribe tu nombre")
        else:
            n=name.strip(); st.session_state.user_name=n
            if n in st.session_state.all_users:
                p=st.session_state.all_users[n].get("picks",[None]*TOTAL)
                if len(p)<TOTAL: p+=[None]*(TOTAL-len(p))
                st.session_state.picks=p
            else:
                st.session_state.all_users[n]={"picks":[None]*TOTAL,"points":0,"submitted":False}
                st.session_state.picks=[None]*TOTAL
                gh_save()
            st.rerun()
    st.stop()

# ══ MAIN APP ════════════════════════════════════════════════════════════
st.markdown('<p class="big-title">⚽ QUINIELA 2026</p>', unsafe_allow_html=True)
c1,c2=st.columns([4,1])
with c1:
    rem=time_remaining()
    if rem: st.markdown(f'<span style="color:#F5C518;font-weight:700">⏳ {rem}</span>',unsafe_allow_html=True)
    else: st.caption("🔒 Cerrada")
with c2:
    if st.button("Salir"):
        st.session_state.user_name=None; st.session_state.picks=[None]*TOTAL; st.rerun()

st.caption(f"Jugando como: **{st.session_state.user_name}**")

# Live leaderboard always visible
recalc_all()
users_main=sorted(st.session_state.all_users.items(),key=lambda x:x[1].get("points",0),reverse=True)
if users_main:
    medals={0:"🥇",1:"🥈",2:"🥉"}
    st.markdown("### 📊 Tabla en vivo")
    rows_m=[]
    for rank,(uid,u) in enumerate(users_main):
        rows_m.append({"#":medals.get(rank,rank+1),
                       "Nombre":f"⭐ {uid}" if uid==st.session_state.user_name else uid,
                       "Enviado":"✅" if u.get("submitted") else "⏳",
                       "Puntos 🏆":u.get("points",0)})
    st.dataframe(pd.DataFrame(rows_m),use_container_width=True,hide_index=True)
st.markdown("---")

locked=is_locked(); already_done=user_submitted()
tab_picks,tab_lb,tab_admin=st.tabs(["🎯 Mis Picks","📊 Tabla detallada","⚙️ Admin"])

# ══ TAB 1 — PICKS ══════════════════════════════════════════════════════
with tab_picks:
    if already_done:
        st.markdown('<div class="locked-banner">✅ Ya enviaste tu quiniela — ¡suerte!</div>',unsafe_allow_html=True)
    elif locked:
        st.markdown('<div class="locked-banner">🔒 El tiempo se acabó.</div>',unsafe_allow_html=True)
    else:
        st.markdown('<div class="open-banner">🟢 Selecciona todos tus picks y guárdalos. Una vez que guardes, no podrás cambiarlos.</div>',unsafe_allow_html=True)

    picks=list(st.session_state.picks); changed=False; sc={}
    can_edit=not locked and not already_done

    for stage,matches in MATCHES_DEF.items():
        is_group="Jornada" in stage; is_past=stage!="Ronda de 16"
        with st.expander(f"{'🔒' if is_past else '🟢'} {stage}",expanded=not is_past):
            for i,(stg,m) in enumerate(ALL_MATCHES):
                if stg!=stage: continue
                t1,t2,date,_=m
                sidx=sc.get(stage,0); sc[stage]=sidx+1
                pick=picks[i]; pts=get_pts(stage)
                if is_past:
                    actual=get_result(stage,sidx)
                    correct=(pick==actual) if actual else False
                    if already_done or locked:
                        icon="✅" if correct else("❌" if(pick and actual) else "📋")
                        st.markdown(f"**{icon} {t1} vs {t2}** · {date}"+(f" · Ganó: **{actual}**" if actual else ""))
                        if pick: st.caption(f"Tu pick: {pick}"+(f" · **+{pts}pts** 🎉" if correct else ""))
                        else: st.caption("_Sin pick_")
                    else:
                        if can_edit:
                            opts=["— Sin pick —",t1,"Empate",t2] if is_group else ["— Sin pick —",t1,t2]
                            ci=0
                            if pick==t1: ci=1
                            elif pick=="Empate" and is_group: ci=2
                            elif pick==t2: ci=3 if is_group else 2
                            st.markdown(f"**{t1} vs {t2}** · {date}")
                            sel=st.radio(f"p{i}",opts,index=ci,key=f"pick_{i}",horizontal=True,label_visibility="collapsed")
                            nv=None if sel=="— Sin pick —" else sel
                            if nv!=picks[i]: picks[i]=nv; changed=True
                        else:
                            st.markdown(f"**{t1} vs {t2}** · {date}")
                            st.caption(f"Tu pick: {pick or '_sin pick_'}")
                else:
                    actual=get_result(stage,sidx)
                    if actual and(already_done or locked):
                        correct=(pick==actual); icon="✅" if correct else("❌" if pick else "⏹️")
                        st.markdown(f"**{icon} {t1} vs {t2}** · {date} · Ganó: **{actual}**")
                        if pick: st.caption(f"Tu pick: {pick}"+(f" · **+{pts}pts** 🎉" if correct else ""))
                    elif can_edit:
                        opts=[t1,t2]; cur=picks[i] if picks[i] in opts else None
                        st.markdown(f"**🕐 {t1} vs {t2}** · {date}")
                        sel=st.radio(f"p{i}",opts,index=opts.index(cur) if cur else None,key=f"pick_{i}",horizontal=True,label_visibility="collapsed")
                        if sel!=picks[i]: picks[i]=sel; changed=True
                    else:
                        st.markdown(f"**🕐 {t1} vs {t2}** · {date}")
                        st.caption(f"Tu pick: {picks[i] or '_sin pick_'}")
                st.divider()

    if changed: st.session_state.picks=picks
    if can_edit:
        total_p=sum(1 for p in picks if p)
        st.progress(total_p/TOTAL,text=f"{total_p}/{TOTAL} picks completados")
        st.warning("⚠️ Una vez que guardes, **no podrás cambiar tus picks**.")
        if st.button("🚀 GUARDAR Y ENVIAR MI QUINIELA (definitivo)",type="primary",use_container_width=True):
            save_my_picks(); st.success("✅ ¡Quiniela enviada!"); st.balloons(); st.rerun()

# ══ TAB 2 — LEADERBOARD DETALLADO ══════════════════════════════════════
with tab_lb:
    recalc_all()
    st.subheader("📊 Tabla Detallada")
    users=sorted(st.session_state.all_users.items(),key=lambda x:x[1].get("points",0),reverse=True)
    if not users: st.info("Nadie registrado aún.")
    else:
        medals={0:"🥇",1:"🥈",2:"🥉"}
        sl={}
        for i,(stage,m) in enumerate(ALL_MATCHES): sl.setdefault(stage,[]).append(i)
        rows=[]
        for rank,(uid,u) in enumerate(users):
            upicks=u.get("picks",[])
            def sp(stg):
                t=0
                for i,(s,m) in enumerate(ALL_MATCHES):
                    if s!=stg: continue
                    sidx=sl[stg].index(i); r=get_result(stg,sidx); p=upicks[i] if i<len(upicks) else None
                    if r and p and p==r: t+=get_pts(stg)
                return t
            rows.append({"#":medals.get(rank,rank+1),
                         "Nombre":f"⭐ {uid}" if uid==st.session_state.user_name else uid,
                         "Enviado":"✅" if u.get("submitted") else "⏳",
                         "G1":sp("Jornada 1"),"G2":sp("Jornada 2"),"G3":sp("Jornada 3"),
                         "R32":sp("Ronda de 32"),"R16":sp("Ronda de 16"),"Total 🏆":u.get("points",0)})
        st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)

# ══ TAB 3 — ADMIN ══════════════════════════════════════════════════════
with tab_admin:
    if not st.session_state.admin_unlocked:
        st.subheader("🔐 Acceso Admin")
        pw=st.text_input("Contraseña",type="password",key="admin_pw")
        if st.button("Entrar",key="admin_login"):
            if pw==ADMIN_PASSWORD: st.session_state.admin_unlocked=True; st.rerun()
            else: st.error("Contraseña incorrecta")
    else:
        st.subheader("⚙️ Panel de Admin")
        adm1,adm2,adm3=st.tabs(["🏆 Poner resultados","👤 Picks de usuario","➕ Usuarios"])

        with adm1:
            st.caption("Selecciona quién ganó. Los puntos se recalculan y guardan en GitHub.")
            for stage,matches in MATCHES_DEF.items():
                with st.expander(f"📋 {stage}",expanded=(stage in ["Ronda de 16","Ronda de 32"])):
                    is_group="Jornada" in stage; new_res={}
                    for sidx,(t1,t2,date,_) in enumerate(matches):
                        cur=get_result(stage,sidx)
                        st.markdown(f"**{t1} vs {t2}** · {date}")
                        if is_group:
                            opts=["⏳ Pendiente",t1,"Empate",t2]
                            ci=1 if cur==t1 else(2 if cur=="Empate" else(3 if cur==t2 else 0))
                        else:
                            opts=["⏳ Pendiente",t1,t2]
                            ci=1 if cur==t1 else(2 if cur==t2 else 0)
                        sel=st.radio(f"res_{stage}_{sidx}",opts,index=ci,key=f"admin_res_{stage}_{sidx}",horizontal=True,label_visibility="collapsed")
                        new_res[f"{stage}_{sidx}"]=None if sel=="⏳ Pendiente" else sel
                        st.divider()
                    if st.button(f"💾 Guardar {stage}",key=f"save_{stage}",type="primary",use_container_width=True):
                        st.session_state.result_overrides.update(new_res)
                        recalc_all(); gh_save()
                        st.success(f"✅ {stage} guardado en GitHub.")

        with adm2:
            user_list=list(st.session_state.all_users.keys())
            if not user_list: st.info("No hay usuarios aún.")
            else:
                sel_user=st.selectbox("Usuario",user_list,key="admin_user_sel")
                u_picks=list(st.session_state.all_users[sel_user].get("picks",[None]*TOTAL))
                if len(u_picks)<TOTAL: u_picks+=[None]*(TOTAL-len(u_picks))
                edited=list(u_picks); sc2={}
                for stage,matches in MATCHES_DEF.items():
                    with st.expander(f"📋 {stage}"):
                        is_group="Jornada" in stage
                        for i,(stg,m) in enumerate(ALL_MATCHES):
                            if stg!=stage: continue
                            t1,t2,date,_=m
                            sidx=sc2.get(stage,0); sc2[stage]=sidx+1
                            result=get_result(stage,sidx); pts=get_pts(stage)
                            st.markdown(f"**{t1} vs {t2}** · {date}"+(f" · Ganó: **{result}**" if result else ""))
                            if is_group:
                                opts=["— Sin pick —",t1,"Empate",t2]
                                ci=1 if edited[i]==t1 else(2 if edited[i]=="Empate" else(3 if edited[i]==t2 else 0))
                            else:
                                opts=["— Sin pick —",t1,t2]
                                ci=1 if edited[i]==t1 else(2 if edited[i]==t2 else 0)
                            sel=st.radio(f"up{i}",opts,index=ci,key=f"adm_up_{sel_user}_{i}",horizontal=True,label_visibility="collapsed")
                            edited[i]=None if sel=="— Sin pick —" else sel
                            if result and edited[i]==result: st.caption(f"✅ Correcto · +{pts}pts")
                            elif edited[i]: st.caption("❌ Incorrecto")
                            st.divider()
                col1,col2=st.columns(2)
                with col1:
                    if st.button(f"💾 Guardar picks de {sel_user}",type="primary",use_container_width=True):
                        save_user_picks(sel_user,edited)
                        st.success(f"✅ {sel_user}: {st.session_state.all_users[sel_user]['points']} pts")
                with col2:
                    if st.button("🔓 Marcar como enviado",use_container_width=True):
                        st.session_state.all_users[sel_user]["submitted"]=True
                        gh_save(); st.success("✅ Marcado como enviado.")

        with adm3:
            st.subheader("➕ Agregar usuario")
            new_name=st.text_input("Nombre",max_chars=30,key="admin_new_user")
            if st.button("Crear",key="admin_create",type="primary"):
                n=new_name.strip()
                if not n: st.error("Escribe un nombre")
                elif n in st.session_state.all_users: st.warning(f"{n} ya existe.")
                else:
                    st.session_state.all_users[n]={"picks":[None]*TOTAL,"points":0,"submitted":False}
                    gh_save(); st.success(f"✅ Usuario **{n}** creado y guardado en GitHub."); st.rerun()
            st.markdown("---")
            st.subheader("👥 Todos los usuarios")
            users_s=sorted(st.session_state.all_users.items(),key=lambda x:x[1].get("points",0),reverse=True)
            for rank,(uid,u) in enumerate(users_s):
                picks_done=sum(1 for p in u.get("picks",[]) if p)
                submitted="✅" if u.get("submitted") else "⏳"
                col_a,col_b=st.columns([5,1])
                with col_a:
                    st.markdown(f"**{rank+1}. {uid}** · {submitted} · {picks_done}/{TOTAL} picks · **{u.get('points',0)} pts**")
                with col_b:
                    if st.button("🗑️",key=f"del_{uid}",help=f"Eliminar {uid}"):
                        del st.session_state.all_users[uid]
                        gh_save(); st.rerun()

        st.markdown("---")
        if st.button("🔒 Cerrar sesión admin"):
            st.session_state.admin_unlocked=False; st.rerun()
