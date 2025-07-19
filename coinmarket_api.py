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
    """Reads the last timestamp from the CSV file to avoid duplicates."""
    last_date = None
    if not os.path.exists(file_path):
        print(f"Warning: CSV file '{file_path}' not found. A new one will be created.")
        return None
        
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            # Skip header
            next(reader, None) 
            for row in reader:
                if row:  # Ensure row is not empty
                    last_date = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S UTC')
    except Exception as e:
        print(f"Could not read the last date from CSV: {e}")
    return last_date

def update_btc_data():
    """Fetches the latest BTC/USD data from CoinGecko and appends it to btc-usd-max.csv."""
    
    # 1. Get the last recorded date from your CSV
    last_recorded_date = get_last_date_from_csv(CSV_FILE)
    print(f"Last recorded date in CSV: {last_recorded_date}")

    # --- API Parameters ---
    # Fetching the last few days is enough to check for new data.
    parameters = {
        'vs_currency': 'usd',
        'days': '5', # Fetching the last 5 days should be sufficient
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
            
            new_rows = []
            for i in range(len(prices)):
                # Convert timestamp from milliseconds to a datetime object
                record_date = datetime.fromtimestamp(prices[i][0] / 1000)
                
                # 2. Check if the record is newer than the last one in the file
                if last_recorded_date is None or record_date > last_recorded_date:
                    formatted_timestamp = record_date.strftime('%Y-%m-%d %H:%M:%S UTC')
                    price = prices[i][1]
                    market_cap = market_caps[i][1]
                    total_volume = total_volumes[i][1]
                    
                    new_rows.append([formatted_timestamp, price, market_cap, total_volume])

            # 3. Append only the new rows to the CSV file
            if new_rows:
                with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(new_rows)
                print(f"Successfully added {len(new_rows)} new records to {CSV_FILE}.")
            else:
                print("No new data to add. The CSV file is already up-to-date.")

        else:
            print(f"Error: Unexpected API response structure.")
            print("Received data:", json.dumps(data, indent=4))

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        if 'response' in locals():
            print("Response Status Code:", response.status_code)
            print("Response Text:", response.text)

if __name__ == '__main__':
    update_btc_data()
