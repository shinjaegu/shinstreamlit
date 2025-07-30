# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta

# 개선된 UI 컴포넌트 및 기능 불러오기
from styles import CSS_CODE
from ui_components import render_main_logo, render_header, render_info_footer, ICON_ANALYSIS
from stock_model import run_prediction_pipeline
from calculations import calculate_strategy_performance

# --- 1. 페이지 및 CSS 설정 ---
st.set_page_config(
    page_title="투자침팬치",
    page_icon="🐵",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(CSS_CODE, unsafe_allow_html=True)

# --- 2. 종목 데이터 및 검색 시스템 구축 ---
STOCKS_DATA = [
    # Top 20
    {'name': 'NVIDIA', 'ticker': 'NVDA', 'aliases': ['엔비디아']},
    {'name': 'Microsoft', 'ticker': 'MSFT', 'aliases': ['마이크로소프트']},
    {'name': 'Apple', 'ticker': 'AAPL', 'aliases': ['애플']},
    {'name': 'Alphabet (Google)', 'ticker': 'GOOGL', 'aliases': ['알파벳', '구글']},
    {'name': 'Amazon', 'ticker': 'AMZN', 'aliases': ['아마존']},
    {'name': 'Meta Platforms', 'ticker': 'META', 'aliases': ['메타', '페이스북']},
    {'name': 'Berkshire Hathaway', 'ticker': 'BRK-B', 'aliases': ['버크셔해서웨이']},
    {'name': 'Eli Lilly', 'ticker': 'LLY', 'aliases': ['일라이릴리']},
    {'name': 'Broadcom', 'ticker': 'AVGO', 'aliases': ['브로드컴']},
    {'name': 'Tesla', 'ticker': 'TSLA', 'aliases': ['테슬라']},
    {'name': 'Visa', 'ticker': 'V', 'aliases': ['비자']},
    {'name': 'JPMorgan Chase', 'ticker': 'JPM', 'aliases': ['jp모건']},
    {'name': 'Walmart', 'ticker': 'WMT', 'aliases': ['월마트']},
    {'name': 'Exxon Mobil', 'ticker': 'XOM', 'aliases': ['엑손모빌']},
    {'name': 'UnitedHealth Group', 'ticker': 'UNH', 'aliases': ['유나이티드헬스']},
    {'name': 'Mastercard', 'ticker': 'MA', 'aliases': ['마스터카드']},
    {'name': 'Johnson & Johnson', 'ticker': 'JNJ', 'aliases': ['존슨앤존슨']},
    {'name': 'Procter & Gamble', 'ticker': 'PG', 'aliases': ['p&g', '피앤지']},
    {'name': 'Home Depot', 'ticker': 'HD', 'aliases': ['홈디포']},
    {'name': 'Costco', 'ticker': 'COST', 'aliases': ['코스트코']},
    # Next 16
    {'name': 'Merck & Co', 'ticker': 'MRK', 'aliases': ['머크']},
    {'name': 'Oracle', 'ticker': 'ORCL', 'aliases': ['오라클']},
    {'name': 'Chevron', 'ticker': 'CVX', 'aliases': ['쉐브론']},
    {'name': 'AbbVie', 'ticker': 'ABBV', 'aliases': ['애브비']},
    {'name': 'Salesforce', 'ticker': 'CRM', 'aliases': ['세일즈포스']},
    {'name': 'Netflix', 'ticker': 'NFLX', 'aliases': ['넷플릭스']},
    {'name': 'AMD', 'ticker': 'AMD', 'aliases': ['에이엠디']},
    {'name': 'Coca-Cola', 'ticker': 'KO', 'aliases': ['코카콜라']},
    {'name': 'PepsiCo', 'ticker': 'PEP', 'aliases': ['펩시']},
    {'name': 'Bank of America', 'ticker': 'BAC', 'aliases': ['뱅크오브아메리카']},
    {'name': 'Adobe', 'ticker': 'ADBE', 'aliases': ['어도비']},
    {'name': 'Linde', 'ticker': 'LIN', 'aliases': ['린데']},
    {'name': 'Qualcomm', 'ticker': 'QCOM', 'aliases': ['퀄컴']},
    {'name': 'Cisco Systems', 'ticker': 'CSCO', 'aliases': ['시스코']},
    {'name': 'T-Mobile US', 'ticker': 'TMUS', 'aliases': ['티모바일']},
    {'name': 'Intel', 'ticker': 'INTC', 'aliases': ['인텔']}
]
TOP_STOCKS = {stock['name']: stock['ticker'] for stock in STOCKS_DATA}
TICKER_LOOKUP = {}
for stock in STOCKS_DATA:
    keys = [stock['name'].lower(), stock['ticker'].lower()] + [alias.lower() for alias in stock['aliases']]
    for key in keys:
        TICKER_LOOKUP[key] = stock['ticker']

# --- 3. UI 상태 초기화 및 컨트롤 렌더링 함수 ---

if 'search_term' not in st.session_state:
    st.session_state.search_term = 'Tesla'
if 'initial_investment' not in st.session_state:
    st.session_state.initial_investment = 10000

def update_search_term(stock_name):
    st.session_state.search_term = stock_name

def render_controls_mobile():
    """모바일 뷰를 위한 컨트롤 렌더링. 위젯 레이블이 보이지 않음."""
    st.text_input(
        "종목명 또는 코드 검색",
        key='search_mobile',
        value=st.session_state.search_term,
        on_change=lambda: st.session_state.update(search_term=st.session_state.search_mobile),
        placeholder="종목명 또는 코드 검색 (예: Apple, NVDA)",
        label_visibility="collapsed"
    )
    st.number_input(
        "초기 투자금 ($)",
        min_value=1000,
        max_value=10000000,
        key='invest_mobile',
        value=st.session_state.initial_investment,
        step=1000,
        on_change=lambda: st.session_state.update(initial_investment=st.session_state.invest_mobile),
        label_visibility="collapsed"
    )
    return st.button("분석 실행", use_container_width=True, type="primary", key='run_mobile')

def render_controls_sidebar():
    """사이드바를 위한 컨트롤 렌더링. 위젯 레이블이 보임."""
    st.text_input(
        "종목명 또는 코드 검색",
        key='search_sidebar',
        value=st.session_state.search_term,
        on_change=lambda: st.session_state.update(search_term=st.session_state.search_sidebar),
        placeholder="종목명 또는 코드 입력 (예: Apple, NVDA)"
    )
    st.number_input(
        "초기 투자금 ($)",
        min_value=1000,
        max_value=10000000,
        key='invest_sidebar',
        value=st.session_state.initial_investment,
        step=1000,
        on_change=lambda: st.session_state.update(initial_investment=st.session_state.invest_sidebar)
    )
    return st.button("분석 실행", use_container_width=True, type="primary", key='run_sidebar')


# --- 4. 모바일 및 사이드바 UI 구성 ---

# 모바일용 헤더 (st.expander를 컨테이너로 활용)
mobile_header_expander = st.expander("", expanded=True)
with mobile_header_expander:
    render_main_logo()
    st.divider()
    st.markdown("<h6>분석 설정</h6>", unsafe_allow_html=True)
    mobile_run_button = render_controls_mobile()

# 데스크탑용 사이드바
with st.sidebar:
    render_main_logo()
    st.divider()
    st.markdown("<h6>분석 설정</h6>", unsafe_allow_html=True)
    sidebar_run_button = render_controls_sidebar()


# --- 5. 메인 대시보드 렌더링 ---
run_analysis = mobile_run_button or sidebar_run_button

if not run_analysis:
    render_header("시가총액 상위 36 종목", "⭐")
    st.markdown("관심 있는 종목의 카드를 클릭하면 왼쪽 검색창에 자동으로 입력됩니다.")

    cols = st.columns(6)
    stock_items = list(TOP_STOCKS.items())

    for i, (name, stock_ticker) in enumerate(stock_items):
        with cols[i % 6]:
            st.button(
                f"{name} ({stock_ticker})",
                key=f"stock_{stock_ticker}",
                on_click=update_search_term,
                args=(name,),
                use_container_width=True
            )

    footer_html = render_info_footer()
    st.markdown(f"<div class='info-footer'>{footer_html}</div>", unsafe_allow_html=True)

    st.stop()

# --- 6. 분석 실행 로직 ---
cleaned_search_term = st.session_state.search_term.strip().lower()
ticker = TICKER_LOOKUP.get(cleaned_search_term)


if not ticker:
    st.error(f"'{st.session_state.search_term}'에 해당하는 종목을 찾을 수 없습니다. 종목명 또는 코드를 다시 확인해주세요.")
    st.info("현재는 시가총액 상위 36개 미국 주식에 대한 검색을 지원합니다.")
    st.stop()

render_header(f"{ticker} 분석 리포트", ICON_ANALYSIS)

try:
    with st.spinner("데이터를 다운로드하고 AI 모델을 분석 중입니다. 잠시만 기다려주세요..."):
        end_date = date.today()
        train_start_date = end_date - timedelta(days=7*365)
        result_df, plot_fig = run_prediction_pipeline(ticker, train_start_date, end_date)
        strategy_metrics, buy_hold_metrics, chimp_metrics, asset_df = calculate_strategy_performance(result_df, st.session_state.initial_investment)

    st.toast(f"{ticker} 분석이 완료되었습니다!")

    # 탭에 아이콘 추가
    tab1, tab2, tab3 = st.tabs(["**성과 요약**", "**자산 추이 분석**", "**AI 모델 예측 상세**"])

    with tab1:
        st.markdown("<h5 class='section-title'>전략별 최종 성과</h5>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="AI 예측 전략", value=f"${strategy_metrics['Final Value']:,.2f}", delta=f"{strategy_metrics['Total Return'] * 100:.2f}% 총 수익률")
        with col2:
            st.metric(label="단순 보유 전략", value=f"${buy_hold_metrics['Final Value']:,.2f}", delta=f"{buy_hold_metrics['Total Return'] * 100:.2f}% 총 수익률")
        with col3:
            st.metric(label="침팬치 전략 (동전 던지기)", value=f"${chimp_metrics['Final Value']:,.2f}", delta=f"{chimp_metrics['Total Return'] * 100:.2f}% 총 수익률")

        st.markdown("<h5 class='section-title'>주요 성과 지표 (KPI)</h5>", unsafe_allow_html=True)
        metrics_data = {
            '지표': ['최종 자산', '총 수익률', '연평균 수익률(CAGR)', '최대 낙폭(MDD)'],
            'AI 예측 전략': [ f"${strategy_metrics['Final Value']:,.2f}", f"{strategy_metrics['Total Return'] * 100:,.2f}%", f"{strategy_metrics['CAGR'] * 100:,.2f}%", f"{strategy_metrics['MDD'] * 100:,.2f}%" ],
            '단순 보유 전략': [ f"${buy_hold_metrics['Final Value']:,.2f}", f"${buy_hold_metrics['Total Return'] * 100:,.2f}%", f"{buy_hold_metrics['CAGR'] * 100:,.2f}%", f"{buy_hold_metrics['MDD'] * 100:,.2f}%" ],
            '침팬치 전략 (동전 던지기)': [ f"${chimp_metrics['Final Value']:,.2f}", f"{chimp_metrics['Total Return'] * 100:,.2f}%", f"{chimp_metrics['CAGR'] * 100:,.2f}%", f"{chimp_metrics['MDD'] * 100:,.2f}%" ]
        }
        st.table(pd.DataFrame(metrics_data).set_index('지표'))

    with tab2:
        st.markdown("<h5 class='section-title'>기간별 자산 가치 변화 (최근 1년)</h5>", unsafe_allow_html=True)
        asset_fig = px.line(
            asset_df,
            x=asset_df.index,
            y=asset_df.columns,
            labels={'value': '자산 가치 ($)', 'index': '날짜', 'variable': '전략'},
            color_discrete_map={'예측 전략': '#D4AF37', '단순 보유 전략': '#6c757d', '침팬치 전략': '#3B82F6'}
        )
        asset_fig.update_layout(
            height=500,
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            margin=dict(l=0, r=20, t=20, b=20)
        )
        st.plotly_chart(asset_fig, use_container_width=True)

        st.markdown("<h5 class='section-title'>월별 자산 요약 (월말 기준)</h5>", unsafe_allow_html=True)
        
        monthly_asset_df = asset_df.resample('M').last()

        if not monthly_asset_df.empty:
            monthly_asset_df['차이 (AI vs 보유)'] = monthly_asset_df['예측 전략'] - monthly_asset_df['단순 보유 전략']
            
            table_df = pd.DataFrame({
                '연도-월': monthly_asset_df.index.strftime('%Y-%m'),
                'AI 예측 전략': monthly_asset_df['예측 전략'],
                '단순 보유 전략': monthly_asset_df['단순 보유 전략'],
                '침팬치 전략 (동전 던지기)': monthly_asset_df['침팬치 전략'],
                '차이 (AI vs 보유)': monthly_asset_df['차이 (AI vs 보유)']
            })

            table_df.set_index('연도-월', inplace=True)
            transposed_df = table_df.T

            for col in transposed_df.columns:
                transposed_df[col] = transposed_df[col].apply(lambda x: f"${x:,.2f}")
            
            transposed_df.index.name = "전략"

            st.markdown(transposed_df.to_html(index=True), unsafe_allow_html=True)
        else:
            st.warning("월별 데이터를 생성할 수 없어 요약 테이블을 표시할 수 없습니다.")

    with tab3:
        st.markdown("<h5 class='section-title'>AI 모델의 주가 예측 vs 실제 주가</h5>", unsafe_allow_html=True)
        st.pyplot(plot_fig)

except Exception as e:
    st.error(f"'{ticker}' 분석 중 오류가 발생했습니다: {e}")