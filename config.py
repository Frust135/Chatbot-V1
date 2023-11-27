from botbuilder.core import BotFrameworkAdapterSettings

class BotConfig:
    APP_ID = '143ebc27-dff8-4fdf-b3c6-c33374b54dfa'
    APP_PASSWORD = 'bQb8Q~GMqMGpJToXANLoZxF-44AHY1lW4isYFb0A'

def get_bot_config():
    botconfig = BotConfig()
    return BotFrameworkAdapterSettings(app_id=botconfig.APP_ID, app_password=botconfig.APP_PASSWORD)