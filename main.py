import React, { useState, useEffect } from 'react';
import axios from 'axios';

// 날짜를 YYYYMMDD 형식의 문자열로 변환하는 함수
const formatDate = (date) => {
  const yyyy = date.getFullYear();
  const mm = String(date.getMonth() + 1).padStart(2, '0');
  const dd = String(date.getDate()).padStart(2, '0');
  return `${yyyy}${mm}${dd}`;
};

// 날짜를 YYYY-MM-DD 형식의 문자열로 변환하는 함수 (input type="date"용)
const formatDateForInput = (date) => {
  const yyyy = date.getFullYear();
  const mm = String(date.getMonth() + 1).padStart(2, '0');
  const dd = String(date.getDate()).padStart(2, '0');
  return `${yyyy}-${mm}-${dd}`;
};

const App = () => {
  // 오늘 날짜 및 어제 날짜 계산
  const today = new Date();
  const yesterday = new Date(today);
  yesterday.setDate(today.getDate() - 1);

  // 기본 선택 날짜를 어제로 설정
  const [selectedDate, setSelectedDate] = useState(formatDateForInput(yesterday));
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isEmpty, setIsEmpty] = useState(false);

  const API_KEY = 'YOUR_KOBIS_API_KEY'; // 본인의 Kobis API 키를 입력하세요.

  const fetchBoxOffice = async (dateStr) => {
    // YYYY-MM-DD -> YYYYMMDD 변환
    const targetDate = dateStr.replace(/-/g, '');
    setLoading(true);
    setIsEmpty(false);

    try {
      const response = await axios.get(
        `http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json`,
        {
          params: {
            key: API_KEY,
            targetDt: targetDate,
          },
        }
      );

      const dailyBoxOfficeList =
        response.data.boxOfficeResult?.dailyBoxOfficeList || [];

      if (dailyBoxOfficeList.length === 0) {
        setIsEmpty(true);
        setMovies([]);
      } else {
        setMovies(dailyBoxOfficeList);
      }
    } catch (error) {
      console.error('박스오피스 데이터를 불러오는 중 오류 발생:', error);
      setIsEmpty(true);
      setMovies([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBoxOffice(selectedDate);
  }, [selectedDate]);

  const handleDateChange = (e) => {
    setSelectedDate(e.target.value);
  };

  // 순위 증감 표시 함수
  const renderRankInten = (rankInten) => {
    const inten = Number(rankInten);
    if (inten > 0) {
      return <span style={{ color: 'red' }}>▲ {inten}</span>;
    } else if (inten < 0) {
      return <span style={{ color: 'blue' }}>▼ {Math.abs(inten)}</span>;
    }
    return <span>-</span>;
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>일별 박스오피스 조회</h1>

      {/* 날짜 선택 달력 */}
      <div style={{ marginBottom: '20px' }}>
        <label htmlFor="date-picker" style={{ marginRight: '10px' }}>
          날짜 선택:
        </label>
        <input
          id="date-picker"
          type="date"
          value={selectedDate}
          max={formatDateForInput(yesterday)} // 가장 늦은 날짜는 어제까지로 제한
          onChange={handleDateChange}
        />
      </div>

      {/* 로딩 표시 */}
      {loading && <p>데이터를 불러오는 중입니다...</p>}

      {/* 데이터가 비어있을 때 */}
      {!loading && isEmpty && (
        <p style={{ color: '#666', fontWeight: 'bold' }}>
          그날은 아직 집계 전입니다.
        </p>
      )}

      {/* 박스오피스 목록 표 */}
      {!loading && !isEmpty && movies.length > 0 && (
        <table
          border="1"
          cellPadding="8"
          cellSpacing="0"
          style={{ width: '100%', borderCollapse: 'collapse' }}
        >
          <thead>
            <tr style={{ backgroundColor: '#f2f2f2' }}>
              <th>순위</th>
              <th>순위 증감</th>
              <th>영화명</th>
              <th>개봉일</th>
              <th>당일 관객수</th>
              <th>누적 관객수</th>
            </tr>
          </thead>
          <tbody>
            {movies.map((movie) => {
              const audiAcc = Number(movie.audiAcc);
              const isOverOneMillion = audiAcc >= 1000000;

              return (
                <tr key={movie.movieCd} style={{ textAlign: 'center' }}>
                  <td>{movie.rank}</td>
                  <td>{renderRankInten(movie.rankInten)}</td>
                  <td style={{ textAlign: 'left' }}>
                    {movie.movieNm}
                    {isOverOneMillion && ' 🏆'}
                  </td>
                  <td>{movie.openDt}</td>
                  <td>{Number(movie.audiCnt).toLocaleString()}명</td>
                  <td>{audiAcc.toLocaleString()}명</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default App;
