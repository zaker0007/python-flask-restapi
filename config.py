# JWT SETTING

from datetime import timedelta
JWT_SECRET_key="your_secret_key"

JWT_ACCESS_TOKEN_EXPIRE=timedelta(minutes=1)
JWT_RESFRESH_TOKEN_EXPIRE=timedelta(days=7)