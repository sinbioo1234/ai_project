import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# 페이지 설정
# =========================

st.set_page_config(
    page_title="VALORANT Dashboard",
    page_icon="🎯",
    layout="wide"
)

# =========================
# CSS 스타일
# =========================

st.markdown("""
<style>

.agent-box{
    background: linear-gradient(
        135deg,
        #334155,
        #475569
    );
    color:white;
    padding:20px;
    border-radius:15px;
    margin-bottom:15px;
}

.skill-box{
    background-color:#1e293b;
    color:white;
    padding:12px;
    border-radius:10px;
    margin-bottom:8px;
    border-left:5px solid #ff4655;
}

</style>
""", unsafe_allow_html=True)

# =========================
# 데이터 불러오기
# =========================

@st.cache_data
def load_data():

    df = pd.read_csv("valorant_agents_data.csv")

    df["WinRate_num"] = (
        df["WinRate"]
        .astype(str)
        .str.replace("%", "", regex=False)
        .astype(float)
    )

    df["PickRate_num"] = (
        df["PickRate"]
        .astype(str)
        .str.replace("%", "", regex=False)
        .astype(float)
    )

    return df


df = load_data()

# =========================
# 제목
# =========================

st.title("🎯 VALORANT Agent Dashboard")
st.markdown("### 🔥 발로란트 요원 통계 및 정보 분석")

st.divider()

# =========================
# 요원 선택
# =========================

agent_name = st.selectbox(
    "🔍 요원을 선택하세요",
    sorted(df["Name"].unique())
)

agent = df[df["Name"] == agent_name].iloc[0]

# =========================
# 기본 정보
# =========================

col1, col2 = st.columns([1, 2])

with col1:

    role = str(agent["Role"])

    if role == "타격대":
        st.success("⚔️ 타격대")

    elif role == "감시자":
        st.info("🛡️ 감시자")

    elif role == "척후대":
        st.warning("🔎 척후대")

    else:
        st.error("🌫️ 전략가")

with col2:

    st.markdown(
        f"""
        <div class="agent-box">
            <h2>👤 {agent['Name']}</h2>
            <hr>
            <p style="font-size:18px;">
                {agent['Description']}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# 통계
# =========================

st.subheader("📊 요원 통계")

m1, m2 = st.columns(2)

with m1:
    st.metric(
        "🏆 승률",
        str(agent["WinRate"])
    )

with m2:
    st.metric(
        "🔥 픽률",
        str(agent["PickRate"])
    )

# =========================
# 스킬
# =========================

st.divider()

st.subheader("✨ 보유 스킬")

skills = str(agent["Skills"]).split(",")

for skill in skills:

    st.markdown(
        f"""
        <div class="skill-box">
            🎯 {skill.strip()}
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# TOP 5 승률
# =========================

st.divider()

st.subheader("🏆 승률 TOP 5")

top_win = (
    df.sort_values(
        "WinRate_num",
        ascending=False
    )
    .head(5)
)

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

top_pick = (
    df.sort_values(
        "PickRate_num",
        ascending=False
    )
    .head(5)
)

st.dataframe(
    top_pick[
        ["Name", "PickRate"]
    ],
    use_container_width=True
)

# =========================
# 픽률 그래프
# =========================

st.divider()

st.subheader("📈 픽률 순위")

fig_pick = px.bar(
    df.sort_values(
        "PickRate_num",
        ascending=False
    ),
    x="Name",
    y="PickRate_num",
    color="PickRate_num"
)

st.plotly_chart(
    fig_pick,
    use_container_width=True
)

# =========================
# 승률 그래프
# =========================

st.subheader("📊 승률 순위")

fig_win = px.bar(
    df.sort_values(
        "WinRate_num",
        ascending=False
    ),
    x="Name",
    y="WinRate_num",
    color="WinRate_num"
)

st.plotly_chart(
    fig_win,
    use_container_width=True
)

# =========================
# 전체 데이터
# =========================

st.divider()

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
