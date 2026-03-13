import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style("whitegrid")
# load dataset
df = pd.read_csv("superstore_sales.csv")

# print first rows
print(df.head())

# dataset info
print(df.info())

# dataset shape
print(df.shape)

# check missing values
print(df.isnull().sum())

# check duplicate rows
print("Duplicate rows:", df.duplicated().sum())

# total sales
total_sales = df["Sales"].sum()
print("Total Sales:", total_sales)

# category wise sales
category_sales = df.groupby("Category")["Sales"].sum()
print("Sales by Category:")
print(category_sales)

# Region wise sales
region_sales = df.groupby("Region")["Sales"].sum()
print("Sales by Region:")
print(region_sales)


# category wise sales chart
category_sales.plot(kind="bar")
plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.show()

# region wise sales chart
region_sales.plot(kind="bar")
plt.title("Sales by Region")
plt.xlabel("Region")
plt.ylabel("Total Sales")
plt.show()

# top 10 products by sales
top_products = df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(10)
print("Top 10 Selling Products:")
print(top_products)

top_products.plot(kind="bar")
plt.title("Top 10 Best Selling Products")
plt.xlabel("Product Name")
plt.ylabel("Total Sales")
plt.xticks(rotation=75)
plt.show()

print("\n----- SALES ANALYSIS SUMMARY -----")

print("Total Sales:", df["Sales"].sum())

print("\nSales by Category:")
print(df.groupby("Category")["Sales"].sum())

print("\nSales by Region:")
print(df.groupby("Region")["Sales"].sum())

print("\nTop 10 Products:")
print(df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(10))

# convert order date to datetime
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
print(df["Order Date"].head())

# extract month from order date
df["Month"] = df["Order Date"].dt.month
print(df[["Order Date","Month"]].head())

# monthly sales calculation
monthly_sales = df.groupby("Month")["Sales"].sum()
print("\nMonthly Sales:")
print(monthly_sales)

# sub-category sales analysis
subcategory_sales = df.groupby("Sub-Category")["Sales"].sum().sort_values(ascending=False)
print("\nSales by Sub-Category:")
print(subcategory_sales)

# sales by customer segment
segment_sales = df.groupby("Segment")["Sales"].sum().sort_values(ascending=False)
print("\nSales by Customer Segment:")
print(segment_sales)

# correlation analysis
correlation = df.corr(numeric_only=True)
print("\nCorrelation Matrix:")
print(correlation)


# DASHBOARD VISUALIZATION
fig, axes = plt.subplots(3, 2, figsize=(16,12))

# Category Sales
axes[0,0].bar(category_sales.index, category_sales.values, color="skyblue")
axes[0,0].set_title("Sales by Category")

# Region Sales
axes[0,1].bar(region_sales.index, region_sales.values, color="orange")
axes[0,1].set_title("Sales by Region")

# Segment Sales
axes[1,0].bar(segment_sales.index, segment_sales.values, color="green")
axes[1,0].set_title("Sales by Segment")

# Monthly Trend
axes[1,1].plot(monthly_sales.index, monthly_sales.values, marker="o", color="red")
axes[1,1].set_title("Monthly Sales Trend")

# Top Products
axes[2,0].bar(top_products.index, top_products.values, color="purple")
axes[2,0].set_title("Top 10 Products")
axes[2,0].tick_params(axis="x", rotation=90)

# Sub Category
axes[2,1].bar(subcategory_sales.head(10).index, subcategory_sales.head(10).values, color="brown")
axes[2,1].set_title("Top Sub Categories")
axes[2,1].tick_params(axis="x", rotation=45)

fig.suptitle("Superstore Sales Analysis Dashboard", fontsize=18, fontweight="bold")
plt.tight_layout()
plt.show()