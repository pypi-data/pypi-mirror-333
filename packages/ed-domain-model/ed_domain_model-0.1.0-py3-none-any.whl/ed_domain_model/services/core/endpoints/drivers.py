from ed_domain_model.services.common.endpoint import (BaseEndpoint,
                                                      EndpointDescription)
from ed_domain_model.services.common.http_methods import HttpMethods
from ed_domain_model.services.core.dtos.create_driver_dto import \
    CreateDriverDto
from ed_domain_model.services.core.dtos.delivery_job_dto import DeliveryJobDto
from ed_domain_model.services.core.dtos.driver_dto import DriverDto


class DriveresEndpoint(BaseEndpoint):
    def __init__(self, base_url: str):
        self._base_url = base_url

    def get_descriptions(self) -> list[EndpointDescription]:
        return [
            {
                'method': HttpMethods.POST,
                'url': f"{self._base_url}/drivers",
                'request_dto': CreateDriverDto,
                'response_dto': DriverDto
            },
            {
                'method': HttpMethods.GET,
                'url': f"{self._base_url}/drivers/{{driver_id}}/delivery-jobs",
                'response_dto': list[DeliveryJobDto]
            },
            {
                'method': HttpMethods.POST,
                'url': f"{self._base_url}/drivers/{{driver_id}}/upload",
                'response_dto': DriverDto
            },
            {
                'method': HttpMethods.GET,
                'url': f"{self._base_url}/drivers/{{driver_id}}",
                'response_dto': DriverDto
            }
        ]
