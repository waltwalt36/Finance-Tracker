from datetime import datetime, timedelta
from flask import Flask, jsonify
from textblob import TextBlob
from flask_cors import CORS
import pandas_ta as ta
import yfinance as yf
import finnhub
import math
import os

app = Flask(__name__)
CORS(app)

# Initalize finhub using API key
api_key = os.environ.get("FINNHUB_KEY")
finnhub_client = finnhub.Client(api_key=api_key)

# Helper function to clean up the data pandas returns (particularly the NaN values)
def clean(lst):
    return [None if isinstance(x, float) and math.isnan(x) else x for x in lst]

# Helper function to calculate sentiment of a given article
def get_sentiment(news):
    score = TextBlob(news).sentiment.polarity
    # Logic to determine if the news is bullish or bearish or neutral (very simple)
    if score > 0.1:
        return "Bullish"
    elif score < -0.1:
        return "Bearish"
    else:
        return "Neutral"

@app.route("/")
def home():
    return "Stock API is running!"

# Route to extract a specific stocks data using it's ticker and the desired period/time frame. 
@app.route("/stock/<ticker>/<period>")
def get_stock(ticker, period):
    # Extarct data from yf
    data = yf.Ticker(ticker).history(period=period)

    # Check to see if ticker is invalid or no data available
    if data.empty:
        return jsonify({"error" : "Invalid ticker or no data available"}), 400
    
    # Extract the closing prices
    prices = data["Close"].round(2).tolist()

    # Extract the dates
    dates = data.index.strftime("%Y-%m-%d").tolist()

    # Extract the volume
    volume = data["Volume"].tolist()

    # Calculate the 20 day moving average using pandas ta (handle failures gracefully)
    result_20 = ta.sma(data["Close"], length=20)
    moving_average_20 = result_20.round(2).tolist() if result_20 is not None else []

    # Calculate the 50 day moving average (handle failures gracefully)
    result_50 = ta.sma(data["Close"], length=50)
    moving_average_50 = result_50.round(2).tolist() if result_50 is not None else []

    # Calculate the RSI using ta.rsi() (handles failures gracefully)
    result_rsi = ta.rsi(data["Close"])
    rsi = result_rsi.round(2).tolist() if result_rsi is not None else []

    # Return JSON from a dictionary containing dates and prices
    return jsonify({"dates" : dates, 
                    "prices" : clean(prices),
                    "volume" : volume, 
                    "moving_average_20" : clean(moving_average_20), 
                    "moving_average_50" : clean(moving_average_50), 
                    "rsi" : clean(rsi)
                    })

# New route to extract news for a specified ticker
@app.route("/news/<ticker>")
def get_news(ticker):
    # Initialize two variables to store todays date and the date one week ago
    end_date = datetime.today().strftime("%Y-%m-%d")
    start_date = (datetime.today() - timedelta(days=0.5)).strftime("%Y-%m-%d")

    # Fetch news using ticker, end date, and start date
    news = finnhub_client.company_news(ticker, _from=start_date, to=end_date)

    # Validation check to see if no news is returned
    if not news:
        return jsonify({"error": "No news found for this ticker"}), 404

    # Iterate through all news articles and get the sentiment of the headline
    for article in news:
        article["sentiment"] = get_sentiment(article["headline"])

    return jsonify({"news": news[:10]})


if __name__ == "__main__":
    app.run(debug=True)