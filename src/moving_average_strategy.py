import pandas as pd

def apply_moving_average_strategy(df, short_window=50, long_window=200):
    """
    Apply a simple moving average crossover strategy.
    
    Parameters:
    - df: DataFrame with price data
    - short_window: Period for the short-term moving average
    - long_window: Period for the long-term moving average
    
    Returns:
    - DataFrame with added signal column
    """
    # Calculate short and long-term moving averages
    df['short_ma'] = df['close'].rolling(window=short_window).mean()
    df['long_ma'] = df['close'].rolling(window=long_window).mean()
    
    # Generate signals
    df['signal'] = 0
    df.loc[df['short_ma'] > df['long_ma'], 'signal'] = 1  # Bullish signal
    df.loc[df['short_ma'] < df['long_ma'], 'signal'] = -1  # Bearish signal
    
    # Remove NaN values
    df.dropna(inplace=True)
    
    return df

if __name__ == "__main__":
    # Test the strategy
    from data_handler import load_data
    
    df = load_data('../data/BTCUSD_history.csv')
    df = apply_moving_average_strategy(df)
    
    print(df[['close', 'short_ma', 'long_ma', 'signal']].tail(10))