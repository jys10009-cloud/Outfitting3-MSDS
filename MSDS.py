import streamlit as st
import pandas as pd

# 페이지 기본 설정
st.set_page_config(page_title="의장1부 현장 MSDS 관리 시스템", layout="wide")

# 1. 구글 시트 설정 (깨진 URL을 정상적인 CSV 다운로드 링크로 수정했습니다)
SHEET_ID = "1hRu0cQZGIQp4dxEK0HXdIuiJ1abI55SreVR1JZhPmig"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# 2. 데이터 불러오기
@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df = df.fillna('').astype(str)
        return df
    except:
        return pd.DataFrame(columns=["분류", "MSDS명", "Maker", "링크", "비고"])

df = load_data()

# --- 메인 UI ---
st.title("🗂️ 현장 MSDS 통합 검색")
st.info("💡 **물질명(이름)**을 터치하면 MSDS 파일이 바로 열립니다.")

# --- 7대 대분류 버튼 ---
st.subheader("📌 카테고리별 보기")
row1 = st.columns(4)
row2 = st.columns(4)

category_choice = None
categories = [
    ("🎨", "1. 도장재", "Paint"), ("🔥", "2. 용접재", "용접재"), 
    ("🛢️", "3. 오일,락카", "오일,락카"), ("🧵", "4. 섬유", "섬유"),
    ("🧱", "5. 충진재,경화재", "충진재,경화재"), ("💨", "6. 가스", "가스"), 
    ("🔧", "7. 기타용품", "기타용품")
]

for i, (icon, label, val) in enumerate(categories):
    target_row = row1 if i < 4 else row2
    if target_row[i % 4].button(f"{icon}\n\n{label}", use_container_width=True):
        category_choice = val

if row2[3].button("🔄\n\n전체 초기화", use_container_width=True):
    st.rerun()

# --- 검색창 ---
st.divider()
search_query = st.text_input("🔍 직접 검색 (물질명 또는 제조사)", placeholder="예: Paint, KCC, 가스 등")

# --- 데이터 필터링 ---
if category_choice:
    # 카테고리 버튼 클릭 시 해당 분류만 필터링
    filtered_df = df[df['분류'].str.contains(category_choice, na=False)]
elif search_query:
    # 검색창 입력 시: MSDS명 OR 제조사(Maker) OR 비고 컬럼에서 검색
    filtered_df = df[
        df['MSDS명'].str.contains(search_query, case=False) | 
        df['Maker'].str.contains(search_query, case=False) |
        df['비고'].str.contains(search_query, case=False)
    ]
else:
    filtered_df = df

# --- [핵심] 누르면 바로 열리는 리스트형 출력 ---
st.subheader(f"📄 검색 결과 ({len(filtered_df)}건)")

if len(filtered_df) == 0:
    st.warning("검색 결과가 없습니다.")
else:
    for _, row in filtered_df.iterrows():
        # HTML을 사용하여 물질명에 링크를 입히고 디자인 적용
        msds_name = row['MSDS명']
        link_url = row['링크']
        maker_info = row['Maker']
        category_info = row['분류']
        
        # 카드 스타일로 표시 (이름 클릭 시 링크 연결)
        st.markdown(f"""
            <div style="border: 1px solid #ddd; padding: 15px; border-radius: 10px; margin-bottom: 10px; background-color: #f9f9f9;">
                <a href="{link_url}" target="_blank" style="text-decoration: none; color: #007bff; font-size: 20px; font-weight: bold;">
                    🔗 {msds_name}
                </a>
                <div style="margin-top: 5px; color: #555; font-size: 14px;">
                    <b>제조사:</b> {maker_info} | <b>분류:</b> {category_info}
                </div>
                <div style="color: #888; font-size: 12px; margin-top: 5px;">{row['비고']}</div>
            </div>
        """, unsafe_allow_html=True)
        st.caption("위의 파란색 이름을 클릭하면 구글 드라이브로 연결됩니다.")