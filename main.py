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

# ⚠️ 여기에 영화진흥위원회(KOBIS)에서 발급받은 실제 API 키를 입력하세요.
API_KEY = "YOUR_KOBIS_API_KEY"


def fetch_boxoffice(dt):
    url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json"
    params = {"key": API_KEY, "targetDt": dt}

    if API_KEY == "YOUR_KOBIS_API_KEY" or not API_KEY.strip():
        st.warning("⚠️ API 키가 설정되지 않았습니다. 코드 내부의 API_KEY 변수에 실제 발급받은 키를 넣어주세요.")
        return []

    try:
        res = requests.get(url, params=params, timeout=5)
        res_json = res.json()

        # KOBIS API 실패/에러 응답 처리
        if "faultInfo" in res_json:
            fault = res_json["faultInfo"]
            st.error(f"❌ API 오류 발생: [{fault.get('errorCode')}] {fault.get('message')}")
            return []

        box_office_result = res_json.get("boxOfficeResult", {})
        daily_list = box_office_result.get("dailyBoxOfficeList", [])

        return daily_list

    except requests.exceptions.RequestException as e:
        st.error(f"❌ 네트워크 요청 중 오류 발생: {e}")
        return []
    except Exception as e:
        st.error(f"❌ 데이터 처리 중 오류 발생: {e}")
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

        # 순위 증감 표시 (양수: 🔺, 음수: 🔹, 0: -)
        if rank_inten > 0:
            inten_str = f"🔺 {rank_inten}"
        elif rank_inten < 0:
            inten_str = f"🔹 {abs(rank_inten)}"
        else:
            inten_str = "-"

        # 누적관객수 100만 명 이상 트로피 추가
        movie_nm = m.get("movieNm", "")
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
