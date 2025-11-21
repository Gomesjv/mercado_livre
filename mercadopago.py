import requests 
import uuid

from decouple import config


MP_ACCESS_TOKEN = config('MP_ACCESS_TOKEN')

BASE_URL = 'https://api.mercadopago.com'

headers = {
    'Content-type': 'aplication/json',
    'Authorization': f'Bearer {MP_ACCESS_TOKEN}',
    'X-Idempotency-Key': str(uuid.uuid4()),
} 

payload = {
    'transaction_amount' : 100,
    'description': 'Pix teste',
    'payment_method_id': 'pix',
    'payer': {
        'email': 'teste_user_123@testeuser.com',
        'identification':{
            'type': 'CPF',
            'number': '95749019047'
        }
    }
} 


response = requests.post(
    url= f'{BASE_URL}/v1/payments',
    json=payload,
    headers=headers
)

print(response.json())