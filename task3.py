import pandas as pd
import time
from task1 import fetch_top_50_cryptos
from task2 import analyze_crypto_data
from google.oauth2 import service_account
from googleapiclient.discovery import build


KEY_FILE = 'cred.json'  
SHEET_ID = '1iUAHlr2sdJDPQ9W2pZ_uM_Gem6ygwhCGAU6YBapt-MU'        
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
sheets_service = build('sheets', 'v4', credentials=creds)

headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": "CG-sqx4sgx1cgh2fQBkwySdzaS3"
}

def export_to_excel(df, analysis, filename="crypto_data.xlsx"):
    with pd.ExcelWriter(filename, engine="openpyxl") as writer:

        df.to_excel(writer, sheet_name="Top 50 Cryptocurrencies", index=False)
        

        summary_df = pd.DataFrame([
            ["Average Price (USD)", analysis["Average Price (USD)"]],
        ], columns=["Metric", "Value"])
        
        top_5_df = pd.DataFrame(analysis["Top 5 Cryptocurrencies by Market Cap"])
        highest_change_df = pd.DataFrame([analysis["Highest 24h Price Change"]])
        lowest_change_df = pd.DataFrame([analysis["Lowest 24h Price Change"]])
        

        summary_df.to_excel(writer, sheet_name="Analysis", startrow=0, index=False)
        top_5_df.to_excel(writer, sheet_name="Analysis", startrow=3, index=False)
        highest_change_df.to_excel(writer, sheet_name="Analysis", startrow=9, index=False)
        lowest_change_df.to_excel(writer, sheet_name="Analysis", startrow=12, index=False)
        

        workbook = writer.book
        analysis_sheet = workbook["Analysis"]
        analysis_sheet["A1"] = "Analysis Summary"
        analysis_sheet["A4"] = "Top 5 Cryptocurrencies by Market Cap"
        analysis_sheet["A10"] = "Highest 24h Price Change"
        analysis_sheet["A13"] = "Lowest 24h Price Change"

def update_google_sheet(sheets_service, sheet_id, df, analysis):


    sheets_service.spreadsheets().values().clear(
        spreadsheetId=sheet_id,
        range='Top 50 Cryptocurrencies!A1:Z1000',
    ).execute()
    values = [df.columns.tolist()] + df.values.tolist()
    sheets_service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range='Top 50 Cryptocurrencies!A1',
        valueInputOption='RAW',
        body={'values': values}
    ).execute()
    
    # Clear and update "Analysis" sheet
    sheets_service.spreadsheets().values().clear(
        spreadsheetId=sheet_id,
        range='Analysis!A1:Z1000',
    ).execute()
    
    # Write "Analysis Summary" title
    sheets_service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range='Analysis!A1',
        valueInputOption='RAW',
        body={'values': [['Analysis Summary']]}
    ).execute()
    
    # Write summary header and data
    sheets_service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range='Analysis!A3:B3',
        valueInputOption='RAW',
        body={'values': [['Metric', 'Value']]}
    ).execute()
    sheets_service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range='Analysis!A4:B4',
        valueInputOption='RAW',
        body={'values': [['Average Price (USD)', analysis['Average Price (USD)']]]}
    ).execute()
    

    sheets_service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range='Analysis!A6',
        valueInputOption='RAW',
        body={'values': [['Top 5 Cryptocurrencies by Market Cap']]}
    ).execute()
    

    top_5_df = pd.DataFrame(analysis['Top 5 Cryptocurrencies by Market Cap'])
    sheets_service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range='Analysis!A7:C7',
        valueInputOption='RAW',
        body={'values': [top_5_df.columns.tolist()]}
    ).execute()
    sheets_service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range='Analysis!A8:C12',
        valueInputOption='RAW',
        body={'values': top_5_df.values.tolist()}
    ).execute()
    

    sheets_service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range='Analysis!A14',
        valueInputOption='RAW',
        body={'values': [['Highest 24h Price Change']]}
    ).execute()
    

    highest_change_df = pd.DataFrame([analysis['Highest 24h Price Change']])
    sheets_service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range='Analysis!A15:C15',
        valueInputOption='RAW',
        body={'values': [highest_change_df.columns.tolist()]}
    ).execute()
    sheets_service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range='Analysis!A16:C16',
        valueInputOption='RAW',
        body={'values': highest_change_df.values.tolist()}
    ).execute()
    

    sheets_service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range='Analysis!A18',
        valueInputOption='RAW',
        body={'values': [['Lowest 24h Price Change']]}
    ).execute()
    

    lowest_change_df = pd.DataFrame([analysis['Lowest 24h Price Change']])
    sheets_service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range='Analysis!A19:C19',
        valueInputOption='RAW',
        body={'values': [lowest_change_df.columns.tolist()]}
    ).execute()
    sheets_service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range='Analysis!A20:C20',
        valueInputOption='RAW',
        body={'values': lowest_change_df.values.tolist()}
    ).execute()

def run_live_update(interval_seconds=300):
    while True:
        print("Fetching and updating data...")
        df = fetch_top_50_cryptos()  
        if df is not None:
            analysis = analyze_crypto_data(df)
            export_to_excel(df, analysis)
            update_google_sheet(sheets_service, SHEET_ID, df, analysis)
            print(f"Excel file and Google Sheet updated at {time.ctime()}")
        else:
            print("Failed to fetch data.")
        time.sleep(interval_seconds)

if __name__ == "__main__":
    run_live_update(interval_seconds=300)