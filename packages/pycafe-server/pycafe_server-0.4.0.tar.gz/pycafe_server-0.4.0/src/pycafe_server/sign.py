import base64
from . import config
import jwt


def sign_hash(hash: str, user_id: str) -> str:
    private_key_base64 = config.PYCAFE_SERVER_SIGN_PRIVATE_KEY
    private_key = base64.b64decode(private_key_base64)
    # TODO: we should include the user id, otherwise we cannot confirm the user
    data = {
        "hash": hash,
        "user_id": user_id,
    }
    return jwt.encode(data, private_key, algorithm="RS256")
