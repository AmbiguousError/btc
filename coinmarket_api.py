import os
import requests
import pandas as pd
from datetime import datetime

# --- Configuration ---
CSV_FILE = 'btc-usd-max.csv'
API_URL_HISTORY = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
API_URL_LATEST = "https://api.coingecko.com/api/v3/coins/markets"
DAYS_AGO = 7

def read_and_clean_csv(file_path):
    """
    Reads the CSV, robustly cleans it, and returns a DataFrame with a valid datetime column.
    """
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return pd.DataFrame(columns=['snapped_at', 'price', 'market_cap', 'total_volume'])

    df = pd.read_csv(file_path)

    if 'snapped_at' not in df.columns:
        print("Warning: 'snapped_at' column not found in CSV. Returning empty DataFrame.")
        return pd.DataFrame(columns=['snapped_at', 'price', 'market_cap', 'total_volume'])

    # Robustly parse the date/datetime string into a proper datetime object
    df['snapped_at'] = pd.to_datetime(df['snapped_at'], errors='coerce', utc=True)
    df.dropna(subset=['snapped_at'], inplace=True)

    return df

def update_historical_data():
    """Fetches and appends new daily historical records."""
    print("--- Starting Historical Data Update ---")
    df_existing = read_and_clean_csv(CSV_FILE)
    existing_dates = set(df_existing['snapped_at'].dt.date)
    
    params = {'vs_currency': 'usd', 'days': str(DAYS_AGO), 'interval': 'daily'}
    try:
        response = requests.get(API_URL_HISTORY, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching historical data: {e}")
        return

    df_prices = pd.DataFrame(data.get('prices', []), columns=['timestamp', 'price'])
    df_market_caps = pd.DataFrame(data.get('market_caps', []), columns=['timestamp', 'market_cap'])
    df_total_volumes = pd.DataFrame(data.get('total_volumes', []), columns=['timestamp', 'total_volume'])
    
    if df_prices.empty:
        print("No historical data returned from API.")
        print("--- Finished Historical Data Update ---")
        return

    df_new_history = pd.merge(df_prices, df_market_caps, on='timestamp')
    df_new_history = pd.merge(df_new_history, df_total_volumes, on='timestamp')
    df_new_history['snapped_at'] = pd.to_datetime(df_new_history['timestamp'], unit='ms', utc=True)
    df_new_history = df_new_history.drop(columns='timestamp')

    df_to_add = df_new_history[~df_new_history['snapped_at'].dt.date.isin(existing_dates)]

    if df_to_add.empty:
        print("No new historical daily records to add.")
    else:
        df_combined = pd.concat([df_existing, df_to_add], ignore_index=True)
        df_combined = df_combined.sort_values(by='snapped_at')
        
        # MODIFICATION: Trim the timestamp to date only before saving
        df_combined['snapped_at'] = df_combined['snapped_at'].dt.date
        
        df_combined.to_csv(CSV_FILE, index=False)
        print(f"Added {len(df_to_add)} new historical daily records.")
        
    print("--- Finished Historical Data Update ---")


def update_latest_price():
    """Fetches the latest real-time price and updates today's record in the CSV."""
    print("\n--- Starting Latest Price Update ---")
    params = {'vs_currency': 'usd', 'ids': 'bitcoin'}
    try:
        response = requests.get(API_URL_LATEST, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching latest data: {e}")
        return

    if not data:
        print("No latest price data returned from API.")
        return

    latest = data[0]
    snapped_at = pd.to_datetime(latest.get('last_updated'), utc=True)
    today_date = snapped_at.date()

    new_record_df = pd.DataFrame([{
        'snapped_at': snapped_at,
        'price': latest.get('current_price'),
        'market_cap': latest.get('market_cap'),
        'total_volume': latest.get('total_volume')
    }])

    df_existing = read_and_clean_csv(CSV_FILE)
    df_without_today = df_existing[df_existing['snapped_at'].dt.date != today_date]
    df_final = pd.concat([df_without_today, new_record_df], ignore_index=True)
    df_final = df_final.sort_values(by='snapped_at')
    
    # MODIFICATION: Trim the timestamp to date only before saving
    df_final['snapped_at'] = df_final['snapped_at'].dt.date
    
    df_final.to_csv(CSV_FILE, index=False)
    
    print(f"Successfully updated latest price for {today_date}.")
    print("--- Finished Latest Price Update ---")


if __name__ == "__main__":
    update_historical_data()
    update_latest_price()
