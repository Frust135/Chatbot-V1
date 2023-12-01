from typing import List
from botbuilder.core import (
    ActivityHandler,
    TurnContext,
    CardFactory
)


from botbuilder.schema import (
    ChannelAccount,
    Activity,
    ActivityTypes,
    CardAction,
    HeroCard,
    Attachment,
)
from utils.api_dictionary_en import get_definition_eng
import json

class Bot(ActivityHandler):
    
    async def on_message_activity(self, turn_context: TurnContext):
        if turn_context.activity.value != None:
            action = turn_context.activity.value["action"]
            if action == "go-back":
                await self.send_options(turn_context)
            else:
                await self.echo_form(turn_context, action)
        else:
            text = turn_context.activity.text.lower()
            
            if "formulario" in text:
                await self.send_form(turn_context)
            elif "diccionario" in text:
                await self.send_dictionary(turn_context)
            else:
                await self.send_options(turn_context)
                
    async def echo_form(self, turn_context: TurnContext, form):
        if form == "submit-form-test":
            name = turn_context.activity.value["name"]
            email = turn_context.activity.value["email"]
            password = turn_context.activity.value["password"]
            
            await turn_context.send_activity(f"Nombre: {name}")
            await turn_context.send_activity(f"Email: {email}")
            await turn_context.send_activity(f"Contraseña: {password}")
        
        if form == "submit-form-dictionary":
            word = turn_context.activity.value["word"]
            definition = get_definition_eng(word)
            await turn_context.send_activity(f"Palabra: {word}")
            await turn_context.send_activity(f"Definción: {definition}")
            await self.send_dictionary(turn_context)
            
    async def send_dictionary(self, turn_context: TurnContext):
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
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await self.send_options(turn_context)