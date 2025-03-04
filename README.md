# Cryptocurrency Live Data Tracker

This project fetches live data for the top 50 cryptocurrencies by market capitalization using the CoinGecko API, analyzes it, and updates both an Excel file and a Google Sheet every 5 minutes. It provides insights such as the top 5 cryptocurrencies by market cap, average price, and the highest/lowest 24-hour price changes.

## Features
- Fetches real-time cryptocurrency data using the CoinGecko API.
- Analyzes data to extract key metrics.
- Exports data and analysis to an Excel file (`crypto_data.xlsx`).
- Syncs the data to a Google Sheet for live viewing.
- Runs continuously with a configurable update interval (default: 5 minutes).

## Project Structure
```
ctc_data/
├── task1.py           # Fetches live cryptocurrency data
├── task2.py           # Analyzes the fetched data
├── task3.py           # Updates Excel and Google Sheets periodically
├── requirements.txt   # Lists Python dependencies
├── service_account.json # Google Sheets API credentials (not included in repo)
├── crypto_data.xlsx   # Generated Excel output (not tracked in git)
└── README.md          # Project documentation
```

## Prerequisites
- **Python 3.8+**: Ensure Python is installed on your system.
- **Google Cloud Project**: For Google Sheets API access (see setup below).
- **CoinGecko API**: A demo API key is included for better rate limits.

## Setup Instructions
### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ctc_data.git
cd ctc_data
```
### 2. Install Dependencies
Create a virtual environment and install the required packages:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set Up Google Sheets API
#### Create a Google Cloud Project:
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (e.g., "CryptoSync").
3. Enable the **Google Sheets API**.

#### Create a Service Account:
1. Navigate to **IAM & Admin** > **Service Accounts**.
2. Create a new service account (e.g., "sheet-updater").
3. Generate a JSON key and download it as `service_account.json`.
4. Place this file in the `ctc_data` directory (do **not** commit it to GitHub).

#### Create a Google Sheet:
1. Create a new Google Sheet manually.
2. Add two sheets: `Top 50 Cryptocurrencies` and `Analysis`.
3. Share the sheet with your service account email (found in `service_account.json`) and grant **Editor** access.
4. Copy the **Spreadsheet ID** from the URL: `https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit`.

#### Update `task3.py`:
- Replace the `KEY_FILE` path with the location of your `service_account.json`.
- Replace the `SHEET_ID` with your Google Sheet’s **Spreadsheet ID**.

### 4. Configure `.gitignore`
To avoid committing sensitive or generated files, create a `.gitignore` file:
```
service_account.json
crypto_data.xlsx
__pycache__/
*.pyc
venv/
```
Run `git add .gitignore` if you create it manually.

## Usage
### Run the Script:
```bash
python3 task3.py
```
This script fetches data, analyzes it, and updates both `crypto_data.xlsx` and the Google Sheet every 5 minutes.

### View Live Data:
- Open the **Google Sheet** in your browser using the shared link (set to "Anyone with the link" > "Viewer" for public access).
- The Excel file (`crypto_data.xlsx`) is updated locally in the project directory.

### Stop the Script:
Press `Ctrl+C` in the terminal to stop the update loop.

## Scripts Overview
- **`task1.py`**: Fetches the top 50 cryptocurrencies’ data from CoinGecko.
- **`task2.py`**: Analyzes the data (top 5 by market cap, average price, 24h price changes).
- **`task3.py`**: Orchestrates fetching, analysis, and updates to Excel and Google Sheets.

## Example Output
### **Excel File (`crypto_data.xlsx`)**
- **Sheet "Top 50 Cryptocurrencies"**: Full dataset.
- **Sheet "Analysis"**: Summary metrics.

### **Google Sheet**
- Mirrors the Excel structure with live updates.

## Customization
- **Update Interval**: Modify `interval_seconds` in `run_live_update()` in `task3.py` (e.g., `60` for 1-minute updates).
- **Sheet Names**: Adjust sheet names in `update_google_sheet()` if you use different names in your Google Sheet.

## Troubleshooting
- **Google Sheets API Error**: Ensure the service account has **Editor** access and that the sheet names match exactly (`Top 50 Cryptocurrencies` and `Analysis`).
- **Missing Modules**: Verify all dependencies are installed via `requirements.txt`.
- **API Rate Limits**: If CoinGecko throttles requests, consider reducing the update frequency.

## Contributing
Feel free to fork this repository, submit issues, or create pull requests with improvements!

## License
This project is licensed under the MIT License - see the LICENSE file for details (create one if desired).
