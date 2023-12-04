import requests

def get_definition_eng(word):
    URL = "https://api.dictionaryapi.dev/api/v2/entries/en/" + word
    response = requests.get(URL)
    json_response = response.json()
    if response.status_code == 200:
        definition = json_response[0]["meanings"][0]["definitions"][0]["definition"]
        return definition
    return "No se encontró la palabra"
    