import base64
from typing import Tuple

import httpx


def get_spotify_token(client_id: str, client_secret: str) -> Tuple[str, int]:
    message = f"{client_id}:{client_secret}"
    base64Message = base64.b64encode(message.encode("ascii")).decode("ascii")
    URI = "https://accounts.spotify.com/api/token"
    headers = {"Authorization": f"Basic {base64Message}"}
    data = {"grant_type": "client_credentials"}
    resp = httpx.post(URI, headers=headers, data=data)
    resp_as_dict = resp.json()
    return resp_as_dict["access_token"], resp_as_dict["expires_in"]
