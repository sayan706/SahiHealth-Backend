from utils import exceptions
from django.shortcuts import render
from rest_framework.views import APIView
from utils.response_handler import custom_response_handler
from rest_framework import status
from app.models import Assistant
from app.serializers.assistant import AssistantSerializer, ProfileSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
class AssistantAPIView(APIView):
  def get(self, request, pk=None, format=None):
    data = None
    message = None
    assistant_id = None
    query_params = request.query_params

    if pk is not None:
      assistant_id = pk
    elif 'assistant_id' in query_params:
      assistant_id = query_params['assistant_id']

    if assistant_id is not None:
      try:
        assistant = Assistant.objects.get(id=assistant_id)
        serializedAssistant = AssistantSerializer(
          instance=assistant,
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
          detail=f'No assistant found with id {assistant_id}',
          code='Assistant not found'
        )
    elif not ('page_size' in query_params and 'page' in query_params):
      raise exceptions.GenericException(
        detail='Provide page_size & page in query params',
        code='Page Configuration Missing'
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
        profile_exclude=[
          'id',
          'user',
          'is_active',
          'created_at',
          'updated_at'
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

  def patch(self, request, pk=None, format=None):
    data = None
    message = None
    assistant = None
    assistant_id = None
    request_data = request.data
    query_params = request.query_params

    if pk is not None:
      assistant_id = pk
    elif 'assistant_id' in query_params:
      assistant_id = query_params['assistant_id']
    else:
      raise exceptions.GenericException(
        detail='Mention id as path variable or assistant_id in query params',
        code='Identifier not found for the assistant'
      )

    try:
      assistant = Assistant.objects.get(id=assistant_id)
    except Assistant.DoesNotExist:
      raise exceptions.DoesNotExistException(
        detail=f'No assistant found with id {assistant_id}',
        code='Assistant not found'
      )

    # Update profile if present
    profile_data = request_data.get('profile', {})

    if profile_data:
      # Get the existing profile linked to the assistant
      assistantProfile = assistant.profile
      serializedProfile = ProfileSerializer(instance=assistantProfile, data=profile_data, partial=True)

      if serializedProfile.is_valid(raise_exception=True):
        # Update the profile instance
        serializedProfile.save()

    # Update assistant specific data if present
    assistant_data = {}

    if 'is_active' in request_data:
      assistant_data['is_active'] = request_data['is_active']

    if assistant_data:
      serializedAssistant = AssistantSerializer(instance=assistant, data=assistant_data, partial=True)

      if serializedAssistant.is_valid(raise_exception=True):
        # Update the assistant instance
        serializedAssistant.save()

    # Serialize the updated assistant instance
    serializedAssistant = AssistantSerializer(
      instance=assistant,
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
    message = "Profile updated successfully"

    return custom_response_handler(
      status=status.HTTP_200_OK,
      message=message,
      data=data
    )
