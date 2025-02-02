from utils import exceptions
from rest_framework.views import APIView
from utils.response_handler import custom_response_handler
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from app.serializers.prescription import PrescriptionSerializer, CreatePrescriptionSerializer


class PrescriptionAPIView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def post(self, request, format=None):
    serializedCreatePrescription = CreatePrescriptionSerializer(data=request.data)

    if serializedCreatePrescription.is_valid():
      prescription = serializedCreatePrescription.save()
      serializedPrescription = PrescriptionSerializer(instance=prescription)

      return custom_response_handler(
        status=status.HTTP_201_CREATED,
        message='Prescription created successfully',
        data=serializedPrescription.data
      )
    else:
      raise exceptions.InvalidRequestBodyException(
        detail=serializedCreatePrescription.errors,
        code='Invalid request data'
      )
