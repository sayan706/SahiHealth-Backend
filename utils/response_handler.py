from datetime import datetime
from rest_framework.response import Response


def custom_response_handler(status, message, data):
  response = {
    "status": status,
    "message": message,
    "data": data,
    "timestamp": int(datetime.utcnow().timestamp()),
  }

  return Response(response, status=status)
