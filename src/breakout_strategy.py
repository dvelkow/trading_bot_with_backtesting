import pandas as pd

def apply_breakout_strategy(df):
    """
    Apply the breakout strategy to the hourly data.
    
    Buy signal: Price breaks above the 20-period high
    Sell signal: Price breaks below the 20-period low
    """
    df['signal'] = 0  # 0 represents no signal
    
    # Buy signal
    df.loc[df['close'] > df['20_period_high'].shift(1), 'signal'] = 1
    
    # Sell signal
    df.loc[df['close'] < df['20_period_low'].shift(1), 'signal'] = -1
    
    return df

if __name__ == "__main__":
    # Test the strategy
    from data_handler import load_data, calculate_indicators
    
    df = load_data('../data/BTCUSD_history.csv')
    df = calculate_indicators(df)
    df = apply_breakout_strategy(df)
    
    print(df[['close', '20_period_high', '20_period_low', 'signal']].tail(20))