import requests


class WhisperCppClient():
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.base_url = f'{self.host}:{self.port}'

        self.params = {
            'response_format': 'json',
        }

    def set_params(self, params: dict) -> None:
        self.params = params

    # Will throw if request fails or response contains an error
    # Response needs to be processed according to the response format
    def transcribe(self, wav_path: str) -> str:
        url = f'{self.base_url}/inference'
        files = {'file': open(wav_path, 'rb')}
        response = requests.post(url, data=self.params, files=files)
        json = response.json()
        if json.get('error'):
            raise Exception(json.get('error'))

        return response.content
