from typing import List
from botbuilder.core import (
    ActivityHandler,
    TurnContext,
    CardFactory,
)


from botbuilder.schema import (
    ChannelAccount,
    Activity,
    ActivityTypes,
    CardAction,
    HeroCard,
    Attachment,
)
from .utils.api_dictionary_en import get_definition_eng
import json

class Bot(ActivityHandler):
    
    async def on_message_activity(self, turn_context: TurnContext):
        """
        The `on_message_activity` function handles incoming messages by checking if the message contains a
        value or text and then calling the appropriate handler function.
        """
        if turn_context.activity.value:
            await self.handle_value_activity(turn_context)
        else:
            await self.handle_text_activity(turn_context)
    
    async def handle_value_activity(self, turn_context: TurnContext):
        """
        The function `handle_value_activity` handles different actions based on the value of the `action`
        key in the activity's value property.
        """
        action = turn_context.activity.value["action"]
        if action == "go-back":
            await self.send_options(turn_context)
        elif action == "submit-form-test":
            await self.handle_submit_form_test(turn_context)
        elif action == "submit-form-dictionary":
            await self.handle_submit_form_dictionary(turn_context)
        else:
            await turn_context.send_activity("Acción no reconocida")
    
    async def handle_text_activity(self, turn_context: TurnContext):
        """
        The function `handle_text_activity` checks the user's input and sends a form, a dictionary, or a
        list of options based on the input.
        """
        text = turn_context.activity.text.lower()
        if "formulario" in text:
            await self.send_form(turn_context)
        elif "diccionario" in text:
            await self.send_dictionary(turn_context)
        else:
            await self.send_options(turn_context)
            
    async def handle_submit_form_test(self, turn_context: TurnContext):
        """
        The function `handle_submit_form_test` takes in a `TurnContext` object, extracts the values of
        `name`, `email`, and `password` from the activity, and sends them as separate activities.
        """
        name = turn_context.activity.value["name"]
        email = turn_context.activity.value["email"]
        password = turn_context.activity.value["password"]

        await turn_context.send_activity(f"Nombre: {name}")
        await turn_context.send_activity(f"Email: {email}")
        await turn_context.send_activity(f"Contraseña: {password}")
        
    async def handle_submit_form_dictionary(self, turn_context: TurnContext):
        """
        The function `handle_submit_form_dictionary` takes a word from the user, retrieves its definition
        using the `get_definition_eng` function, and sends the word and its definition as activities to the
        user.
        """
        word = turn_context.activity.value["word"]
        definition = get_definition_eng(word)
        await turn_context.send_activity(f"Palabra: {word}")
        await turn_context.send_activity(f"Definción: {definition}")
        await self.send_dictionary(turn_context)
            
    async def send_dictionary(self, turn_context: TurnContext):
        """
        The `send_dictionary` function sends an adaptive card with a text input field and two buttons to
        the user (one to send the form and other to go back).
        """
        card_json = """
        {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "type": "AdaptiveCard",
            "version": "1.3",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "Ingrese la palabra en inglés",
                    "weight": "bolder",
                    "horizontalAlignment": "center"
                },
                {
                    "type": "Input.Text",
                    "id": "word"
                }
            ],
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "Enviar",
                    "data": {
                        "$type": "Action.Submit",
                        "action": "submit-form-dictionary"
                    }
                },
                {
                    "type": "Action.Submit",
                    "title": "Volver",
                    "data": {
                        "$type": "Action.Submit",
                        "action": "go-back"
                    }
                }
            ]
        }
        """

        await turn_context.send_activity(
            Activity(
                type="message",
                attachments=[Attachment(content_type="application/vnd.microsoft.card.adaptive", content=json.loads(card_json))]
            )
        )

    async def send_form(self, turn_context: TurnContext):
        """
        The `send_form` function sends an adaptive card form to the user for them to fill out.
        """
        card_json = """
        {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "type": "AdaptiveCard",
            "version": "1.5",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "Formulario de Ejemplo",
                    "size": "large",
                    "weight": "bolder",
                    "horizontalAlignment": "center"
                },
                {
                    "type": "TextBlock",
                    "text": "Por favor, completa este formulario",
                    "size": "medium",
                    "wrap": true,
                    "horizontalAlignment": "center"
                },
                {
                    "type": "Input.Text",
                    "id": "name",
                    "placeholder": "Nombre"
                },
                {
                    "type": "Input.Text",
                    "id": "email",
                    "placeholder": "Email"
                },
                {
                    "type": "Input.Text",
                    "id": "password",
                    "placeholder": "Contraseña",
                    "style": "password"
                }
            ],
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "Enviar",
                    "data": {
                        "$type": "Action.Submit",
                        "action": "submit-form-test"
                    }
                },
                {
                    "type": "Action.Submit",
                    "title": "Volver",
                    "data": {
                        "$type": "Action.Submit",
                        "action": "go-back"
                    }
                }
            ]
        }
        """

        await turn_context.send_activity(
            Activity(
                type="message",
                attachments=[Attachment(content_type="application/vnd.microsoft.card.adaptive", content=json.loads(card_json))]
            )
        )

    
    
    async def send_options(self, turn_context: TurnContext):
        """
        The `send_options` function sends a message with a hero card containing a list of options to the
        user.
        """
        options = ["Formulario", "Diccionario Inglés"]
        card = HeroCard(
            title="Opciones",
            buttons=[
               CardAction(type="imBack", title=option, value=option) for option in options
            ]
        )
        attachment = Attachment(content_type=CardFactory.content_types.hero_card, content=card.__dict__)
        
        message = Activity(
            type=ActivityTypes.message,
            text="Selecciona una opción:",
            attachments=[attachment]
        )
        
        await turn_context.send_activity(message)
    
    async def on_members_added_activity(self, members_added: List[ChannelAccount], turn_context: TurnContext):
        """
        The function sends options to a user when new members are added to a conversation.
        
        :param members_added: The `members_added` parameter is a list of `ChannelAccount` objects
        representing the members who were added to the conversation. Each `ChannelAccount` object contains
        information about the member, such as their ID, name, and role
        """
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await self.send_options(turn_context)