import os
import time

from utils import exceptions
from dotenv import load_dotenv
from django.conf import settings
from rest_framework.views import APIView
from utils.response_handler import custom_response_handler
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from app.models import Case, CaseDocument
from app.serializers.case_document import (
  CaseDocumentSerializer, DocumentsUploadSerializer, UpdateCaseDocumentSerializer
)


load_dotenv()


class CaseDocumentAPIView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]
  # parser_classes = [MultiPartParser]

  def get_parser_classes(self):
    if self.request.method == 'POST':
      return [MultiPartParser]
    elif self.request.method == 'PATCH':
      return [JSONParser]

    return super().get_parser_classes()

  def post(self, request, *args, **kwargs):
    if kwargs.get('action') == 'upload':
      case = None
      caseDocuments = []
      base_dir = os.path.join(settings.MEDIA_ROOT, 'case')
      BACKEND_URL = os.getenv('BACKEND_URL', default='http://localhost:8000')
      serializedDocumentsUpload = DocumentsUploadSerializer(data=request.data)

      if serializedDocumentsUpload.is_valid():
        case_id = serializedDocumentsUpload.validated_data['case_id']
        document_section = serializedDocumentsUpload.validated_data['document_section']
        files = serializedDocumentsUpload.validated_data['files']

        try:
          case = Case.objects.get(id=case_id)
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
          upload_dir = os.path.join(base_dir, str(case_id), str(document_section).lower())

          os.makedirs(upload_dir, exist_ok=True)
          final_file_path = os.path.join(upload_dir, uploaded_file_name)

          with open(final_file_path, 'wb') as destination:
            for chunk in file.chunks():
              destination.write(chunk)

          uploaded_file_url = f'{BACKEND_URL}{settings.MEDIA_URL}case/{case_id}/{document_section}/{uploaded_file_name}'

          # Create a document with the provided case_id
          caseDocument = CaseDocument.objects.create(
            case=case,
            file_name=file_name,
            file_extension=file_extension,
            uploaded_file_name=uploaded_file_name,
            file_url=uploaded_file_url,
            document_section=document_section,
          )

          # Accumulate all uploaded files in a list
          caseDocuments.append(caseDocument)

        serializedCaseDocuments = CaseDocumentSerializer(
          instance=caseDocuments,
          many=True
        )

        return custom_response_handler(
          status=status.HTTP_201_CREATED,
          message='Documents uploaded successfully',
          data=serializedCaseDocuments.data,
        )
      else:
        raise exceptions.InvalidRequestBodyException(
          detail=serializedDocumentsUpload.errors,
          code='Invalid request body'
        )

  def patch(self, request, *args, **kwargs):
    if kwargs.get('action') == 'rename':
      caseDocument = None
      case_document_id = kwargs.get('pk')

      try:
        caseDocument = CaseDocument.objects.get(id=case_document_id)
      except CaseDocument.DoesNotExist:
        raise exceptions.DoesNotExistException(
          detail=f'No case document found with id {case_document_id}',
          code='Case document not found'
        )

      serializedUpdateCaseDocument = UpdateCaseDocumentSerializer(
        instance=caseDocument,
        data=request.data,
        partial=True
      )

      if serializedUpdateCaseDocument.is_valid():
        updatedCaseDocument = serializedUpdateCaseDocument.save()
        serializedCaseDocument = CaseDocumentSerializer(instance=updatedCaseDocument)

        return custom_response_handler(
          status=status.HTTP_200_OK,
          message='File renamed successfully',
          data=serializedCaseDocument.data
        )
      else:
        raise exceptions.InvalidRequestBodyException(
          detail=serializedUpdateCaseDocument.errors,
          code='Invalid request body'
        )

  def delete(self, request, *args, **kwargs):
    if kwargs.get('action') == 'remove':
      caseDocument = None
      case_document_id = kwargs.get('pk')
      base_dir = os.path.join(settings.MEDIA_ROOT, 'case')

      try:
        caseDocument = CaseDocument.objects.get(id=case_document_id)
      except CaseDocument.DoesNotExist:
        raise exceptions.DoesNotExistException(
          detail=f'No case document found with id {case_document_id}',
          code='Case document not found'
        )

      # Delete the record of the file from the database
      caseDocument.delete()

      final_file_path = os.path.join(
        base_dir,
        str(caseDocument.case.id),
        str(caseDocument.document_section).lower(),
        caseDocument.uploaded_file_name
      )

      # If the file exists then delete from the storage
      if os.path.exists(final_file_path):
        os.remove(final_file_path)

      serializedCaseDocument = CaseDocumentSerializer(instance=caseDocument)

      return custom_response_handler(
        status=status.HTTP_200_OK,
        message='File removed successfully',
        data=serializedCaseDocument.data
      )
