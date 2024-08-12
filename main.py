from src.data_handler import load_data, calculate_indicators
from src.breakout_strategy import apply_breakout_strategy
from src.moving_average_strategy import apply_moving_average_strategy
from src.backtester import backtest
from src.backtester2 import backtest2

def main():
    # Load and preprocess data
    df = load_data('data/BTCUSD_history.csv')
    df = calculate_indicators(df)
    
    # Ask user which backtest to run
    print("Which backtest would you like to run?")
    print("1. Breakout Strategy")
    print("2. Moving Average Crossover Strategy")
    
    choice = input("Enter 1 or 2: ")
    
    # parameters
    initial_capital = 10000
    risk_percent = 0.01 
    tp_percent = 0.01  
    sl_percent = 0.01 
    max_trades = 100 
    delay = 0.05 
    
    if choice == '1':
        strategy_name = "Breakout"
        df = apply_breakout_strategy(df)
        initial_investment, final_value, return_percentage = backtest(
            df, 
            initial_capital=initial_capital, 
            tp_percent=tp_percent,
            risk_percent=risk_percent,
            max_trades=max_trades,
            delay=delay
        )
    elif choice == '2':
        strategy_name = "Moving Average Crossover"
        df = apply_moving_average_strategy(df)
        initial_investment, final_value, return_percentage = backtest2(
            df, 
            initial_capital=initial_capital, 
            risk_percent=risk_percent,
            tp_percent=tp_percent,
            sl_percent=sl_percent,
            max_trades=max_trades,
            delay=delay
        )
    else:
        print("Invalid choice. Exiting.")
        return
    
    print(f"\nStrategy: {strategy_name}")
    print(f"Initial Investment: ${initial_investment:.2f}")
    print(f"Final Value: ${final_value:.2f}")
    print(f"Return: {'+'if return_percentage >= 0 else '-'}{abs(return_percentage):.2f}%")

if __name__ == "__main__":
    main()