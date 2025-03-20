import http.client
import json


# noinspection PyShadowingBuiltins
def get(path: str, property: str, port: int = 8666) -> str:
    path = path.strip("/")
    connection = http.client.HTTPConnection("localhost", port=port)
    connection.request("GET", f"/{path}")
    j = json.loads(connection.getresponse().fp.read().decode())
    connection.close()
    result = j.get(property) or ""
    result = "\n".join(result.splitlines())  # need to normalize newline
    return result
