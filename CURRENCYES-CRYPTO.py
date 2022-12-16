import requests
import pandas as pd
import datetime

# Define the API endpoint and your API key
endpoint = "https://api.apilayer.com/currency_data/historical?date=YYYY-MM-DD"
api_key = "57J9gDLPxuqGEfrWTPtdR0hEtnPRACVD"

# Set the headers for the request
headers = {
    "apikey": api_key
}

# Define the start and end dates for the historical data
# Get the current date and subtract 1 year
current_date = datetime.datetime.now()
end_date = current_date.strftime("%Y-%m-%d")
start_date = (current_date - datetime.timedelta(days=365)).strftime("%Y-%m-%d")

# Initialize an empty list to store the exchange rate data
exchange_rates = []

# Loop through the dates from start_date to end_date
date = start_date
while date <= end_date:
    # Set the date in the endpoint URL
    url = endpoint.replace("YYYY-MM-DD", date)

    # Make the GET request to the API
    response = requests.get(url, headers=headers)

    # Check the status code of the response
    if response.status_code == 200:
        # Get the data from the response
        data = response.json()

        # Extract the exchange rate data for Euros, GBP, and Peruvian Soles
        exchange_rates.append({
            "date": date,
            "EUR": data['quotes']['USDEUR'],
            "GBP": data['quotes']['USDGBP'],
            "PEN": data['quotes']['USDPEN']
        })
    else:
        # Print an error message
        print(f"An error occurred: {response.status_code}")

    # Increment the date by 1 day
    date = (datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

# Create a dataframe from the exchange rate data
df = pd.DataFrame(exchange_rates)

# Set the index to the date column
df.set_index('date', inplace=True)

# Display the dataframe
print(df)
