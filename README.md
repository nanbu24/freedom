# Binance Dogecoin Futures Data Collection

이 프로젝트는 바이낸스(Binance)에서 도지코인(Dogecoin) 선물 거래 데이터를 수집하는 Python 스크립트입니다.

## 기능

- 바이낸스 선물 API를 통한 DOGEUSDT 과거 데이터 수집
- 다양한 시간 간격 지원 (1분, 5분, 1시간, 1일 등)
- CSV 형식으로 데이터 저장
- 자동 페이지네이션으로 전체 과거 데이터 백필
- API 속도 제한 자동 처리

## 요구사항

- Python 3.7 이상
- 인터넷 연결

## 설치

1. 저장소 클론:
```bash
git clone <repository-url>
cd freedom
```

2. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

## 사용 방법

### 기본 사용

기본 설정으로 데이터 수집:

```bash
python collect_dogecoin_futures.py
```

### 샘플 데이터 생성

실제 API를 호출하지 않고 샘플 데이터를 생성하여 데이터 형식을 확인할 수 있습니다:

```bash
python generate_sample_data.py
```

이 명령은 최근 30일간의 1시간 간격 샘플 데이터를 `data/DOGEUSDT_1h_sample.csv` 파일로 생성합니다.

### 설정 변경

`config.py` 파일을 수정하여 설정을 변경할 수 있습니다:

```python
# 거래 페어
SYMBOL = "DOGEUSDT"

# 시간 간격 (1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M)
INTERVAL = "1h"

# 수집 시작 날짜
START_DATE = "2021-01-01"

# 데이터 저장 디렉토리
DATA_DIR = "data"
```

## 출력 데이터 형식

수집된 데이터는 CSV 파일로 저장되며, 다음 컬럼을 포함합니다:

| 컬럼명 | 설명 |
|--------|------|
| open_time | 캔들 시작 시간 |
| open | 시가 |
| high | 고가 |
| low | 저가 |
| close | 종가 |
| volume | 거래량 (DOGE) |
| close_time | 캔들 종료 시간 |
| quote_volume | 거래량 (USDT) |
| trades | 거래 수 |
| taker_buy_base_volume | 테이커 매수 거래량 (DOGE) |
| taker_buy_quote_volume | 테이커 매수 거래량 (USDT) |

## 데이터 저장 위치

데이터는 `data/` 디렉토리에 다음 형식으로 저장됩니다:
```
data/DOGEUSDT_1h_20240101_120000.csv
```

## API 제한사항

- 바이낸스 선물 API는 공개 데이터에 대해 API 키가 필요하지 않습니다
- 요청 속도 제한을 준수하기 위해 자동으로 0.5초 지연을 추가합니다
- 한 번에 최대 1500개의 캔들을 가져옵니다

## 주의사항

1. 과거 데이터가 많을 경우 수집에 시간이 걸릴 수 있습니다
2. 인터넷 연결이 안정적이어야 합니다
3. 바이낸스 API 서비스 약관을 준수해야 합니다

## 라이선스

MIT License

## 기여

이슈나 풀 리퀘스트를 환영합니다!

---

## English Version

This project collects Dogecoin futures trading data from Binance.

### Features

- Collect historical DOGEUSDT data from Binance Futures API
- Support for various timeframes (1m, 5m, 1h, 1d, etc.)
- Save data in CSV format
- Automatic pagination for complete historical backfill
- Automatic handling of API rate limits

### Installation

```bash
pip install -r requirements.txt
```

### Usage

```bash
python collect_dogecoin_futures.py
```

### Configuration

Edit `config.py` to change settings:

- `SYMBOL`: Trading pair (default: DOGEUSDT)
- `INTERVAL`: Kline interval (default: 1h)
- `START_DATE`: Start date for data collection (default: 2021-01-01)
- `DATA_DIR`: Output directory (default: data)

### Output

Data is saved as CSV files in the `data/` directory with columns including:
- Timestamps (open_time, close_time)
- OHLC prices (open, high, low, close)
- Volume metrics
- Trade counts
