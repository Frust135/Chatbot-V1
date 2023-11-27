from aiohttp import web
from bot import create_bot

app = web.Application()
bot = create_bot()

# Endpoint
async def messages(request):
    if request.method == 'POST':
        if "application/json" in request.headers["Content-Type"]:
            body = await request.json()
        else:
            return web.Response(status=415)
        auth_header = (request.headers["Authorization"] if "Authorization" in request.headers else "")
        data = {}
        data['body'] = body
        data['auth'] = auth_header
        await bot.handle_message(data)
        return web.Response()

app.router.add_post('/api/messages', messages)

if __name__ == '__main__':
    web.run_app(app, host='localhost', port=3978)
