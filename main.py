import requests
import pandas as pd

# Define Pakistan's economic indicators

indicators = {
    "Inflation": "FP.CPI.TOTL.ZG",
    "GDP_Growth": "NY.GDP.MKTP.KD.ZG"
}

# Create an empty dictionary to store data

economic_data = {}

# Retrieve data from World Bank

for indicator_name, indicator_code in indicators.items():

    url = (
        f"https://api.worldbank.org/v2/country/PAK/"
        f"indicator/{indicator_code}"
        "?format=json&per_page=100"
    )

    response = requests.get(url)

    if response.status_code == 200:

        data = response.json()
        records = data[1]

        for record in records:

            year = int(record["date"])
            value = record["value"]

            if 2000 <= year <= 2025:

                if year not in economic_data:
                    economic_data[year] = {}

                economic_data[year][indicator_name] = value

    else:
        print("Data retrieval failed:", indicator_name)

# Convert dictionary into Pandas DataFrame

df = pd.DataFrame.from_dict(
    economic_data,
    orient="index"
)

# Sort years in ascending order

df = df.sort_index()

# Display the economic dataset

print("\nPAKISTAN ECONOMIC DATA")
print(df)

# Display basic information

print("\nDATASET SUMMARY")
print(df.describe())

# STEP 6: ECONOMIC ANALYSIS

print("\n" + "=" * 45)
print("PAKISTAN ECONOMIC ANALYSIS")
print("=" * 45)

# Calculate average inflation

average_inflation = df["Inflation"].mean()

# Calculate average GDP growth

average_gdp_growth = df["GDP_Growth"].mean()

# Identify highest and lowest inflation

highest_inflation_year = df["Inflation"].idxmax()
lowest_inflation_year = df["Inflation"].idxmin()

# Identify highest and lowest GDP growth

highest_growth_year = df["GDP_Growth"].idxmax()
lowest_growth_year = df["GDP_Growth"].idxmin()

# Calculate correlation

correlation = df["Inflation"].corr(df["GDP_Growth"])

# Display results

print(f"Average Inflation: {average_inflation:.2f}%")

print(f"Average GDP Growth: {average_gdp_growth:.2f}%")

print(f"Highest Inflation: {df.loc[highest_inflation_year, 'Inflation']:.2f}% in {highest_inflation_year}")

print(f"Lowest Inflation: {df.loc[lowest_inflation_year, 'Inflation']:.2f}% in {lowest_inflation_year}")

print(f"Highest GDP Growth: {df.loc[highest_growth_year, 'GDP_Growth']:.2f}% in {highest_growth_year}")

print(f"Lowest GDP Growth: {df.loc[lowest_growth_year, 'GDP_Growth']:.2f}% in {lowest_growth_year}")

print(f"Inflation-GDP Growth Correlation: {correlation:.2f}")

# STEP 7: DATA VISUALIZATION

import matplotlib.pyplot as plt

# Chart 1: Pakistan Inflation Trend

plt.figure(figsize=(12, 6))

plt.plot(
    df.index,
    df["Inflation"],
    marker="o",
    label="Inflation Rate"
)

plt.title("Pakistan Annual Inflation Rate (2000-2025)")
plt.xlabel("Year")
plt.ylabel("Inflation (%)")

plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig("inflation_trend.png", dpi=300)
plt.show()

# Chart 2: Pakistan GDP Growth Trend

plt.figure(figsize=(12, 6))

plt.plot(
    df.index,
    df["GDP_Growth"],
    marker="o",
    label="GDP Growth"
)

plt.title("Pakistan Annual GDP Growth (2000-2025)")
plt.xlabel("Year")
plt.ylabel("GDP Growth (%)")

plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig("gdp_growth.png", dpi=300)
plt.show()

# Chart 3: Inflation vs GDP Growth

plt.figure(figsize=(12, 6))

plt.plot(
    df.index,
    df["Inflation"],
    marker="o",
    label="Inflation"
)

plt.plot(
    df.index,
    df["GDP_Growth"],
    marker="s",
    label="GDP Growth"
)

plt.title("Pakistan: Inflation vs GDP Growth")
plt.xlabel("Year")
plt.ylabel("Percentage (%)")

plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig("inflation_vs_growth.png", dpi=300)
plt.show()

# STEP 8: EXPORT ECONOMIC DATA

# Export the complete dataset into CSV

df.to_csv(
    "Pakistan_Economic_Data.csv",
    index_label="Year"
)

print("CSV file successfully created!")

# Create an economic summary

summary = pd.DataFrame({
    "Economic Indicator": [
        "Average Inflation",
        "Average GDP Growth",
        "Highest Inflation",
        "Lowest Inflation",
        "Highest GDP Growth",
        "Lowest GDP Growth",
        "Inflation-GDP Correlation"
    ],

    "Value": [
        average_inflation,
        average_gdp_growth,
        df["Inflation"].max(),
        df["Inflation"].min(),
        df["GDP_Growth"].max(),
        df["GDP_Growth"].min(),
        correlation
    ],

    "Year": [
        "2000-2025",
        "2000-2025",
        highest_inflation_year,
        lowest_inflation_year,
        highest_growth_year,
        lowest_growth_year,
        "2000-2025"
    ]
})

# Export data and summary into Excel

with pd.ExcelWriter(
    "Pakistan_Economic_Report.xlsx",
    engine="openpyxl"
) as writer:

    df.to_excel(
        writer,
        sheet_name="Economic Data",
        index_label="Year"
    )

    summary.to_excel(
        writer,
        sheet_name="Economic Summary",
        index=False
    )

print("Excel report successfully created!")
