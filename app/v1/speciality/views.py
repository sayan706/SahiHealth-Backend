from utils import exceptions
from rest_framework.views import APIView
from utils.response_handler import custom_response_handler
from rest_framework import status
from app.models import Speciality
from app.serializers.speciality import SpecialitySerializer


class SpecialityAPIView(APIView):
  def get(self, request, format=None):
    specialities = Speciality.objects.all()
    serializedSpecialities = SpecialitySerializer(specialities, many=True)

    return custom_response_handler(
      status=status.HTTP_200_OK,
      message="Get All Specialities",
      data=serializedSpecialities.data
    )
