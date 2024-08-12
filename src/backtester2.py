import pandas as pd
import numpy as np
import time

def backtest2(df, initial_capital=10000, risk_percent=0.01, tp_percent=0.02, sl_percent=0.01, max_trades=100, delay=0.5):
    """
    Backtest the Moving Average Crossover strategy with stop loss and take profit.
    
    Parameters:
    - df: DataFrame with price and signal data
    - initial_capital: Starting capital for the backtest
    - risk_percent: Percentage of account to risk per trade
    - tp_percent: Take profit percentage
    - sl_percent: Stop loss percentage
    - max_trades: Maximum number of trades to execute
    - delay: Delay between trades in seconds
    """
    df = df.copy()
    
    # Ensure all relevant columns are float
    float_columns = ['open', 'high', 'low', 'close', 'short_ma', 'long_ma']
    for col in float_columns:
        df[col] = df[col].astype(float)
    
    account_value = initial_capital
    current_position = 0.0
    trades_executed = 0
    entry_price = 0.0
    stop_loss_price = 0.0
    take_profit_price = 0.0
    
    print("Trade Log:")
    print("-----------------------------------------------------------------------------------------------------------------------")
    print("Trade # |  Action  |   Price   |  Position  | Account Value |   Stop Loss   |   Take Profit   |    P/L    ")
    print("-----------------------------------------------------------------------------------------------------------------------")

    for index, row in df.iterrows():
        current_price = row['close']
        
        # Check if we need to close the position due to stop loss or take profit
        if current_position > 0:
            if current_price <= stop_loss_price or current_price >= take_profit_price or row['signal'] == -1:
                # Close long position
                closing_price = min(max(current_price, stop_loss_price), take_profit_price)
                profit_loss = (closing_price - entry_price) * current_position
                account_value += profit_loss
                trades_executed += 1
                print(f"{trades_executed:7d} |   SELL   | {closing_price:9.2f} | {0:10.6f} | {account_value:13.2f} | {stop_loss_price:13.2f} | {take_profit_price:15.2f} | {profit_loss:9.2f}")
                current_position = 0.0
                time.sleep(delay)
        elif current_position < 0:
            if current_price >= stop_loss_price or current_price <= take_profit_price or row['signal'] == 1:
                # Close short position
                closing_price = max(min(current_price, stop_loss_price), take_profit_price)
                profit_loss = (entry_price - closing_price) * abs(current_position)
                account_value += profit_loss
                trades_executed += 1
                print(f"{trades_executed:7d} |   BUY    | {closing_price:9.2f} | {0:10.6f} | {account_value:13.2f} | {stop_loss_price:13.2f} | {take_profit_price:15.2f} | {profit_loss:9.2f}")
                current_position = 0.0
                time.sleep(delay)

        # Check if we need to open a new position
        if current_position == 0 and trades_executed < max_trades:
            if row['signal'] == 1:  # Buy signal
                entry_price = current_price
                position_size = (risk_percent * account_value) / (entry_price * sl_percent)
                current_position = position_size
                stop_loss_price = entry_price * (1 - sl_percent)
                take_profit_price = entry_price * (1 + tp_percent)
                trades_executed += 1
                print(f"{trades_executed:7d} |   BUY    | {entry_price:9.2f} | {current_position:10.6f} | {account_value:13.2f} | {stop_loss_price:13.2f} | {take_profit_price:15.2f} |    0.00   ")
                time.sleep(delay)
            elif row['signal'] == -1:  # Sell signal (short)
                entry_price = current_price
                position_size = (risk_percent * account_value) / (entry_price * sl_percent)
                current_position = -position_size
                stop_loss_price = entry_price * (1 + sl_percent)
                take_profit_price = entry_price * (1 - tp_percent)
                trades_executed += 1
                print(f"{trades_executed:7d} |   SELL   | {entry_price:9.2f} | {current_position:10.6f} | {account_value:13.2f} | {stop_loss_price:13.2f} | {take_profit_price:15.2f} |    0.00   ")
                time.sleep(delay)

        # Stop if we've reached the maximum number of trades
        if trades_executed >= max_trades:
            # Close any open position
            if current_position != 0:
                profit_loss = (current_price - entry_price) * current_position
                account_value += profit_loss
                trades_executed += 1
                print(f"{trades_executed:7d} |   CLOSE  | {current_price:9.2f} | {0:10.6f} | {account_value:13.2f} | {stop_loss_price:13.2f} | {take_profit_price:15.2f} | {profit_loss:9.2f}")
                time.sleep(delay)
            break

    return_percentage = ((account_value / initial_capital) - 1) * 100
    
    print("\nBacktest Summary:")
    print(f"Total Trades: {trades_executed}")
    
    return initial_capital, account_value, return_percentage

if __name__ == "__main__":
    # Test the backtester
    from data_handler import load_data, calculate_indicators
    from moving_average_strategy import apply_moving_average_strategy
    
    df = load_data('../data/BTCUSD_history.csv')
    df = calculate_indicators(df)
    df = apply_moving_average_strategy(df)
    
    initial_capital, final_value, return_percentage = backtest2(df, max_trades=100, delay=0.5)
    print(f"Initial Capital: ${initial_capital:.2f}")
    print(f"Final Value: ${final_value:.2f}")
    print(f"Return: {'+'if return_percentage >= 0 else '-'}{abs(return_percentage):.2f}%")