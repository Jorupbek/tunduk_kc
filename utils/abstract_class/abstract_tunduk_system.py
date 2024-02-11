from abc import ABC, abstractmethod
from bs4 import BeautifulSoup as bs
from xml.etree.ElementTree import XML

import requests

from utils.utils import byte_to_file


# member_code = 70000005
# system_code = 'passport-service'
# service_code = 'testBankPinService'
# xmlns = prod
# xmlns_url = "http://tunduk-seccurity-infocom.x-road.fi/producer"

class TundukSystem(ABC):
    system_name = None
    member_code = None
    system_code = None
    xmlns = None
    xmlns_url = None
    HEADERS = {
        'Content-Type': 'text/xml; charset=utf-8',
        'accept': 'application/json'
    }

    def __init__(self, service_code, user=None, version='v1', road_instance='central-server'):
        self.service_code = service_code
        self.version = version
        self.road_instance = road_instance
        self.user = user

    @property
    @abstractmethod
    def member_code(self):
        pass

    @property
    @abstractmethod
    def system_code(self):
        pass

    @property
    @abstractmethod
    def service_amount(self):
        pass

    @property
    def get_url(self) -> str:
        """
        Формирование URL адреса
        """
        url = (f"http://{self.user.company.ip_addr}/{self.road_instance}/GOV/"
               f"{self.member_code}/{self.system_code}/{self.service_code}/"
               f"{self.version}")

        return url

    @property
    def get_service_data(self) -> XML:
        """
        Формирование сервисных данных
        """
        version = f'<iden:serviceVersion>{self.version}</iden:serviceVersion>'
        service_data = \
            f"""
                <xro:service iden:objectType=\"SERVICE\">
                    <iden:xRoadInstance>{self.road_instance}</iden:xRoadInstance>
                    <iden:memberClass>GOV</iden:memberClass>
                    <iden:memberCode>{self.member_code}</iden:memberCode>
                    <!--Optional:-->
                    <iden:subsystemCode>{self.system_code}</iden:subsystemCode>
                    <iden:serviceCode>{self.service_code}</iden:serviceCode>
                    {version if self.version else ''}
                </xro:service>
            """
        return service_data

    @property
    def get_soap_header(self):
        """
        Формирование заголовка для отправки данных в СМЭВ Тундук
        """
        soap_header = \
            f"""
                <soapenv:Header>
                    <xro:protocolVersion>4.0</xro:protocolVersion>
                    <xro:issue>1</xro:issue>
                    <xro:id>1</xro:id>
                    <xro:userId>1</xro:userId>
                    {self.get_service_data}
                    <xro:client iden:objectType=\"SUBSYSTEM\">
                        <iden:xRoadInstance>central-server</iden:xRoadInstance>
                        <iden:memberClass>COM</iden:memberClass>
                        <iden:memberCode>{self.user.company.member_code}</iden:memberCode>
                        <iden:subsystemCode>{self.user.company.subsystem_code}</iden:subsystemCode>
                    </xro:client>
                </soapenv:Header>
            """
        return soap_header

    @property
    def get_headers(self):
        headers = dict(self.__class__.HEADERS)
        if self.user and self.user.company:
            headers[
                'X-Road-Client'] = f'central-server/COM/{self.user.company.member_code}/{self.user.company.subsystem_code}'
        return headers

    def get_soap_body(self, request_data):
        soap_body = \
            f"""
        <soapenv:Body>
            <{self.xmlns}:{self.service_code}>
                {request_data}
            </{self.xmlns}:{self.service_code}>
        </soapenv:Body>
        """

        return soap_body

    def get_payload(self, request_data):
        """Формирование итоговых XML данных для отправки запроса в СМЭВ Тундук"""
        payload = \
            f"""
                <soapenv:Envelope 
                    xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" 
                    xmlns:xro=\"http://x-road.eu/xsd/xroad.xsd\" 
                    xmlns:iden=\"http://x-road.eu/xsd/identifiers\" 
                    xmlns:{self.xmlns}=\"{self.xmlns_url}\"
                >
                    {self.get_soap_header}
                    {self.get_soap_body(request_data)}
                </soapenv:Envelope>
            """

        return payload

    def post_request_data(self, request_data):
        """
        Отправка данныъ в СМЭВ Тундук
        """
        data = self.get_payload(request_data)
        response = requests.request(
            method="POST",
            url=self.get_url,
            headers=self.get_headers,
            data=data
        )

        return response

    def parse_xml_data(self, response, fields):
        soup = bs(response.content, features="lxml-xml")
        result = {}

        if 'faultcode' in response.text:
            return {'Ошибка': soup.find('faultstring').text}

        for field in fields:
            soup_data = soup.find(field)

            if soup_data:
                result[field] = soup_data.text

        if photo := soup.find('photo'):
            result['image'] = byte_to_file(photo.text)

        return result
