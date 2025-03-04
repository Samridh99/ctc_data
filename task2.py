import pandas as pd


def analyze_crypto_data(df):
    
    df["Current Price (USD)"] = pd.to_numeric(df["Current Price (USD)"], errors="coerce")
    df["24h Price Change (%)"] = pd.to_numeric(df["24h Price Change (%)"], errors="coerce")


    top_5 = df.head(5)[["Name", "Symbol", "Market Cap"]]


    average_price = df["Current Price (USD)"].mean()


    highest_change_idx = df["24h Price Change (%)"].idxmax()
    lowest_change_idx = df["24h Price Change (%)"].idxmin()

    highest_change = df.loc[highest_change_idx, ["Name", "Symbol", "24h Price Change (%)"]]
    lowest_change = df.loc[lowest_change_idx, ["Name", "Symbol", "24h Price Change (%)"]]


    analysis_results = {
        "Top 5 Cryptocurrencies by Market Cap": top_5.to_dict(orient="records"),
        "Average Price (USD)": average_price,
        "Highest 24h Price Change": highest_change.to_dict(),
        "Lowest 24h Price Change": lowest_change.to_dict()
    }

    return analysis_results


df = pd.read_csv("crypto_data.csv")


results = analyze_crypto_data(df)
print("Top 5 Cryptocurrencies by Market Cap:")
print(pd.DataFrame(results["Top 5 Cryptocurrencies by Market Cap"]))
print(f"\nAverage Price (USD): ${results['Average Price (USD)']:.2f}")
print(f"\nHighest 24h Price Change: {results['Highest 24h Price Change']}")
print(f"Lowest 24h Price Change: {results['Lowest 24h Price Change']}")


