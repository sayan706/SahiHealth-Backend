import os
import logging
import traceback

from datetime import datetime
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from .exceptions import InvalidRequestBodyException
from rest_framework.serializers import ValidationError


load_dotenv()
environment = os.getenv('ENV', default='dev').lower()


def get_response(exc):
	stack_trace = str(traceback.format_tb(exc.__traceback__)) if hasattr(exc, '__traceback__') else None
	status_code = None
	message = None
	errors = {}

	if isinstance(exc, ValidationError) or isinstance(exc, InvalidRequestBodyException):
		# Populate the errors dictionary
		for key, value in exc.detail.items():
			if isinstance(value, list):
				errors[key] = value[0]

		status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
		message = "Invalid Input Received" if exc.default_code in ['error', 'invalid'] else exc.default_code
	elif isinstance(exc, APIException):
		status_code = exc.status_code
		message = exc.default_code
		errors = {
			'error': str(exc)
		}
	else:
		status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		message = exc.__class__.__name__
		errors = {
			'error': str(exc)
		}

	logger = logging.getLogger(__name__)
	logger.info(f'{status_code} - {message}', extra={
		'errors': errors,
		'stack_trace': stack_trace
	})

	return Response(
		status=status_code,
		data={
			"status": status_code,
			"message": message,
			"errors": errors,
			"timestamp": int(datetime.utcnow().timestamp()),
			**({'stack_trace': stack_trace} if environment == 'dev' else {})
		}
	)


def global_exception_handler(exc, context):
	# Call REST framework's default exception handler first to get the standard error response.
	response = exception_handler(exc, context)

	# Now add the HTTP status code to the response.
	if response is not None:
		response.data['status_code'] = response.status_code

	if exc:
		return get_response(exc)

	logger = logging.getLogger(__name__)
	logger.info(f'exception handler - {response}')

	return response
