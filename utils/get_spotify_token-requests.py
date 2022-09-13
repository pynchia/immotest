import base64
import json
from secrets import *

import httpx

client_id = "d8a71f09a5f94f6594205652a783ca48"
client_secret = "8f06313016084ff7b0f9fb2301749494"
# Encode as Base64
message = f"{client_id}:{client_secret}"
messageBytes = message.encode("ascii")
base64Bytes = base64.b64encode(messageBytes)
base64Message = base64Bytes.decode("ascii")

url = "https://accounts.spotify.com/api/token"
headers = {"Authorization": f"Basic {base64Message}"}
data = {"grant_type": "client_credentials"}

resp = httpx.post(url, headers=headers, data=data)

print(json.dumps(resp.json(), indent=2))
