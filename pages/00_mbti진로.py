import streamlit as st

st.set_page_config(page_title="MBTI 진로 추천", page_icon="💼")

st.title("💼 MBTI 기반 진로 추천 프로그램")
st.write("MBTI를 선택하면 어울리는 진로 2가지를 추천해줍니다!")

# MBTI별 데이터
career_data = {
    "INTJ": [
        {
            "job": "데이터 분석가",
            "major": "통계학과, 컴퓨터공학과",
            "personality": "논리적이고 분석적인 사람",
            "salary": "평균 연봉 약 5,500만 원"
        },
        {
            "job": "연구원",
            "major": "자연과학계열, 공학계열",
            "personality": "탐구심이 강하고 집중력이 높은 사람",
            "salary": "평균 연봉 약 6,000만 원"
        }
    ],

    "INTP": [
        {
            "job": "프로그래머",
            "major": "컴퓨터공학과",
            "personality": "창의적이고 문제 해결을 좋아하는 사람",
            "salary": "평균 연봉 약 5,000만 원"
        },
        {
            "job": "게임 개발자",
            "major": "소프트웨어학과",
            "personality": "아이디어가 많고 독창적인 사람",
            "salary": "평균 연봉 약 4,800만 원"
        }
    ],

    "ENTJ": [
        {
            "job": "CEO",
            "major": "경영학과",
            "personality": "리더십이 강하고 목표 지향적인 사람",
            "salary": "평균 연봉 약 8,000만 원"
        },
        {
            "job": "마케팅 매니저",
            "major": "광고홍보학과",
            "personality": "추진력이 있고 전략적인 사람",
            "salary": "평균 연봉 약 6,000만 원"
        }
    ],

    "ENTP": [
        {
            "job": "기획자",
            "major": "경영학과",
            "personality": "새로운 아이디어를 좋아하는 사람",
            "salary": "평균 연봉 약 5,500만 원"
        },
        {
            "job": "창업가",
            "major": "창업학과",
            "personality": "도전 정신이 강한 사람",
            "salary": "평균 연봉 약 7,000만 원"
        }
    ],

    "INFJ": [
        {
            "job": "심리상담사",
            "major": "심리학과",
            "personality": "공감 능력이 뛰어난 사람",
            "salary": "평균 연봉 약 4,500만 원"
        },
        {
            "job": "작가",
            "major": "문예창작학과",
            "personality": "상상력이 풍부한 사람",
            "salary": "평균 연봉 약 4,000만 원"
        }
    ],

    "INFP": [
        {
            "job": "웹툰 작가",
            "major": "만화애니메이션학과",
            "personality": "감수성이 풍부한 사람",
            "salary": "평균 연봉 약 4,500만 원"
        },
        {
            "job": "디자이너",
            "major": "시각디자인학과",
            "personality": "창의적이고 섬세한 사람",
            "salary": "평균 연봉 약 4,800만 원"
        }
    ],

    "ENFJ": [
        {
            "job": "교사",
            "major": "교육학과",
            "personality": "사람을 돕는 것을 좋아하는 사람",
            "salary": "평균 연봉 약 5,200만 원"
        },
        {
            "job": "HR 담당자",
            "major": "경영학과",
            "personality": "의사소통 능력이 좋은 사람",
            "salary": "평균 연봉 약 5,000만 원"
        }
    ],

    "ENFP": [
        {
            "job": "광고 기획자",
            "major": "광고홍보학과",
            "personality": "활발하고 창의적인 사람",
            "salary": "평균 연봉 약 5,300만 원"
        },
        {
            "job": "유튜버",
            "major": "미디어학과",
            "personality": "표현력이 뛰어난 사람",
            "salary": "평균 연봉 다양함"
        }
    ],

    "ISTJ": [
        {
            "job": "회계사",
            "major": "회계학과",
            "personality": "꼼꼼하고 책임감 있는 사람",
            "salary": "평균 연봉 약 7,000만 원"
        },
        {
            "job": "공무원",
            "major": "행정학과",
            "personality": "성실하고 체계적인 사람",
            "salary": "평균 연봉 약 4,500만 원"
        }
    ],

    "ISFJ": [
        {
            "job": "간호사",
            "major": "간호학과",
            "personality": "배려심이 깊은 사람",
            "salary": "평균 연봉 약 5,000만 원"
        },
        {
            "job": "사회복지사",
            "major": "사회복지학과",
            "personality": "헌신적인 사람",
            "salary": "평균 연봉 약 3,800만 원"
        }
    ],

    "ESTJ": [
        {
            "job": "경찰관",
            "major": "경찰행정학과",
            "personality": "원칙을 중요하게 생각하는 사람",
            "salary": "평균 연봉 약 5,500만 원"
        },
        {
            "job": "관리자",
            "major": "경영학과",
            "personality": "조직 관리 능력이 뛰어난 사람",
            "salary": "평균 연봉 약 6,000만 원"
        }
    ],

    "ESFJ": [
        {
            "job": "승무원",
            "major": "항공서비스학과",
            "personality": "친절하고 사교적인 사람",
            "salary": "평균 연봉 약 4,800만 원"
        },
        {
            "job": "호텔리어",
            "major": "호텔관광학과",
            "personality": "서비스 정신이 강한 사람",
            "salary": "평균 연봉 약 4,500만 원"
        }
    ],

    "ISTP": [
        {
            "job": "기계 엔지니어",
            "major": "기계공학과",
            "personality": "실용적이고 문제 해결 능력이 좋은 사람",
            "salary": "평균 연봉 약 6,000만 원"
        },
        {
            "job": "파일럿",
            "major": "항공운항학과",
            "personality": "침착하고 판단력이 좋은 사람",
            "salary": "평균 연봉 약 8,000만 원"
        }
    ],

    "ISFP": [
        {
            "job": "플로리스트",
            "major": "원예학과",
            "personality": "감각적이고 따뜻한 사람",
            "salary": "평균 연봉 약 3,500만 원"
        },
        {
            "job": "사진작가",
            "major": "사진영상학과",
            "personality": "예술 감각이 뛰어난 사람",
            "salary": "평균 연봉 약 4,000만 원"
        }
    ],

    "ESTP": [
        {
            "job": "영업 전문가",
            "major": "경영학과",
            "personality": "도전적이고 활동적인 사람",
            "salary": "평균 연봉 약 5,500만 원"
        },
        {
            "job": "운동선수",
            "major": "체육학과",
            "personality": "에너지가 넘치는 사람",
            "salary": "평균 연봉 다양함"
        }
    ],

    "ESFP": [
        {
            "job": "배우",
            "major": "연극영화학과",
            "personality": "사람들과 어울리기를 좋아하는 사람",
            "salary": "평균 연봉 다양함"
        },
        {
            "job": "이벤트 플래너",
            "major": "이벤트학과",
            "personality": "밝고 활발한 사람",
            "salary": "평균 연봉 약 4,500만 원"
        }
    ]
}

# MBTI 선택
mbti_list = list(career_data.keys())

selected_mbti = st.selectbox(
    "당신의 MBTI를 선택하세요",
    mbti_list
)

# 결과 출력
if selected_mbti:
    st.subheader(f"✨ {selected_mbti} 추천 진로")

    careers = career_data[selected_mbti]

    for idx, career in enumerate(careers, start=1):
        st.markdown(f"## {idx}. {career['job']}")
        st.write(f"📚 적합한 학과: {career['major']}")
        st.write(f"😊 어울리는 성격: {career['personality']}")
        st.write(f"💰 {career['salary']}")
        st.divider()

st.caption("※ 연봉은 평균적인 예시이며 실제와 차이가 있을 수 있습니다.")
