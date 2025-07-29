# styles.py

CSS_CODE = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
<style>
    :root {
        --primary-color: #D4AF37;
        --primary-color-hover: #EACD6F;
        --plus-color: #3B82F6;
        --plus-color-hover: #60A5FA;
        --minus-color: #EF4444;
        --minus-color-hover: #F87171;
        --text-color: #fafafa;
        --text-color-light: #aaa;
        --bg-color: #0f1116;
        --secondary-bg-color: #1c202a;
        --border-color: #2a2f3b;
        --hover-bg-color: #252a36;
    }
    html, body, [class*="st-"] {
        font-family: 'Noto Sans KR', sans-serif;
    }
    /* 헤더 등 불필요한 요소 숨김 */
    [data-testid="stHeader"], [data-testid="stSidebarHeader"], [data-testid="stLogoSpacer"] {
        display: none !important;
    }
    div[data-testid="stSidebarContent"] {
        padding: 20px 15px !important;
        background-color: var(--bg-color);
    }
    div.block-container {
        padding: 1.5rem 2.5rem 3rem 2.5rem !important;
    }
    .logo-container {
        display: flex; align-items: center; gap: 0.75rem;
        margin-bottom: 0.5rem;
    }
    .logo-text { font-size: 1.5rem; color: var(--text-color); font-weight: 700; }
    .logo-svg svg { width: 32px; height: 32px; color: var(--primary-color); }

    div[data-testid="stSidebarContent"] h6,
    [data-testid="stExpander"] h6 {
        color: var(--text-color); font-weight: 500; margin-bottom: 0.75rem;
    }

    /* --- 입력창(st.text_input, st.number_input) 스타일 --- */
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input {
        background-color: var(--secondary-bg-color);
        color: var(--text-color);
        border: 1px solid var(--border-color);
        transition: border-color 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
    }
    [data-testid="stTextInput"] input:focus,
    [data-testid="stNumberInput"] input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 1px var(--primary-color);
    }

    /* --- 숫자 입력 (+/-) 버튼 스타일 --- */
    [data-testid="stNumberInput"] button {
        transition: background-color 0.2s ease-in-out, border-color 0.2s ease-in-out;
        border: 1.5px solid transparent !important;
    }
    [data-testid="stNumberInput"] button:first-of-type {
        background-color: var(--border-color);
        color: var(--text-color-light);
        border-color: var(--border-color) !important;
    }
    [data-testid="stNumberInput"] button:first-of-type:hover {
        background-color: var(--hover-bg-color);
        border-color: var(--hover-bg-color) !important;
    }
    [data-testid="stNumberInput"] button:last-of-type {
        background-color: var(--primary-color);
        color: var(--bg-color);
        border-color: var(--primary-color) !important;
    }
    [data-testid="stNumberInput"] button:last-of-type:hover {
        background-color: var(--primary-color-hover);
        border-color: var(--primary-color-hover) !important;
    }

    /* --- 종목 선택 버튼(카드) 스타일 --- */
    div[data-testid="stButton"] > button {
        background-color: var(--secondary-bg-color);
        border: 1px solid var(--border-color);
        color: var(--text-color);
        padding: 0.75rem;
        border-radius: 8px;
        transition: background-color 0.2s, border-color 0.2s;
        height: 100%;
        font-weight: 500;
    }
    div[data-testid="stButton"] > button:hover {
        background-color: var(--hover-bg-color);
        border-color: var(--primary-color);
        color: var(--primary-color);
    }
    /* Primary Button (분석 실행)은 이 스타일에서 제외 */
    div[data-testid="stButton"] > button.st-emotion-cache-1de5w8r {
        background-color: var(--primary-color) !important;
        color: var(--bg-color) !important;
        border: none !important;
    }
    div[data-testid="stButton"] > button.st-emotion-cache-1de5w8r:hover {
        background-color: var(--primary-color-hover) !important;
        color: var(--bg-color) !important;
    }


    .section-header {
        display: flex; align-items: center; gap: 0.75rem;
        margin-bottom: 1.25rem;
    }
    .section-header h4 { margin: 0; color: var(--text-color); }
    .header-icon svg { color: var(--primary-color); }

    h5.section-title {
        color: var(--text-color);
        font-weight: 500;
        margin-top: 1.25rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--border-color);
    }

    div[data-testid="stMetric"] {
        background-color: var(--secondary-bg-color);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 15px 20px;
    }
    div[data-testid="stMetricLabel"] { font-size: 1rem; color: var(--text-color-light); }

    table {
        width: 100%;
        border-collapse: collapse;
    }
    th, td {
        padding: 12px 15px;
        text-align: left;
        border-bottom: 1px solid var(--border-color);
    }
    th {
        background-color: var(--secondary-bg-color);
        color: var(--text-color);
        font-weight: 500;
    }
    td { color: #EAEAEA; }
    tr:last-child td { border-bottom: none; }
    tr:hover { background-color: var(--hover-bg-color); }

    /* 월별 요약 테이블 첫 열 너비 고정 */
    table tbody th {
        width: 200px;
        min-width: 200px;
    }

    /* --- 탭(st.tabs) 커스텀 --- */
    [data-testid="stTabs"] {
        border-bottom: 1px solid var(--border-color);
        margin-bottom: 1.5rem;
    }
    [data-testid="stTab"] {
        padding: 10px 16px;
        color: var(--text-color-light);
        border-bottom: 2px solid transparent;
        transition: all 0.2s ease-in-out;
    }
    [data-testid="stTab"][aria-selected="true"] {
        color: var(--primary-color);
        border-bottom: 2px solid var(--primary-color);
        background-color: transparent;
    }

    /* --- 정보/면책조항 푸터 카드 스타일 (폰트 크기 조정) --- */
    .info-footer {
        background-color: var(--secondary-bg-color);
        border-radius: 8px;
        padding: 20px 25px;
        margin-top: 2.5rem;
        display: flex;
        flex-wrap: wrap;
        gap: 30px;
    }
    .footer-section {
        flex: 1;
        min-width: 300px;
    }
    .footer-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 0.8rem;
    }
    .footer-icon svg {
        width: 16px;
        height: 16px;
        color: var(--primary-color);
    }
    .footer-title {
        font-size: 15px;
        font-weight: 700;
        color: var(--text-color);
    }
    .footer-text {
        font-size: 12px !important; /* 내용 폰트 크기 수정 */
        color: var(--text-color-light);
        line-height: 1.6;
        margin-bottom: 0.5em !important;
        padding-left: 2px;
    }
    .footer-text strong {
        font-weight: 500;
        color: var(--text-color);
    }

    /* --- 토스트(st.toast) 알림 커스텀 --- */
    [data-testid="stToast"] {
        position: fixed;
        bottom: 2rem;
        left: 50%;
        transform: translateX(-50%);
        right: auto;
        top: auto;
        background-color: #2E7D32;
        border: 1px solid #43A047;
        color: var(--text-color);
        border-radius: 6px;
        text-align: center;
    }

    /* --- 모바일 반응형 레이아웃 (st.expander 활용) --- */

    /* 데스크탑에서 모바일 헤더(첫 번째 expander) 숨기기 */
    [data-testid="stExpander"]:first-of-type {
        display: none;
    }

    @media (max-width: 991px) {
        /* 모바일에서 사이드바 숨기기 */
        [data-testid="stSidebar"] {
            display: none !important;
        }

        /* 모바일 뷰에서 메인 컨텐츠 상단 패딩 조정 */
        div.block-container {
            padding-top: 0.5rem !important;
        }

        /* 모바일에서 헤더(expander) 보이기 및 스타일 초기화 */
        [data-testid="stExpander"]:first-of-type {
            display: block !important;
            padding: 0 !important;
            margin: 0 !important;
            background-color: transparent !important;
            border: none !important; /* 테두리 제거 */
        }

        /* expander 헤더(summary) 자체를 완전히 숨김 */
        [data-testid="stExpander"]:first-of-type summary {
            display: none !important;
        }

        /* expander 내용물(body)의 불필요한 패딩 및 테두리 제거 */
        [data-testid="stExpander"]:first-of-type [data-testid="stExpanderDetails"] {
            padding: 0px !important;
        }

        [data-testid="stExpander"] > details {
            border-width: 0px !important;
        }
    }
</style>
"""