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

try:
    df = load_data()
except Exception as e:
    st.error(f"CSV 파일을 불러오지 못했습니다.\n{e}")
    st.stop()

# =========================
# 컬럼 확인
# =========================

required_columns = [
    "Name",
    "Role",
    "WinRate",
    "PickRate",
    "Skills",
    "Description"
]

missing = [col for col in required_columns if col not in df.columns]

if missing:
    st.error(f"CSV에 없는 컬럼: {missing}")
    st.stop()

# =========================
# 헤더
# =========================

st.title("🎯 VALORANT Agent Dashboard")
st.markdown("### 원하는 요원을 선택해 정보를 확인해보세요!")

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
# 역할 표시
# =========================

role = str(agent["Role"])

if role == "타격대":
    role_color = "⚔️"
elif role == "감시자":
    role_color = "🛡️"
elif role == "척후대":
    role_color = "🔎"
elif role == "전략가":
    role_color = "🌫️"
else:
    role_color = "🎮"

# =========================
# 기본 정보
# =========================

col1, col2 = st.columns([1, 2])

with col1:
    st.info(f"{role_color} {role}")

with col2:
    st.subheader(f"👤 {agent['Name']}")

st.write("### 📖 요원 소개")
st.write(agent["Description"])

st.divider()

# =========================
# 통계
# =========================

st.subheader("📊 요원 통계")

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

# 쉼표 기준 분리
skill_list = [s.strip() for s in skills.split(",")]

for skill in skill_list:

    st.markdown(
        f"""
<div style="
background-color:#1e293b;
padding:12px;
border-radius:10px;
margin-bottom:10px;
border-left:5px solid #ff4655;
">
🎯 {skill}
</div>
""",
        unsafe_allow_html=True
    )

st.divider()

# =========================
# TOP 5 승률
# =========================

st.subheader("🏆 승률 TOP 5")

top_win = df.sort_values(
    "WinRate",
    ascending=False
).head(5)

st.dataframe(
    top_win[
        ["Name", "WinRate"]
    ],
    use_container_width=True
)

# =========================
# TOP 5 픽률
# =========================

st.subheader("🔥 픽률 TOP 5")

top_pick = df.sort_values(
    "PickRate",
    ascending=False
).head(5)

st.dataframe(
    top_pick[
        ["Name", "PickRate"]
    ],
    use_container_width=True
)

# =========================
# 전체 순위
# =========================

st.subheader("📈 전체 요원 순위")

sort_option = st.radio(
    "정렬 기준",
    ["승률", "픽률"],
    horizontal=True
)

if sort_option == "승률":

    ranking = df.sort_values(
        "WinRate",
        ascending=False
    )

else:

    ranking = df.sort_values(
        "PickRate",
        ascending=False
    )

st.dataframe(
    ranking[
        [
            "Name",
            "Role",
            "WinRate",
            "PickRate"
        ]
    ],
    use_container_width=True
)
