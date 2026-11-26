from starlette.responses import JSONResponse


class ChatBodyLimit:
    def __init__(self, app, max_bytes=512 * 1024):
        self.app = app
        self.max_bytes = max_bytes

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope["method"] != "POST" or scope["path"] != "/chat":
            return await self.app(scope, receive, send)

