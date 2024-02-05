from decimal import Decimal

from core.settings import IP_ADDR
from utils.get_data import get_request


class Kadastr(object):
    service_amount = Decimal('175.75')
    system_name = 'Kadastr'

    def __init__(self):
        self.url = f'http://{IP_ADDR}/r1/central-server/GOV/70000019/dkrpni-service/'

    def getPropertyInfo(self, eni_code):
        """
        Проверка ЕНИ по коду
        Если ЕНИ существует, то возвращает следующие данные:
            Адрес - Addres
            Форма собственности - ownForm
            Вид недвижимости - type
            Форма использования - forUseType
            Целевое назначение - forType
            {
               "status": true,
               "message": null,
               "response":    {
                  "propCode": 102020007000101061,
                  "address": "г. Бишкек, пр. Чыңгыза Айтматова, д. 18 кв. 61.",
                  "ownForm": "Частная",
                  "type": "Часть строения ",
                  "forUseType": "Квартира",
                  "forType": "Жилое"
               }
            }
        Если ЕНИ не существует:
            {
               "status": false,
               "message": "Код ЕНИ не существует либо ликвидирован",
               "response": null
            }
        """
        url = self.url.join(['api_GetPropertyInfo', eni_code])
        response = get_request(url, method="GET")

        return response

    def getPropertyPDF(self, eni_code):
        """
        Выписка прав и ограничений на ЕНИ в формате Pdf.
        """
        url = ''.join([self.url, 'api_GetPropertyPdf/', eni_code])
        response = get_request(url, method="GET")

        return response

    def getPropertyHistoryPDF(self, eni_code):
        """
        Выписка истории прав и ограничений в формате Pdf
        """
        url = self.url.join(['api_GetPropertyHistoryPdf', eni_code])
        response = get_request(url, method="GET")

        return response

    def getTechParamPDF(self, eni_code):
        """
        Справка о технических параметрах в формате Pdf
        Результат работы данных сервисов, если результат положительный:
        {
           "status": true,
           "message": null,
           "response":    {
              "info":       {
                 "propCode": 102020007000101061,
                 "address": "г. Бишкек, пр. Чыңгыза Айтматова, д. 18 кв. 61.",
                 "ownForm": "Частная",
                 "type": "Часть строения ",
                 "forUseType": "Квартира",
                 "forType": "Жилое"
              },
              "image": <Pdf файл в формате BASE64String>,
              "uri": <Путь к копии справки>,
              "name": "Информация о недвижимости 1-02-02-0007-0001-01-061.Pdf"
           }
        }

        """
        url = self.url.join(['api_TechParamPdf', eni_code])
        response = get_request(url, method="GET")

        return response

    def getPersonRightsPdf(self, eni_code, full_name=None):
        """
        Справка об имении либо неимении прав собственности на недвижимое имущество.
        Если на человека с данным ПИН-ом зарегистрировано или ранее было зарегистрировано
        недвижимое имущество, то будет выдана справка об имении, иначе справка о неимении.
        {
           "status": true,
           "message": null,
           "response":    {
              "image":  <Pdf файл в формате BASE64String>,
              "uri":  <Путь к копии справки>
           }
        }

        ВАЖНО: Параметры ПИН и ФИО автоматически заполняются мобильным приложением.
        Данную справку можно брать «только на себя»!

        """
        url = self.url.join(['api_GetPersonRightsPdf', eni_code, full_name])
        response = get_request(url, method="GET")

        return response
