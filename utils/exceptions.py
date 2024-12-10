from rest_framework import status
from rest_framework.exceptions import APIException


class GenericException(APIException):
  def __init__(
      self,
      detail='Generic error occurred',
      code='Generic Error Occurred',
      status_code=status.HTTP_400_BAD_REQUEST
    ):
    super().__init__(detail=detail)

    self.default_code = code
    self.status_code = status_code


class InvalidRequestBodyException(APIException):
  def __init__(
      self,
      detail={},
      code='Invalid Input Received',
      status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    ):
    super().__init__(detail=detail)

    self.default_code = code
    self.status_code = status_code


class DoesNotExistException(APIException):
  def __init__(
      self,
      detail='Entity does not exist',
      code='Entity Does Not Exist',
      status_code=status.HTTP_404_NOT_FOUND
    ):
    super().__init__(detail=detail)

    self.default_code = code
    self.status_code = status_code


class UnauthorizedException(APIException):
  def __init__(
      self,
      detail='You are not authorized',
      code='Unauthorized Access',
      status_code=status.HTTP_401_UNAUTHORIZED
    ):
    super().__init__(detail=detail)

    self.default_code = code
    self.status_code = status_code
