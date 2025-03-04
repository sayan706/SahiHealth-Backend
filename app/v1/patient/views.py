from utils import exceptions
from rest_framework.views import APIView
from utils.response_handler import custom_response_handler
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.models import Profile, Doctor, Patient
from app.serializers.patient import PatientSerializer, CreatePatientSerializer


class PatientAPIView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  # Define search fields at the class level
  search_fields = [
    'full_name',
    'phone_number',
    'gender',
    'age',
    # 'address',
    # 'allergy',
    # 'other_diseases',
    # 'other_habits'
  ]

  def get(self, request, pk=None, format=None):
    data = None
    message = None
    profile = None
    doctor_id = None
    query_params = request.query_params

    if pk is not None:
      try:
        patient = Patient.objects.get(id=pk)
        serializedPatient = PatientSerializer(
          instance=patient,
          exclude=['doctors']
        )
        data = serializedPatient.data
        message = "Get patient"
      except Patient.DoesNotExist:
        raise exceptions.DoesNotExistException(
          detail=f'No patient found with id {pk}',
          code='Patient not found'
        )

    # Retrieve the profile instance
    profile = Profile.objects.get(user=request.user)

    if 'doctor_id' in query_params:
      doctor_id = query_params['doctor_id']

    patients = []

    if data is not None:
      pass
    elif 'all' in query_params:
      patients = Patient.objects.all().order_by('-created_at')
      message = "Get all patients"
    elif doctor_id is not None:
      try:
        doctor = Doctor.objects.get(id=doctor_id)
        patients = Patient.objects.filter(doctors=doctor).order_by('-created_at')
        message = "Get patients by doctor"
      except Doctor.DoesNotExist:
        raise exceptions.DoesNotExistException(
          detail=f'No doctor found with id {doctor_id}',
          code='Doctor not found'
        )
    elif profile is not None:
      if profile.role == 'DOCTOR' and query_params.get('doctor', None) == 'true':
        try:
          doctor = Doctor.objects.get(profile=profile)
          patients = Patient.objects.filter(doctors=doctor).order_by('-created_at')
          message = "Get patients by current doctor"
        except Doctor.DoesNotExist:
          raise exceptions.DoesNotExistException(
            detail=f'No doctor found with this profile',
            code='Doctor not found'
          )
      else:
        patients = Patient.objects.filter(created_by=profile).order_by('-created_at')
        message = "Get patients by creator"

    if data is not None:
      pass
    elif not ('page_size' in query_params and 'page' in query_params):
      raise exceptions.GenericException(
        detail='Provide page_size & page in query params',
        code='Page configuration missing'
      )
    else:
      # Apply search filter
      search_filter = SearchFilter()

      if 'search' in request.query_params:
        patients = search_filter.filter_queryset(request, patients, self)

      current_page = 1
      page_size = int(query_params['page_size'])

      total_count = len(patients)
      paginator = Paginator(patients, page_size)

      try:
        current_page = int(query_params['page'])
        patients = paginator.page(current_page)
      except PageNotAnInteger:
        patients = paginator.page(1)
      except EmptyPage:
        patients = []

      serializedPatients = PatientSerializer(
        instance=patients,
        many=True,
        fields=[
          'id',
          'full_name',
          'phone_number',
          'gender',
          'age',
          'created_at',
        ]
      )
      data = {
        'count': len(serializedPatients.data),
        'total_count': total_count,
        'total_pages': paginator.num_pages,
        'current_page': current_page,
        'next_page': None if (paginator.num_pages - current_page) <= 0 else current_page + 1,
        'page_size': page_size,
        'values': serializedPatients.data,
      }

    return custom_response_handler(
      status=status.HTTP_200_OK,
      message=message,
      data=data
    )

  def post(self, request, format=None):
    request_data = request.data

    # Retrieve the profile instance from the request user
    profile = Profile.objects.get(user=request.user)

    request_data['creator_profile_id'] = profile.id
    serializedCreatePatient = CreatePatientSerializer(data=request_data)

    if serializedCreatePatient.is_valid():
      patient = serializedCreatePatient.save()
      serializedPatient = PatientSerializer(
        instance=patient,
        exclude=['doctors']
      )

      return custom_response_handler(
        status=status.HTTP_200_OK,
        message="Patient created successfully",
        data=serializedPatient.data
      )
    else:
      raise exceptions.InvalidRequestBodyException(
        detail=serializedCreatePatient.errors,
        code='Invalid request data'
      )

  def patch(self, request, pk, format=None):
    patient = None

    try:
      patient = Patient.objects.get(id=pk)
    except Patient.DoesNotExist:
      raise exceptions.DoesNotExistException(
        detail=f'No patient found with id {pk}',
        code='Patient not found'
      )

    serializedCreatePatient = CreatePatientSerializer(
      instance=patient,
      data=request.data,
      partial=True
    )

    if serializedCreatePatient.is_valid():
      updatedPatient = serializedCreatePatient.save()
      serializedPatient = PatientSerializer(
        instance=updatedPatient,
        exclude=['doctors']
      )

      return custom_response_handler(
        status=status.HTTP_200_OK,
        message='Patient updated successfully',
        data=serializedPatient.data
      )
    else:
      raise exceptions.InvalidRequestBodyException(
        detail=serializedCreatePatient.errors,
        code='Invalid request data'
      )

  def delete(self, request, pk, format=None):
    patient = None

    try:
      patient = Patient.objects.get(id=pk)
    except Patient.DoesNotExist:
      raise exceptions.DoesNotExistException(
        detail=f'No patient found with id {pk}',
        code='Patient not found'
      )

    patient.delete()

    return custom_response_handler(
      status=status.HTTP_200_OK,
      message='Patient has been successfully removed',
      data=None
    )
