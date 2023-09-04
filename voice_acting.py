import json
import requests


class Requests:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": ""
    }

    def get_voices(self, headers=headers):
        try:
            response = requests.get('https://api.voice.steos.io/v1/get/voices',
                                    headers=headers)
            if response.status_code == 500:
                raise ConnectionError
        except ConnectionError:
            return {"status": "fail",
                    "content": "Упс, ведутся ремонтные работы"}

        data = response.json()
        return {"status": "success",
                "content": data}  # 'voices'

    def get_symbols(self, headers=headers):
        try:
            response = requests.get('https://api.voice.steos.io/v1/get/symbols',
                                    headers=headers)
            if response.status_code == 500:
                raise ConnectionError
        except ConnectionError:
            return {"status": "fail",
                    "content": "Упс, ведутся ремонтные работы"}

        data = response.json()
        return {"status": "success",
                "content": data}  # 'symbols'

    def get_speech(self, data, headers=headers):
        try:
            response = requests.post('https://api.voice.steos.io/v1/get/tts',
                                     headers=headers, json=data)
            if response.status_code == 500:
                raise ConnectionError
        except ConnectionError:
            return {"status": "fail",
                    "content": "Упс, ведутся ремонтные работы"}

        data = response.json()
        return {"status": "success",
                "content": data}  # 'audio_url'
