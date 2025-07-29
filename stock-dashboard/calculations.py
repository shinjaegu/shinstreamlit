# calculations.py

import pandas as pd
import numpy as np

def calculate_strategy_performance(result_df, initial_investment):
    if result_df.empty:
        return {}, {}, {}, pd.DataFrame()

    # --- 1. 예측 기반 투자 전략 ---
    result_df['Signal'] = np.where(result_df['Predicted_Close'] > result_df['Close'], 1, 0)
    result_df['Daily_Return'] = result_df['Close'].pct_change()
    result_df['Strategy_Return'] = result_df['Signal'].shift(1) * result_df['Daily_Return']
    result_df.fillna(0, inplace=True)
    result_df['Strategy_Cumulative_Return'] = (1 + result_df['Strategy_Return']).cumprod()
    result_df['Strategy_Asset'] = initial_investment * result_df['Strategy_Cumulative_Return']

    # --- 2. 단순 보유 (Buy and Hold) 전략 ---
    result_df['Buy_Hold_Cumulative_Return'] = result_df['Close'] / result_df['Close'].iloc[0]
    result_df['Buy_Hold_Asset'] = initial_investment * result_df['Buy_Hold_Cumulative_Return']

    # --- 3. 침팬치 (동전 던지기) 전략 ---
    np.random.seed(42) # 결과 재현을 위한 시드 설정
    result_df['Chimp_Signal'] = np.random.randint(0, 2, size=len(result_df))
    result_df['Chimp_Return'] = result_df['Chimp_Signal'].shift(1) * result_df['Daily_Return']
    result_df.fillna(0, inplace=True)
    result_df['Chimp_Cumulative_Return'] = (1 + result_df['Chimp_Return']).cumprod()
    result_df['Chimp_Asset'] = initial_investment * result_df['Chimp_Cumulative_Return']


    # --- 4. 성과 지표 계산 ---
    strategy_metrics = calculate_metrics(result_df['Strategy_Asset'])
    buy_hold_metrics = calculate_metrics(result_df['Buy_Hold_Asset'])
    chimp_metrics = calculate_metrics(result_df['Chimp_Asset'])
    
    # 시각화를 위한 자산 데이터프레임 (컬럼명 한국어 변경)
    asset_df = result_df[['Strategy_Asset', 'Buy_Hold_Asset', 'Chimp_Asset']].rename(columns={
        'Strategy_Asset': '예측 전략',
        'Buy_Hold_Asset': '단순 보유 전략',
        'Chimp_Asset': '침팬치 전략'
    })

    return strategy_metrics, buy_hold_metrics, chimp_metrics, asset_df

def calculate_metrics(asset_series):
    if asset_series.empty or asset_series.iloc[0] == 0:
        return {"Final Value": 0, "Total Return": 0, "CAGR": 0, "MDD": 0}

    final_value = asset_series.iloc[-1]
    initial_value = asset_series.iloc[0]
    total_return = (final_value / initial_value) - 1
    
    years = (asset_series.index[-1] - asset_series.index[0]).days / 365.25
    cagr = ((final_value / initial_value) ** (1 / years) - 1) if years > 0 and initial_value > 0 else 0

    rolling_max = asset_series.cummax()
    drawdown = (asset_series - rolling_max) / rolling_max
    mdd = drawdown.min()

    return {
        "Final Value": final_value,
        "Total Return": total_return,
        "CAGR": cagr,
        "MDD": mdd
    }