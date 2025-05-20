import streamlit.py
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import matplotlib.pyplot as plt
from seat import plot_seats_with_pairs, csp_points

st_autorefresh(interval=30000, key="datarefresh")
st.title("A507 실시간 좌석 & 공기질")

occupied_input = st.text_input("재실 좌석 (예: 1,2,4)", "1,2,4")
occupied = set(s.strip() for s in occupied_input.split(",") if s.strip())

fig, ax = plt.subplots(figsize=(6,5))
plot_seats_with_pairs(points=csp_points, occupied=occupied, ax=ax)
st.pyplot(fig)
