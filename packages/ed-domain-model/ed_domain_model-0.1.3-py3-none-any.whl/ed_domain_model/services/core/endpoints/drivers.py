from ed_domain_model.services.common.endpoint import (BaseEndpoint,
                                                      EndpointDescription)
from ed_domain_model.services.common.http_methods import HttpMethod
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
                'method': HttpMethod.POST,
                'path': f"{self._base_url}/drivers",
                'request_model': CreateDriverDto,
                'response_model': DriverDto
            },
            {
                'method': HttpMethod.GET,
                'path': f"{self._base_url}/drivers/{{driver_id}}/delivery-jobs",
                'path_params': {'driver_id': str},
                'response_model': list[DeliveryJobDto]
            },
            {
                'method': HttpMethod.POST,
                'path': f"{self._base_url}/drivers/{{driver_id}}/upload",
                'path_params': {'driver_id': str},
                'response_model': DriverDto
            },
            {
                'method': HttpMethod.GET,
                'path': f"{self._base_url}/drivers/{{driver_id}}",
                'path_params': {'driver_id': str},
                'response_model': DriverDto
            }
        ]
