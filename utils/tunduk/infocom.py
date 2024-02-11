import requests

from utils.abstract_class.abstract_tunduk_system import TundukSystem


class Infocom(TundukSystem):
    system_name = 'Infocom'
    member_code = 70000005
    system_code = 'passport-service'
    service_amount = 0
    xmlns = "prod"
    xmlns_url = "http://tunduk-seccurity-infocom.x-road.fi/producer"

    @property
    def sanarip_addr(self):
        return f'http://{self.user.company.ip_addr}/r1/central-server/GOV/70000050/sanaripaymak-service/address-fact/'

    @property
    def sanarip_family(self):
        return f'http://{self.user.company.ip_addr}/r1/central-server/GOV/70000050/sanaripaymak-service/family-members/'

    def createbankPinServiceRequest(self, inn, passport_series, passport_number):
        """
        Формирование XML данных для запроса в Инфокос
        """
        data = f"""
                <prod:request>
                    <prod:clientid>{self.user.company.client_id}</prod:clientid>
                    <prod:secret>{self.user.company.infocom_secret_key}</prod:secret>
                    <prod:pin>{inn}</prod:pin>
                    <prod:series>{passport_series}</prod:series>
                    <prod:number>{passport_number}</prod:number>
                </prod:request>
            """

        return data

    def get_sanarip_fact_addr(self, url: str, inn: str):
        response = requests.request(
            method='GET',
            url=f'{url}{inn}',
            headers=self.get_headers
        )

        return response

    def post_bankPinService(self, cleaned_data):
        """
        Отравка запроса сформированных данных в Инфоком
        """
        bank_service_fields = [
            'pin', 'surname', 'name', 'patronymic', 'gender', 'dateOfBirth',
            'passportSeries', 'passportNumber', 'voidStatus', 'issuedDate',
            'passportAuthority', 'passportAuthorityCode', 'expiredDate',
            'familyStatus', 'maritalStatus', 'message',
        ]
        request_data = self.createbankPinServiceRequest(
            cleaned_data.get('inn'),
            cleaned_data.get('passport_series'),
            cleaned_data.get('passport_number')
        )
        response = self.post_request_data(request_data)
        sanarip_family = self.get_sanarip_fact_addr(self.sanarip_family, cleaned_data.get('inn'))
        result = self.parse_xml_data(response, bank_service_fields)
        result['sanarip'] = sanarip_family.json()

        return result, response
