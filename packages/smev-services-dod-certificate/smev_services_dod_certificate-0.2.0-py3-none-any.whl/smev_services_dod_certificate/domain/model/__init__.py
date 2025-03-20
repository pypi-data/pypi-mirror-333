from .request import (
    DiedParticipant,
    DoDCertificateRequest,
    Participant,
    ParticipantType,
    Passport,
    ServiceInfo,
)
from .response import (
    DodCertificateResponse,
    OrderId,
    OrderInfo,
    StatusCode,
)


__all__ = [
    # запрос
    DiedParticipant,
    DoDCertificateRequest,
    Participant,
    ParticipantType,
    Passport,
    ServiceInfo,

    # ответ
    DodCertificateResponse,
    OrderId,
    OrderInfo,
    StatusCode,
]
