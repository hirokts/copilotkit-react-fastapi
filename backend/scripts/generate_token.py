import jwt
from datetime import datetime, timedelta, UTC

SECRET = "dev-secret-key"
payload = {
    "user_id": "user_123",
    "exp": datetime.now(UTC) + timedelta(days=30),
}
token = jwt.encode(payload, SECRET, algorithm="HS256")
print(token)
