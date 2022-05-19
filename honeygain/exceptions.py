class ClientException(Exception):
    pass


class SecurityCheckException(ClientException):
    pass


class HTTPException(Exception):
    pass
