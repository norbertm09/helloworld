
import os
import base64
import tempfile
from fastapi import FastAPI, HTTPException, Path, Query
import requests

app = FastAPI()

def save_cert(varname):
    content = os.getenv(varname)
    if not content:
        raise ValueError(f"{varname} is missing")
    decoded = base64.b64decode(content)
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(decoded)
    temp_file.close()
    return temp_file.name

def visa_headers():
    return {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

def visa_cert():
    return (
        save_cert("VISA_CERT_B64"),
        save_cert("VISA_KEY_B64")
    )

@app.post("/simulate/payouts")
def simulate_payout():
    url = "https://sandbox.api.visa.com/visapayouts/v3/payouts"
    try:
        res = requests.post(
            url,
            headers=visa_headers(),
            json={},  # Payload de test vide ou exemple à insérer
            cert=visa_cert(),
            auth=(os.getenv("VISA_USER"), os.getenv("VISA_PASS"))
        )
        return {"status": res.status_code, "response": res.json() if res.content else res.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/simulate/payouts/{payout_id}")
def get_payout(payout_id: str = Path(...)):
    url = f"https://sandbox.api.visa.com/visapayouts/v3/payouts/{payout_id}"
    try:
        res = requests.get(url, headers=visa_headers(), cert=visa_cert(), auth=(os.getenv("VISA_USER"), os.getenv("VISA_PASS")))
        return {"status": res.status_code, "response": res.json() if res.content else res.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/simulate/receivedfunds")
def get_received_funds():
    url = "https://sandbox.api.visa.com/visapayouts/v3/receivedfunds"
    try:
        res = requests.get(url, headers=visa_headers(), cert=visa_cert(), auth=(os.getenv("VISA_USER"), os.getenv("VISA_PASS")))
        return {"status": res.status_code, "response": res.json() if res.content else res.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/simulate/eligibility")
def check_eligibility():
    url = "https://sandbox.api.visa.com/visapayouts/v3/additionalservices/eligibility"
    try:
        res = requests.get(url, headers=visa_headers(), cert=visa_cert(), auth=(os.getenv("VISA_USER"), os.getenv("VISA_PASS")))
        return {"status": res.status_code, "response": res.json() if res.content else res.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/simulate/fx-quotes")
def get_fx_quotes():
    url = "https://sandbox.api.visa.com/forex/v3/quotes"
    try:
        res = requests.get(url, headers=visa_headers(), cert=visa_cert(), auth=(os.getenv("VISA_USER"), os.getenv("VISA_PASS")))
        return {"status": res.status_code, "response": res.json() if res.content else res.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/simulate/legacy-send")
def legacy_send_payout():
    url = "https://sandbox.api.visa.com/payouts/v1/sendpayouts"
    try:
        res = requests.post(
            url,
            headers=visa_headers(),
            json={},  # Payload exemple à insérer
            cert=visa_cert(),
            auth=(os.getenv("VISA_USER"), os.getenv("VISA_PASS"))
        )
        return {"status": res.status_code, "response": res.json() if res.content else res.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
