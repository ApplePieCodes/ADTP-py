import json
from typing import Any
from enum import Enum

def _serializer(obj: Any) -> str | dict[str, Any] | Any:
    if isinstance(obj, Version):
        if obj == Version.Adtp2:
            return "ADTP/2.0"
    elif isinstance(obj, Status):
        match obj:
            case Status.Ok:
                return "ok"
            case Status.InternalError:
                return "internal-error"
            case Status.Denied:
                return "denied"
            case Status.Pending:
                return "pending"
            case Status.NotFound:
                return "not-found"
            case Status.BadRequest:
                return "bad-request"
            case Status.Redirect:
                return "redirect"
            case Status.SwitchProtocols:
                return "switch-protocols"
            case Status.TooManyRequests:
                return "too-many-requests"
            case Status.Unauthorized:
                return "unauthorized"
    elif isinstance(obj, Method):
        return obj.name.lower()
    elif hasattr(obj, "__dict__"):
        return obj.__dict__
    else:
        raise TypeError(f"Type {type(obj)} not serializable")

class Method(Enum):
    Check = 0,
    Read = 1,
    Create = 2,
    Update = 3,
    Append = 4,
    Destroy = 5,
    Auth = 6,

class Version(Enum):
    Adtp2 = 1

class RequestBuilder:
    def __init__(self) -> None:
        self.version: Version = Version.Adtp2
        self.method: Method = Method.Check
        self.headers: dict[str, str] = {}
        self.uri: str = "/"
        self.content: str = ""

    def set_version(self, version: Version) -> None:
        self.version = version

    def set_method(self, method: Method) -> None:
        self.method = method

    def add_header(self, key: str, value: str) -> None:
        self.headers[key] = value

    def set_uri(self, uri: str) -> None:
        self.uri = uri

    def set_content(self, content: str) -> None:
        self.content = content

    def build(self) -> str:
        return json.dumps(self, default=_serializer)

class Status(Enum):
    SwitchProtocols = 0
    Ok = 1
    Pending = 2
    Redirect = 3
    Denied = 4
    BadRequest = 5
    Unauthorized = 6
    NotFound = 7
    TooManyRequests = 8
    InternalError = 9

class ResponseBuilder:
    def __init__(self) -> None:
        self.version: Version = Version.Adtp2
        self.status: Status = Status.Ok
        self.headers: dict[str, str] = {}
        self.content: str = ""

    def set_version(self, version: Version) -> None:
        self.version = version

    def set_status(self, status: Status) -> None:
        self.status = status

    def add_header(self, key: str, value: str) -> None:
        self.headers[key] = value

    def set_content(self, content: str) -> None:
        self.content = content

    def build(self) -> str:
        return json.dumps(self, default=_serializer)