import os
import time

from utils import exceptions
from dotenv import load_dotenv
from django.conf import settings
from rest_framework.views import APIView
from utils.response_handler import custom_response_handler
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from app.models import Case, FindingImage
from app.serializers.finding_image import FindingImageSerializer, ImagesUploadSerializer


load_dotenv()


class FindingImageAPIView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]
  parser_classes = [MultiPartParser]

  def post(self, request, *args, **kwargs):
    if kwargs.get('action') == 'upload':
      findingImages = []
      base_dir = os.path.join(settings.MEDIA_ROOT, 'case')
      BACKEND_URL = os.getenv('BACKEND_URL', default='http://localhost:8000')
      serializedImagesUpload = ImagesUploadSerializer(data=request.data)

      if serializedImagesUpload.is_valid():
        case_id = serializedImagesUpload.validated_data['case_id']
        files = serializedImagesUpload.validated_data['files']

        try:
          Case.objects.get(id=case_id)
        except Case.DoesNotExist:
          raise exceptions.DoesNotExistException(
            detail=f'No case found with id {case_id}',
            code='Case not found'
          )

        for file in files:
          # Save file to the media folder
          timestamp = int(time.time() * 1000)
          file_name = file.name.rsplit('.', 1)[0]
          file_extension = file.name.rsplit('.', 1)[1]
          uploaded_file_name = f'{file_name}-{timestamp}.{file_extension}'
          upload_dir = os.path.join(base_dir, str(case_id), 'finding')

          os.makedirs(upload_dir, exist_ok=True)
          final_file_path = os.path.join(upload_dir, uploaded_file_name)

          with open(final_file_path, 'wb') as destination:
            for chunk in file.chunks():
              destination.write(chunk)

          uploaded_file_url = f'{BACKEND_URL}{settings.MEDIA_URL}case/{case_id}/finding/{uploaded_file_name}'

          # Create a document with the provided case_id
          findingImage = FindingImage.objects.create(
            file_name=file_name,
            file_extension=file_extension,
            uploaded_file_name=uploaded_file_name,
            file_url=uploaded_file_url
          )

          # Insert the uploaded image in a list
          findingImages.append(findingImage)

        serializedFindingImages = FindingImageSerializer(
          instance=findingImages,
          many=True
        )

        return custom_response_handler(
          status=status.HTTP_201_CREATED,
          message='Images uploaded successfully',
          data=serializedFindingImages.data,
        )
      else:
        raise exceptions.InvalidRequestBodyException(
          detail=serializedImagesUpload.errors,
          code='Invalid request body'
        )

  def delete(self, request, *args, **kwargs):
    if kwargs.get('action') == 'remove':
      findingImage = None
      finding_image_id = kwargs.get('pk')
      base_dir = os.path.join(settings.MEDIA_ROOT, 'case')

      try:
        findingImage = FindingImage.objects.get(id=finding_image_id)
      except FindingImage.DoesNotExist:
        raise exceptions.DoesNotExistException(
          detail=f'No finding image found with id {finding_image_id}',
          code='Finding image not found'
        )

      # Delete the record of the image from the database
      findingImage.delete()

      final_file_path = os.path.join(
        base_dir,
        str(findingImage.case_finding.case.id),
        'finding',
        findingImage.uploaded_file_name
      )

      # If the image exists then delete from the storage
      if os.path.exists(final_file_path):
        os.remove(final_file_path)

      serializedFindingImage = FindingImageSerializer(
        instance=findingImage,
        fields=[
          'file_name',
          'file_extension'
        ]
      )

      return custom_response_handler(
        status=status.HTTP_200_OK,
        message='Image has been successfully deleted',
        data=serializedFindingImage.data
      )
