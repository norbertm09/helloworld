
import os
import base64
import tempfile
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class VisaTransfer(BaseModel):
    amount: float
    card: str
    currency: str = "USD"
    sender_name: str
    recipient_name: str

def save_cert(varname):
    content = os.getenv(varname)
    if not content:
        raise ValueError(f"{varname} is missing")
    decoded = base64.b64decode(content)
    file = tempfile.NamedTemporaryFile(delete=False)
    file.write(decoded)
    file.close()
    return file.name

@app.get("/test-visa")
def test_visa():
    try:
        cert_file = save_cert("VISA_CERT_B64")
        key_file = save_cert("VISA_KEY_B64")
        user = os.getenv("VISA_USER")
        passwd = os.getenv("VISA_PASS")

        response = requests.get(
            "https://sandbox.api.visa.com/vdp/helloworld",
            cert=(cert_file, key_file),
            auth=(user, passwd)
        )

        return {
            "status": response.status_code,
            "response": response.json() if response.content else response.text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/send-visa")
def send_visa_payment(transfer: VisaTransfer):
    try:
        cert_file = save_cert("VISA_CERT_B64")
        key_file = save_cert("VISA_KEY_B64")
        user = os.getenv("VISA_USER")
        passwd = os.getenv("VISA_PASS")

        payload = {
            "amount": str(transfer.amount),
            "transactionCurrencyCode": transfer.currency,
            "recipientPrimaryAccountNumber": transfer.card,
            "senderName": transfer.sender_name,
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
            "https://sandbox.api.visa.com/visadirect/fundstransfer/v1/pushfundstransactions",
            json=payload,
            cert=(cert_file, key_file),
            auth=(user, passwd)
        )

        return {
            "status": response.status_code,
            "response": response.json() if response.content else response.text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
