from aiohttp import web
from bot import create_bot

app = web.Application()
bot = create_bot()

# Endpoint
async def messages(request):
    if request.method == 'POST':
        body = await request.json()
        await bot.handle_message(body)
        return web.Response()

app.router.add_post('/api/messages', messages)

if __name__ == '__main__':
    web.run_app(app, host='localhost', port=3978)
