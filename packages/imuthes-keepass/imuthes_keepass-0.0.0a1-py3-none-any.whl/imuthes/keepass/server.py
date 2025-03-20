# Localhost REST server for Keepass

import os
import pathlib
import signal

import fastapi
import uvicorn

from .keepass import KeePass

app = fastapi.FastAPI()


# noinspection PyUnresolvedReferences
@app.get("/{full_path:path}")
async def get_value(full_path: str, p: str = None):
    if full_path.startswith("__SHUTDOWN"):
        os.kill(os.getpid(), signal.SIGTERM)
        return fastapi.Response(status_code=200, content="Server shutting down...")
    try:
        if p:
            return app.state.kp.get_property(full_path, p)
        return app.state.kp.get(full_path)
    except KeyError:
        raise fastapi.HTTPException(status_code=404, detail=f"{full_path} not found")


# noinspection PyUnresolvedReferences
def server(
    filename: pathlib.Path,
    password: str,
    keyfile: pathlib.Path = None,
    port: int = 8666,
) -> None:
    """Start REST server to read KeePass

    :param filename: KeePass Database file
    :param password: Password for KeePass database
    :param keyfile:
    :param port: Server port
    """
    app.state.kp = KeePass(filename=filename, password=password, keyfile=keyfile)
    uvicorn.run(app, port=port, log_level="info")
