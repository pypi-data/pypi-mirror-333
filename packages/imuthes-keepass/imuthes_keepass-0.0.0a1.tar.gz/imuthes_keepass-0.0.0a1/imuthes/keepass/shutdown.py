import http.client


def shutdown(port: int = 8666) -> str:
    connection = http.client.HTTPConnection("localhost", port=port)
    connection.request("GET", "/__SHUTDOWN")
    result = connection.getresponse().fp.read().decode()
    connection.close()
    return result
