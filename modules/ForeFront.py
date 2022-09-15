import requests
class ForeFrontApi:
    def __init__(self, api_key: str, model_url: str) -> None:
        self.__api_key = api_key
        self.__model_url = model_url
    
    def generate(self, prompt, top_p=1, top_k=40, temperature=0.7, repetition_penalty=1, length=100, stop_sequences=[]):
        headers = {
            "Authorization": f"Bearer {self.__api_key}",
            "Content-Type": "application/json"
        }

        body = {
            "text": f"{prompt}",
            "top_p": top_p,
            "top_k": top_k,
            "temperature": temperature,
            "repetition_penalty":  repetition_penalty,
            "length": length,
            "stop_sequences": stop_sequences
        }

        while True:
            res = requests.post(
                f"{self.__model_url}",
                json=body,
                headers=headers
            )

            data = res.json()

            completion = data['result'][0]['completion']
            if completion.isspace():
                continue
            else:
                return completion