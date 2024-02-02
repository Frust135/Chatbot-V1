from typing import List
from botbuilder.core import (
    ActivityHandler,
    TurnContext,
)


from botbuilder.schema import (
    ChannelAccount,
)
from botbuilder.core.teams import TeamsInfo
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class Bot(ActivityHandler):
    async def on_members_added_activity(
        self, members_added: List[ChannelAccount], turn_context: TurnContext
    ):        
        """
        The function sends options to a user when new members are added to a conversation.

        :param members_added: The `members_added` parameter is a list of `ChannelAccount` objects
        representing the members who were added to the conversation. Each `ChannelAccount` object contains
        information about the member, such as their ID, name, and role
        """
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Bienvenido, ¿en qué puedo ayudarte?")

    async def on_message_activity(self, turn_context: TurnContext):
        """
        The `on_message_activity` function handles incoming messages by checking if the message contains a
        value or text and then calling the appropriate handler function.
        """
        text = turn_context.activity.text
        try:
            member = await TeamsInfo.get_member(turn_context, turn_context.activity.from_property.id)
            logger.info(f"Member: {member}")
        except Exception as e:
            logger.error(turn_context.activity.from_property.id)
            logger.error(f"Error getting member: {e}")
        await turn_context.send_activity(text)