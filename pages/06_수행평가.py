import streamlit as st
import pandas as pd

# =========================

# 페이지 설정

# =========================

st.set_page_config(
page_title="VALORANT Agent Dashboard",
page_icon="🎯",
layout="wide"
)

# =========================

# 데이터 로드

# =========================

@st.cache_data
def load_data():
return pd.read_csv("valorant_agents_data.csv")

df = load_data()

# =========================

# 헤더

# =========================

st.markdown(
"""
# 🎯 VALORANT Agent Dashboard

```
원하는 요원을 선택해 통계를 확인해보세요!
"""
```

)

st.divider()

# =========================

# 요원 선택

# =========================

agent_name = st.selectbox(
"🔍 요원 선택",
sorted(df["Name"].unique())
)

agent = df[df["Name"] == agent_name].iloc[0]

# =========================

# 기본 정보

# =========================

left, right = st.columns([1, 2])

with left:

```
role = str(agent["Role"])

if "타격대" in role:
    st.success("⚔️ 타격대")
elif "감시자" in role:
    st.info("🛡️ 감시자")
elif "척후대" in role:
    st.warning("🔎 척후대")
else:
    st.error("🌫️ 전략가")
```

with right:

```
st.subheader(f"👤 {agent['Name']}")

st.write("### 📖 소개")
st.write(agent["Description"])
```

st.divider()

# =========================

# 통계

# =========================

st.subheader("📊 통계")

c1, c2 = st.columns(2)

with c1:
st.metric(
"🏆 승률",
f"{agent['WinRate']}%"
)

with c2:
st.metric(
"🔥 픽률",
f"{agent['PickRate']}%"
)

st.divider()

# =========================

# 스킬

# =========================

st.subheader("✨ 스킬")

skills = str(agent["Skills"])

for skill in skills.split(","):
st.markdown(
f""" <div style="
         background-color:#1E293B;
         padding:10px;
         border-radius:10px;
         margin-bottom:10px;
     ">
🎯 {skill.strip()} </div>
""",
unsafe_allow_html=True
)

st.divider()

# =========================

# 전체 순위

# =========================

st.subheader("🏅 전체 요원 순위")

sort_option = st.radio(
"정렬 기준",
["승률", "픽률"],
horizontal=True
)

if sort_option == "승률":
rank_df = df.sort_values(
"WinRate",
ascending=False
)
else:
rank_df = df.sort_values(
"PickRate",
ascending=False
)

st.dataframe(
rank_df[
["Name", "Role", "WinRate", "PickRate"]
],
use_container_width=True
)

