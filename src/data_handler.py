import pandas as pd

def load_data(file_path):
    """
    Load and preprocess the Binance BTCUSDT hourly data from CSV.
    """
    df = pd.read_csv(file_path, parse_dates=['Date'])
    df.set_index('Date', inplace=True)
    df.sort_index(inplace=True, ascending=True)  # Ensure chronological order
    
    # Rename columns to lowercase for consistency
    df.columns = [col.lower() for col in df.columns]
    
    # Convert string columns to numeric
    for col in ['open', 'high', 'low', 'close', 'volume btc', 'volume usdt']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

def calculate_indicators(df):
    """
    Calculate indicators for the breakout strategy.
    """
    # Calculate 20-period high and low
    df['20_period_high'] = df['high'].rolling(window=20).max()
    df['20_period_low'] = df['low'].rolling(window=20).min()
    
    # Calculate Average True Range (ATR) for volatility
    df['tr'] = pd.concat([df['high'] - df['low'], 
                          abs(df['high'] - df['close'].shift(1)), 
                          abs(df['low'] - df['close'].shift(1))], axis=1).max(axis=1)
    df['atr'] = df['tr'].rolling(window=14).mean()
    
    return df

if __name__ == "__main__":
    # Test the functions
    df = load_data('../data/BTCUSD_history.csv')
    df = calculate_indicators(df)
    print(df.tail())
    print(df.columns)