from botbuilder.core import BotFrameworkAdapter, TurnContext
from botbuilder.schema import Activity
from config import get_bot_config

async def on_message_activity(turn_context: TurnContext):
    await turn_context.send_activity('Hello World!')

class Bot:
    def __init__(self, adapter: BotFrameworkAdapter):
        self.adapter = adapter

    async def handle_message(self, data):
        activity = Activity.deserialize(data['body'])
        await self.adapter.process_activity(activity, data['auth'], on_message_activity)

def create_bot():
    config = get_bot_config()
    adapter = BotFrameworkAdapter(config)
    return Bot(adapter)
