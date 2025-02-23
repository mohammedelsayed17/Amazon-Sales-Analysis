import streamlit as st
from PIL import Image
import requests
from streamlit_lottie import st_lottie

st.set_page_config(
    page_title="Amazon Sentiment",
    page_icon="🌎",
)



st.title("Amazon sales analysis")
# st.sidebar.success("Select a demo above.")
# img=Image.open("cafe.gif")
# img_rezie=img.resize((400,400))
with st.container():  
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
       st.markdown("""
    <div style="text-align: justify; font-size:24px;">
    This project is for analyzing the sales of Amazon.The goal of this project is to show some KPIS and
     answer some questions that will benefit the
     business.
    </div>
""", unsafe_allow_html=True)

    with right_column:
        # st_lottie(lottie_coding, height=350, key="coding")
        # st.image(img_rezie,caption="this is mona picture",use_container_width=True)
        # st.video("cafe.mp4")
        st.image(r'E:\sale.gif')