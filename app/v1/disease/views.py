from utils import exceptions
from rest_framework.views import APIView
from utils.response_handler import custom_response_handler
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from app.models import Disease
from app.serializers.disease import DiseaseSerializer


# Create your views here.
class DiseaseAPIView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request, pk=None, format=None):
    data = None
    message = None

    if pk is not None:
      try:
        disease = Disease.objects.get(id=pk)
        serializedDisease = DiseaseSerializer(instance=disease)
        data = serializedDisease.data
        message = "Get Disease"
      except Disease.DoesNotExist:
        raise exceptions.DoesNotExistException(
          detail=f'No disease found with id {pk}',
          code='Disease not found'
        )
    else:
      diseases = Disease.objects.all()
      serializedDiseases = DiseaseSerializer(instance=diseases, many=True)
      data = serializedDiseases.data
      message = "Get All Diseases"

    return custom_response_handler(
      status=status.HTTP_200_OK,
      message=message,
      data=data
    )
