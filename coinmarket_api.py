import requests
import json
import csv
from datetime import datetime
import os

# --- Configuration ---
API_URL = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
CSV_FILE = 'btc-usd-max.csv'
API_KEY = 'CG-EtHdqNNb9LXmWMXs8KBA9v4i' # Your CoinGecko API Key

def get_last_date_from_csv(file_path):
    """
    Reads the last date from the CSV file.
    It handles both 'YYYY-MM-DD' and 'YYYY-MM-DD HH:MM:SS UTC' formats.
    """
    last_date = None
    if not os.path.exists(file_path):
        print(f"Warning: CSV file '{file_path}' not found. A new one will be created.")
        return None
        
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            # Use a generator expression to efficiently find the last valid line
            last_line = None
            for line in file:
                if line.strip(): # Ensure the line is not empty
                    last_line = line
            
            if last_line:
                # Extract the date part from the last row
                last_date_str = last_line.split(',')[0]
                # Try parsing with and without the timestamp
                try:
                    last_date = datetime.strptime(last_date_str, '%Y-%m-%d %H:%M:%S UTC').date()
                except ValueError:
                    last_date = datetime.strptime(last_date_str, '%Y-%m-%d').date()

    except Exception as e:
        print(f"Could not read the last date from CSV: {e}")
        
    return last_date

def update_btc_data():
    """Fetches the latest BTC/USD data and appends only new, unique daily records."""
    
    last_recorded_date = get_last_date_from_csv(CSV_FILE)
    if last_recorded_date:
        print(f"Last recorded date in CSV: {last_recorded_date.strftime('%Y-%m-%d')}")
    else:
        print("No previous data found.")

    parameters = {
        'vs_currency': 'usd',
        'days': '30', # Fetch a longer period to ensure we get all missing data
        'interval': 'daily',
        'x_cg_demo_api_key': API_KEY
    }

    print("Fetching latest data from CoinGecko...")
    try:
        response = requests.get(API_URL, params=parameters)
        response.raise_for_status()
        data = response.json()

        if 'prices' in data:
            prices = data['prices']
            market_caps = data['market_caps']
            total_volumes = data['total_volumes']
            
            # Use a dictionary to store the latest record for each day
            latest_records = {}
            for i in range(len(prices)):
                record_date = datetime.fromtimestamp(prices[i][0] / 1000).date()
                
                # We only care about dates after our last recorded one
                if last_recorded_date is None or record_date > last_recorded_date:
                    price = prices[i][1]
                    market_cap = market_caps[i][1]
                    total_volume = total_volumes[i][1]
                    
                    # Store or overwrite to keep only the latest entry for that date
                    latest_records[record_date] = [record_date.strftime('%Y-%m-%d 00:00:00 UTC'), price, market_cap, total_volume]
            
            # Sort the new records by date before appending
            new_rows = sorted(latest_records.values())

            if new_rows:
                with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(new_rows)
                print(f"Successfully added {len(new_rows)} new records to {CSV_FILE}.")
            else:
                print("No new data to add. The CSV file is already up-to-date.")

        else:
            print(f"Error: Unexpected API response structure.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during API request: {e}")

if __name__ == '__main__':
    update_btc_data() 
