from typing import List
from botbuilder.core import (
    ActivityHandler,
    TurnContext,
)


from botbuilder.schema import (
    ChannelAccount,
)


class Bot(ActivityHandler):
    async def on_members_added_activity(
        self, members_added: List[ChannelAccount], turn_context: TurnContext
    ):
        from botbuilder.core.teams import TeamsInfo
        """
        The function sends options to a user when new members are added to a conversation.

        :param members_added: The `members_added` parameter is a list of `ChannelAccount` objects
        representing the members who were added to the conversation. Each `ChannelAccount` object contains
        information about the member, such as their ID, name, and role
        """
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                member = await TeamsInfo.get_member(turn_context, turn_context.activity.from_property.id)
                print(member)
                await self.send_categories('hola')

    async def on_message_activity(self, turn_context: TurnContext):
        """
        The `on_message_activity` function handles incoming messages by checking if the message contains a
        value or text and then calling the appropriate handler function.
        """
        # For activities, ex: forms, buttons
        if turn_context.activity.value:
            await self.handle_value_activity(turn_context)
        # For text inputs, ex: select an option
        else:
            await self.handle_text_activity(turn_context)

    async def handle_value_activity(self, turn_context: TurnContext):
        """
        The function `handle_value_activity` handles different actions based on the value of the `action`
        key in the activity's value property.
        """
        action = turn_context.activity.value["action"]
        turn_context.send_activity("Acción no reconocida")

    async def handle_text_activity(self, turn_context: TurnContext):
        """
        The function `handle_text_activity` checks the user's input and sends a form, a dictionary, or a
        list of options based on the input.
        """
        text = turn_context.activity.text.lower()
        if text in self.categories:
            await self.send_options_in_category(turn_context, text)
        elif text == "volver":
            await self.send_categories(turn_context)

    async def send_categories(self, turn_context: TurnContext):
        """
        Sends a message with a list of categories to the user.
        """
        title = "Selecciona una categoría"
        options = self.categories
        message = display_elements.message_options(title, options)
        await turn_context.send_activity(message)
        
    async def send_options_in_category(self, turn_context: TurnContext, category):
        """
        Sends a message with a list of options of a category to the user.
        """
        from utils.falabella_api_client import get_swagger_options

        title = "Selecciona una opción"
        options = await get_swagger_options(category)
        message = display_elements.message_options_with_back(title, options)
        await turn_context.send_activity(message)