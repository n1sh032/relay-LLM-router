from starlette.responses import JSONResponse


class ChatBodyLimit:
    def __init__(self, app, max_bytes=512 * 1024):
        self.app = app
