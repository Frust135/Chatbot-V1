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
    Attachment
)

class Bot(ActivityHandler):
    
    async def on_message_activity(self, turn_context: TurnContext):
        text = turn_context.activity.text.lower()
        
        if "formulario" in text:
            await self.send_form(turn_context)
        else:
            await self.send_options(turn_context)
    
    async def send_form(self, turn_context: TurnContext):

        fields = [
            {
                "label": "Nombre:",
                "type": "text",
                "id": "nombre"
            },
            {
                "label": "Apellido:",
                "type": "text",
                "id": "apellido"
            },
            {
                "label": "Correo electrónico:",
                "type": "text",
                "id": "correo"
            },
            {
                "label": "Mensaje:",
                "type": "text",
                "id": "mensaje"
            }
        ]

        card = HeroCard(
            title="Formulario",
            subtitle="Por favor, rellene los siguientes campos:",
            buttons=[
                CardAction(type="imBack", title="Enviar formulario", value="submit")
            ],
            items=[
                {
                    "type": "AdaptiveCard",
                    "content": {
                        "type": "VerticalCard",
                        "items": [
                            {
                                "type": "TextRun",
                                "text": field["label"]
                            },
                            {
                                "type": "Input.TextInput",
                                "id": field["id"],
                                "placeholder": "Introduzca su respuesta",
                                "style": "block"
                            }
                        ]
                    }
                } for field in fields
            ]
        )

        attachment = Attachment(content_type=CardFactory.content_types.hero_card, content=card.__dict__)

        message = Activity(
            type=ActivityTypes.message,
            text="Por favor, complete el siguiente formulario:",
            attachments=[attachment]
        )

        await turn_context.send_activity(message)

    
    
    async def send_options(self, turn_context: TurnContext):
        options = ["Formulario"]
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