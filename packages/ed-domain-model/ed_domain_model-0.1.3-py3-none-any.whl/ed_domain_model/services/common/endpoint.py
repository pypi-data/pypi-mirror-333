from abc import ABCMeta
from typing import NotRequired, TypedDict

from ed_domain_model.services.common.http_methods import HttpMethod


class EndpointDescription(TypedDict):
    path: str
    method: HttpMethod
    headers: NotRequired[type]
    query_params: NotRequired[type]
    path_params: NotRequired[dict[str, type]]
    request_model: NotRequired[type]
    response_model: NotRequired[type]


class EndpointCallParams(TypedDict):
    headers: NotRequired[dict]
    query_params: NotRequired[dict]
    path_params: NotRequired[dict]
    request: NotRequired[dict]


class BaseEndpoint(metaclass=ABCMeta):
    def get_descriptions(self) -> list[EndpointDescription]: ...

