import logging

from datetime import datetime
from rest_framework.response import Response


def custom_response_handler(status, message, data):
  response = {
    "status": status,
    "message": message,
    "data": data,
    "timestamp": int(datetime.utcnow().timestamp()),
  }

  logger = logging.getLogger(__name__)
  logger.info(f'{response["status"]} - {response["message"]}', extra={'data': response['data']})

  return Response(response, status=status)
