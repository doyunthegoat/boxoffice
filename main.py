import datetime
import zoneinfo
import requests
import pandas as pd
import streamlit as st

# -----------------------------------------------------------------------------
# 1. 페이지 기본 설정 및 한국 시간 기준 어제 날짜 구하기
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="어제 박스오피스",
    page_icon="🎬",
    layout="wide"
)

# 해외 서버(배포 환경)에서도 정확한 한국 시간(Asia/Seoul) 기준 '어제' 날짜 계산
kst_timezone = zoneinfo.ZoneInfo("Asia/Seoul")
now_kst = datetime.datetime.now(kst_timezone)
yesterday_kst = now_kst - datetime.timedelta(days=1)

# API 요청에 필요한 'YYYYMMDD' 형식 및 화면 표시용 'YYYY-MM-DD' 형식 문자열 만들기
target_dt_str = yesterday_kst.strftime("%Y%m%d")
display_dt_str = yesterday_kst.strftime("%Y년 %m월 %d일")

st.title(f"🎬 {display_dt_str} 일별 박스오피스")

# -----------------------------------------------------------------------------
# 2. Streamlit Secrets에서 KOBIS API 키 불러오기
# -----------------------------------------------------------------------------
# Streamlit Cloud의 Secrets에 저장된 KOBIS_KEY를 가져옵니다.
if "KOBIS_KEY" not in st.secrets:
    st.error("🔑 API 키가 없노 이기야!!!!!! 우흥북딱한드르라흔드르라이기야")
    st.info(
        "Streamlit Cloud 설정(Secrets)에 `KOBIS_KEY = '발급받은키'`를 등록하였는지 확인해 주세요."
    )
    st.stop()

api_key = st.secrets["KOBIS_KEY"]

# -----------------------------------------------------------------------------
# 3. KOBIS API 데이터 요청
# -----------------------------------------------------------------------------
url = "https://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json"
params = {
    "key": api_key,
    "targetDt": target_dt_str
}

try:
    response = requests.get(url, params=params, timeout=10)
    # HTTP 네트워크 응답 코드 검사 (200이 아니면 예외 발생)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    st.error("🌐 네트워크 통신 중 오류가 발생했습니다.")
    st.caption(f"상세 오류: {e}")
    st.info("인터넷 연결 상태 또는 API 서버 주소가 올바른지 확인해 주세요.")
    st.stop()

# -----------------------------------------------------------------------------
# 4. API 응답 데이터 예외 처리 (faultInfo 또는 데이터 누락 검사)
# -----------------------------------------------------------------------------
# KOBIS API는 인증키 오류 시에도 HTTP 200 상태코드와 함께 'faultInfo'를 반환합니다.
if "faultInfo" in data:
    st.error("⚠️ KOBIS API 인증 및 처리 오류가 발생했습니다.")
    fault_msg = data["faultInfo"].get("message", "알 수 없는 오류")
    st.warning(f"오류 메시지: {fault_msg}")
    st.info(
        "💡 **확인할 사항:**\n"
        "1. Streamlit Secrets에 입력한 `KOBIS_KEY` 값이 정확한지 확인해 주세요.\n"
        "2. [KOBIS 오픈API 포털](https://www.kobis.or.kr/kobisopenapi)에서 키가 활성화 상태인지 확인해 주세요."
    )
    st.stop()

box_office_result = data.get("boxOfficeResult", {})
daily_list = box_office_result.get("dailyBoxOfficeList", [])

# 영화 목록 데이터가 비어 있는 경우 처리
if not daily_list:
    st.warning(f"⚠️ {display_dt_str} 기준 박스오피스 데이터가 비어 있습니다.")
    st.info(
        "💡 **확인할 사항:**\n"
        "1. 영화진흥위원회의 일별 데이터 집계 시점(보통 오전 중) 이전일 수 있습니다.\n"
        "2. 입력된 날짜의 데이터 업데이트 여부를 나중에 다시 확인해 주세요."
    )
    st.stop()

# -----------------------------------------------------------------------------
# 5. 데이터 전처리 (문자열 -> 숫자 변환 및 판다스 데이터프레임 생성)
# -----------------------------------------------------------------------------
df = pd.DataFrame(daily_list)

# 숫자로 다루어야 할 데이터 컬럼들을 정수(int) 타입으로 변환 (KOBIS API는 기본적으로 문자열로 전송함)
numeric_cols = ["rank", "rankInten", "audiCnt", "audiAcc", "scrnCnt", "showCnt"]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

# -----------------------------------------------------------------------------
# 6. 1위 영화 핵심 지표 카드 (Metric) 표시
# -----------------------------------------------------------------------------
top1 = df.iloc[0]

st.subheader("🏆 어제의 박스오피스 1위")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="영화명",
        value=top1["movieNm"]
    )

with col2:
    st.metric(
        label="일일 관객수",
        value=f"{top1['audiCnt']:,} 명"
    )

with col3:
    st.metric(
        label="누적 관객수",
        value=f"{top1['audiAcc']:,} 명"
    )

st.divider()

# -----------------------------------------------------------------------------
# 7. 관객수 상위 5개 영화 막대그래프 시각화
# -----------------------------------------------------------------------------
st.subheader("📊 관객수 상위 5개 영화")

# 순위 기준 상위 5개 추출
top5_df = df.head(5)

# Streamlit 내장 막대그래프 사용 (x축: 영화명, y축: 관객수)
st.bar_chart(
    data=top5_df,
    x="movieNm",
    y="audiCnt",
    color="#FF4B4B"
)

st.divider()

# -----------------------------------------------------------------------------
# 8. 전체 박스오피스 순위 표 (Table) 출력
# -----------------------------------------------------------------------------
st.subheader("📋 박스오피스 전체 순위")

# 화면에 표시할 컬럼선택 및 이름 변경
display_df = df[[
    "rank", "movieNm", "openDt", "audiCnt", "audiAcc", "scrnCnt"
]].copy()

display_df.columns = ["순위", "영화명", "개봉일", "관객수", "누적관객", "스크린수"]

# 데이터프레임 스타일 설정 (숫자 천 단위 쉼표 서식)
st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "관객수": st.column_config.NumberColumn(format="%d 명"),
        "누적관객": st.column_config.NumberColumn(format="%d 명"),
        "스크린수": st.column_config.NumberColumn(format="%d 개")
    }
)
