from utils import exceptions
from rest_framework.views import APIView
from utils.response_handler import custom_response_handler
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from app.models import DietAdvice


class DietAdviceAPIView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def delete(self, request, pk, format=None):
    diet_advice = None

    try:
      diet_advice = DietAdvice.objects.get(id=pk)
      diet_advice.delete()
    except DietAdvice.DoesNotExist:
      raise exceptions.DoesNotExistException(
        detail=f'No diet advice found with id {pk}',
        code='Diet advice not found'
      )

    return custom_response_handler(
      status=status.HTTP_200_OK,
      message=f'1 item has been deleted ({diet_advice.description})',
      data=None
    )
