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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.models import Patient, Case, CaseDocument
from app.serializers.case import CaseSerializer, CreateCaseSerializer, DocumentsUploadSerializer
from app.serializers.case_document import CaseDocumentSerializer


load_dotenv()


class CaseAPIView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request, pk=None, format=None):
    data = None
    message = None
    query_params = request.query_params
    patient_id = query_params.get('patient_id', None)

    if pk is not None:
      try:
        case = Case.objects.get(id=pk)
        serializedCase = CaseSerializer(
          instance=case,
          exclude=['is_active', 'updated_at']
        )
        data = serializedCase.data
        message = 'Get Case'
      except Case.DoesNotExist:
        raise exceptions.DoesNotExistException(
          detail=f'No case found with id {pk}',
          code='Case not found'
        )
    elif not (patient_id is not None and 'page_size' in query_params and 'page' in query_params):
      raise exceptions.GenericException(
        detail='Provide patient_id, page_size & page in query params',
        code='Patient identifier missing'
      )
    else:
      try:
        Patient.objects.get(id=patient_id)
      except Patient.DoesNotExist:
        raise exceptions.DoesNotExistException(
          detail=f'No patient found with id {patient_id}',
          code='Patient not found'
        )

      current_page = 1
      page_size = int(query_params['page_size'])

      cases = Case.objects.filter(patient_id=patient_id)
      total_count = len(cases)
      paginator = Paginator(cases, page_size)

      try:
        current_page = int(query_params['page'])
        cases = paginator.page(current_page)
      except PageNotAnInteger:
        cases = paginator.page(1)
      except EmptyPage:
        cases = []

      serializedCases = CaseSerializer(
        instance=cases,
        many=True,
        fields=[
          'id',
          'assigned_doctor',
          'findings',
          'is_follow_up',
          'follow_up_date',
          'is_active',
          'created_at'
        ]
      )
      data = {
        'count': len(serializedCases.data),
        'total_count': total_count,
        'total_pages': paginator.num_pages,
        'current_page': current_page,
        'next_page': None if (paginator.num_pages - current_page) <= 0 else current_page + 1,
        'page_size': page_size,
        'values': serializedCases.data,
      }
      message = 'Get Cases by Patient'

    return custom_response_handler(
      status=status.HTTP_200_OK,
      message=message,
      data=data
    )

  def post(self, request, format=None):
    serializedCreateCase = CreateCaseSerializer(data=request.data)

    if serializedCreateCase.is_valid():
      case = serializedCreateCase.save()
      serializedPatient = CaseSerializer(
        instance=case,
        exclude=[
          'is_active',
          'updated_at'
        ]
      )

      return custom_response_handler(
        status=status.HTTP_200_OK,
        message='Case created successfully',
        data=serializedPatient.data
      )
    else:
      raise exceptions.InvalidRequestBodyException(
        detail=serializedCreateCase.errors,
        code='Invalid request data'
      )


class DocumentsUploadAPIView(APIView):
  parser_classes = [MultiPartParser]

  def post(self, request, format=None):
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
        code='Invalid Request Body'
      )
