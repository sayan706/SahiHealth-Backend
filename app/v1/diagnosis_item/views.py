from utils import exceptions
from rest_framework.views import APIView
from utils.response_handler import custom_response_handler
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from app.models import Diagnosis, DiagnosisItem
from app.serializers.diagnosis import DiagnosisSerializer


class DiagnosisAPIView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  # Define search fields at the class level
  search_fields = ['title']

  def get(self, request, format=None):
    diagnosises = Diagnosis.objects.all()

    # Apply search filter
    search_filter = SearchFilter()

    if 'search' in request.query_params:
      diagnosises = search_filter.filter_queryset(request, diagnosises, self)

    diagnosises = diagnosises[:50]
    serializedDiagnosises = DiagnosisSerializer(diagnosises, many=True)

    return custom_response_handler(
      status=status.HTTP_200_OK,
      message="Get all diagnosises",
      data=serializedDiagnosises.data
    )

  def post(self, request, *args, **kwargs):
    serializedDiagnosis = DiagnosisSerializer(data=request.data)

    if serializedDiagnosis.is_valid():
      diagnosis = serializedDiagnosis.save()
      serializedDiagnosis = DiagnosisSerializer(instance=diagnosis)
    else:
      raise exceptions.InvalidRequestBodyException(
        detail=serializedDiagnosis.errors,
        code='Invalid request data'
      )

    return custom_response_handler(
      status=status.HTTP_201_CREATED,
      message="Diagnosis created successfully",
      data=serializedDiagnosis.data
    )

  def patch(self, request, pk, format=None):
    diagnosis = None

    try:
      diagnosis = Diagnosis.objects.get(id=pk)
    except Diagnosis.DoesNotExist:
      raise exceptions.DoesNotExistException(
        detail=f'No diagnosis found with id {pk}',
        code=f'Diagnosis not found'
      )

    serializedDiagnosis = DiagnosisSerializer(
      instance=diagnosis,
      data=request.data,
      partial=True
    )

    if serializedDiagnosis.is_valid():
      diagnosis = serializedDiagnosis.save()
      serializedDiagnosis = DiagnosisSerializer(instance=diagnosis)
    else:
      raise exceptions.InvalidRequestBodyException(
        detail=serializedDiagnosis.errors,
        code='Invalid request data'
      )

    return custom_response_handler(
      status=status.HTTP_200_OK,
      message="Diagnosis updated successfully",
      data=serializedDiagnosis.data
    )


class DiagnosisItemAPIView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def delete(self, request, pk, format=None):
    diagnosis_item = None

    try:
      diagnosis_item = DiagnosisItem.objects.get(id=pk)
      diagnosis_item.delete()
    except DiagnosisItem.DoesNotExist:
      raise exceptions.DoesNotExistException(
        detail=f'No diagnosis item found with id {pk}',
        code='Diagnosis item not found'
      )

    return custom_response_handler(
      status=status.HTTP_200_OK,
      message=f'1 item has been deleted',
      data=None
    )
