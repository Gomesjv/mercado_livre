import requests
import uuid
from decouple import config


class MercadoPago:
    BASE_URL = 'https://api.mercadopago.com'

    def __init__(self):
        self.__acess_token = config('MP_ACCESS_TOKEN')
        self.__headers = {
    'Content-type': 'aplication/json',
    'Authorization': f'Bearer {self.__acess_token}',
}

    def __post(self, path: str, payload: dict) -> dict:
        url=f'{self.BASE_URL}{path}'
        headers ={**self.__headers, 'X-Idempotency-Key': str(uuid.uuid4())}
        response = requests.post(
            url=url,
            json=payload,
            headers=headers,
        )
        try:
            response.raise_for_status()
        except requests.HTTPErro:
            try:
                error = response.json()
            except ValueError:
                error = response.text
                raise RuntimeError(f'Erro MP {response.status_code}:{error}')
        return response.json()

    def __create_payment(self, payment_payload: dict) -> dict:
        return self.__post('/v1/payments', payment_payload )

    def pay_with_pix(self, amount: float, description: str, payer: dict) -> dict:
        payload = {
        'transaction_amount' : amount,
        'description': description,
        'payment_method_id': 'pix',
        'payer': payer,
}
        return self.__create_payment(payload)
















# response = requests.post(
#     url= f'{BASE_URL}/v1/payments',
#     json=payload,
#     headers=headers
# )

# print(response.json())