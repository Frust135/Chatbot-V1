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


async def get_all_swagger_categories():
    """
    Returns a list of the available categories in the swagger.
    """
    from re import compile

    response = requests.get(f"{URL}/landing/v1/build_openapi_json")
    swagger_json = response.json()
    paths = swagger_json.get("paths", {})

    pattern = compile(r"/api/(.*?)/v1/")
    categories = {match.group(1) for path in paths if (match := pattern.search(path))}

    category_list = list(categories)
    return category_list


async def get_swagger_options(category):
    """
    Retrieves the Swagger options for a given category.
    Args:
        category (str): The category to filter the Swagger options.

    Returns:
        dict: A dictionary containing the descriptions of the api options for the specified category.
    """
    from re import compile

    response = requests.get(f"{URL}/landing/v1/build_openapi_json")
    swagger_json = response.json()
    paths = swagger_json.get("paths", {})

    pattern = compile(r"/api/(.*?)/v1/")

    # descriptions = {}
    description_list = []

    for path, data in paths.items():
        match = pattern.search(path)
        if match and match.group(1) == category:
            description = data.get("get", {}).get("description", "")
            description_list.append(description)
            # descriptions[path] = description
    return description_list
