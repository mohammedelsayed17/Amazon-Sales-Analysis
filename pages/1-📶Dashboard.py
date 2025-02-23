import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import plotly.express as px 
# ===Add configration ============
st.set_page_config(
    page_title="Amazon Sentiment",
    page_icon="🌎",
)

#### ========== Read the Data =============
@st.cache_data
def load_data():
    files = [
        "Sales_January_2019.csv", "Sales_February_2019.csv", "Sales_March_2019.csv",
        "Sales_April_2019.csv", "Sales_May_2019.csv", "Sales_June_2019.csv",
        "Sales_July_2019.csv", "Sales_August_2019.csv", "Sales_September_2019.csv",
        "Sales_October_2019.csv", "Sales_November_2019.csv", "Sales_December_2019.csv"
    ]
    All_Data = pd.concat([pd.read_csv(f"amazon data/{file}") for file in files], ignore_index=True)
    return All_Data

All_Data = load_data()
# All_Data.to_excel(r'E:/sales_2019.xlsx')
# print(All_Data)
# ===========Validation and prepartions ============
# ===Ensure there are duplicated rows or not ========
# print(All_Data.duplicated().value_counts())
# ========= drop duplicated Rows =========
All_Data.drop_duplicates(inplace=True)
# print(All_Data.duplicated().value_counts())
#======== Ensure that there are nan value or not=========
# print(All_Data[All_Data.isna().any(axis=1)])
# ==== drop rows have nan value ===============
All_Data.dropna(axis=0,inplace=True)
# ====== fillter the Data  and Ensure there are nan massing value ==========
All_Data=All_Data[All_Data['Order ID']!='Order ID']
# All_Data[All_Data.isna().any(axis=1)]
# print(All_Data)
# ==== Convert each colunms to suitable datatype =========
@st.cache_data
def optimize_data(All_Data):
    All_Data['Order ID'] = pd.to_numeric(All_Data['Order ID'], downcast='integer')
    All_Data['Quantity Ordered'] = pd.to_numeric(All_Data['Quantity Ordered'], downcast='integer')
    All_Data['Price Each'] = pd.to_numeric(All_Data['Price Each'], downcast='float')
    All_Data['Order Date'] = pd.to_datetime(All_Data['Order Date'])
    All_Data['Sales'] = All_Data['Quantity Ordered'] * All_Data['Price Each']
    return All_Data
All_Data = optimize_data(All_Data)
# =====ADD colunms time and day and month=============
All_Data['Hour']=All_Data['Order Date'].dt.hour
All_Data['Day']=All_Data['Order Date'].dt.day
All_Data['Month']=All_Data['Order Date'].dt.month
# ===============drop order Date colunms================
All_Data.drop(labels='Order Date',axis=1,inplace=True)
# print(All_Data)
# ============= ADD city colunm================
All_Data['City']=All_Data['Purchase Address'].apply(lambda x:x.split(',')[1])
# print(All_Data.columns)
# ========================== sidebare =======================
# ========================================================
# sidebare to select city 
st.sidebar.header("Filter Data")
City_option=["All city"]+sorted(All_Data['City'].dropna().unique().tolist())
selected_city = st.sidebar.selectbox("Select city",City_option )
# ========================================================
# Sidebar to select the month 
month_options = ["All Months"] + sorted(All_Data['Month'].dropna().unique().tolist())
selected_month = st.sidebar.selectbox("Select Month",month_options )
# =============================================================
# Filter Data Based on Selected Month

@st.cache_data
def filter_data(All_Data, selected_month, selected_city):
    if selected_month != "All Months":
        All_Data = All_Data[All_Data['Month'] == selected_month]
    if selected_city != "All city":
        All_Data = All_Data[All_Data['City'] == selected_city]
    return All_Data

filtered_data = filter_data(All_Data, selected_month, selected_city)

# ================= Metrics calculation ===================
@st.cache_data
def compute_metrics(filtered_data):
    Total_sales = filtered_data['Sales'].sum()
    Total_sales_by_millions = Total_sales / 1_000_000
    Average_price = filtered_data['Price Each'].mean()
    return Total_sales_by_millions, Average_price

