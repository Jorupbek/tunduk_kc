import requests

from utils.constants import HEADERS


def get_request(url, method="POST", data=None):
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=HEADERS,
            data=data
        )

        # Проверка на успешный статус код (200 OK)
        response.raise_for_status()

        return response
    except requests.exceptions.HTTPError as e:
        print(f"HTTP ошибка: {e}")
        return None

    except requests.exceptions.RequestException as e:
        # Обработка ошибок, связанных с запросами
        print(f"Ошибка во время запроса: {e}")
        return None

    except Exception as e:
        # Обработка других исключений, если они возникнут
        print(f"Другая ошибка: {e}")
        return None
