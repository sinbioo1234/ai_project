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

    # 날짜 처리 수정
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str).str.strip(),
        errors="coerce"
    )

    # 날짜 오류 제거
    df = df.dropna(subset=["날짜"])

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

# 그래프
fig, ax = plt.subplots(figsize=(12, 6))

# 최고기온
ax.plot(
    filtered["연도"],
    filtered["최고기온(℃)"],
    color="hotpink",
    marker="o",
    linewidth=2,
    label="최고기온"
)

# 최저기온
ax.plot(
    filtered["연도"],
    filtered["최저기온(℃)"],
    color="lightblue",
    marker="o",
    linewidth=2,
    label="최저기온"
)

ax.set_xlabel("연도")
ax.set_ylabel("기온(℃)")
ax.set_title(
    f"{selected_month}월 {selected_day}일 기온 변화"
)

ax.grid(True)
ax.legend()

st.pyplot(fig)

# 데이터 표
st.dataframe(
    filtered[
        ["연도", "최고기온(℃)", "최저기온(℃)"]
    ].reset_index(drop=True),
    use_container_width=True
)
