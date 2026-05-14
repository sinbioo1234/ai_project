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
### 사용 방법
1. MBTI 유형 선택
2. 해당 MBTI 비율이 높은 국가 확인
3. 국가 선택
4. 국가의 전체 MBTI 분포 확인
""")

# --------------------------------
# 데이터 불러오기
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
# MBTI 선택
# --------------------------------
selected_mbti = st.selectbox(
    "🧠 MBTI 유형 선택",
    mbti_types
)

# --------------------------------
# 선택 MBTI 기준 국가 정렬
# --------------------------------
ranked_df = df.sort_values(
    by=selected_mbti,
    ascending=False
).reset_index(drop=True)

# --------------------------------
# 국가 리스트 생성
# --------------------------------
country_options = ranked_df["Country"].tolist()

st.subheader(f"🌎 {selected_mbti} 비율이 높은 국가")

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
    country_options
)

# --------------------------------
# 국가 데이터 추출
# --------------------------------
country_data = df[df["Country"] == selected_country].iloc[0]

mbti_values = country_data[mbti_types]

chart_df = pd.DataFrame({
    "MBTI": mbti_types,
    "Ratio": mbti_values.values
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
# Plotly 그래프
# --------------------------------
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

# --------------------------------
# 그래프 레이아웃
# --------------------------------
fig.update_layout(
    title=f"{selected_country} MBTI 분포",
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    template="plotly_white",
    height=650,
    hovermode="x unified"
)

fig.update_yaxes(tickformat=".0%")

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
# 원본 데이터
# --------------------------------
with st.expander("📄 전체 데이터 보기"):
    st.dataframe(
        chart_df,
        use_container_width=True
    )
