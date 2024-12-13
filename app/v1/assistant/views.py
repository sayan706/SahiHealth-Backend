from utils import exceptions
from django.shortcuts import render
from rest_framework.views import APIView
from utils.response_handler import custom_response_handler
from rest_framework import status
from app.models import Assistant
from app.serializers.assistant import AssistantSerializer , ProfileSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
class AssistantAPIView(APIView):
  def get(self, request, pk=None, format=None):
    data = None
    message = None
    query_params = request.query_params

    if pk is not None:
      try:
        assistant = Assistant.objects.get(id=pk)
        serializedAssistant = AssistantSerializer(instance=assistant)
        data = serializedAssistant.data
        message = "Get Assistant"
      except Assistant.DoesNotExist:
        raise exceptions.DoesNotExistException(
          detail=f'No assistant found with id {pk}',
          code="Assistant Not Found"
        )
    elif 'assistant_id' in query_params:
      try:
        assistant = Assistant.objects.get(id=query_params['assistant_id'])
        serializedAssistant = AssistantSerializer(instance=assistant)
        data = serializedAssistant.data
        message = "Get Assistant"
      except Assistant.DoesNotExist:
        raise exceptions.DoesNotExistException(
          detail=f'No assistant found with id {query_params["assistant_id"]}',
          code="Assistant Not Found"
        )
    elif not ('page_size' in query_params and 'page' in query_params):
      raise exceptions.GenericException(detail='Provide page_size & page in query params')
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
      
      serializedAssistants = AssistantSerializer(instance=assistants, many=True)
      data = {
        'values': serializedAssistants.data,
        'total_count': total_count,
        'page_size': page_size,
        'current_page': current_page,
        'next_page': None if (paginator.num_pages - current_page) <= 0 else current_page + 1,
        'total_pages': paginator.num_pages,
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
        query_params = request.query_params

        if 'assistant_id' not in query_params:
            raise exceptions.GenericException(detail='Provide assistant_id in query params')

        try:
            assistant = Assistant.objects.get(id=query_params['assistant_id'])
        except Assistant.DoesNotExist:
            raise exceptions.DoesNotExistException(
                detail=f'No assistant found with id {query_params["assistant_id"]}',
                code="Assistant Not Found"
            )

        request_data = request.data

        # Update Profile data if present
        profile_data = request_data.get('profile', {})
        if profile_data:
            # Get the existing profile linked to the assistant
            profile_instance = assistant.profile

            print(f"Updating Profile for Assistant: {assistant.id}")
            profile_serializer = ProfileSerializer(instance=profile_instance, data=profile_data, partial=True)
            print(f"Profile data: {profile_data}")
            if profile_serializer.is_valid(raise_exception=True):
                profile_serializer.save()  # Update the existing profile

        # Update Assistant-specific data if present
        assistant_data = {}
        if 'role' in request_data:
            assistant_data['role'] = request_data['role']
        if 'is_active' in request_data:
            assistant_data['is_active'] = request_data['is_active']

        if assistant_data:
            assistant_serializer = AssistantSerializer(instance=assistant, data=assistant_data, partial=True)
            if assistant_serializer.is_valid(raise_exception=True):
                assistant_serializer.save()  # Update the assistant instance

        # Serialize the updated assistant instance
        serialized_assistant = AssistantSerializer(instance=assistant)
        data = serialized_assistant.data
        message = "Assistant updated successfully"

        return custom_response_handler(
            status=status.HTTP_200_OK,
            message=message,
            data=data
        )
