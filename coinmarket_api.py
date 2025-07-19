import requests
import json
import csv
from datetime import datetime

# Your CoinGecko API Key
API_KEY = 'CG-EtHdqNNb9LXmWMXs8KBA9v4i'

# --- Configuration for CoinGecko Historical Price Data ---
# This endpoint fetches historical data for a specific coin.
API_URL = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'

# --- Parameters for the API request ---
# We are fetching data for the last 7 days in USD.
# The API key is added as a parameter for authenticated requests.
parameters = {
    'vs_currency': 'usd',
    'days': '31',
    'interval': 'daily',
    'x_cg_demo_api_key': API_KEY
}

# Initialize response variable to None to prevent NameError on request failure
response = None
try:
    # Make the GET request to the CoinGecko API
    response = requests.get(API_URL, params=parameters)
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

    # Parse the JSON response
    data = json.loads(response.text)

    # Check if the API call was successful and the data structure is as expected
    if 'prices' in data:
        prices = data['prices']
        market_caps = data['market_caps']
        total_volumes = data['total_volumes']

        # Define the CSV file name
        csv_file = 'coingecko_btc_history_7_days.csv'

        print(f"Successfully fetched historical data for Bitcoin (BTC) from CoinGecko.")

        # Write the data to a CSV file
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Write the header row
            writer.writerow(['Timestamp', 'Price (USD)', 'Market Cap', 'Total Volume'])

            # Loop through the price data and combine with other metrics
            # CoinGecko returns parallel arrays, so we iterate by index
            for i in range(len(prices)):
                # Convert Unix timestamp (in milliseconds) to a readable format
                timestamp = datetime.fromtimestamp(prices[i][0] / 1000).strftime('%Y-%m-%d')
                price = prices[i][1]
                market_cap = market_caps[i][1]
                total_volume = total_volumes[i][1]

                writer.writerow([timestamp, price, market_cap, total_volume])

        print(f"\nHistorical price data saved to {csv_file}")

    else:
        # Print an error message if the API call was not successful or data is missing
        print(f"Error fetching data from CoinGecko API: Unexpected response structure.")
        print("Received data:", json.dumps(data, indent=4))

except requests.exceptions.RequestException as e:
    # Handle network-related errors
    print(f"An error occurred: {e}")
    if response is not None:
        print("Response Status Code:", response.status_code)
        print("Response Text:", response.text)

except (KeyError, IndexError) as e:
    # Handle errors related to the structure of the API response
    print(f"Error parsing the API response: {e}")
    if 'data' in locals():
        print("Received data:", json.dumps(data, indent=4))
except json.JSONDecodeError:
    # Handle errors when parsing the JSON response
    print("Error decoding the JSON response from the API.")
    if response is not None:
        print("Received text:", response.text)
