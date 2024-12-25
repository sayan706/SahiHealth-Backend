from utils import exceptions
from rest_framework.views import APIView
from utils.response_handler import custom_response_handler
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.models import Profile, Assistant
from app.serializers.profile import UpdateProfileSerializer
from app.serializers.assistant import AssistantSerializer, UpdateAssistantSerializer


# Create your views here.
class AssistantAPIView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request, format=None):
    data = None
    message = None
    query_params = request.query_params

    # Retrieve the profile instance
    profile = Profile.objects.get(user=request.user)

    if ('page_size' in query_params or 'page' in query_params):
      pass
    else:
      try:
        assistant = Assistant.objects.get(profile=profile)
        serializedAssistant = AssistantSerializer(
          instance=assistant,
          exclude=[
            'is_active',
            'created_at'
          ],
          profile_exclude=[
            'id',
            'is_active',
            'created_at',
            'updated_at'
          ],
          user_fields=[
            'username',
            'date_joined'
          ]
        )
        data = serializedAssistant.data
        message = "Get Assistant"
      except Assistant.DoesNotExist:
        raise exceptions.DoesNotExistException(
          detail=f'Requested assistant profile not found',
          code='Assistant not found'
        )

    if data is not None:
      pass
    elif not ('page_size' in query_params and 'page' in query_params):
      raise exceptions.GenericException(
        detail='Provide page_size & page in query params',
        code='Page configuration missing'
      )
    else:
      current_page = 1
      page_size = int(query_params['page_size'])

      assistants = Assistant.objects.all()
      total_count = len(assistants)
      paginator = Paginator(assistants, page_size)

      try:
        current_page = int(query_params['page'])
        assistants = paginator.page(current_page)
      except PageNotAnInteger:
        assistants = paginator.page(1)
      except EmptyPage:
        assistants = []

      serializedAssistants = AssistantSerializer(
        instance=assistants,
        many=True,
        exclude=['created_at'],
        profile_exclude=[
          'id',
          'email',
          'phone_number',
          'profile_picture',
          'role',
          'is_active',
          'created_at',
          'updated_at'
        ],
        user_fields=[
          'username',
          'date_joined'
        ]
      )
      data = {
        'count': len(serializedAssistants.data),
        'total_count': total_count,
        'total_pages': paginator.num_pages,
        'current_page': current_page,
        'next_page': None if (paginator.num_pages - current_page) <= 0 else current_page + 1,
        'page_size': page_size,
        'values': serializedAssistants.data,
      }
      message = "Get All Assistants"

    return custom_response_handler(
      status=status.HTTP_200_OK,
      message=message,
      data=data
    )

  def patch(self, request, format=None):
    data = None
    message = None
    request_data = request.data

    # Retrieve the profile and assistant instance
    assistant = None
    profile = Profile.objects.get(user=request.user)

    if profile.role != 'ASSISTANT':
      raise exceptions.PermissionDeniedException(
        detail='Only assistant is allowed to perform edit',
        code='Only assistant is allowed'
      )
    else:
      assistant = Assistant.objects.get(profile=profile)

    # Update profile instance if present
    profile_data = request_data.pop('profile', {})
    serializedUpdateProfile = UpdateProfileSerializer(
      instance=profile,
      data=profile_data,
      partial=True
    )

    if serializedUpdateProfile.is_valid():
      serializedUpdateProfile.save()
    else:
      raise exceptions.InvalidRequestBodyException(
        detail=serializedUpdateProfile.errors,
        code='Invalid profile data'
      )

    # Update assistant instance at last
    serializedUpdateAssistant = UpdateAssistantSerializer(
      instance=assistant,
      data=request_data,
      partial=True
    )

    if serializedUpdateAssistant.is_valid():
      updatedAssistant = serializedUpdateAssistant.save()
      serializedUpdatedAssistant = AssistantSerializer(
        instance=updatedAssistant,
        exclude=[
          'is_active',
          'created_at'
        ],
        profile_exclude=[
          'id',
          'is_active',
          'created_at',
          'updated_at'
        ],
        user_fields=[
          'username',
          'date_joined'
        ]
      )
      data = serializedUpdatedAssistant.data
      message = "Profile updated successfully"
    else:
      raise exceptions.InvalidRequestBodyException(
        detail=serializedUpdateAssistant.errors,
        code='Invalid assistant data'
      )

    return custom_response_handler(
      status=status.HTTP_200_OK,
      message=message,
      data=data
    )
