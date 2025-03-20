from pathlib import (
    Path,
)
from typing import (
    Any,
    Optional,
)

from smev_services.utils.xml.base import (
    XMLConverter,
)

from .domain.model import (
    DiedParticipant,
    DoDCertificateRequest,
    Participant,
    ParticipantType,
    Passport,
    ServiceInfo,
)


CURRENT_DIR = Path(__file__).parent


class DodCertificateConverter(XMLConverter):
    """Конвертер из domain-моделей в XML для отправки данных."""

    xsd_file_dir = CURRENT_DIR / Path('schemas/')
    xsd_file = CURRENT_DIR / Path('schemas/SOMC.xsd')

    def _prepare_service_xml_data(self, service: ServiceInfo) -> dict[str, Any]:
        return {
            'tns:currentDate': service.current_date.strftime('%d.%m.%Y'),
            'tns:orderStatusCode': service.order_status_code,
            'tns:TargetId': service.target_id,
            'tns:TargetName': service.target_name,
        }

    def _prepare_participant_type_xml_data(self, partipiant: ParticipantType) -> dict[str, Any]:
        if partipiant.died_participant:
            return {'tns:DiedParticipant': self._prepare_died_participant_xml_data(partipiant.died_participant)}
        return {'tns:Participant': self._prepare_participant_xml_data(partipiant.participant)}

    def _prepare_participant_xml_data(self, partipiant: Participant) -> dict[str, Any]:
        data = {
            'tns:lastname': partipiant.lastname,
            'tns:firstname': partipiant.firstname,
            'tns:dateBirth': partipiant.date_of_birth.strftime('%d.%m.%Y'),
            'tns:birthPlace': partipiant.birth_place,
            'tns:snils': partipiant.snils,
            'tns:passportRF': self._prepare_passport_xml_data(partipiant.passport),
            'tns:FOIVROIVID': partipiant.unit_ogrn,
            'tns:FOIVROIVName': partipiant.unit_name,
            'tns:FOIVROIVRegionCODE': partipiant.unit_region_code,
        }
        if middlename := partipiant.middlename:
            data['tns:middlename'] = middlename

        return data

    def _prepare_died_participant_xml_data(self, partipiant: DiedParticipant) -> dict[str, Any]:
        data = {
            'tns:lastname': partipiant.lastname,
            'tns:firstname': partipiant.firstname,
            'tns:dateBirth': partipiant.date_of_birth.strftime('%d.%m.%Y'),
            'tns:birthPlace': partipiant.birth_place,
            'tns:snils': partipiant.snils,
            'tns:passportRF': self._prepare_passport_xml_data(partipiant.passport),
            'tns:FOIVROIVID': partipiant.unit_ogrn,
            'tns:FOIVROIVName': partipiant.unit_name,
            'tns:FOIVROIVRegionCODE': partipiant.unit_region_code,
        }
        if middlename := partipiant.middlename:
            data['tns:middlename'] = middlename

        return data

    def _prepare_passport_xml_data(self, passport: Passport) -> dict[str, Any]:
        return {
            'tns:docseries': passport.series,
            'tns:docnumber': passport.number,
            'tns:issuedate': passport.issue_date.strftime('%d.%m.%Y'),
            'tns:issueorg': passport.issuer,
            'tns:issueidPassportRF': passport.issuer_code
        }

    def _prepare_xml_data(self, request_data: DoDCertificateRequest) -> tuple[dict[str, Any], Optional[str]]:
        """Подготавливает словарь с данными для последующего формирования по нему XML.

        Возвращает словарь с данными, а также путь в схеме до элемента по которому формируются XML.
        """
        request_path = self._schema.elements['request'].get_path()

        xml_data = {
            '@xmlns:tns': 'urn://rostelekom.ru/SOMC/1.0.3',

            '@oktmo': request_data.oktmo,
            'tns:Service': self._prepare_service_xml_data(request_data.service_info),
            'tns:FOIVROIVData': self._prepare_participant_type_xml_data(request_data.participant_type),
        }
        return xml_data, request_path
