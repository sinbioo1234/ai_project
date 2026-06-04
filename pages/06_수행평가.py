import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================

# 페이지 설정

# ==============================

st.set_page_config(
page_title="VALORANT Agent Dashboard",
page_icon="🎯",
layout="wide"
)

# ==============================

# CSS

# ==============================

st.markdown("""

<style>

.main {
    background-color: #0f172a;
}

.agent-card {
    padding: 15px;
    border-radius: 15px;
    background: linear-gradient(
        135deg,
        #1e293b,
        #334155
    );
    margin-bottom: 10px;
}

.skill-card {
    background-color: #111827;
    padding: 12px;
    border-radius: 12px;
    border-left: 5px solid #ff4655;
    margin-bottom: 8px;
}

</style>

""", unsafe_allow_html=True)

# ==============================

# 데이터 로드

# ==============================

@st.cache_data
def load_data():
df = pd.read_csv("valorant_agents_data.csv")

```
df["WinRate_num"] = (
    df["WinRate"]
    .str.replace("%","", regex=False)
    .astype(float)
)

df["PickRate_num"] = (
    df["PickRate"]
    .str.replace("%","", regex=False)
    .astype(float)
)

return df
```

df = load_data()

# ==============================

# 제목

# ==============================

st.title("🎯 VALORANT Agent Dashboard")
st.markdown(
"### 🔥 발로란트 요원 통계 및 정보 분석"
)

st.divider()

# ==============================

# 요원 선택

# ==============================

agent_name = st.selectbox(
"🔍 요원을 선택하세요",
sorted(df["Name"])
)

agent = df[df["Name"] == agent_name].iloc[0]

# ==============================

# 기본 정보

# ==============================

left, right = st.columns([1,2])

with left:

```
role = agent["Role"]

if "타격대" in role:
    st.success(f"⚔️ {role}")

elif "감시자" in role:
    st.info(f"🛡️ {role}")

elif "척후대" in role:
    st.warning(f"🔎 {role}")

else:
    st.error(f"🌫️ {role}")
```

with right:

```
st.markdown(
    f"""
    <div class="agent-card">
    <h2>👤 {agent['Name']}</h2>
    <p>{agent['Description']}</p>
    </div>
    """,
    unsafe_allow_html=True
)
```

# ==============================

# 통계

# ==============================

st.subheader("📊 요원 통계")

c1, c2 = st.columns(2)

with c1:
st.metric(
"🏆 승률",
agent["WinRate"]
)

with c2:
st.metric(
"🔥 픽률",
agent["PickRate"]
)

# ==============================

# 스킬

# ==============================

st.subheader("✨ 보유 스킬")

skills = [
skill.strip()
for skill in agent["Skills"].split(",")
]

for skill in skills:

```
st.markdown(
    f"""
    <div class="skill-card">
    🎯 {skill}
    </div>
    """,
    unsafe_allow_html=True
)
```

st.divider()

# ==============================

# TOP 5 승률

# ==============================

st.subheader("🏆 승률 TOP 5")

top_win = (
df
.sort_values(
"WinRate_num",
ascending=False
)
.head(5)
)

st.dataframe(
top_win[
["Name","WinRate"]
],
use_container_width=True
)

# ==============================

# TOP 5 픽률

# ==============================

st.subheader("🔥 픽률 TOP 5")

top_pick = (
df
.sort_values(
"PickRate_num",
ascending=False
)
.head(5)
)

st.dataframe(
top_pick[
["Name","PickRate"]
],
use_container_width=True
)

# ==============================

# 그래프

# ==============================

st.subheader("📈 전체 픽률 순위")

fig_pick = px.bar(
df.sort_values(
"PickRate_num",
ascending=False
),
x="Name",
y="PickRate_num"
)

st.plotly_chart(
fig_pick,
use_container_width=True
)

st.subheader("📊 전체 승률 순위")

fig_win = px.bar(
df.sort_values(
"WinRate_num",
ascending=False
),
x="Name",
y="WinRate_num"
)

st.plotly_chart(
fig_win,
use_container_width=True
)

# ==============================

# 전체 순위표

# ==============================

st.subheader("🏅 전체 요원 데이터")

st.dataframe(
df[
[
"Name",
"Role",
"WinRate",
"PickRate"
]
],
use_container_width=True
)

# ==============================

# 메타 분석

# ==============================

best_win = df.loc[
df["WinRate_num"].idxmax()
]

best_pick = df.loc[
df["PickRate_num"].idxmax()
]

st.success(
f"🏆 최고 승률 요원: {best_win['Name']} ({best_win['WinRate']})"
)

st.info(
f"🔥 최고 픽률 요원: {best_pick['Name']} ({best_pick['PickRate']})"
)

