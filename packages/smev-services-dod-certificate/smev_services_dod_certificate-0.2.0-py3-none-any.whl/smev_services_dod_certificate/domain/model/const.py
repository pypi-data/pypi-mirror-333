from smev_services.utils.enums import (
    NamedEnum,
)


class ResponseResultStatus(NamedEnum):

    """Результат обработки запроса."""

    FOUND = 3, 'Услуга оказана (статус гражданина подтвержден)'
    NOT_FOUND = 4, 'Отказано в предоставлении услуги (статус гражданина не подтвержден)'
