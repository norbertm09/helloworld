
import os
import base64
import tempfile
import requests
from fastapi import FastAPI, HTTPException

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
