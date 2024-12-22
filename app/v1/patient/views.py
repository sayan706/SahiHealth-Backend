from utils import exceptions
from rest_framework.views import APIView
from utils.response_handler import custom_response_handler
from rest_framework import status
from app.models import Profile, Doctor, Patient
from app.serializers.patient import PatientSerializer, CreatePatientSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class PatientAPIView(APIView):
  def get(self, request, pk=None, format=None):
    data = None
    message = None
    doctor_id = None
    creator_profile_id = None
    query_params = request.query_params

    if 'doctor_id' in query_params:
      doctor_id = query_params['doctor_id']
    elif 'creator_profile_id' in query_params:
      creator_profile_id = query_params['creator_profile_id']

    if pk is not None:
      try:
        patient = Patient.objects.get(id=pk)
        serializedPatient = PatientSerializer(instance=patient, exclude=['doctors'])
        data = serializedPatient.data
        message = "Get Patient"
      except Patient.DoesNotExist:
        raise exceptions.DoesNotExistException(
          detail=f'No patient found with id {pk}',
          code='Patient not found'
        )
    elif doctor_id is not None:
      try:
        doctor = Doctor.objects.get(id=doctor_id)
        patients = Patient.objects.filter(doctors=doctor)
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
        data = serializedPatients.data
        message = "Get Patients by Doctor"
      except Doctor.DoesNotExist:
        raise exceptions.DoesNotExistException(
          detail=f'No doctor found with id {doctor_id}',
          code='Doctor not found'
        )
    elif creator_profile_id is not None:
      try:
        Profile.objects.get(id=creator_profile_id)
        patients = Patient.objects.filter(created_by=creator_profile_id)
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
        data = serializedPatients.data
        message = "Get Patients by Creator"
      except Profile.DoesNotExist:
        raise exceptions.DoesNotExistException(
          detail=f'No profile found with id {creator_profile_id}',
          code='Profile not found'
        )
    elif not ('page_size' in query_params and 'page' in query_params):
      raise exceptions.GenericException(
        detail='Provide page_size & page in query params',
        code='Page Configuration Missing'
      )
    else:
      current_page = 1
      page_size = int(query_params['page_size'])

      patients = Patient.objects.all()
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
      message = "Get All Patients"

    return custom_response_handler(
      status=status.HTTP_200_OK,
      message=message,
      data=data
    )

  def post(self, request, format=None):
    query_params = request.query_params
    request.data['doctor_id'] = query_params['doctor_id']
    request.data['creator_profile_id'] = query_params['creator_profile_id']
    serializedCreatePatient = CreatePatientSerializer(data=request.data)

    if serializedCreatePatient.is_valid():
      patient = serializedCreatePatient.save()
      serializedPatient = PatientSerializer(instance=patient)

      return custom_response_handler(
        status=status.HTTP_200_OK,
        message="Patient created successfully",
        data=serializedPatient.data
      )
    else:
      raise exceptions.InvalidSerializerException(
        detail=serializedCreatePatient.errors,
        code='Invalid Serializer'
      )
