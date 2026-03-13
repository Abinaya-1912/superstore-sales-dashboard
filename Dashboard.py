import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(page_title="Superstore Sales Dashboard", layout="wide")

st.title("Superstore Sales Analysis Dashboard")

# ---------------------------------
# LOAD DATA
# ---------------------------------
df = pd.read_csv("superstore_sales.csv")

# Convert order date
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)

# Extract month
df["Month"] = df["Order Date"].dt.month

# ---------------------------------
# SIDEBAR FILTERS
# ---------------------------------
st.sidebar.header("Filter Data")

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# Apply filters
df = df[(df["Region"].isin(region)) & (df["Category"].isin(category))]

# ---------------------------------
# KPI CALCULATIONS
# ---------------------------------
total_sales = df["Sales"].sum()
total_orders = df["Order ID"].nunique()
avg_sales = df["Sales"].mean()

# ---------------------------------
# KPI DISPLAY
# ---------------------------------
st.subheader("Key Performance Indicators")

kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric(
    label="Total Sales",
    value=f"${total_sales:,.2f}",
    delta="Revenue"
)

kpi2.metric(
    label="Total Orders",
    value=total_orders,
    delta="Orders"
)

kpi3.metric(
    label="Average Sales",
    value=f"${avg_sales:,.2f}",
    delta="Avg Order Value"
)

st.markdown("---")

# ---------------------------------
# SALES BY CATEGORY
# ---------------------------------
category_sales = df.groupby("Category")["Sales"].sum().reset_index()

fig_category = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    color="Category",
    title="Sales by Category"
)

# ---------------------------------
# SALES BY REGION
# ---------------------------------
region_sales = df.groupby("Region")["Sales"].sum().reset_index()

fig_region = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    color="Region",
    title="Sales by Region"
)

col1, col2 = st.columns(2)

col1.plotly_chart(fig_category, use_container_width=True)
col2.plotly_chart(fig_region, use_container_width=True)

# ---------------------------------
# SALES BY SEGMENT
# ---------------------------------
segment_sales = df.groupby("Segment")["Sales"].sum().reset_index()

fig_segment = px.bar(
    segment_sales,
    x="Segment",
    y="Sales",
    color="Segment",
    title="Sales by Customer Segment"
)

# ---------------------------------
# MONTHLY SALES TREND
# ---------------------------------
monthly_sales = df.groupby("Month")["Sales"].sum().reset_index()

fig_month = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

col3, col4 = st.columns(2)

col3.plotly_chart(fig_segment, use_container_width=True)
col4.plotly_chart(fig_month, use_container_width=True)

# ---------------------------------
# TOP PRODUCTS (HORIZONTAL BAR)
# ---------------------------------
top_products = df.groupby("Product Name")["Sales"].sum()\
    .sort_values(ascending=False).head(10).reset_index()

fig_products = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    title="Top 10 Products by Sales"
)

# ---------------------------------
# TOP SUB CATEGORIES
# ---------------------------------
subcategory_sales = df.groupby("Sub-Category")["Sales"].sum()\
    .sort_values(ascending=False).head(10).reset_index()

fig_subcat = px.bar(
    subcategory_sales,
    x="Sub-Category",
    y="Sales",
    title="Top Sub-Categories by Sales"
)

col5, col6 = st.columns(2)

col5.plotly_chart(fig_products, use_container_width=True)
col6.plotly_chart(fig_subcat, use_container_width=True)

st.markdown("---")

# ---------------------------------
# DOWNLOAD DATA
# ---------------------------------
st.subheader("Download Sales Data")

csv = df.to_csv(index=False)

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="sales_report.csv",
    mime="text/csv"
)

# ---------------------------------
# BUSINESS INSIGHTS
# ---------------------------------
st.subheader("Key Insights")

st.write("• Technology category generates the highest revenue.")
st.write("• West region contributes significantly to total sales.")
st.write("• Consumer segment dominates the customer base.")
st.write("• Sales tend to increase towards the end of the year.")

# ---------------------------------
# VIEW DATA TABLE
# ---------------------------------
st.subheader("View Filtered Data")

st.dataframe(df)