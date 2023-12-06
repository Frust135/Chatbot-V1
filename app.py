from flask import Flask, Response, jsonify, request
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    TurnContext,
    BotFrameworkAdapter
)
from botbuilder.schema import Activity, ActivityTypes
from datetime import datetime


from bot.bot import Bot
from config import DefaultConfig

app = Flask(__name__)

CONFIG = DefaultConfig()

SETTINGS = BotFrameworkAdapterSettings(
    app_id=CONFIG.APP_ID, 
    app_password=CONFIG.APP_PASSWORD
)

ADAPTER = BotFrameworkAdapter(settings=SETTINGS)

BOT = Bot()

async def on_error(context: TurnContext, error: Exception):
    """
    The `on_error` function sends an error message and a trace activity when an exception occurs in the
    bot.
    
    """
    
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

@app.route("/api/messages", methods=["POST"])
async def messages():
    """
    The function `messages` processes incoming messages, deserializes the activity, and passes it to the
    bot for processing, returning a response if available.

    """
    if "application/json" in request.headers["Content-Type"]:
        body = request.get_json()
    else:
        return Response(staus=415)
    
    activity = Activity().deserialize(body)
    auth_header = request.headers["Authorization"] if "Authorization" in request.headers else ""
    
    response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
    if response:
        return jsonify(response.body), response.status
    return Response(status=201)

# APP = web.Application(middlewares=[aiohttp_error_middleware])
# APP.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    try:
        app.run(host="localhost", port=CONFIG.PORT)
    except Exception as error:
        raise error