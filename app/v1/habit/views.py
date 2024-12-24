from utils import exceptions
from rest_framework.views import APIView
from utils.response_handler import custom_response_handler
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from app.models import Habit
from app.serializers.habit import HabitSerializer


# Create your views here.
class HabitAPIView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request, pk=None, format=None):
    data = None
    message = None

    if pk is not None:
      try:
        habit = Habit.objects.get(id=pk)
        serializedHabit = HabitSerializer(instance=habit)
        data = serializedHabit.data
        message = "Get Habit"
      except Habit.DoesNotExist:
        raise exceptions.DoesNotExistException(
          detail=f'No habit found with id {pk}',
          code='Habit not found'
        )
    else:
      habits = Habit.objects.all()
      serializedHabits = HabitSerializer(instance=habits, many=True)
      data = serializedHabits.data
      message = "Get All Habits"

    return custom_response_handler(
      status=status.HTTP_200_OK,
      message=message,
      data=data
    )
