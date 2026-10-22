import datetime
import requests
import streamlit as st

# 페이지 설정을 화면 전체(wide) 및 다크 테마 느낌으로 구성
st.set_page_config(page_title="박스오피스 순위", layout="wide")

# ---------------------------------------------------------
# 🎨 사이버펑크 네온 스타일 커스텀 CSS 적용
# ---------------------------------------------------------
cyberpunk_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;800;900&family=Noto+Sans+KR:wght@400;700&display=swap');

/* 전체 배경 및 폰트 */
.stApp {
    background-color: #0d0a1a !important;
    font-family: 'Noto Sans KR', sans-serif;
    color: #e2e8f0;
}

/* 한국어 네온 메인 타이틀 */
.cyber-title {
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 2.6rem;
    font-weight: 900;
    text-align: center;
    color: #fff;
    text-shadow: 
        0 0 5px #fff,
        0 0 10px #ffee00,
        0 0 20px #ffee00,
        0 0 40px #ff007f,
        0 0 80px #ff007f;
    margin-bottom: 2rem;
    letter-spacing: 1px;
}

/* 네온 카드 컨테이너 */
.neon-card {
    background: rgba(18, 11, 38, 0.85);
    border: 1px solid #00f3ff;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
    box-shadow: 0 0 15px rgba(0, 243, 255, 0.2), inset 0 0 10px rgba(0, 243, 255, 0.1);
    transition: all 0.25s ease-in-out;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.neon-card:hover {
    transform: translateY(-2px) scale(1.003);
    border-color: #ff007f;
    box-shadow: 0 0 25px rgba(255, 0, 127, 0.6), inset 0 0 15px rgba(255, 0, 127, 0.2);
}

/* 툴팁 및 영화 포스터 호버 스타일 */
.movie-title-wrap {
    position: relative;
    display: inline-block;
    cursor: pointer;
    font-weight: 700;
    font-size: 1.15rem;
    color: #00f3ff;
    text-shadow: 0 0 8px rgba(0, 243, 255, 0.6);
}

.movie-title-wrap:hover {
    color: #ffee00;
    text-shadow: 0 0 12px rgba(255, 238, 0, 0.9);
}

.movie-title-wrap .poster-tooltip {
    visibility: hidden;
    width: 180px;
    background-color: #120b26;
    border: 2px solid #ff007f;
    border-radius: 8px;
    padding: 6px;
    position: absolute;
    z-index: 999;
    bottom: 125%;
    left: 50%;
    transform: translateX(-50%);
    box-shadow: 0 0 20px rgba(255, 0, 127, 0.8);
    opacity: 0;
    transition: opacity 0.3s ease-in-out;
}

.movie-title-wrap:hover .poster-tooltip {
    visibility: visible;
    opacity: 1;
}

.poster-tooltip img {
    width: 100%;
    border-radius: 4px;
    display: block;
}

/* 네온 배지 및 텍스트 스타일 */
.rank-badge {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    color: #ffee00;
    text-shadow: 0 0 10px #ffee00;
    min-width: 50px;
}

.rank-up {
    color: #ff3366;
    font-weight: bold;
    text-shadow: 0 0 8px #ff3366;
}

.rank-down {
    color: #00f3ff;
    font-weight: bold;
    text-shadow: 0 0 8px #00f3ff;
}

.rank-same {
    color: #888;
}

/* 날짜 선택 인풋 네온 스타일 */
div[data-baseweb="input"] {
    border-radius: 8px !important;
    border: 1px solid #bd00ff !important;
    box-shadow: 0 0 10px rgba(189, 0, 255, 0.3) !important;
}
</style>
"""
st.markdown(cyberpunk_css, unsafe_allow_html=True)

# ---------------------------------------------------------
