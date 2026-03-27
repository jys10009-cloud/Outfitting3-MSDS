import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(page_title="의장3부 MSDS 관리 시스템", layout="centered")

# --- 모바일 화면 2열 강력 고정 CSS ---
st.markdown("""
    <style>
    @media (max-width: 768px) {
        div[data-testid="stHorizontalBlock"] {
            flex-wrap: nowrap !important;
            gap: 8px !important; 
        }
        div[data-testid="column"] {
            width: 48% !important;
            flex: 1 1 48% !important;
            min-width: 48% !important;
            padding: 0 !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# 2. 구글 시트 설정
SHEET_ID = "1bGoZmkSBZnckeuhELCQgQP9qcpLMjFbZR5Y1ortYE1M"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# 3. 데이터 불러오기
@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df = df.fillna('').astype(str)
        return df
    except Exception:
        return pd.DataFrame(columns=["분류", "MSDS명", "Maker", "링크", "비고"])

df = load_data()

# --- 메인 UI ---
st.title("🔍 의장3부 MSDS 관리 시스템")
st.info("💡 **물질명(이름)**을 터치하면 MSDS 파일이 바로 열립니다.")

# --- 카테고리 버튼 (2열 고정 배치) ---
st.subheader("📌 카테고리별 보기")

category_choice = None
categories = [
    ("🎨", "1. 도장재", "도장재"), ("🔥", "2. 용접재", "용접재"), 
    ("🛢️", "3. 오일, 락카", "오일, 락카"), ("🪨", "4. 숫돌 및 사포", "숫돌 및 사포"),
    ("🧱", "5. 충진재,경화재", "충진재,경화재"), ("🔩", "6. 부자재", "부자재"), 
    ("🔫", "7. 실리콘", "실리콘"), ("🔧", "8. 기타용품", "기타용품")
]

for i in range(0, len(categories), 2):
    cols = st.columns(2)
    if cols[0].button(f"{categories[i][0]} {categories[i][1]}", use_container_width=True):
        category_choice = categories[i][2]
    if cols[1].button(f"{categories[i+1][0]} {categories[i+1][1]}", use_container_width=True):
        category_choice = categories[i+1][2]

# --- 전체 초기화 버튼 ---
st.write("") 
if st.button("🔄 전체 초기화", use_container_width=True):
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

# --- 검색창 ---
st.divider()
search_query = st.text_input("🔍 직접 검색 (물질명 또는 제조사)", placeholder="예: Paint, KCC, 가스 등")

# --- 데이터 필터링 ---
if category_choice:
    filtered_df = df[df['분류'].str.contains(category_choice, na=False)]
elif search_query:
    filtered_df = df[
        df['MSDS명'].str.contains(search_query, case=False) | 
        df['Maker'].str.contains(search_query, case=False) |
        df['비고'].str.contains(search_query, case=False)
    ]
else:
    filtered_df = df

# --- 검색 결과 출력 ---
st.subheader(f"📄 검색 결과 ({len(filtered_df)}건)")

if len(filtered_df) == 0:
    st.warning("검색 결과가 없습니다.")
else:
    for _, row in filtered_df.iterrows():
        msds_name = row['MSDS명']
        link_url = row['링크']
        maker_info = row['Maker']
        category_info = row['분류']
        
        # 여기서 따옴표 3개가 정확히 열리고 닫히도록 수정되었습니다.
        st.markdown(f"""
            <div style="border: 1px solid #ddd; padding: 12px; border-radius: 8px; margin-bottom: 12px; background-color: #fcfcfc;">
                <a href="{link_url}" target="_blank" style="text-decoration: none; color: #0056b3; font-size: 17px; font-weight: 700;">
                    🔗 {msds_name}
                </a>
                <div style="margin-top: 8px; color: #444; font-size: 13px;">
                    <span style="background
