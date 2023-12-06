import requests
from .apis import APIS_GOLIAT

async def call_api(api_name, params):
    api_info = APIS_GOLIAT.get(api_name)
    if api_info:
        url = api_info["url"]
        method = api_info["method"]
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, data=params)
        else:
            response = None
        data = response.json()
        return data
    else:
        return {"error": "API not found"}
    
async def handle_option(option_name, params):
    api_name = f"api_{option_name}"
    result = await call_api(api_name, params)
    print(result)
    # Here we can display it as a card, or show the info, idk