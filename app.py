from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from services import MercadoPago

mp = MercadoPago()


app = FastAPI()

templates = Jinja2Templates(
    directory='templates',
) 

@app.get('/', response_class= HTMLResponse)
async def checkout_page(request : Request):
    return templates.TemplateResponse(
        name='checkout.html',
        context={'request':request},
    )

@app.get('/create_payment')
async def create_payment(request : Request):
    data = await request.json()
    method = data.get('payment_method')
    amount = float(data.get('transaction_amount', 0))
    description = data.get('description')

    try:
        if method == 'pix':
            payer = {
                'email' : data.get('email'),
                'identification': {
                    'type': 'CPF',
                    'number': data.get('identification_number'),
                },
            }
            result = mp.pay_with_pix(
                amount=amount,
                description=description,
                payer=payer,
            )
        else:
            raise HTTPException(status_code=400, detail='metodo de pagamento invalido')
    except RuntimeError as err:
        raise HTTPException(status_code=502, detail=(err))
