from typing import ClassVar
from ocpi_pydantic.v221.base import OcpiBaseResponse
from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, HttpUrl

from ocpi_pydantic.v221.enum import OcpiConnectorFormatEnum, OcpiConnectorTypeEnum, OcpiPowerTypeEnum



class OcpiConnector(BaseModel):
    '''
    OCPI 8.3.3. Connector Object
    '''
    id: str = Field(description='Identifier of the Connector within the EVSE.', max_length=36)
    standard: OcpiConnectorTypeEnum = Field(description='The standard of the installed connector.')
    format: OcpiConnectorFormatEnum = Field(description='The format (socket/cable) of the installed connector.')
    power_type: OcpiPowerTypeEnum
    max_voltage: int = Field(description='Maximum voltage of the connector (line to neutral for AC_3_PHASE), in volt [V].', gt=0)
    max_amperage: int = Field(description='Maximum amperage of the connector, in ampere [A].', gt=0)
    max_electric_power: int | None = Field(None, description='Maximum electric power that can be delivered by this connector, in Watts (W).', gt=0)
    tariff_ids: list[str] = Field([], description='Identifiers of the currently valid charging tariffs.')
    terms_and_conditions: HttpUrl | None = Field(None, description='URL to the operator’s terms and conditions.')
    last_updated: AwareDatetime = Field(description='Timestamp when this Connector was last updated (or created).')



class OcpiConnectorResponse(OcpiBaseResponse):
    data: OcpiConnector

    _examples: ClassVar[dict] = [{ # Version details response (one object)
        'data': {}, 'status_code': 1000, 'timestamp': '2015-06-30T21:59:59Z',
    }]
    model_config = ConfigDict(json_schema_extra={'examples': _examples})