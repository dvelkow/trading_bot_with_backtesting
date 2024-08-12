import pandas as pd
import numpy as np
import time

def calculate_stop_loss(df, current_index, lookback=20):
    """Calculate stop loss based on recent low."""
    current_location = df.index.get_loc(current_index)
    start_location = max(0, current_location - lookback)
    recent_low = df['low'].iloc[start_location:current_location].min()
    return recent_low

def backtest(df, initial_capital=10000, tp_percent=0.02, risk_percent=0.01, max_trades=100, delay=0.5):
    """
    Backtest the breakout strategy with 1:2 risk-to-reward and dynamic position sizing.
    
    Parameters:
    - delay: Time delay in seconds between trades (default: 0.5 seconds)
    """
    df = df.copy()
    
    # Ensure all relevant columns are float
    float_columns = ['open', 'high', 'low', 'close']
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
        
        # Check if we need to close the position
        if current_position > 0:
            if current_price <= stop_loss_price or current_price >= take_profit_price or row['signal'] == -1:
                # Close position
                closing_price = min(max(current_price, stop_loss_price), take_profit_price)
                profit_loss = (closing_price - entry_price) * current_position
                account_value += profit_loss
                trades_executed += 1
                print(f"{trades_executed:7d} |   SELL   | {closing_price:9.2f} | {0:10.6f} | {account_value:13.2f} | {stop_loss_price:13.2f} | {take_profit_price:15.2f} | {profit_loss:9.2f}")
                current_position = 0.0
                time.sleep(delay)  # Add delay after closing a position

        # Check if we need to open a new position
        if current_position == 0 and row['signal'] == 1 and trades_executed < max_trades:
            entry_price = current_price
            stop_loss_price = calculate_stop_loss(df, index)
            position_size = (risk_percent * account_value) / (entry_price - stop_loss_price)
            take_profit_price = entry_price + 2 * (entry_price - stop_loss_price)
            
            # Open position
            current_position = position_size
            trades_executed += 1
            print(f"{trades_executed:7d} |   BUY    | {entry_price:9.2f} | {current_position:10.6f} | {account_value:13.2f} | {stop_loss_price:13.2f} | {take_profit_price:15.2f} |    0.00   ")
            time.sleep(delay)  # Add delay after opening a position

        # Stop if we've reached the maximum number of trades
        if trades_executed >= max_trades:
            # Close any open position
            if current_position > 0:
                account_value += current_position * current_price
                print(f"{trades_executed:7d} |   SELL   | {current_price:9.2f} | {0:10.6f} | {account_value:13.2f} | {stop_loss_price:13.2f} | {take_profit_price:15.2f} | {(current_price - entry_price) * current_position:9.2f}")
                time.sleep(delay)  # Add delay after final trade
            break

    return_percentage = ((account_value / initial_capital) - 1) * 100
    
    print("\nBacktest Summary:")
    print(f"Total Trades: {trades_executed}")
    
    return initial_capital, account_value, return_percentage

if __name__ == "__main__":
    # Test the backtester
    from data_handler import load_data, calculate_indicators
    from breakout_strategy import apply_breakout_strategy
    
    df = load_data('../data/BTCUSD_history.csv')
    df = calculate_indicators(df)
    df = apply_breakout_strategy(df)
    
    initial_capital, final_value, return_percentage = backtest(df, max_trades=100, delay=0.5)
    print(f"Initial Capital: ${initial_capital:.2f}")
    print(f"Final Value: ${final_value:.2f}")
    print(f"Return: {'+'if return_percentage >= 0 else '-'}{abs(return_percentage):.2f}%")