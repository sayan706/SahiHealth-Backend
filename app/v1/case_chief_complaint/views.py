from utils import exceptions
from rest_framework.views import APIView
from utils.response_handler import custom_response_handler
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from app.models import CaseChiefComplaint


class CaseChiefComplaintAPIView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def delete(self, request, pk, format=None):
    try:
      caseChiefComplaint = CaseChiefComplaint.objects.get(id=pk)
      caseChiefComplaint.delete()

      return custom_response_handler(
        status=status.HTTP_200_OK,
        message='Chief complaint deleted successfully',
        data=None
      )
    except CaseChiefComplaint.DoesNotExist:
      raise exceptions.DoesNotExistException(
        detail=f'No chief complaint found with id {pk}',
        code='Chief complaint not found'
      )
