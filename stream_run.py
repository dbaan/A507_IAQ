import streamlit as st
from streamlit_autorefresh import st_autorefresh
import matplotlib.pyplot as plt

from seat import plot_seats_with_pairs, csp_points

# 30초 자동 새로고침
st_autorefresh(interval=30000, key="datarefresh")

st.title("A507 실시간 좌석 및 공기질 모니터링")

# 재실 좌석을 코드에 직접 정의 (필요 시 수정)
occupied = {"3", "5", "7", "9", "13", "15", "17", "19"}

# 플롯 생성
fig, ax = plt.subplots(figsize=(6, 5))
plot_seats_with_pairs(points=csp_points, occupied=occupied, ax=ax)

# Streamlit에 출력
st.pyplot(fig)
