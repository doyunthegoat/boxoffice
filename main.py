import datetime
import requests
import streamlit as st

# 페이지 설정을 화면 전체(wide) 및 검은 배경 느낌으로 구성
st.set_page_config(page_title="NEON CYBERPUNK BOXOFFICE", layout="wide")

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

/* 사이버펑크 메인 네온 타이틀 */
.cyber-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.8rem;
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
    letter-spacing: 2px;
}

/* 네온 카드 컨테이너 */
.neon-card {
    background: rgba(18, 11, 38, 0.85);
    border: 1px solid #00f3ff;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
    box-shadow: 0 0 15px rgba(0, 243, 255, 0.2), inset 0 0 10px rgba(0, 243, 255, 0.1);
    transition: all 0.3s ease-in-out;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.neon-card:hover {
    transform: translateY(-3px) scale(1.005);
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
    min-width: 45px;
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

/* 입력 폼 커스텀 네온 선 스타일 */
div[data-baseweb="input"] {
    border-radius: 8px !important;
    border: 1px solid #bd00ff !important;
    box-shadow: 0 0 10px rgba(189, 0, 255, 0.3) !important;
}
</style>
"""
st.markdown(cyberpunk_css, unsafe_allow_html=True)

# ---------------------------------------------------------
# 타이틀 & 날짜 계산
# ---------------------------------------------------------
st.markdown('<div class="cyber-title">⚡ CYBERPUNK BOXOFFICE ⚡</div>', unsafe_allow_html=True)

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

# ⚠️ 발급받은 KOBIS API KEY를 입력하세요.
API_KEY = "YOUR_KOBIS_API_KEY"

# 상단 제어 바 (날짜 선택 + 기능 2: 검색 필터)
col1, col2 = st.columns([1, 2])

with col1:
    selected_date = st.date_input(
        "🗓️ 조회 날짜 선택 (최대 어제)",
        value=yesterday,
        max_value=yesterday,
    )

with col2:
    search_keyword = st.text_input("🔍 [추가 기능] 영화 제목 실시간 필터링", placeholder="검색할 영화 제목을 입력하세요...")

target_dt = selected_date.strftime("%Y%m%d")

# ---------------------------------------------------------
# API 데이터 호출 함수
# ---------------------------------------------------------
def fetch_boxoffice(dt):
    url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json"
    params = {"key": API_KEY, "targetDt": dt}

    if API_KEY == "YOUR_KOBIS_API_KEY" or not API_KEY.strip():
        st.warning("⚠️ API 키가 설정되지 않았습니다. 코드 내 API_KEY 변수에 영진위 키를 넣어주세요.")
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
        st.error(f"❌ 데이터 요청 중 오류 발생: {e}")
        return []

movies = fetch_boxoffice(target_dt)

# ---------------------------------------------------------
# 결과 출력 및 사이버펑크 UI 렌더링
# ---------------------------------------------------------
if not movies:
    st.info("🌌 해당 날짜는 아직 집계 전이거나 데이터가 없습니다.")
else:
    # 키워드 검색 필터 적용
    if search_keyword:
        movies = [m for m in movies if search_keyword.lower() in m.get("movieNm", "").lower()]

    if not movies:
        st.warning("🔍 검색 조건에 일치하는 영화가 없습니다.")

    for m in movies:
        rank = m.get("rank")
        rank_inten = int(m.get("rankInten", 0))
        movie_nm = m.get("movieNm", "")
        audi_cnt = int(m.get("audiCnt", 0))
        audi_acc = int(m.get("audiAcc", 0))
        open_dt = m.get("openDt", "-")

        # 1위~3위 크라운 배지 추가 (추가 기능 1)
        crown_badge = ""
        if rank == "1":
            crown_badge = "👑 "
        elif rank == "2":
            crown_badge = "🥈 "
        elif rank == "3":
            crown_badge = "🥉 "

        # 100만 관객 트로피
        trophy = " 🏆" if audi_acc >= 1000000 else ""

        # 순위 증감 네온 텍스트
        if rank_inten > 0:
            inten_html = f'<span class="rank-up">▲ {rank_inten}</span>'
        elif rank_inten < 0:
            inten_html = f'<span class="rank-down">▼ {abs(rank_inten)}</span>'
        else:
            inten_html = '<span class="rank-same">-</span>'

        # 포스터 이미지 (샘플 네온 포스터 이미지 링크 / 필요시 실제 이미지 주소 연동 가능)
        poster_url = f"https://via.placeholder.com/300x420/120b26/00f3ff?text={requests.utils.quote(movie_nm)}"

        # HTML 구조로 카드 생성
        card_html = f"""
        <div class="neon-card">
            <div style="display: flex; align-items: center; gap: 18px;">
                <div class="rank-badge">{crown_badge}#{rank}</div>
                <div>
                    <div class="movie-title-wrap">
                        {movie_nm}{trophy}
                        <div class="poster-tooltip">
                            <img src="{poster_url}" alt="{movie_nm}">
                            <div style="text-align:center; font-size: 0.8rem; color:#fff; margin-top:4px;">{movie_nm}</div>
                        </div>
                    </div>
                    <div style="font-size: 0.85rem; color: #a0aec0; margin-top: 4px;">
                        개봉일: {open_dt} | 순위변동: {inten_html}
                    </div>
                </div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 1.1rem; font-weight: bold; color: #ffee00; text-shadow: 0 0 8px #ffee00;">
                    당일 {audi_cnt:,} 명
                </div>
                <div style="font-size: 0.85rem; color: #00f3ff;">
                    누적 {audi_acc:,} 명
                </div>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
