from botbuilder.core import BotFrameworkAdapter, TurnContext, BotFrameworkAdapterSettings
from botbuilder.schema import Activity
from aiohttp import web

async def on_message_activity(turn_context: TurnContext):
    user_state = turn_context.turn_state.get("UserState", {})
    user_state["counter"] = user_state.get("counter", 0) + 1

    await turn_context.send_activity(f"Hello world!")

async def messages(req):
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return web.Response(status=415)
    activity = Activity().deserialize(body)
    auth_header = (req.headers["Authorization"] if "Authorization" in req.headers else "")
    await adapter.process_activity(activity, auth_header, on_message_activity)
    return web.Response()

if __name__ == "__main__":
    app_id = "143ebc27-dff8-4fdf-b3c6-c33374b54dfa"
    app_password = "bQb8Q~GMqMGpJToXANLoZxF-44AHY1lW4isYFb0A"
    settings = BotFrameworkAdapterSettings(app_id=app_id, app_password=app_password)
    adapter = BotFrameworkAdapter(settings)

    app = web.Application()
    app.router.add_post("/api/messages", messages)

    try:
        web.run_app(app, host="localhost", port=3978)
    except Exception as e:
        raise e
