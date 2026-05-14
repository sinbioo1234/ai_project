# app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="Country MBTI Analyzer",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 국가별 MBTI 비율 분석")
st.markdown("국가를 선택하면 MBTI 유형 비율을 인터랙티브하게 확인할 수 있습니다.")

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# -----------------------------
# 국가 선택
# -----------------------------
countries = sorted(df["Country"].unique())

selected_country = st.selectbox(
    "국가 선택",
    countries
)

# -----------------------------
# 선택 국가 데이터
# -----------------------------
country_data = df[df["Country"] == selected_country].iloc[0]

mbti_cols = [
    'INFJ', 'ISFJ', 'INTP', 'ISFP',
    'ENTP', 'INFP', 'ENTJ', 'ISTP',
    'INTJ', 'ESFP', 'ESTJ', 'ENFP',
    'ESTP', 'ISTJ', 'ENFJ', 'ESFJ'
]

mbti_values = country_data[mbti_cols]

chart_df = pd.DataFrame({
    "MBTI": mbti_cols,
    "Ratio": mbti_values.values
})

# -----------------------------
# 정렬
# -----------------------------
chart_df = chart_df.sort_values(
    by="Ratio",
    ascending=False
).reset_index(drop=True)

# -----------------------------
# 색상 설정
# 1등 = 빨강
# 나머지 = 파란 그라데이션
# -----------------------------
blue_scale = px.colors.sequential.Blues

colors = []

for i in range(len(chart_df)):
    if i == 0:
        colors.append("#ff3b30")  # 빨강
    else:
        idx = min(i + 2, len(blue_scale) - 1)
        colors.append(blue_scale[idx])

# -----------------------------
# Plotly 그래프
# -----------------------------
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=chart_df["MBTI"],
        y=chart_df["Ratio"],
        marker_color=colors,
        text=[f"{v:.2%}" for v in chart_df["Ratio"]],
        textposition="outside",
        hovertemplate=
        "<b>%{x}</b><br>" +
        "비율: %{y:.2%}<extra></extra>"
    )
)

# -----------------------------
# 레이아웃
# -----------------------------
fig.update_layout(
    title=f"{selected_country} MBTI 비율",
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    template="plotly_white",
    height=650,
    hovermode="x unified"
)

fig.update_yaxes(tickformat=".0%")

# -----------------------------
# 출력
# -----------------------------
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# 최고 비율 MBTI
# -----------------------------
top_mbti = chart_df.iloc[0]

st.success(
    f"🏆 {selected_country}에서 가장 높은 MBTI는 "
    f"**{top_mbti['MBTI']}** "
    f"({top_mbti['Ratio']:.2%}) 입니다."
)

# -----------------------------
# 데이터 테이블
# -----------------------------
with st.expander("원본 데이터 보기"):
    st.dataframe(
        chart_df,
        use_container_width=True
    )
