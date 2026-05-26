from framework import screen, Button


class SearchHandler:
    async def inline(self, client, message):

        return screen("inline", {})
    
    async def current(self, client, message):

        return screen("current", {})