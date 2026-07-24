import pandas as pd
import pandas_ta as ta
import math
import random

# Function manually calculates simple moving average
# Test case: [10, 11, 12, 13, 14] with period 3 returns [None, None, 11, 12, 13]
def manual_sma(prices, period):
    sma_values = []

    # Edge case check
    if not prices:
        return sma_values

    for i in range(len(prices)):
        if i < period - 1:
            sma_values.append(None)
        else:
            window = prices[i - period + 1 : i + 1]
            average = sum(window) / period
            sma_values.append(average)
    return sma_values

# Function manually calculates relative strength index (rsi)
# Test case: [10, 12, 11, 13, 14] 
def manual_rsi(prices, period=14):
    changes = []
    gains = []
    losses = []

    for i in range(len(prices) - 1):
        changes.append(prices[i+1] - prices[i])
    for n in changes:
        if n >= 0:
            gains.append(n)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(n * -1)
    
    rsi_values = [None] * period

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    if avg_loss != 0:
        rsi_values.append(100 - (100 / (1 + (avg_gain / avg_loss))))
    else:
        rsi_values.append(None)

    for i in range(period, len(gains)):
        current_gain = gains[i]
        current_loss = losses[i]

        avg_gain = (avg_gain * (period - 1) + current_gain) / period
        avg_loss = (avg_loss * (period - 1) + current_loss) / period

        if avg_loss != 0:
            rsi_values.append(100 - (100 / (1 + (avg_gain / avg_loss))))
        else:
            rsi_values.append(None)
    return rsi_values

sample_prices = [150.0, 152.3, 149.8, 151.2, 153.4, 
                 152.1, 154.6, 156.2, 155.8, 157.3,
                 158.1, 156.9, 159.2, 160.4, 158.7,
                 161.2, 162.8, 161.5, 163.4, 164.2,
                 165.1, 163.8, 166.2, 167.4, 165.9,
                 168.1, 169.3, 167.8, 170.2, 171.5,
                 169.8, 172.1, 173.4, 171.9, 174.2,
                 175.6, 173.8, 176.1, 177.3, 175.8,
                 178.2, 179.5, 177.8, 180.1, 181.4,
                 179.6, 182.1, 183.4, 181.7, 184.2]
random.seed(42)
extra = [sample_prices[-1] + random.uniform(-2, 2) for _ in range(100)]
sample_prices = sample_prices + extra

def compare_indicators(name, ta_values, manual_values, tolerance=0.01, warmup=100):
    passed = 0
    failed = 0
    for i in range(warmup, len(ta_values)):
        if ta_values[i] is None or manual_values[i] is None:
            continue
        if isinstance(ta_values[i], float) and math.isnan(ta_values[i]):
            continue

        if abs(ta_values[i] - manual_values[i]) < tolerance:
            passed += 1
        else:
            failed += 1

    print(f"{name} Summary: {passed} passed, {failed} failed")

# RSI comparison
sample_series = pd.Series(sample_prices)
ta_rsi = ta.rsi(sample_series, length=14).tolist()
manual_rsi_values = manual_rsi(sample_prices)
compare_indicators("RSI", ta_rsi, manual_rsi_values)

# SMA comparison
ta_sma = ta.sma(sample_series, length=20).tolist()
manual_sma_values = manual_sma(sample_prices, 20)
compare_indicators("SMA", ta_sma, manual_sma_values, warmup=20)