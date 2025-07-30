# stock_model.py
import yfinance as yf
import pandas as pd
import numpy as np
from lightgbm import LGBMRegressor
import matplotlib.pyplot as plt
import re

FEATURES = ['Open', 'High', 'Low', 'Close', 'Volume', 'Return', 'Volatility', 'MA5', 'MA10', 'MACD']

def fetch_stock_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end, group_by="ticker", progress=False, auto_adjust=False)
    if df.empty: raise ValueError(f"'{ticker}'에 대한 데이터를 가져올 수 없습니다. Yahoo Finance에서 유효한 종목 코드인지 확인하세요.")
    if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.droplevel(0)
    df.dropna(inplace=True)
    return df

def create_features(df):
    df_feat = df.copy()
    df_feat['Return'] = df_feat['Close'].pct_change()
    df_feat['Volatility'] = df_feat['Return'].rolling(window=21).std()
    df_feat['MA5'] = df_feat['Close'].rolling(window=5).mean()
    df_feat['MA10'] = df_feat['Close'].rolling(window=10).mean()
    exp12 = df_feat['Close'].ewm(span=12, adjust=False).mean()
    exp26 = df_feat['Close'].ewm(span=26, adjust=False).mean()
    df_feat['MACD'] = exp12 - exp26
    df_feat['Target'] = df_feat['Close'].shift(-1)
    df_feat.dropna(inplace=True)
    return df_feat

def train_and_predict(train_df, test_df):
    train_df_cleaned, test_df_cleaned = train_df.copy(), test_df.copy()
    def clean_name(name): return re.sub(r'[^A-Za-z0-9_]+', '', name)
    original_to_clean_map = {col: clean_name(col) for col in train_df_cleaned.columns}
    train_df_cleaned.rename(columns=original_to_clean_map, inplace=True)
    test_df_cleaned.rename(columns=original_to_clean_map, inplace=True)
    clean_features = [clean_name(f) for f in FEATURES]
    clean_target = clean_name('Target')
    X_train, y_train = train_df_cleaned[clean_features], train_df_cleaned[clean_target]
    X_test = test_df_cleaned[clean_features]
    model = LGBMRegressor(n_estimators=200, learning_rate=0.01, num_leaves=31, random_state=42, n_jobs=-1, verbose=-1)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    result_df = test_df.copy()
    result_df['Predicted_Close'] = predictions
    return result_df

def plot_predictions(result_df):
    # CSS 변수와 색상 통일
    PRIMARY_COLOR, SECONDARY_COLOR = '#D4AF37', '#6c757d'
    TEXT_COLOR, BG_COLOR, PLOT_BG_COLOR, GRID_COLOR = '#fafafa', '#0f1116', '#1c202a', '#2a2f3b'
    
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Noto Sans KR']
    plt.rcParams['axes.unicode_minus'] = False # 마이너스 폰트 깨짐 방지
    
    fig, ax = plt.subplots(figsize=(14, 7), facecolor=BG_COLOR)
    ax.set_facecolor(PLOT_BG_COLOR)

    ax.plot(result_df.index, result_df['Close'], label='actual closing price', color=SECONDARY_COLOR, alpha=0.9, linewidth=2)
    ax.plot(result_df.index, result_df['Predicted_Close'], label='AI predicted closing price', color=PRIMARY_COLOR, linestyle='--', alpha=0.9, linewidth=2)

    ax.set_title("Actual closing price vs. AI predicted closing price (last 1 year)", fontsize=16, color=TEXT_COLOR, pad=20, weight='bold')
    ax.set_xlabel("Date", fontsize=12, color=TEXT_COLOR)
    ax.set_ylabel("Price ($)", fontsize=12, color=TEXT_COLOR)
    ax.tick_params(axis='x', colors=TEXT_COLOR); ax.tick_params(axis='y', colors=TEXT_COLOR)
    for spine in ax.spines.values(): spine.set_edgecolor(GRID_COLOR)
    
    legend = ax.legend(facecolor=PLOT_BG_COLOR, edgecolor=GRID_COLOR, fontsize=11, framealpha=0.8)
    for text in legend.get_texts(): text.set_color(TEXT_COLOR)
    ax.grid(True, color=GRID_COLOR, linestyle='--', linewidth=0.5, alpha=0.5)
    fig.tight_layout()
    return fig

def run_prediction_pipeline(ticker, start_date, end_date):
    full_df = fetch_stock_data(ticker, start_date, end_date)
    df_featured = create_features(full_df)
    # 예측 기간을 명확하게 최근 1년으로 설정
    predict_period_start = pd.to_datetime(end_date) - pd.to_timedelta('365 days')
    train_df = df_featured[df_featured.index < predict_period_start]
    test_df = df_featured[df_featured.index >= predict_period_start]
    if train_df.empty or test_df.empty: raise ValueError("모델 학습 또는 예측을 위한 데이터가 부족합니다. 분석 기간을 확인해주세요.")
    result_df = train_and_predict(train_df, test_df)
    prediction_plot = plot_predictions(result_df)
    return result_df, prediction_plot