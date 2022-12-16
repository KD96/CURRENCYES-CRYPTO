#currencylayer API

import requests
import pandas as pd

# Define the API endpoint and your API key
endpoint = "http://api.currencylayer.com/live"
api_key = "57J9gDLPxuqGEfrWTPtdR0hEtnPRACVD"

# Define the base currency and the target currencies you want to get
base_currency = "YOUR_BASE_CURRENCY"
target_currencies = ["EUR", "USD", "PEN"]

# Build the query string with the API key and the base and target currencies
query_string = f"?access_key={api_key}&base={base_currency}&currencies={','.join(target_currencies)}"

# Make the request to the API
response = requests.get(endpoint + query_string)

# Get the data from the response
data = response.json()

# Get the quotes from the response data
quotes = data["quotes"]

# Extract the exchange rates for each currency
euro_rate = quotes[f"{base_currency}EUR"]
usd_rate = quotes[f"{base_currency}USD"]
pen_rate = quotes[f"{base_currency}PEN"]

import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc

# Define the Dash app
app = dash.Dash()

# Define the layout of the app
app.layout = html.Div([
    # Dropdown menu to select the timeframe
    dcc.Dropdown(
        id="timeframe-dropdown",
        options=[
            {"label": "1 Day", "value": "1day"},
            {"label": "1 Week", "value": "1week"},
            {"label": "1 Month", "value": "1month"},
            {"label": "1 Year", "value": "1year"},
            {"label": "5 Years", "value": "5years"},
            {"label": "10 Years", "value": "10years"}
        ],
        value="1day"
    ),
    # Graph to display the exchange rates
    dcc.Graph(id="exchange-rates-graph")
])

# Callback function to update the graph when the timeframe is changed
@app.callback(
    dash.dependencies.Output("exchange-rates-graph", "figure"),
    [dash.dependencies.Input("timeframe-dropdown", "value")]
)
def update_graph(timeframe):
    # Make the API request with the specified timeframe
    endpoint = "http://api.currencylayer.com/historical"
    query_string = f"?access_key={api_key}&base={base_currency}&currencies={','.join(target_currencies)}&date={timeframe}"
    response = requests.get(endpoint + query_string)
    data = response.json()

    # Get the quotes from the response data, if it exists
    quotes = data.get("quotes")

    if quotes is not None:
        # Extract the exchange rates for each currency
        euro_rate = quotes[f"{base_currency}EUR"]
        usd_rate = quotes[f"{base_currency}USD"]
        pen_rate = quotes[f"{base_currency}PEN"]
    else:
        # Set the exchange rates to 0 if the quotes key is not present
        euro_rate = 0
        usd_rate = 0
        pen_rate = 0

    # Create a data frame with the exchange rates and the dates
    df = pd.DataFrame({
        "Date": data["history"].keys(),
        "EUR": euro_rate,
        "USD": usd_rate,
        "PEN": pen_rate
    })

    # Plot the exchange rates using Plotly
    fig = px.line(df, x="Date", y=["EUR", "USD", "PEN"], title=f"Exchange Rates ({timeframe})")

    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)








#yahoo API

import requests

# Define the API endpoint and your Yahoo Finance API key
endpoint = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-quotes"
api_key = "dj0yJmk9WGxISUxMTlZOTmd4JmQ9WVdrOU1qRlRiRU4zU2pNbWNHbzlNQT09JnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTFm"  # Replace YOUR_YAHOO_FINANCE_API_KEY with your actual API key

# Define the base currency and the target currencies you want to get
base_currency = "YOUR_BASE_CURRENCY"
target_currencies = ["EUR", "USD", "PEN"]

# Build the query string with the symbols for the currencies you want to get
symbols = [f"{base_currency}{currency}" for currency in target_currencies]
query_string = f"?symbols={','.join(symbols)}"

# Set the headers for the request
headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
}

# Make the request to the API
response = requests.get(endpoint + query_string, headers=headers)

# Get the data from the response
data = response.json()
