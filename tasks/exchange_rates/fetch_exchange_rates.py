#----- IMPORTS
from prefect import task
import requests
import pandas as pd

#----- TASKS | FUNCTIONS
@task
def fetch_exchange_rates(api_key, base_currency, date):

    """
    Fetch historical exchange rates for a given date and base currency from an external API.

    Parameters:
    api_key (str): The API key for authentication.
    base_currency (str): The base currency code (e.g., 'USD').
    date (datetime): The date for which to fetch the exchange rates.

    Returns:
    pd.DataFrame: A DataFrame containing the exchange rates, with columns 'date', 
                  'base_currency', 'target_currency', and 'exchange_rate'.

    Raises:
    ValueError: If the API returns an error or fails to fetch exchange rates.
    ConnectionError: If the API request fails due to network issues or a bad response status code.
    """

    base_url = "https://api.apilayer.com/currency_data/historical"
    date_str = date.strftime('%Y-%m-%d')
    url = f"{base_url}?date={date_str}&source={base_currency}"

    headers = {"apikey": api_key}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data.get('success', False):
            rates = data['quotes']
            df = pd.DataFrame(
                [{"date": date_str, "base_currency": base_currency,
                  "target_currency": key[3:], "exchange_rate": value}
                 for key, value in rates.items()]
            )
            print(f"Fetched exchange rates for {date_str}")
            return df
        else:
            error_msg = f"API Error: {data.get('error')}"
            print(error_msg)
            raise ValueError(error_msg)
    else:
        error_msg = f"Failed to fetch data: {response.status_code}"
        print(error_msg)
        raise ConnectionError(error_msg)
