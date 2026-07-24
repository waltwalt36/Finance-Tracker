import pandas as pd
import pandas_ta as ta

'''
==========================================================
==========================================================
                    MANUAL TESTS
==========================================================
==========================================================
'''

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
# Test case: [10, 12, 11, 13, 14] returns [None, None, 11, 12, 13]
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

'''
==========================================================
==========================================================
                   SAMPLE DATA INPUT
==========================================================
==========================================================
'''

sample_prices = [150.0, 152.3, 149.8, 151.2, 153.4, 
                 152.1, 154.6, 156.2, 155.8, 157.3,
                 158.1, 156.9, 159.2, 160.4, 158.7,
                 161.2, 162.8, 161.5, 163.4, 164.2]

sample_series = pd.Series(sample_prices)
ta_rsi = ta.rsi(sample_series, length=14).tolist()

manual_rsi_values = manual_rsi(sample_prices)

print(ta_rsi)
print(manual_rsi_values)