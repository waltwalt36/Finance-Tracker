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
| Database | PostgreSQL |
| Data     | yfinance (price history), Finnhub (news) |
| Analysis | pandas-ta (SMA, RSI, Bollinger Bands), TextBlob (sentiment) |
| Frontend | Vanilla HTML/CSS/JS, Chart.js 4 |

## Project Structure

```
Finance-Tracker/
├── backend/
│   ├── app.py              # Flask API
│   ├── .env                # API keys & DB password (not committed)
│   └── validation/
│       └── sanity_check.py # Validation tests for SMA & RSI calculations
└── frontend/
    └── stock_tracker_predictor.html
```

## Setup

### Prerequisites

- Python 3.10–3.13 (Python 3.14+ has compatibility issues with pandas-ta dependencies)
- A free [Finnhub API key](https://finnhub.io)

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install flask flask-cors yfinance finnhub-python pandas-ta textblob python-dotenv
```

**Note:** If you have Python 3.14+, install Python 3.13 first:
- **macOS:** Download from [python.org/downloads](https://www.python.org/downloads/), then use `python3.13 -m venv venv`
- **Other OS:** Similar process, ensure Python 3.13 is in your PATH

Create `backend/.env`:

```
FINNHUB_KEY=your_api_key_here
DB_PASSWORD=your_postgres_password
```

### Database Setup

Ensure PostgreSQL is installed and running. Create the database and tables:

```bash
createdb stock_tracker
psql stock_tracker < schema.sql  # or run the SQL below manually
```

**Or create tables manually:**

```sql
CREATE TABLE favorites (
  id SERIAL PRIMARY KEY,
  ticker VARCHAR(10) UNIQUE NOT NULL,
  saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE history (
  id SERIAL PRIMARY KEY,
  ticker VARCHAR(10) NOT NULL,
  viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE news (
  id SERIAL PRIMARY KEY,
  ticker VARCHAR(10) NOT NULL,
  headline TEXT NOT NULL,
  sentiment VARCHAR(20),
  url TEXT,
  source VARCHAR(100),
  fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
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
| GET | `/favorites` | Get all favorite tickers |
| POST | `/favorites/<ticker>` | Add a ticker to favorites |
| DELETE | `/favorites/<ticker>` | Remove a ticker from favorites |

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

Valid `period` values: `1mo`, `2mo`, `3mo`, `6mo`, `12mo`

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

### `/favorites` response fields

**GET** `/favorites`:
```json
{
  "favorites": [
    {
      "id": 1,
      "ticker": "AAPL",
      "saved_at": "2026-07-24T10:30:00"
    }
  ]
}
```

**POST** `/favorites/<ticker>`:
```json
{
  "message": "AAPL added to favorites"
}
```
Returns 201 on success, 409 if ticker is already in favorites.

**DELETE** `/favorites/<ticker>`:
```json
{
  "message": "AAPL deleted from favorites"
}
```
Returns 200 on success, 404 if ticker not found.

## Database

The application uses PostgreSQL with three tables:

### Schema

**favorites** — Stores user's favorite tickers
| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL PRIMARY KEY | Unique identifier |
| ticker | VARCHAR(10) UNIQUE NOT NULL | Stock ticker symbol |
| saved_at | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | When ticker was favorited |

**history** — Tracks user's search history
| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL PRIMARY KEY | Unique identifier |
| ticker | VARCHAR(10) NOT NULL | Stock ticker symbol |
| viewed_at | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | When ticker was viewed |

**news** — Caches news articles with sentiment scores
| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL PRIMARY KEY | Unique identifier |
| ticker | VARCHAR(10) NOT NULL | Stock ticker symbol |
| headline | TEXT NOT NULL | Article headline |
| sentiment | VARCHAR(20) | Bullish / Neutral / Bearish |
| url | TEXT | Link to full article |
| source | VARCHAR(100) | News source |
| fetched_at | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | When article was cached |

## Validation

**sanity_check.py** contains manual implementations of SMA (Simple Moving Average) and RSI (Relative Strength Index) calculations, used to verify that the pandas-ta library outputs match expected values. Run this file to compare manual calculations against pandas-ta results:

```bash
cd backend/validation
python sanity_check.py
```

This is useful for validating technical indicator accuracy and understanding the calculation logic behind the signals.

