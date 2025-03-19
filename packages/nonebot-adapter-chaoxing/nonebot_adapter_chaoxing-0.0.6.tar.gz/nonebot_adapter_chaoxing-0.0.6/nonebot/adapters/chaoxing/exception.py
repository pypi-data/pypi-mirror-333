import json
from typing import Optional

from nonebot.drivers import Response
from nonebot.exception import AdapterException
from nonebot.exception import ActionFailed as BaseActionFailed
from nonebot.exception import NetworkError as BaseNetworkError
from nonebot.exception import NoLogException as BaseNoLogException
from nonebot.exception import ApiNotAvailable as BaseApiNotAvailable


class CxAdapterException(AdapterException):
    def __init__(self):
        super().__init__("ChaoXing")


class NoLogException(BaseNoLogException, CxAdapterException):
    pass


class ActionFailed(BaseActionFailed, CxAdapterException):
    def __init__(self, response: Response):
        self.response = response

        self.body: Optional[dict] = None
        if response.content:
            try:
                self.body = json.loads(response.content)
            except Exception:
                pass

    @property
    def status_code(self) -> int:
        return self.response.status_code

    @property
    def code(self) -> Optional[int]:
        return None if self.body is None else self.body.get("errcode", self.body.get("errCode", None))

    @property
    def msg(self) -> Optional[str]:
        return None if self.body is None else self.body.get("errmsg", self.body.get("errMsg", None))

    @property
    def data(self) -> Optional[dict]:
        return None if self.body is None else self.body.get("data", None)

    def __repr__(self) -> str:
        args = ("code", "msg", "data")
        return (
            f"<ActionFailed: {self.status_code}, "
            + ", ".join(f"{k}={v}" for k in args if (v := getattr(self, k)) is not None)
            + ">"
        )

    def __str__(self):
        return self.__repr__()


class NetworkError(BaseNetworkError, CxAdapterException):
    def __init__(self, msg: Optional[str] = None):
        super().__init__()
        self.msg: Optional[str] = msg
        """ 错误原因 """

    def __repr__(self):
        return f"<NetWorkError message={self.msg}>"

    def __str__(self):
        return self.__repr__()


class ApiNotAvailable(BaseApiNotAvailable, CxAdapterException):
    pass


class UnkonwnEventError(CxAdapterException):
    """ 未知事件 """

    def __init__(self, event: dict):
        self.event = event

    def __repr__(self):
        return f"<UnkonwnEvent {self.event}>"

    def __str__(self):
        return self.__repr__()
