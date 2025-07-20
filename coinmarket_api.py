import requests
import json
import csv
from datetime import datetime
import os

# --- Configuration ---
API_URL = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
CSV_FILE = 'btc-usd-max.csv'
API_KEY = 'CG-EtHdqNNb9LXmWMXs8KBA9v4i' # Your CoinGecko API Key

def get_existing_dates(file_path):
    """Reads all unique dates from the CSV file to prevent duplicates."""
    dates = set()
    if not os.path.exists(file_path):
        print(f"File '{file_path}' not found. A new one will be created.")
        return dates
        
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            # Skip header
            next(reader, None) 
            for row in reader:
                if row:
                    # Extract just the date part (YYYY-MM-DD)
                    date_str = row[0].split(' ')[0]
                    dates.add(date_str)
    except Exception as e:
        print(f"Could not read existing dates from CSV: {e}")
    return dates

def update_btc_data():
    """Fetches the latest BTC/USD data and appends only new, unique daily records."""
    
    existing_dates = get_existing_dates(CSV_FILE)
    if existing_dates:
        print(f"Found {len(existing_dates)} existing records. Last known date: {max(existing_dates)}")
    else:
        print("No previous data found or file does not exist.")

    parameters = {
        'vs_currency': 'usd',
        'days': '90', # Fetch a wider range to ensure all missing days are covered
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
            
            latest_records_for_new_dates = {}
            for i in range(len(prices)):
                record_date_str = datetime.fromtimestamp(prices[i][0] / 1000).strftime('%Y-%m-%d')
                
                # Only process dates that are not already in the file
                if record_date_str not in existing_dates:
                    price = prices[i][1]
                    market_cap = market_caps[i][1]
                    total_volume = total_volumes[i][1]
                    
                    # Store the record; if a date appears twice, this will keep the latest one
                    latest_records_for_new_dates[record_date_str] = [record_date_str, price, market_cap, total_volume]
            
            # Sort the new records by date before appending
            new_rows = sorted(latest_records_for_new_dates.values())

            if new_rows:
                # Append the new unique rows to the CSV file
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
