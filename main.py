import datetime
import requests
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="박스오피스 순위", layout="wide")

# ---------------------------------------------------------
# 🎨 사이버펑크 네온 다크 커스텀 CSS
# ---------------------------------------------------------
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;800;900&family=Noto+Sans+KR:wght@400;700&display=swap');

/* 전체 배경을 사이버펑크 다크 컬러로 고정 */
.stApp {
    background-color: #0d0a1a !important;
    font-family: 'Noto Sans KR', sans-serif;
    color: #e2e8f0;
}

/* 메인 타이틀 네온 효과 */
.cyber-title {
    font-size: 2.6rem;
    font-weight: 800;
    text-align: center;
    color: #ffffff;
    text-shadow: 
        0 0 5px #fff,
        0 0 10px #ffee00,
        0 0 20px #ffee00,
        0 0 40px #ff007f,
        0 0 80px #ff007f;
    margin-bottom: 25px;
}

/* 영화 카드 컨테이너 */
.movie-card {
    background-color: rgba(26, 22, 43, 0.9);
    border: 1px solid #00f3ff;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 0 15px rgba(0, 243, 255, 0.2);
    transition: all 0.25s ease-in-out;
}

.movie-card:hover {
    transform: translateY(-2px);
    border-color: #ff007f;
    box-shadow: 0 0 20px rgba(255, 0, 127, 0.6);
}

/* 영화 제목 및 툴팁(포스터) 호버 효과 */
.title-container {
    position: relative;
    display: inline-block;
    cursor: pointer;
    font-weight: bold;
    font-size: 1.2rem;
    color: #00f3ff;
    text-shadow: 0 0 8px rgba(0, 243, 255, 0.5);
}

.title-container:hover {
    color: #ffee00;
    text-shadow: 0 0 12px rgba(255, 238, 0, 0.9);
}

.title-container .poster-hover {
    visibility: hidden;
    width: 170px;
    background-color: #0d0a1a;
    border: 2px solid #ff007f;
    border-radius: 8px;
    padding: 6px;
    position: absolute;
    z-index: 999;
    bottom: 125%;
    left: 0;
    opacity: 0;
    transition: opacity 0.3s;
    box-shadow: 0 0 20px rgba(255, 0, 127, 0.8);
}

.title-container:hover .poster-hover {
    visibility: visible;
    opacity: 1;
}

.poster-hover img {
    width: 100%;
    border-radius: 4px;
    display: block;
}

/* 순위 증감 색상 */
.rank-up { color: #ff3366; font-weight: bold; text-shadow: 0 0 5px #ff3366; }
.rank-down { color: #00f3ff; font-weight: bold; text-shadow: 0 0 5px #00f3ff; }
.rank-same { color: #888888; }

/* 날짜 입력창 네온 스타일 */
div[data-baseweb="input"] {
    border-radius: 8px !important;
    border: 1px solid #bd00ff !important;
    box-shadow: 0 0 10px rgba(189, 0, 255, 0.3) !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------------------------------------
# 타이틀 & 날짜 선택
# ---------------------------------------------------------
st.markdown('<div class="cyber-title">⚡ 박스오피스 순위 ⚡</div>', unsafe_allow_html=True)

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

# ⚠️ 여기에 영화진흥위원회(KOBIS) API 키를 넣어주세요.
API_KEY = "cd44c04dd87e16570306335bcf73c1da"

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    selected_date = st.date_input(
        "🗓️ 조회 날짜 선택 (최대 어제까지)",
        value=yesterday,
        max_value=yesterday,
    )

target_dt = selected_date.strftime("%Y%m%d")

# ---------------------------------------------------------
# API 호출 함수
# ---------------------------------------------------------
def fetch_boxoffice(dt):
    # API 키가 설정되지 않았을 경우 테스트용 샘플 데이터 제공
    if API_KEY == "YOUR_KOBIS_API_KEY" or not API_KEY.strip():
        st.warning("⚠️ API 키가 설정되지 않았습니다. API_KEY 변수에 실제 발급받은 키를 넣어주세요.")
        return
