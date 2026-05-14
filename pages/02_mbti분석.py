# app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# --------------------------------
# 페이지 설정
# --------------------------------
st.set_page_config(
    page_title="MBTI World Analyzer",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 MBTI 국가 분석기")

st.markdown("""
### 기능
- MBTI 유형 선택
- 해당 MBTI 비율이 높은 국가 확인
- 국가 선택
- 국가별 전체 MBTI 분포 그래프 확인
- 그래프에서 MBTI 클릭 시:
    → 해당 MBTI 비율이 높은 국가 자동 정렬
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
# 세션 상태 초기화
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
# MBTI 비율 높은 국가 정렬
# --------------------------------
ranked_df = df.sort_values(
    by=selected_mbti,
    ascending=False
).reset_index(drop=True)

# --------------------------------
# TOP 10 표시
# --------------------------------
st.subheader(f"🌎 {selected_mbti} 비율 TOP 국가")

top10 = ranked_df[["Country", selected_mbti]].head(10)

st.dataframe(
    top10.rename(columns={
        selected_mbti: "비율"
    }),
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
# 국가 데이터
# --------------------------------
country_data = df[df["Country"] == selected_country].iloc[0]

chart_df = pd.DataFrame({
    "MBTI": mbti_types,
    "Ratio": [country_data[m] for m in mbti_types]
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
        idx = min(i + 2, len(blue_scale) - 1)
        colors.append(blue_scale[idx])

# --------------------------------
# 그래프 생성
# --------------------------------
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=chart_df["MBTI"],
        y=chart_df["Ratio"],
        marker_color=colors,
        text=[f"{v:.2%}" for v in chart_df["Ratio"]],
        textposition="outside",
        customdata=chart_df["MBTI"],
        hovertemplate=
        "<b>%{x}</b><br>" +
        "비율: %{y:.2%}<extra></extra>"
    )
)

fig.update_layout(
    title=f"{selected_country} MBTI 분포",
    xaxis_title="MBTI",
    yaxis_title="비율",
    template="plotly_white",
    height=650,
    hovermode="x unified"
)

fig.update_yaxes(tickformat=".0%")

# --------------------------------
# Plotly 클릭 이벤트
# streamlit-plotly-events 필요
# --------------------------------
from streamlit_plotly_events import plotly_events

selected_points = plotly_events(
    fig,
    click_event=True,
    hover_event=False,
    select_event=False,
    override_height=650,
    key="mbti_chart"
)

# --------------------------------
# 클릭 시 MBTI 변경
# --------------------------------
if selected_points:
    clicked_mbti = selected_points[0]["x"]

    if clicked_mbti != st.session_state.selected_mbti:
        st.session_state.selected_mbti = clicked_mbti
        st.rerun()

# --------------------------------
# 최고 MBTI
# --------------------------------
top_mbti = chart_df.iloc[0]

st.success(
    f"""
🏆 {selected_country}에서 가장 높은 MBTI는
{top_mbti['MBTI']} ({top_mbti['Ratio']:.2%}) 입니다.
"""
)

# --------------------------------
# 데이터 테이블
# --------------------------------
with st.expander("📄 전체 데이터 보기"):
    st.dataframe(
        chart_df,
        use_container_width=True
    )
