from bs4 import BeautifulSoup as bs

from utils.abstract_class.abstract_tunduk_system import TundukSystem


class Unaa(TundukSystem):
    system_name = 'Unaa'
    member_code = 70000005
    system_code = 'vehicles-service'
    service_amount = 300
    xmlns = "ts1"
    xmlns_url = "http://tunduk-seccurity-infocom.x-road.fi/producer"

    def createTransportByPinRequest(self, inn):
        """
        Формирование XML данных для запроса в УНАА c помошью ПИНа
        """
        data = f"""
                <ts1:request>
                    <ts1:pin>{inn}</ts1:pin>
                </ts1:request>
            """

        return data

    def postTransportByPin(self, cleaned_data):
        """
        Отравка запроса сформированных данных в УНАА
        """
        request_data = self.createTransportByPinRequest(
            cleaned_data.get('inn')
        )
        response = self.post_request_data(request_data)
        result = self.parse_xml_data(response)

        return result, response

    def parse_xml_data(self, response, fields=None):
        soup = bs(response.content, features="lxml-xml")
        result = {}

        # Проверка на наличие ошибки в ответе
        if 'faultcode' in response.text:
            return {'Ошибка': soup.find('faultstring').text}

        # Извлечение данных о транспортных средствах
        cars = soup.find_all('ts1:cars')
        result['cars'] = []
        result['inn'] = soup.find('ts1:pin').text

        for car in cars:
            car_data = {
                'govPlate': car.find('ts1:govPlate').text,
                'carTypeName': car.find('ts1:carTypeName').text,
                'bodyType': car.find('ts1:bodyType').text,
                'brand': car.find('ts1:brand').text,
                'model': car.find('ts1:model').text,
                'steering': car.find('ts1:steering').text,
                'year': car.find('ts1:year').text,
                'color': car.find('ts1:color').text,
                'bodyNo': car.find('ts1:bodyNo').text,
                'vin': car.find('ts1:vin').text,
                'engineVolume': car.find('ts1:engineVolume').text,
                'dateFrom': car.find('ts1:dateFrom').text
            }
            result['cars'].append(car_data)

        return result
