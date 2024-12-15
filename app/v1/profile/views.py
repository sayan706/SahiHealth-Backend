import os
import shutil

from utils import exceptions
from dotenv import load_dotenv
from django.conf import settings
from rest_framework.decorators import api_view
from utils.response_handler import custom_response_handler
from rest_framework import status
from app.models import Profile
from app.serializers.profile import ProfileSerializer, FileUploadSerializer


load_dotenv()


@api_view(['POST', 'DELETE'])
def upload_dp(request):
  profile = None
  profile_id = request.query_params['profile_id'][0]

  try:
    profile = Profile.objects.get(id=profile_id)
  except:
    raise exceptions.DoesNotExistException(
      detail=f'No profile found with id {profile_id}',
      code='Doctor not found'
    )

  if request.method == 'POST':
    file = None
    file_ext = None
    file_name = None
    request_data = {
      'file': request.FILES.get('file'),
      'file_ext': request.data.get('file_ext'),
      'file_name': request.data.get('file_name'),
    }
    serializedFileUpload = FileUploadSerializer(data=request_data)

    if serializedFileUpload.is_valid():
      file = serializedFileUpload.validated_data['file']
      file_ext = serializedFileUpload.validated_data['file_ext']
      file_name = serializedFileUpload.validated_data['file_name']
    else:
      raise exceptions.InvalidRequestBodyException(detail=serializedFileUpload.errors)

    if not file:
      raise exceptions.GenericException(
        detail=f'No picture provided for profile of id {profile_id}',
        code='No file provided'
      )
    else:
      base_dir = os.path.join(settings.MEDIA_ROOT, 'profile_picture', profile.role.lower())
      upload_dir = os.path.join(base_dir, str(profile.id))

      # Removing the existing folder and recreating it (if exists)
      if os.path.exists(upload_dir):
        shutil.rmtree(upload_dir)

      os.makedirs(upload_dir, exist_ok=True)
      uploaded_file_name = f'{file_name}.{file_ext}'
      final_file_path = os.path.join(upload_dir, uploaded_file_name)

      with open(final_file_path, 'wb') as dp:
        for chunk in file.chunks():
          dp.write(chunk)

      BACKEND_URL = os.getenv('BACKEND_URL', default='http://localhost:8000')
      uploaded_file_url = f'{BACKEND_URL}{settings.MEDIA_URL}profile_picture/{profile.role.lower()}/{profile.id}/{uploaded_file_name}'

      profile_data = {'dp_url': uploaded_file_url}
      serializedProfile = ProfileSerializer(instance=profile, data=profile_data, partial=True)

      if serializedProfile.is_valid():
        serializedProfile.save()

      return custom_response_handler(
        status=status.HTTP_200_OK,
        message="Profile picture uploaded successfully",
        data={
          'file_name': uploaded_file_name,
          'file_url': uploaded_file_url,
        }
      )
  elif request.method == 'DELETE':
    base_dir = os.path.join(settings.MEDIA_ROOT, 'profile_picture', profile.role.lower())
    upload_dir = os.path.join(base_dir, str(profile.id))

    # Removing the existing folder (if exists)
    if os.path.exists(upload_dir):
      shutil.rmtree(upload_dir)

    profile_data = {'dp_url': None}
    serializedProfile = ProfileSerializer(instance=profile, data=profile_data, partial=True)

    if serializedProfile.is_valid():
      serializedProfile.save()

    return custom_response_handler(
      status=status.HTTP_200_OK,
      message="Profile picture removed successfully",
      data={
        'file_url': None,
      }
    )
