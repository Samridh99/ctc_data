import requests
import pandas as pd

def fetch_top_50_cryptos():

    url = "https://api.coingecko.com/api/v3/coins/markets"
    headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": "CG-sqx4sgx1cgh2fQBkwySdzaS3"
}
    

    params = {
        "vs_currency": "usd",        
        "per_page": 50,              
        "page": 1,                   
        "order": "market_cap_desc"   
    }
    

    response = requests.get(url, params=params, headers=headers)
    

    if response.status_code == 200:

        data = response.json()
        

        crypto_data = [
            {
                "Name": coin["name"],
                "Symbol": coin["symbol"],
                "Current Price (USD)": coin["current_price"],
                "Market Cap": coin["market_cap"],
                "24h Trading Volume": coin["total_volume"],
                "24h Price Change (%)": coin["price_change_percentage_24h"]
            }
            for coin in data
        ]
        

        df = pd.DataFrame(crypto_data)
        return df
    else:

        print(f"Error fetching data: HTTP Status Code {response.status_code}")
        return None


if __name__ == "__main__":
    df = fetch_top_50_cryptos()
    if df is not None:
        print(df)  
        

        df.to_csv("crypto_data.csv", index=False)







