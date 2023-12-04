import requests

def get_definition_eng(word):
    """
    The function `get_definition_eng` takes a word as input and returns its English definition using an
    API.
    
    :param word: The word parameter is the word for which you want to get the English definition
    :return: the definition of the word in English. If the word is found in the dictionary API, it will
    return the definition. If the word is not found, it will return the message "No se encontró la
    palabra" which means "Word not found" in Spanish.
    """
    URL = "https://api.dictionaryapi.dev/api/v2/entries/en/" + word
    response = requests.get(URL)
    json_response = response.json()
    if response.status_code == 200:
        definition = json_response[0]["meanings"][0]["definitions"][0]["definition"]
        return definition
    return "No se encontró la palabra"
    