import os

from utils import exceptions
from utils.response_handler import custom_response_handler
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.models import Doctor, Patient, Case
from app.serializers.doctor import DoctorSerializer
from app.serializers.case import CaseSerializer, CreateCaseSerializer, UpdateCaseSerializer


load_dotenv()


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def generate_prescription_html(request):
  if request.method == 'POST':
    case = None
    case_id = request.query_params.get('case_id', None)
    base_dir = os.path.join(settings.MEDIA_ROOT, 'case')
    BACKEND_URL = os.getenv('BACKEND_URL', default='http://localhost:8000')

    if not case_id:
      raise exceptions.GenericException(
        detail='Provide case_id in query params',
        code='Case identifier missing'
      )

    try:
      case = Case.objects.get(id=case_id)
    except Case.DoesNotExist:
      raise exceptions.DoesNotExistException(
        detail=f'No case found with id {case_id}',
        code='Case not found'
      )

    serializedCase = CaseSerializer(
      instance=case,
      exclude=['is_active']
    )
    full_case = serializedCase.data
    context = {
      'blood_pressure_low': full_case['blood_pressure_low'],
      'blood_pressure_high': full_case['blood_pressure_high'],
      'pulse': full_case['pulse'],
      'oxygen': full_case['oxygen'],
      'body_temperature': full_case['body_temperature'],
      'weight': full_case['weight'],
      'patient_full_name': full_case['patient']['full_name'],
      'patient_age': full_case['patient']['age'],
      'patient_gender': full_case['patient']['gender'],
      'patient_phone_number': full_case['patient']['phone_number'],
      'patient_address': full_case['patient']['address'],
      'patient_allergy': full_case['patient']['allergy'],
      'patient_diseases': full_case['patient']['diseases'],
      'patient_other_diseases': full_case['patient']['other_diseases'],
      'chief_complaints_length': len(full_case['chief_complaints']),
      'chief_complaints': full_case['chief_complaints'],
      'findings_length': len(full_case['findings']),
      'findings': full_case['findings'],
      'medicines_length': len(full_case['prescription']['medicines']),
      'medicines': full_case['prescription']['medicines'],
      'diagnosis_items_length': len(full_case['prescription']['diagnosis_items']),
      'diagnosis_items': full_case['prescription']['diagnosis_items'],
      'investigation_items_length': len(full_case['prescription']['investigation_items']),
      'investigation_items': full_case['prescription']['investigation_items'],
      'referred_doctors_length': len(full_case['prescription']['referred_doctors']),
      'referred_doctors': full_case['prescription']['referred_doctors'],
      'prescription_note': full_case['prescription']['note'],
    }
    rendered_template = render_to_string("prescription.html", context)

    patient_full_name = '_'.join(case.patient.full_name.lower().split())
    prescription_name = f'prescription-{patient_full_name}.html'
    prescription_dir = os.path.join(base_dir, str(case_id))

    os.makedirs(prescription_dir, exist_ok=True)
    prescription_path = os.path.join(prescription_dir, prescription_name)

    with open(prescription_path, 'wb') as destination:
      destination.write(rendered_template.encode("utf-8"))

    prescription_url = f'{BACKEND_URL}{settings.MEDIA_URL}case/{case_id}/{prescription_name}'

    return custom_response_handler(
      status=status.HTTP_201_CREATED,
      message='Prescription has been successfully generated',
      data={
        'prescription_name': prescription_name,
        'prescription_url': prescription_url,
      }
    )


class CaseAPIView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request, pk=None, format=None):
    data = None
    message = None
    query_params = request.query_params

    doctor = None
    serializedDoctor = None
    doctor_id = query_params.get('doctor_id', None)
    patient_id = query_params.get('patient_id', None)

    if pk is not None:
      try:
        case = Case.objects.get(id=pk)
        serializedCase = CaseSerializer(
          instance=case,
          exclude=[
            'is_active',
            'updated_at'
          ]
        )
        data = serializedCase.data
        message = 'Get case'
      except Case.DoesNotExist:
        raise exceptions.DoesNotExistException(
          detail=f'No case found with id {pk}',
          code='Case not found'
        )
    elif not (patient_id is not None and 'page_size' in query_params and 'page' in query_params):
      raise exceptions.GenericException(
        detail='Provide patient_id, page_size & page in query params',
        code='Patient & page configuration missing'
      )
    else:
      try:
        Patient.objects.get(id=patient_id)
      except Patient.DoesNotExist:
        raise exceptions.DoesNotExistException(
          detail=f'No patient found with id {patient_id}',
          code='Patient not found'
        )

      if doctor_id:
        try:
          doctor = Doctor.objects.get(id=doctor_id)
          serializedDoctor = DoctorSerializer(
            instance=doctor,
            fields=[
              'profile',
              'degree',
              'speciality'
            ],
            profile_fields=[
              'first_name',
              'last_name'
            ]
          )
        except Doctor.DoesNotExist:
          raise exceptions.DoesNotExistException(
            detail=f'No doctor found with id {doctor_id}',
            code='Doctor not found'
          )

      current_page = 1
      page_size = int(query_params['page_size'])

      if doctor_id:
        cases = Case.objects.filter(patient=patient_id, assigned_doctor=doctor_id)
        message = 'Get cases by patient and assigned doctor'
      else:
        cases = Case.objects.filter(patient=patient_id)
        message = 'Get cases by patient'

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
          'chief_complaints',
          'findings',
          'is_follow_up',
          'follow_up_date',
          'is_completed',
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
        **({'doctor': serializedDoctor.data} if doctor_id else {}),
        'values': serializedCases.data,
      }

    return custom_response_handler(
      status=status.HTTP_200_OK,
      message=message,
      data=data
    )

  def post(self, request, format=None):
    serializedCreateCase = CreateCaseSerializer(data=request.data)

    if serializedCreateCase.is_valid():
      case = serializedCreateCase.save()
      serializedCase = CaseSerializer(
        instance=case,
        exclude=[
          'is_active',
          'updated_at'
        ]
      )

      return custom_response_handler(
        status=status.HTTP_201_CREATED,
        message='Case created successfully',
        data=serializedCase.data
      )
    else:
      raise exceptions.InvalidRequestBodyException(
        detail=serializedCreateCase.errors,
        code='Invalid request data'
      )

  def patch(self, request, pk, format=None):
    case = None

    try:
      case = Case.objects.get(id=pk)
    except Case.DoesNotExist:
      raise exceptions.DoesNotExistException(
        detail=f'No case found with id {pk}',
        code='Case not found'
      )

    serializedUpdateCase = UpdateCaseSerializer(
      instance=case,
      data=request.data,
      partial=True
    )

    if serializedUpdateCase.is_valid():
      updatedCase = serializedUpdateCase.save()
      serializedCase = CaseSerializer(
        instance=updatedCase,
        exclude=[
          'is_active',
          'updated_at'
        ]
      )

      return custom_response_handler(
        status=status.HTTP_200_OK,
        message='Case updated successfully',
        data=serializedCase.data
      )
    else:
      raise exceptions.InvalidRequestBodyException(
        detail=serializedUpdateCase.errors,
        code='Invalid request data'
      )

  def delete(self, request, pk, format=None):
    case = None

    try:
      case = Case.objects.get(id=pk)
    except Case.DoesNotExist:
      raise exceptions.DoesNotExistException(
        detail=f'No case found with id {pk}',
        code='Case not found'
      )

    case.delete()

    return custom_response_handler(
      status=status.HTTP_200_OK,
      message='Case has been successfully removed',
      data=None
    )
