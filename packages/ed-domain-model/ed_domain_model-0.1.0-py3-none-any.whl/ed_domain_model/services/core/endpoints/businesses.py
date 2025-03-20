from ed_domain_model.services.common.endpoint import (BaseEndpoint,
                                                      EndpointDescription)
from ed_domain_model.services.common.http_methods import HttpMethods
from ed_domain_model.services.core.dtos.business_dto import BusinessDto
from ed_domain_model.services.core.dtos.create_business_dto import \
    CreateBusinessDto
from ed_domain_model.services.core.dtos.create_orders_dto import CreateOrderDto
from ed_domain_model.services.core.dtos.order_dto import OrderDto


class BusinessesEndpoint(BaseEndpoint):
    def __init__(self, base_url: str):
        self._base_url = base_url

    def get_descriptions(self) -> list[EndpointDescription]:
        return [
            {
                'method': HttpMethods.GET,
                'url': f"{self._base_url}/businesses",
                'response_dto': list[BusinessDto]
            },
            {
                'method': HttpMethods.POST,
                'url': f"{self._base_url}/businesses",
                'request_dto': CreateBusinessDto,
                'response_dto': BusinessDto
            },
            {
                'method': HttpMethods.GET,
                'url': f"{self._base_url}/businesses/{{business_id}}",
                'response_dto': BusinessDto
            },
            {
                'method': HttpMethods.GET,
                'url': f"{self._base_url}/businesses/{{business_id}}/orders",
                'response_dto': list[OrderDto]
            },
            {
                'method': HttpMethods.POST,
                'url': f"{self._base_url}/businesses/{{business_id}}/orders",
                'request_dto': CreateOrderDto,
                'response_dto': OrderDto
            }
        ]