Total_sales_by_millions, Average_price = compute_metrics(filtered_data)
# =======================================
filtered_data1 = All_Data if selected_month == "All Months" else All_Data[All_Data['Month'] == selected_month]
filtered_data2 = All_Data if selected_city == "All city" else All_Data[All_Data['City'] == selected_city]
# ==============================Dashboard Title=====================
st.title('Amazon sales analysis Insights Dashboard')
st.write('---')
st.subheader('Total Revenue and Average price based on selected month')
col1,col2=st.columns(2)
with col1:
    st.metric(label=f'Total Revenue to month ({selected_month})', value=f"${Total_sales_by_millions:,.2f}M")
with col2:
    st.metric(label=f'Average price to month ({selected_month})', value=f"${Average_price:,.2f}")
st.write('----')

# ========= Analysis ==============
# fig, ax = plt.subplots()
# ax.plot((All_Data.groupby('Month').sum()['Sales']).index,(All_Data.groupby('Month').sum()['Sales']).values,marker='o')
# ax.set_xlabel('Month')
# ax.set_ylabel('Total Sales by millions')
# ax.set_title('Monthly Sales Trend')
# st.pyplot(fig)
# =============interactive visual=================================
st.subheader('What was the best month for sales based on selected city ? How much was earned that month based on selected city?')
sales_monthly=filtered_data2.groupby('Month').sum()['Sales'].reset_index()
fig=px.line(
    sales_monthly,
    x='Month',
    y='Sales',
    markers='O',
    title=f'Monthly sales trend to City ({selected_city})',
    labels={'Month':'Month','Sales':'total Sales by millions'}
)
st.plotly_chart(fig)

#====================================================
# fig, ax = plt.subplots()
# ax.barh(All_Data.groupby('City').sum()['Quantity Ordered'].index,All_Data.groupby('City').sum()['Quantity Ordered'].values)
# ax.set_xlabel('Pice')
# ax.set_ylabel('City')
# ax.set_title('Total Quantity Ordered by City')
# st.plotly_chart(fig)
# =============interactive visual=================================
st.subheader('What city sold the most product based on selected month?')
city_product=filtered_data1.groupby('City').sum()['Quantity Ordered'].reset_index()
fig = px.bar(
    city_product,
    x='Quantity Ordered',  # Correct column name
    y='City',  # Correct column name
    orientation='h',  # Horizontal bar chart
    title=f'Total Quantity Ordered by City to month ({selected_month})',
    labels={'Quantity Ordered': 'Quantity Ordered', 'City': 'City'},  # Correct labels
    text_auto=True  # Show values on bars
)
# Update layout
fig.update_layout(
    xaxis_title="Quantity Ordered in Millions",
    yaxis_title="City",
    template="plotly_dark"  # Optional: change to "plotly_white" for a light theme
)
# Display in Streamlit
st.plotly_chart(fig)
# ========================================================
# fig, ax = plt.subplots()
# ax.barh(All_Data.groupby('City').sum()['Sales'].index , All_Data.groupby('City').sum()['Sales'].values)
# ax.set_xlabel('Sales by milions')
# ax.set_ylabel('City')
# ax.set_title('Total sales by City')
# =============interactive visual=================================
st.subheader('What city sold the most Sales based on selected month?')
city_sales = filtered_data1.groupby('City').sum()['Sales'].reset_index()
fig = px.bar(
    city_sales, 
    x='Sales', 
    y='City', 
    orientation='h',  # Horizontal bar chart
    title=f'Total sales by City to month ({selected_month})',
    labels={'Sales': 'Sales in Millions', 'City': 'City'},
    text_auto=True  # Show sales values on bars
)
fig.update_layout(
    xaxis_title="Sales in Millions",
    yaxis_title="City",
    template="plotly_dark"  # Optional: use "plotly_white" for a light theme
)
st.plotly_chart(fig)
# ======================================================
# =============interactive visual=================================
st.subheader('What time should we display advertisemens to maximize the likelihood of customer’s buying product based on selected month?')
hourly_counts = All_Data['Hour'].value_counts().reset_index()
hourly_counts.columns = ['Hour', 'Count']
hourly_counts['Hour'] = hourly_counts['Hour'] + 1
fig = px.bar(hourly_counts, x='Hour', y='Count', title=f'Oreder per hour to month ({selected_month})')
st.plotly_chart(fig)
