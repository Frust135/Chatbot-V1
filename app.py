from botbuilder.core import (
    BotFrameworkAdapterSettings,
    TurnContext,
    BotFrameworkAdapter
)
from botbuilder.schema import Activity, ActivityTypes
from botbuilder.core.integration import aiohttp_error_middleware
from aiohttp import web
from aiohttp.web import Request, Response, json_response
from datetime import datetime


from bot import Bot
from config import DefaultConfig

CONFIG = DefaultConfig()

SETTINGS = BotFrameworkAdapterSettings(
    app_id=CONFIG.APP_ID, 
    app_password=CONFIG.APP_PASSWORD
)

ADAPTER = BotFrameworkAdapter(settings=SETTINGS)

BOT = Bot()
async def on_error(context: TurnContext, error: Exception):
    
    await context.send_activity("The bot encountered an error")
    await context.send_activity(
        "To continue to run this bot, please fix the bot source code."
    )
    
    # Send the error if the bot is running through the Bot Framework Emulator
    if context.activity.channel_id == "emulator":
        trace_activity  = Activity(
            label="TurnError",
            name="on_turn_error Trace",
            timestamp=datetime.utcnow(),
            type=ActivityTypes.trace,
            value=f"{error}",
            value_type="https://www.botframework.com/schemas/error"
        )
        await context.send_activity(trace_activity)
        
ADAPTER.on_turn_error = on_error

# Listen request on /api/messages
async def messages(req: Request) -> Response:
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(staus=415)
    
    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""
    
    response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
    if response:
        return json_response(data=response.body, status=response.status)
    return Response(status=201)

APP = web.Application(middlewares=[aiohttp_error_middleware])
APP.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    try:
        web.run_app(APP, host="localhost", port=CONFIG.PORT)
    except Exception as error:
        raise error