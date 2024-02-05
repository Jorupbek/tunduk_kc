from bs4 import BeautifulSoup as bs

from utils.abstract_class.abstract_tunduk_system import TundukSystem

animal_codes = {
    '1': 'Крупный рогатый скот / Як',
    '2': 'Лошадь',
    '3': 'Мелко рогатый скот (Овца / Коза)',
    '4': 'Свинья',
    '5': 'Домашняя птица',
    '6': 'Пчелы'
}


class MinSelXoz(TundukSystem):
    system_name = 'MinSelXoz'
    member_code = 70000036
    system_code = 'AITS'
    service_amount = 0
    xmlns = "gvfi"
    xmlns_url = "http://gvfi.gov.kg/"

    def get_animal_data_from_inn(self, inn):
        """
        Формирование XML данных для запроса в Мин сель хоз
        """
        data = f"""
                <request>
                    <INN>{inn}</INN>
                 </request>
            """

        return data

    def post_animal_data_from_inn(self, cleaned_data):
        """
        Отравка запроса сформированных данных в Инфоком
        """
        test_bank_service_fields = [
            'Item', 'item', 'Type', 'Gender',
            'Age',
        ]
        request_data = self.get_animal_data_from_inn(
            cleaned_data.get('inn')
        )
        response = self.post_request_data(request_data)
        result = self.parse_xml_data(response, test_bank_service_fields)

        return result, response

    def parse_xml_data(self, response, fields):
        soup = bs(response.content, features="lxml-xml")
        result = {}

        if 'faultcode' in response.text:
            return {'Ошибка': soup.find('faultstring').text}

        items = soup.find_all('item')
        result['inn'] = soup.find('INN').text
        result['items'] = []

        for item in items:
            item_data = {
                'type': animal_codes.get(item.find('Type').text),
                'gender': 'М' if item.find('Gender').text == 'True' else 'Ж',
                # Replace comma with period for the age
                'age': item.find('Age').text.replace(',', '.')
            }
            result['items'].append(item_data)

        return result
