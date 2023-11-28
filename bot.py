from typing import List
from botbuilder.core import (
    ActivityHandler,
    TurnContext
)

from botbuilder.schema import (
    ChannelAccount,
    Activity,
    ActivityTypes,
    SuggestedActions,
    CardAction
)

class Bot(ActivityHandler):
    
    async def on_message_activity(self, turn_context: TurnContext):
        text = turn_context.activity.text.lower()
        
        if "options" in text:
            await self.send_options(turn_context)
        else:
            await turn_context.send_activity("Hello World!")
    
    async def send_options(self, turn_context: TurnContext):
        options = ["Option 1", "Option 2", "Option 3"]
        
        actions = [
            CardAction(type="imBack", title=option, value=option) for option in options
        ]        
        suggest = SuggestedActions(actions=actions)
        
        message = Activity(
            type=ActivityTypes,
            text="Select an option:",
            suggested_actions=suggest
        )
        
        await turn_context.send_activity(message)
    
    async def on_members_added_activity(self, members_added: List[ChannelAccount], turn_context: TurnContext):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")