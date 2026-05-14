import streamlit as st

# MBTI별 추천 데이터
recommendations = {
    "INTJ": {
        "book": ("1984", "디스토피아 / 철학"),
        "movie": ("인터스텔라", "SF / 철학")
    },
    "INTP": {
        "book": ("코스모스", "과학 / 교양"),
        "movie": ("매트릭스", "SF / 철학")
    },
    "ENTJ": {
        "book": ("손자병법", "전략 / 자기계발"),
        "movie": ("아이언맨", "액션 / 성장")
    },
    "ENTP": {
        "book": ("멋진 신세계", "SF / 풍자"),
        "movie": ("데드풀", "액션 / 코미디")
    },
    "INFJ": {
        "book": ("어린 왕자", "성장 / 철학"),
        "movie": ("쇼생크 탈출", "드라마 / 희망")
    },
    "INFP": {
        "book": ("데미안", "성장 / 문학"),
        "movie": ("센과 치히로의 행방불명", "판타지 / 성장")
    },
    "ENFJ": {
        "book": ("미움받을 용기", "심리 / 자기계발"),
        "movie": ("죽은 시인의 사회", "드라마 / 성장")
    },
    "ENFP": {
        "book": ("연금술사", "모험 / 성장"),
        "movie": ("라라랜드", "뮤지컬 / 로맨스")
    },
    "ISTJ": {
        "book": ("정의란 무엇인가", "철학 / 사회"),
        "movie": ("포레스트 검프", "드라마 / 인생")
    },
    "ISFJ": {
        "book": ("나미야 잡화점의 기적", "감동 / 힐링"),
        "movie": ("코코", "애니메이션 / 가족")
    },
    "ESTJ": {
        "book": ("원칙", "자기계발 / 경영"),
        "movie": ("머니볼", "드라마 / 스포츠")
    },
    "ESFJ": {
        "book": ("아몬드", "성장 / 감성"),
        "movie": ("인사이드 아웃", "애니메이션 / 감동")
    },
    "ISTP": {
        "book": ("해저 2만리", "모험 / SF"),
        "movie": ("존 윅", "액션 / 스릴러")
    },
    "ISFP": {
        "book": ("채식주의자", "문학 / 감성"),
        "movie": ("월-E", "애니메이션 / 힐링")
    },
    "ESTP": {
        "book": ("헝거게임", "액션 / 생존"),
        "movie": ("분노의 질주", "액션 / 범죄")
    },
    "ESFP": {
        "book": ("완득이", "청춘 / 성장"),
        "movie": ("위대한 쇼맨", "뮤지컬 / 드라마")
    }
}

# 제목
st.title("📚🎬 MBTI 책 & 영화 추천기")
st.write("당신의 MBTI를 선택하면 어울리는 책과 영화를 추천해드립니다!")

# MBTI 선택
mbti = st.selectbox(
    "MBTI를 선택하세요",
    list(recommendations.keys())
)

# 추천 출력
if mbti:
    data = recommendations[mbti]

    st.subheader(f"✨ {mbti} 추천 결과")

    # 책 추천
    st.markdown("## 📚 추천 책")
    st.write(f"**책 제목:** {data['book'][0]}")
    st.write(f"**추천 장르:** {data['book'][1]}")

    # 영화 추천
    st.markdown("## 🎬 추천 영화")
    st.write(f"**영화 제목:** {data['movie'][0]}")
    st.write(f"**추천 장르:** {data['movie'][1]}")

    # 설명
    st.markdown("## 📝 왜 이런 장르가 어울릴까?")
    
    explanations = {
        "철학": "깊게 사고하고 의미를 탐구하는 성향과 잘 어울립니다.",
        "SF": "상상력과 새로운 아이디어를 좋아하는 사람에게 적합합니다.",
        "성장": "자기 발전과 감정 변화를 중요하게 여기는 유형에게 잘 맞습니다.",
        "액션": "긴장감과 에너지를 좋아하는 성향에 잘 맞습니다.",
        "감성": "감정 이입과 섬세한 분위기를 좋아하는 사람에게 어울립니다.",
        "힐링": "편안함과 따뜻한 분위기를 원하는 사람에게 적합합니다.",
        "모험": "새로운 경험과 도전을 좋아하는 성향과 잘 맞습니다.",
        "드라마": "인간관계와 감정선을 중요하게 여기는 사람에게 적합합니다."
    }

    genres = data['book'][1].split(" / ") + data['movie'][1].split(" / ")

    shown = set()

    for genre in genres:
        if genre in explanations and genre not in shown:
            st.write(f"**{genre}** → {explanations[genre]}")
            shown.add(genre)

# 하단 문구
st.markdown("---")
st.caption("Streamlit Cloud에서 바로 실행 가능한 MBTI 추천 앱")
