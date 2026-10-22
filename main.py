import datetime
import requests
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="박스오피스 순위", layout="wide")

# ---------------------------------------------------------
# 🎨 사이버펑크 네온 커스텀 CSS (안정화 버전)
# ---------------------------------------------------------
custom_css = """
<style>
/* 메인 타이틀 네온 효과 */
.cyber-title {
    font-size: 2.5rem;
    font-weight: 800;
    text-align: center;
    color: #ffffff;
    text-shadow: 0 0 10px #ffee00, 0 0 20px #ffee00, 0 0 30px #ff007f;
    margin-bottom: 25px;
}

/* 영화 카드 컨테이너 */
.movie-card {
    background-color: #1a162b;
    border: 1px solid #00f3ff;
    border-radius: 10px;
    padding: 15px 20px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 0 10px rgba(0, 243, 255, 0.2);
}

.movie-card:hover {
    border-color: #ff007f;
    box-shadow: 0 0 15px rgba(255, 0, 127, 0.5);
}

/* 영화 제목 및 툴팁(포스터) 호버 효과 */
.title-container {
    position: relative;
    display: inline-block;
    cursor: pointer;
    font-weight: bold;
    font-size: 1.2rem;
    color: #00f3ff;
}

.title-container:hover {
    color: #ffee00;
}

.title-container .poster-hover {
    visibility: hidden;
    width: 160px;
    background-color: #0f0c1b;
    border: 2px solid #ff007f;
    border-radius: 8px;
    padding: 5px;
    position: absolute;
    z-index: 99;
    bottom: 120%;
    left: 0;
    opacity: 0;
    transition: opacity 0.3s;
    box-shadow: 0 0 15px rgba(255, 0, 127, 0.8);
}

.title-container:hover .poster-hover {
    visibility: visible;
    opacity: 1;
}

.poster-hover img {
    width: 100%;
    border-radius: 4px;
}

/* 순위 증감 색상 */
.rank-up { color: #ff3366; font-weight: bold; }
.rank-down { color: #00f3ff; font-weight: bold; }
.rank-same { color: #888888; }
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
API_KEY = "YOUR_KOBIS_API_KEY"

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
    url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json"
    params = {"key": API_KEY, "targetDt": dt}

    if API_KEY == "YOUR_KOBIS_API_KEY" or not API_KEY.strip():
        st.warning("⚠️ API 키가 설정되지 않았습니다. 코드 내부의 API_KEY 변수에 실제 API 키를 입력해 주세요.")
        return []

    try:
        res = requests.get(url, params=params, timeout=5)
        res_json = res.json()

        if "faultInfo" in res_json:
            fault = res_json["faultInfo"]
            st.error(f"❌ API 오류: [{fault.get('errorCode')}] {fault.get('message')}")
            return []

        return res_json.get("boxOfficeResult", {}).get("dailyBoxOfficeList", [])
    except Exception as e:
        st.error(f"❌ 네트워크/데이터 오류 발생: {e}")
        return []

movies = fetch_boxoffice(target_dt)

# ---------------------------------------------------------
# 박스오피스 목록 렌더링
# ---------------------------------------------------------
if
