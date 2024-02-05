from utils.abstract_class.abstract_tunduk_system import TundukSystem


class Minjyst(TundukSystem):
    system_name = 'Minjyst'
    member_code = 70000024
    system_code = 'minjust-service'
    xmlns = "tun"
    xmlns_url = "http://tunduk.gov.kg"
    service_amount = 0

    def get_soap_body(self, request_data):
        soap_body = \
            f"""
        <soapenv:Body>
            <{self.xmlns}:{self.service_code}Request>
                {request_data}
            </{self.xmlns}:{self.service_code}Request>
        </soapenv:Body>
        """

        return soap_body

    def createSubjectByTinRequest(self, pin):
        """
        Формирование XML данных для запроса в Министерство Юстиции по ПИНу
        """
        data = \
            f"""
                <tun:tin>{pin}</tun:tin>
            """

        return data

    def postSubjectByTin(self, cleaned_data):
        """
        Отравка запроса сформированных данных в Инфоком
        """
        test_bank_service_fields = [
            'fullNameGl', 'fullNameOl', 'registrCode', 'statSubCode',
            'tin', 'region', 'district', 'city', 'street', 'house', 'room',
            'phones', 'email1', 'chief', 'description'
        ]
        request_data = self.createSubjectByTinRequest(
            cleaned_data.get('inn')
        )
        response = self.post_request_data(request_data)
        result = self.parse_xml_data(response, test_bank_service_fields)

        return result, response