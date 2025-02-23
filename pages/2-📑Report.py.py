import streamlit as st
st.set_page_config(
    page_title="Amazon Sales Analysis",
    page_icon="🌎",
)
st.title("Amazon sales Analysis Insights Report")
st.subheader("about Data")
st.write('We have 12 files, each of which contains sales for a month in the year 2019.')
st.write('1) Order ID: it is an ID for each Product') 
st.write(' 2) Product: it is a Product Nam')
st.write('3) Quantity Ordered: Quantity of product ordered')
st.write("4) Price Each: It's the price per piece")
st.write('5) Order Date: Date of order')
st.write('6) Purchase Address: Customer address')
st.write('---------')
st.subheader('Data Preparing')
st.write('1) We can concat all sales files in one excel file.')
st.write('2) Drop Duplicated Rows')
st.write('3) There is missing values in one row, we can drop it')
st.write('4) Covert each column to suitable data type')
st.write('5) ADD Column Sales by multiply Quantity Ordered and Price Each')
st.write('6) ADD Columns time, Day, month by extract them from Order Date column')
st.write('7) Drop Order Date column')
st.write('8) ADD City Column by extract it from Purchase Address')
st.write('---')
st.subheader('Questions')
st.write('1) What was the best month for sales based on selected City? How much was earned that month based on selected City?')
st.write('2) What city sold the most product based on selected month?')
st.write('3) What city sold the most Sales based on selected month?')
st.write(' 4) What time should we display advertisements to maximize the likelihood of customer’s buying product based on selected month ?')
st.write('----')
st.subheader('Insights')
st.write('1) the best sales in December Month')
st.write('2) The city that buys the most products is San Francisco.')
st.write('3) The best time to advertise our new products is from 10 AM to 8 PM because this is the time when most purchases are made')
