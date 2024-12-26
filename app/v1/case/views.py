from utils import exceptions
from rest_framework.views import APIView
from utils.response_handler import custom_response_handler
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.models import Case, Patient , Doctor , CaseChiefComplaint, CaseDocument, CaseFinding
from app.serializers.case import CaseSerializer


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
        message = "Get Case"
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
      message = "Get Cases by Patient"

    return custom_response_handler(
      status=status.HTTP_200_OK,
      message=message,
      data=data
    )

  def post(self, request, format=None):
    doctor_id = request.data.get('doctor_id')
    patient_id = request.data.get('patient_id')

    if not (doctor_id and patient_id):
      raise exceptions.GenericException(
        detail='Provide doctor_id & patient_id in request body',
        code='Doctor and patient identifiers missing'
      )
    
    try:
      doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
      raise exceptions.DoesNotExistException(
          detail=f'No doctor found with id {doctor_id}',
          code='Doctor not found'
        )
    
    try:
      patient = Patient.objects.get(id=patient_id)
    except Patient.DoesNotExist:
      raise exceptions.DoesNotExistException(
          detail=f'No patient found with id {patient_id}',
          code='Patient not found'
        )
    
    case_data = {
      'past_treatment': request.data.get('past_treatment'),
      'treatment_location': request.data.get('treatment_location'),
      'treatment_type': request.data.get('treatment_type'),
      'note': request.data.get('note'),
      'follow_up_id': request.data.get('follow_up_id'),
      'follow_up_date': request.data.get('follow_up_date'),
      'assigned_doctor': doctor,
      'patient': patient
    }

    case = Case.objects.create(**case_data)

    # for case findings, and documents and chief complaints

    chief_complaints = request.data.get('chief_complaints', [])
    for complaint in chief_complaints:
        CaseChiefComplaint.objects.create(
            case=case,
            title=complaint.get('title'),
            severity=complaint.get('severity'),
            duration=complaint.get('duration'),
            duration_unit=complaint.get('duration_unit')
        )
  
    findings = request.data.get('findings', [])
    for finding in findings:
        CaseFinding.objects.create(case=case, title=finding)

    documents = request.data.get('documents', [])
    for document in documents:
      CaseDocument.objects.create(
        case=case,
        file_name=document.get('file_name'),
        file_extension=document.get('file_extension'),
        file_url=document.get('file_url'),
        document_section=document.get('document_section')
      )

    serialized_case = CaseSerializer(
      instance=case,
      fields=[
      'id',
      'patient',
      'assigned_doctor',
      'chief_complaints',
      'findings',
      'documents',
      'past_treatment',
      'treatment_location',
      'treatment_type',
      'note',
      'follow_up_id',
      'follow_up_date',
      'created_at'
      ]
    )

    return custom_response_handler(
      status=status.HTTP_201_CREATED,
      message="Case created successfully",
      data=serialized_case.data
    )
    