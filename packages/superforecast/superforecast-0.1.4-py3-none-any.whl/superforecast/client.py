import requests
import json

class SuperForecast:
    def __init__(self):
        """
        Inicializa o cliente para chamar a API.
        
        :param base_url: URL base do serviço
        :param api_key: Chave de API (se necessário)
        """
        self.base_url = "https://forecast-api-316143582006.us-central1.run.app"
        self.client = "free@superforecast.dev"
        self.secret = "superforecast"
        self.timeout = 50


    def forecast(self, history:list, generalization:int=1, steps:int=10, ret_all_series:bool=True, ysmooth:bool=False, method:int=1, segments:int=50):
        """Makes a request to the API service for forecasting.

        This function sends a request to the API to generate a forecast based on the provided parameters.

        :param history: Historical data used for training the forecast.
            * Maximum history length in the free version: 360
            * More history improves accuracy.
        :param generalization: Level of generalization applied to the forecast (default=1).
        :param steps: Number of steps to forecast (default=10).
            * Maximum steps in the free version: 10
        :param ret_all_series: Whether to return all series or only the forecasted steps (default=True).
        :param ysmooth: Whether to apply smoothing to the forecasted values (default=False).
        :param method: Forecasting method to use (default=1, maximum=7).
        :param segments: Number of segments used in the forecast (default=50).
            * Maximum segments in the free version: 50
            * More segments improve accuracy.
        :return: The forecasted values.
        """
        data = {'history': history, "generalization":generalization, 'steps': steps, 'ret_all_series': ret_all_series, 'ysmooth': ysmooth, 'method': method, 'segments': segments}

        headers = {'Content-type': 'application/json', "x-api-client": self.client, "x-api-secret" : self.secret}
        r = requests.post(f"{self.base_url}/forecast", data=json.dumps(data), headers=headers, timeout = self.timeout)
        r.raise_for_status()
        return r.json()