import os

class DefaultConfig:
    """ Bot Configuration """
    
    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "143ebc27-dff8-4fdf-b3c6-c33374b54dfa")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", ".ZD8Q~bKMHTa2nsV5EWhDRoJSzm1bnerwSl1_c_h")