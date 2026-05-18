import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="서울 관광지 TOP10",
    page_icon="🗺️",
    layout="wide"
)

st.title("🌏 외국인들이 좋아하는 서울 관광지 TOP10")
st.markdown("지도에서 관광지를 클릭하면 가까운 지하철역과 놀거리를 확인할 수 있어요!")

# 관광지 데이터
tourist_spots = [
    {
        "name": "경복궁",
        "lat": 37.579617,
        "lon": 126.977041,
        "subway": "경복궁역(3호선)",
        "fun": "한복 체험, 궁궐 야간관람, 북촌 산책"
    },
    {
        "name": "명동",
        "lat": 37.563757,
        "lon": 126.985302,
        "subway": "명동역(4호선)",
        "fun": "쇼핑, 길거리 음식, K-뷰티 투어"
    },
    {
        "name": "남산서울타워",
        "lat": 37.551169,
        "lon": 126.988227,
        "subway": "명동역(4호선)",
        "fun": "야경 감상, 케이블카, 사랑의 자물쇠"
    },
    {
        "name": "홍대거리",
        "lat": 37.556350,
        "lon": 126.922672,
        "subway": "홍대입구역(2호선)",
        "fun": "버스킹, 카페 투어, 클럽"
    },
    {
        "name": "강남",
        "lat": 37.497942,
        "lon": 127.027621,
        "subway": "강남역(2호선)",
        "fun": "쇼핑, 맛집 탐방, 코엑스 방문"
    },
    {
        "name": "북촌한옥마을",
        "lat": 37.582604,
        "lon": 126.983998,
        "subway": "안국역(3호선)",
        "fun": "전통 한옥 체험, 사진 촬영, 공방 체험"
    },
    {
        "name": "롯데월드타워",
        "lat": 37.512462,
        "lon": 127.102544,
        "subway": "잠실역(2호선)",
        "fun": "서울스카이 전망대, 쇼핑몰, 아쿠아리움"
    },
    {
        "name": "동대문디자인플라자(DDP)",
        "lat": 37.566526,
        "lon": 127.009224,
        "subway": "동대문역사문화공원역(2호선)",
        "fun": "야시장, 전시회, 디자인 쇼핑"
    },
    {
        "name": "이태원",
        "lat": 37.534981,
        "lon": 126.994110,
        "subway": "이태원역(6호선)",
        "fun": "세계 음식, 펍 투어, 루프탑 바"
    },
    {
        "name": "한강공원",
        "lat": 37.520694,
        "lon": 126.939507,
        "subway": "여의나루역(5호선)",
        "fun": "치맥, 자전거, 한강 유람선"
    }
]

# 지도 생성
m = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=11,
    tiles="OpenStreetMap"
)

# 마커 추가
for spot in tourist_spots:
    popup_text = f"""
    <b>{spot['name']}</b><br>
    🚇 가까운 역: {spot['subway']}<br>
    🎉 놀거리: {spot['fun']}
    """

    folium.Marker(
        location=[spot["lat"], spot["lon"]],
        popup=folium.Popup(popup_text, max_width=300),
        tooltip=spot["name"],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# 지도 출력
map_data = st_folium(
    m,
    width=1200,
    height=650
)

# 클릭된 관광지 정보 표시
st.markdown("---")
st.subheader("📍 관광지 정보")

clicked = map_data.get("last_object_clicked_popup")

if clicked:
    st.success(clicked.replace("<br>", " | ").replace("<b>", "").replace("</b>", ""))
else:
    st.info("지도의 관광지 마커를 클릭해보세요!")
