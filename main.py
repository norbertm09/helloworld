
import os
import base64
import tempfile
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
import requests
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def save_cert(varname):
    content = os.getenv(varname)
    if not content:
        raise ValueError(f"{varname} is missing")
    decoded = base64.b64decode(content)
    file = tempfile.NamedTemporaryFile(delete=False)
    file.write(decoded)
    file.close()
    return file.name

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/simulate/payouts", response_class=HTMLResponse)
def simulate_payout(
    request: Request,
    amount: str = Form(...),
    card: str = Form(...),
    sender_name: str = Form(...),
    recipient_name: str = Form(...)
):
    try:
        cert_file = save_cert("VISA_CERT_B64")
        key_file = save_cert("VISA_KEY_B64")
        user = os.getenv("VISA_USER")
        passwd = os.getenv("VISA_PASS")

        payload = {
            "amount": amount,
            "transactionCurrencyCode": "USD",
            "recipientPrimaryAccountNumber": card,
            "senderName": sender_name,
            "retrievalReferenceNumber": "412770451018",
            "systemsTraceAuditNumber": "451018",
            "localTransactionDateTime": "2025-05-23T17:00:00",
            "acquiringBin": "408999",
            "acquirerCountryCode": "840",
            "businessApplicationId": "AA",
            "merchantCategoryCode": "6012",
            "pointOfServiceData": {
                "panEntryMode": "90",
                "posConditionCode": "00",
                "motoECIIndicator": "0"
            }
        }

        response = requests.post(
            "https://sandbox.api.visa.com/visapayouts/v3/payouts",
            json=payload,
            cert=(cert_file, key_file),
            auth=(user, passwd)
        )

        return templates.TemplateResponse("result.html", {
            "request": request,
            "status": response.status_code,
            "result": response.json() if response.content else response.text
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
