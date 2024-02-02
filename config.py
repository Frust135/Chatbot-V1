import os

class DefaultConfig:
    """ Bot Configuration """
    
    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "143ebc27-dff8-4fdf-b3c6-c33374b54dfa")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "bQb8Q~GMqMGpJToXANLoZxF-44AHY1lW4isYFb0A")