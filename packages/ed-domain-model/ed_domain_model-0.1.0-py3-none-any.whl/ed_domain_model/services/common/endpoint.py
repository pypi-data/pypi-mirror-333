from abc import ABCMeta
from typing import NotRequired, TypedDict

from ed_domain_model.services.common.http_methods import HttpMethods


class EndpointDescription(TypedDict):
    method: HttpMethods
    url: str
    request_dto: NotRequired[type]
    response_dto: NotRequired[type]

class BaseEndpoint(metaclass=ABCMeta):
    def get_descriptions(self) -> list[EndpointDescription]: ...

