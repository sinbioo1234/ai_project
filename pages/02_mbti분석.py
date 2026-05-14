import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from streamlit_plotly_events import plotly_events

# --------------------------------
# 페이지 설정
# --------------------------------
st.set_page_config(
    page_title="MBTI World Analyzer",
    page_icon="🌍",
    layout="wide"
)

# --------------------------------
# 제목
# --------------------------------
st.title("🌍 MBTI 국가 분석기")

st.markdown("""
### 기능
- MBTI 유형 선택
- 해당 MBTI 비율이 높은 국가 확인
- 국가 선택
- 국가별 MBTI 분포 확인
- 그래프 막대 클릭 가능
- 클릭한 MBTI 기준으로 국가 자동 재정렬
""")

# --------------------------------
# 데이터 로드
# --------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("countriesMBTI_16types.csv")

df = load_data()

# --------------------------------
# MBTI 목록
# --------------------------------
mbti_types = [
    'INFJ', 'ISFJ', 'INTP', 'ISFP',
    'ENTP', 'INFP', 'ENTJ', 'ISTP',
    'INTJ', 'ESFP', 'ESTJ', 'ENFP',
    'ESTP', 'ISTJ', 'ENFJ', 'ESFJ'
]

# --------------------------------
# 세션 상태
# --------------------------------
if "selected_mbti" not in st.session_state:
    st.session_state.selected_mbti = "INFP"

# --------------------------------
# MBTI 선택
# --------------------------------
selected_mbti = st.selectbox(
    "🧠 MBTI 선택",
    mbti_types,
    index=mbti_types.index(st.session_state.selected_mbti)
)

st.session_state.selected_mbti = selected_mbti

# --------------------------------
# MBTI 기준 국가 정렬
# --------------------------------
ranked_df = df.sort_values(
    by=selected_mbti,
    ascending=False
).reset_index(drop=True)

# --------------------------------
# TOP 10 국가 표시
# --------------------------------
st.subheader(f"🌎 {selected_mbti} 비율 TOP 국가")

top10 = ranked_df[["Country", selected_mbti]].head(10)

top10_display = top10.copy()
top10_display[selected_mbti] = (
    top10_display[selected_mbti] * 100
).round(2).astype(str) + "%"

top10_display.columns = ["국가", "비율"]

st.dataframe(
    top10_display,
    use_container_width=True
)

# --------------------------------
# 국가 선택
# --------------------------------
selected_country = st.selectbox(
    "🏳️ 국가 선택",
    ranked_df["Country"].tolist()
)

# --------------------------------
# 국가 데이터 추출
# --------------------------------
country_data = df[
    df["Country"] == selected_country
].iloc[0]

chart_df = pd.DataFrame({
    "MBTI": mbti_types,
    "Ratio": [
        float(country_data[m])
        for m in mbti_types
    ]
})

# --------------------------------
# 정렬
# --------------------------------
chart_df = chart_df.sort_values(
    by="Ratio",
    ascending=False
).reset_index(drop=True)

# --------------------------------
# 색상 설정
# 1등 빨강
# 나머지 블루 그라데이션
# --------------------------------
blue_scale = px.colors.sequential.Blues

colors = []

for i in range(len(chart_df)):
    if i == 0:
        colors.append("#ff3b30")
    else:
        idx = min(i + 3, len(blue_scale) - 1)
        colors.append(blue_scale[idx])

# --------------------------------
# Plotly 그래프
# --------------------------------
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=chart_df["MBTI"].tolist(),
        y=chart_df["Ratio"].tolist(),
        marker_color=colors,
        text=[
            f"{v:.2%}"
            for v in chart_df["Ratio"]
        ],
        textposition="outside",
        customdata=chart_df["MBTI"],
        hovertemplate=
        "<b>%{x}</b><br>" +
        "비율: %{y:.2%}<extra></extra>"
    )
)

# --------------------------------
# 그래프 레이아웃
# --------------------------------
fig.update_layout(
    title=f"{selected_country} MBTI 분포",
    xaxis_title="MBTI",
    yaxis_title="비율",
    template="plotly_white",
    height=650,
    hovermode="x unified"
)

fig.update_yaxes(
    tickformat=".0%",
    rangemode="tozero"
)

fig.update_xaxes(
    categoryorder="array",
    categoryarray=chart_df["MBTI"].tolist()
)

# --------------------------------
# 클릭 이벤트
# --------------------------------
selected_points = plotly_events(
    fig,
    click_event=True,
    hover_event=False,
    select_event=False,
    override_height=650,
    key="mbti_chart"
)

# --------------------------------
# 클릭한 MBTI로 자동 변경
# --------------------------------
if selected_points:
    clicked_mbti = selected_points[0]["x"]

    if clicked_mbti != st.session_state.selected_mbti:
        st.session_state.selected_mbti = clicked_mbti
        st.rerun()

# --------------------------------
# 그래프 출력
# --------------------------------
st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------
# 최고 MBTI 표시
# --------------------------------
top_mbti = chart_df.iloc[0]

st.success(
    f"""
🏆 {selected_country}에서 가장 높은 MBTI는
{top_mbti['MBTI']} ({top_mbti['Ratio']:.2%}) 입니다.
"""
)

# --------------------------------
# 전체 데이터
# --------------------------------
with st.expander("📄 전체 데이터 보기"):
    display_df = chart_df.copy()

    display_df["Ratio"] = (
        display_df["Ratio"] * 100
    ).round(2).astype(str) + "%"

    st.dataframe(
        display_df,
        use_container_width=True
    )
)
