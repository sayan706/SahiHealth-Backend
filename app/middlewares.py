import json

from datetime import datetime
from rest_framework.response import Response
from django.utils.deprecation import MiddlewareMixin


class FormatDateTimeMiddleware(MiddlewareMixin):
  def process_response(self, request, response):
    if isinstance(response, Response):
      data = json.loads(response.content)
      formatted_data = self.format_dates(data)
      response.content = json.dumps(formatted_data)

    return response

  def format_dates(self, data):
    if isinstance(data, dict):
      return {k: self.format_dates(v) for k, v in data.items()}
    elif isinstance(data, list):
      return [self.format_dates(i) for i in data]
    elif isinstance(data, str):
      try:
        dt = datetime.fromisoformat(data)

        # Get the day without leading zeros
        day = dt.day
        formatted_date = f"{day}{self._get_day_suffix(day)} {dt.strftime('%b %Y')}"

        return formatted_date
      except ValueError:
        # If the date string is not in ISO format, return the original string
        return data

    return data

  @staticmethod
  def _get_day_suffix(day):
    if 11 <= day <= 13:
      return 'th'

    return {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
