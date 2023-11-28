import os
from typing import List
import aiohttp
from botbuilder.core import (
    ActivityHandler,
    TurnContext
)

from botbuilder.schema import ChannelAccount

class Bot(ActivityHandler):
    
    async def on_message_activity(self, turn_context: TurnContext):
        await turn_context.send_activity("Hello World!")
        
    async def on_members_added_activity(self, members_added: List[ChannelAccount], turn_context: TurnContext):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")