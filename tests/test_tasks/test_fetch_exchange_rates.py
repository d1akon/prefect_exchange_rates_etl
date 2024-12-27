import pytest
from unittest.mock import patch
from datetime import datetime
from tasks.exchange_rates.fetch_exchange_rates import fetch_exchange_rates

#----- Utiliza un mock para testear la funcion/task fetch_exchange_rates
@patch('tasks.exchange_rates.fetch_exchange_rates.requests.get')
def test_fetch_exchange_rates(mock_get):
    # Simulamos la respuesta de la API
    mock_response = {
        "success": True,
        "quotes": {
            "USDARS": 150.5,
            "USDEUR": 0.85
        }
    }
    
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response
    
    date = datetime.strptime("2024-01-01", "%Y-%m-%d")
    
    #----- Se usa `.fn()` para ejecutar el task fuera de un flow (caso contrario da error)
    df = fetch_exchange_rates.fn("dummy_api_key", "USD", date)
    
    #----- Validando que los datos retornados son correctos
    assert df is not None
    assert "target_currency" in df.columns
    assert "exchange_rate" in df.columns
    assert df.loc[df['target_currency'] == 'ARS', 'exchange_rate'].iloc[0] == 150.5
