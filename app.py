from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Stock API is running!"

# Route to extract a specific stocks data using it's ticker and the desired period/time frame. 
@app.route("/stock/<ticker>/<period>")
def get_stock(ticker, period):
    # Extarct data from yf
    data = yf.Ticker(ticker).history(period=period)

    # Extract the closing prices
    prices = data["Close"].round(2).tolist()

    # Extract the dates
    dates = data.index.strftime("%Y-%m-%d").tolist()

    # Return JSON from a dictionary containing dates and prices
    return jsonify({"dates" : dates, "prices" : prices})
        






if __name__ == "__main__":
    app.run(debug=True)