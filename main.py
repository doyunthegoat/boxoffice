import datetime
import requests
import streamlit as st

st.set_page_config(page_title="일별 박스오피스 조회", layout="wide")

# 오늘 날짜 및 어제 날짜 계산
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

st.title("🎬 일별 박스오피스 조회")

# 1. 달력에서 날짜 선택 (최대 어제까지)
selected_date = st.date_input(
    "날짜 선택",
    value=yesterday,
    max_value=yesterday,
)

# YYYYMMDD 포맷 변환
target_dt = selected_date.strftime("%Y%m%d")

API_KEY = "YOUR_KOBIS_API_KEY"  # 본인의 Kobis API 키 입력


def fetch_boxoffice(dt):
    url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json"
    params = {"key": API_KEY, "targetDt": dt}
    try:
        res = requests.get(url, timeout=5)
        res_json = res.json()
        return res_json.get("boxOfficeResult", {}).get("dailyBoxOfficeList", [])
    except Exception as e:
        return []


movies = fetch_boxoffice(target_dt)

# 2. 결과가 비어있는 경우
if not movies:
    st.info("그날은 아직 집계 전입니다.")
else:
    # 데이터 가공
    table_data = []
    for m in movies:
        rank = m.get("rank")
        rank_inten = int(m.get("rankInten", 0))

        # 순위 증감 표시
        if rank_inten > 0:
            inten_str = f"🔺 {rank_inten}"
        elif rank_inten < 0:
            inten_str = f"🔹 {abs(rank_inten)}"
        else:
            inten_str = "-"

        # 누적관객수 100만 명 이상 트로피 추가
        movie_nm = m.get("movieNm")
        audi_acc = int(m.get("audiAcc", 0))
        if audi_acc >= 1000000:
            movie_nm += " 🏆"

        table_data.append(
            {
                "순위": rank,
                "순위 증감": inten_str,
                "영화명": movie_nm,
                "개봉일": m.get("openDt"),
                "당일 관객수": f"{int(m.get('audiCnt', 0)):,}명",
                "누적 관객수": f"{audi_acc:,}명",
            }
        )

    st.table(table_data)
