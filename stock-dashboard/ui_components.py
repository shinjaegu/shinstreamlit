# ui_components.py

import streamlit as st

# '투자침팬치'의 정체성을 살린 전문적이고 미니멀한 로고
ICON_LOGO_UPGRADED = """
<svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2Z" stroke="currentColor" stroke-width="1.5"/>
    <path d="M9 16C9.85064 16.6303 10.8858 17 12 17C13.1142 17 14.1494 16.6303 15 16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
    <path d="M16 11.5C16 12.3284 15.5523 13 15 13C14.4477 13 14 12.3284 14 11.5C14 10.6716 14.4477 10 15 10C15.5523 10 16 10.6716 16 11.5Z" fill="currentColor"/>
    <path d="M10 11.5C10 12.3284 9.55228 13 9 13C8.44772 13 8 12.3284 8 11.5C8 10.6716 8.44772 10 9 10C9.55228 10 10 10.6716 10 11.5Z" fill="currentColor"/>
</svg>
"""

ICON_ANALYSIS = """
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M21 21H3V3"/>
  <path d="M9 15l4-4 4 4"/>
  <path d="M6 18l3-3"/>
</svg>
"""

# 푸터에 사용할 정보 및 경고 아이콘
ICON_INFO = """
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M12 16V12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M12 8H12.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

ICON_WARNING = """
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M10.29 3.86L1.82 18C1.6256 18.3421 1.6343 18.7502 1.84413 19.083C2.05397 19.4158 2.43579 19.625 2.85 19.625H21.15C21.5642 19.625 21.946 19.4158 22.1559 19.083C22.3657 18.7502 22.3744 18.3421 22.18 18L13.71 3.86C13.5105 3.51881 13.1255 3.30365 12.705 3.30365C12.2845 3.30365 11.8995 3.51881 11.7 3.86Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M12 9V13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M12 17H12.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""


def render_main_logo():
    """사이드바 로고 렌더링"""
    st.markdown(f"""
    <div class="logo-container">
        <span class="logo-svg">{ICON_LOGO_UPGRADED}</span>
        <span class="logo-text">투자침팬치</span>
    </div>
    """, unsafe_allow_html=True)

def render_header(title, icon_svg):
    """아이콘이 포함된 섹션 헤더 렌더링"""
    st.markdown(f"""
    <div class="section-header">
        <span class="header-icon">{icon_svg}</span>
        <h4>{title}</h4>
    </div>
    """, unsafe_allow_html=True)

def render_info_footer():
    """메인 화면 하단 정보/면책조항 HTML 문자열을 반환"""
    return f"""
        <div class="footer-section">
            <div class="footer-header">
                <span class="footer-icon">{ICON_INFO}</span>
                <span class="footer-title">About</span>
            </div>
            <p class="footer-text">이 앱은 LightGBM 모델을 사용하여 주가를 예측하고, 이를 기반으로 한 투자 전략의 성과를 백테스팅합니다.</p>
            <p class="footer-text"><strong>데이터 출처:</strong> Yahoo Finance</p>
        </div>
        <div class="footer-section">
            <div class="footer-header">
                <span class="footer-icon">{ICON_WARNING}</span>
                <span class="footer-title">면책조항</span>
            </div>
            <p class="footer-text">본 분석 결과는 정보 제공 목적으로만 사용되어야 하며, 실제 투자 결정에 대한 조언으로 해석되어서는 안 됩니다. 모든 투자의 책임은 본인에게 있습니다.</p>
        </div>
    """