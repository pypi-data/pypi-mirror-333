from yta_general_utils.programming.env import Environment
from typing import Union

import requests


class Wit:
    """
    Class to interact with the Wit platform.
    """

    def request(
        message: str
    ) -> Union[dict, str]:
        """
        Send a request to our Wip app endpoint.
        """
        url = 'https://api.wit.ai/'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': Environment.get_current_project_env('WIT_ACCESS_TOKEN')
        }

        params = {
            'v': '20250311',
            'message': message
        }

        response = requests.get(
            url = url,
            headers = headers,
            params = params
        )

        # Comprobando el estado de la respuesta
        if response.status_code == 200:
            return response.json()
        else:
            return response.text