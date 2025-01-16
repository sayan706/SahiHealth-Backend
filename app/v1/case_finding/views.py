import os

from utils import exceptions
from django.conf import settings
from rest_framework.views import APIView
from utils.response_handler import custom_response_handler
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from app.models import CaseFinding, FindingImage


class CaseFindingAPIView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def delete(self, request, pk, format=None):
    base_dir = os.path.join(settings.MEDIA_ROOT, 'case')

    try:
      caseFinding = CaseFinding.objects.get(id=pk)
      findingImages = FindingImage.objects.filter(case_finding=caseFinding)

      for findingImage in findingImages:
        final_file_path = os.path.join(
          base_dir,
          str(caseFinding.case.id),
          'finding',
          findingImage.uploaded_file_name
        )

        # If the image exists then delete from the storage
        if os.path.exists(final_file_path):
          os.remove(final_file_path)

      # At last delete the case finding
      caseFinding.delete()

      return custom_response_handler(
        status=status.HTTP_200_OK,
        message='Finding deleted successfully',
        data=None
      )
    except CaseFinding.DoesNotExist:
      raise exceptions.DoesNotExistException(
        detail=f'No finding found with id {pk}',
        code='Finding not found'
      )
