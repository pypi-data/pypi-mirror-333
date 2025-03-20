from smev_services.services.base import (
    ConsumerSmevService,
)
from smev_services.typing import (
    Message,
)

from .converter import (
    DodCertificateConverter,
)
from .domain.model import (
    DoDCertificateRequest,
    DodCertificateResponse,
)


class DoDCertificateRequestService(ConsumerSmevService):

    """Сервис "Предоставление справки Минобороны РФ"."""

    message_type = 'Получение ФОИВ (РОИВ) справки по линии Минобороны'
    name = 'Предоставление сведений справки Минобороны РФ'
    provider_name = 'Минобороны РФ'

    xml_converter_cls = DodCertificateConverter

    def build_request_message(self, request_data: DoDCertificateRequest) -> str:
        return self.xml_converter.build(request_data)

    def process_response_message(self, message: Message) -> DodCertificateResponse:
        return self.xml_converter.parse(message.body, DodCertificateResponse)
