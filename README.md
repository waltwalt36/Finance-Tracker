# Finance Tracker — Stock Tracker & Predictor

A lightweight stock analysis tool with a Python/Flask backend and a single-page HTML frontend. Look up any ticker to see live price data, technical indicators, recent news with sentiment analysis, and a short-term price forecast.

## Features

- **Live price chart** — closing prices with 20-day and 50-day moving averages and Bollinger Bands
- **Technical signals** — RSI (14), MA crossover signal, trend direction, and an overall buy/sell/hold signal
- **Key metrics** — current price, period change, RSI value, and daily volatility
- **News feed** — last 12 hours of company news via Finnhub, each headline scored Bullish / Neutral / Bearish using TextBlob sentiment analysis
- **5-day forecast** — simulated trend extrapolation with a confidence band
- **Time range selector** — 1M, 2M, 3M, 6M, 1Y
- **Ticker search** — quick-select badges for AAPL, MSFT, NVDA, TSLA, AMZN, plus a free-text search bar for any ticker

## Tech Stack

| Layer    | Technology |
|----------|------------|
| Backend  | Python, Flask, Flask-CORS |
| Data     | yfinance (price history), Finnhub (news) |
| Analysis | pandas-ta (SMA, RSI, Bollinger Bands), TextBlob (sentiment) |
| Frontend | Vanilla HTML/CSS/JS, Chart.js 4 |

## Project Structure

```
Finance-Tracker/
├── backend/
│   ├── app.py        # Flask API
│   └── .env          # API keys (not committed)
└── frontend/
    └── stock_tracker_predictor.html
```

## Setup

### Prerequisites

- Python 3.10+
- A free [Finnhub API key](https://finnhub.io)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install flask flask-cors yfinance finnhub-python pandas-ta textblob python-dotenv
```

Create `backend/.env`:

```
FINNHUB_KEY=your_api_key_here
```

Start the server:

```bash
python app.py
```

The API runs at `http://127.0.0.1:5000`.

### Frontend

Open `frontend/stock_tracker_predictor.html` directly in a browser. It expects the backend running on port 5000.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/stock/<ticker>/<period>` | Price history + indicators (e.g. `/stock/AAPL/1mo`) |
| GET | `/news/<ticker>` | Last ~12 hours of news with sentiment (e.g. `/news/AAPL`) |

### `/stock` response fields

```json
{
  "dates": ["2025-01-01", ...],
  "prices": [150.0, ...],
  "volume": [1000000, ...],
  "moving_average_20": [148.5, ...],
  "moving_average_50": [145.2, ...],
  "rsi": [52.3, ...],
  "bollinger_lower": [144.1, ...],
  "bollinger_upper": [156.3, ...]
}
```

### `/news` response fields

```json
{
  "news": [
    {
      "datetime": 1719360000,
      "headline": "Apple Reports Record Q2 Earnings",
      "summary": "Apple Inc. reported earnings that beat analyst expectations...",
      "source": "Reuters",
      "url": "https://...",
      "sentiment": "Bullish"
    }
  ]
}
```

Returns up to 10 articles. `sentiment` is appended server-side and will be `"Bullish"`, `"Bearish"`, or `"Neutral"`. All other fields come directly from the Finnhub API. `datetime` is a UNIX timestamp.

Valid `period` values: `1mo`, `2mo`, `3mo`, `6mo`, `12mo`
