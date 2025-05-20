# streamlit.py
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import matplotlib.pyplot as plt

# seat.py 에서 방금까지 만든 함수와 좌표 딕셔너리를 import
from seat import plot_seats_with_pairs, csp_points

# 30초마다 새로고침
st_autorefresh(interval=30000, key="datarefresh")

st.title("A507 실시간 좌석 및 공기질 모니터링")

# 사용자로부터 재실 좌석 입력 받기
occupied_input = st.text_input(
    "재실 좌석 번호를 쉼표로 구분하여 입력하세요",
    value="1,2,4,6,7"
)
occupied = set(s.strip() for s in occupied_input.split(",") if s.strip())

# matplotlib Figure/Axis 생성
fig, ax = plt.subplots(figsize=(6, 5))

# seat.py 의 plot_seats_with_pairs 를 호출하되,
# 그 안에서 input() 대신 occupied, ax 를 인자로 받도록 시그니처가 수정되어 있어야 합니다.
plot_seats_with_pairs(
    points=csp_points,
    occupied=occupied,
    ax=ax
)

# Streamlit 에 그려주기
st.pyplot(fig)
