import requests

URL = "https://goliat.falabella.cl/api"


async def call_api(type_api, function, action, params):
    """
    Calls an API endpoint of Falabella with the specified parameters.

    Args:
        type_api (str): The type of API.
        function (str): The API function to call.
        action (str): The HTTP action to perform (GET or POST).
        params (list): The list of parameters to include in the API call.

    Returns:
        dict: The JSON response from the API.

    Raises:
        Exception: If the API call fails with a non-200 status code.
    
    Example:
    json_response = await call_api(
        type_api="awx",
        function="get_inventories",
        action="GET",
        params=[
            {"name": "search_pattern", "value": "GoLiAtInventory_202"}
        ,
    )
    """
    api_url = f"{URL}/{type_api}/v1/{function}"
    for index, param in enumerate(params):
        aux_text = "?" if index == 0 else "&"
        api_url += f"{aux_text}{param['name']}={param['value']}"
    json_response = None
    if action == "GET":
        response = requests.get(api_url)
    elif action == "POST":
        response = requests.post(api_url)
    if response.status_code == 200:
        json_response = response.json()
        return json_response
    else:
        print(f"Error en la solicitud: {response.status_code}")
        print(f"URL: {api_url}")
        print(f"Response: {response.text}")
        raise Exception(f"Error en la solicitud: {response.status_code}")
