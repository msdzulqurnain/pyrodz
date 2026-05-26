from framework import screen

class StartHandler:
    async def start(self, client, message):
        return screen("start", "start")
