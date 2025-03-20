from typing import (
    Optional,
)

from attrs import (
    define,
)
from smev_services.utils.domain.model import (
    BaseModel,
)
from smev_services.utils.xml.base import (
    xml_field,
)


@define
class OrderId(BaseModel):

    """Номер заявки."""

    id: str = xml_field('pguId')

@define
class StatusCode(BaseModel):

    """Статус заявки."""

    code: Optional[str] = xml_field('orgCode', default=None)
    epgu_code: Optional[str] = xml_field('techCode', default=None)


@define
class OrderInfo(BaseModel):

    """Информация по заявке."""

    order_id: OrderId = xml_field('tns:orderIdType')
    status_code: StatusCode = xml_field('tns:statusCodeType')
    comment: Optional[str] = xml_field('comment', default=None)
    is_cancel_allowed: Optional[bool] = xml_field('cancelAllowed', default=None)
    is_correspondence_allowed: Optional[bool] = xml_field('sendMessageAllowed', default=None)


@define
class DodCertificateResponse(BaseModel):

    """Ответ на запрос на предоставление сведений о справке Минобороны РФ."""

    order_info: OrderInfo = xml_field('tns:changeOrderInfo')
