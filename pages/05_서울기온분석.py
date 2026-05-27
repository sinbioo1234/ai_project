import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(
    page_title="서울 기온 분석",
    layout="wide"
)

st.title("🌡️ 서울 연도별 기온 변화")

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("seoul.csv", encoding="euc-kr")

    # 날짜 처리
    df["날짜"] = pd.to_datetime(df["날짜"])

    # 연/월/일 컬럼 생성
    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month
    df["일"] = df["날짜"].dt.day

    return df

df = load_data()

# 월 선택
selected_month = st.selectbox(
    "월 선택",
    sorted(df["월"].unique())
)

# 해당 월의 일만 표시
available_days = sorted(
    df[df["월"] == selected_month]["일"].unique()
)

# 일 선택
selected_day = st.selectbox(
    "일 선택",
    available_days
)

# 데이터 필터링
filtered = df[
    (df["월"] == selected_month) &
    (df["일"] == selected_day)
].sort_values("연도")

# 제목
st.subheader(
    f"{selected_month}월 {selected_day}일 연도별 최고/최저 기온"
)

# 그래프 생성
fig, ax = plt.subplots(figsize=(12, 6))

# 최고기온 (핫핑크)
ax.plot(
    filtered["연도"],
    filtered["최고기온(℃)"],
    color="hotpink",
    marker="o",
    linewidth=2,
    label="최고기온"
)

# 최저기온 (연한 파란색)
ax.plot(
    filtered["연도"],
    filtered["최저기온(℃)"],
    color="lightblue",
    marker="o",
    linewidth=2,
    label="최저기온"
)

# 그래프 꾸미기
ax.set_xlabel("연도")
ax.set_ylabel("기온(℃)")
ax.set_title(
    f"{selected_month}월 {selected_day}일 기온 변화"
)

ax.grid(True)
ax.legend()

# 스트림릿에 출력
st.pyplot(fig)

# 데이터 표 출력
st.dataframe(
    filtered[
        ["연도", "최고기온(℃)", "최저기온(℃)"]
    ].reset_index(drop=True),
    use_container_width=True
)
