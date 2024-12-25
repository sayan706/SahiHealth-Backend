from utils import exceptions
from collections import defaultdict
from rest_framework.views import APIView
from utils.response_handler import custom_response_handler
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.functions import TruncDate
from app.models import Profile, Doctor, Case
from app.serializers.patient import PatientSerializer, CreatePatientSerializer
from app.serializers.case import AppointmentSerializer


def get_cases_grouped_by_date(doctor):
  grouped_cases = defaultdict(list)
  cases = (
    Case.objects.filter(assigned_doctor=doctor)
    .annotate(date=TruncDate('created_at'))  # Extract the date portion
    .order_by('-created_at')  # Order by descending datetime
  )

  for case in cases:
    date_in_str = case.date.strftime('%Y-%m-%d')  # Convert date to string
    grouped_cases[date_in_str].append(case)

  # Flatten grouped cases into a list for pagination
  flattened_cases = []

  for date, case_list in grouped_cases.items():
    serializedAppointments = AppointmentSerializer(
      case_list,
      many=True,
      fields=[
        'id',
        'patient',
        'assigned_doctor',
      ]
    )
    flattened_cases.append({"date": date, "appointments": serializedAppointments.data})

  return flattened_cases
  # # Serialize grouped cases
  # serialized_grouped_cases = {
  #   date: CaseSerializer(grouped_cases[date], many=True).data
  #   for date in grouped_cases
  # }
  # return [serialized_grouped_cases]


class AppointmentAPIView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request, format=None):
    data = None
    message = None
    profile = None
    doctor_id = None
    query_params = request.query_params

    # Retrieve the profile instance
    profile = Profile.objects.get(user=request.user)

    if 'doctor_id' in query_params:
      doctor_id = query_params['doctor_id']

    appointments = []

    if doctor_id is not None:
      try:
        doctor = Doctor.objects.get(id=doctor_id)
        appointments = get_cases_grouped_by_date(doctor)
        message = "Get Appointments by Doctor"
      except Doctor.DoesNotExist:
        raise exceptions.DoesNotExistException(
          detail=f'No doctor found with id {doctor_id}',
          code='Doctor not found'
        )
    elif profile.role == 'DOCTOR':
      try:
        doctor = Doctor.objects.get(profile=profile)
        appointments = get_cases_grouped_by_date(doctor)
        message = "Get Appointments by Current Doctor"
      except Doctor.DoesNotExist:
        raise exceptions.DoesNotExistException(
          detail=f'No doctor found with this profile',
          code='Doctor not found'
        )

    if not ('page_size' in query_params and 'page' in query_params):
      raise exceptions.GenericException(
        detail='Provide page_size & page in query params',
        code='Page configuration missing'
      )
    else:
      current_page = 1
      page_size = int(query_params['page_size'])
      paginator = Paginator(appointments, page_size)

      try:
        current_page = int(query_params['page'])
        appointments = paginator.page(current_page)
      except PageNotAnInteger:
        appointments = paginator.page(1)
      except EmptyPage:
        appointments = []

      data = {
        'total_pages': paginator.num_pages,
        'current_page': current_page,
        'next_page': None if (paginator.num_pages - current_page) <= 0 else current_page + 1,
        'page_size': page_size,
        'values': appointments if isinstance(appointments, list) else list(appointments),
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
      serializedPatient = PatientSerializer(instance=patient)

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
