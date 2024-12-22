from utils import exceptions
from django.shortcuts import render
from rest_framework.views import APIView
from utils.response_handler import custom_response_handler
from rest_framework import status
from app.models import Doctor
from app.serializers.doctor import DoctorSerializer, ProfileSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
class DoctorAPIView(APIView):
  def get(self, request, pk=None, format=None):
    data = None
    message = None
    doctor_id = None
    query_params = request.query_params

    if pk is not None:
      doctor_id = pk
    elif 'doctor_id' in query_params:
      doctor_id = query_params['doctor_id']

    if doctor_id is not None:
      try:
        doctor = Doctor.objects.get(id=doctor_id)
        serializedDoctor = DoctorSerializer(
          instance=doctor,
          profile_exclude=[
            'id',
            'is_active',
            'created_at',
            'updated_at'
          ],
          user_fields=[
            'username',
            'last_login',
            'date_joined',
            'user_permissions'
          ]
        )
        data = serializedDoctor.data
        message = "Get Doctor"
      except Doctor.DoesNotExist:
        raise exceptions.DoesNotExistException(
          detail=f'No doctor found with id {doctor_id}',
          code='Doctor not found'
        )
    elif not ('page_size' in query_params and 'page' in query_params):
      raise exceptions.GenericException(
        detail='Provide page_size & page in query params',
        code='Page Configuration Missing'
      )
    else:
      current_page = 1
      page_size = int(query_params['page_size'])

      doctors = Doctor.objects.all()
      total_count = len(doctors)
      paginator = Paginator(doctors, page_size)

      try:
        current_page = int(query_params['page'])
        doctors = paginator.page(current_page)
      except PageNotAnInteger:
        doctors = paginator.page(1)
      except EmptyPage:
        doctors = []

      serializedDoctors = DoctorSerializer(
        instance=doctors,
        many=True,
        profile_exclude=[
          'id',
          'user',
          'is_active',
          'created_at',
          'updated_at'
        ]
      )
      data = {
        'count': len(serializedDoctors.data),
        'total_count': total_count,
        'total_pages': paginator.num_pages,
        'current_page': current_page,
        'next_page': None if (paginator.num_pages - current_page) <= 0 else current_page + 1,
        'page_size': page_size,
        'values': serializedDoctors.data,
      }
      message = "Get All Doctors"

    return custom_response_handler(
      status=status.HTTP_200_OK,
      message=message,
      data=data
    )

  def patch(self, request, pk=None, format=None):
    data = None
    message = None
    doctor = None
    doctor_id = None
    request_data = request.data
    query_params = request.query_params

    if pk is not None:
      doctor_id = pk
    elif 'doctor_id' in query_params:
      doctor_id = query_params['doctor_id']
    else:
      raise exceptions.GenericException(
        detail='Mention id as path variable or doctor_id in query params',
        code='Identifier not found for the doctor'
      )

    try:
      doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
      raise exceptions.DoesNotExistException(
        detail=f'No doctor found with id {doctor_id}',
        code='Doctor not found'
      )

    # Update profile if present
    profile_data = request_data.get('profile', {})

    if profile_data:
      # Get the existing profile linked to the doctor
      doctorProfile = doctor.profile
      serializedProfile = ProfileSerializer(instance=doctorProfile, data=profile_data, partial=True)

      if serializedProfile.is_valid(raise_exception=True):
        # Update the profile instance
        serializedProfile.save()

    # Update doctor specific data if present
    doctor_data = {}

    if 'is_active' in request_data:
      doctor_data['is_active'] = request_data['is_active']
    if 'speciality' in request_data:
      doctor_data['speciality'] = request_data['speciality']

    if doctor_data:
      serializedDoctor = DoctorSerializer(instance=doctor, data=doctor_data, partial=True)

      if serializedDoctor.is_valid(raise_exception=True):
        # Update the doctor instance
        serializedDoctor.save()

    # Serialize the updated doctor instance
    serializedDoctor = DoctorSerializer(
      instance=doctor,
      profile_exclude=[
        'id',
        'is_active',
        'created_at',
        'updated_at'
      ],
      user_fields=[
        'username',
        'last_login',
        'date_joined',
        'user_permissions'
      ]
    )
    data = serializedDoctor.data
    message = "Profile updated successfully"

    return custom_response_handler(
      status=status.HTTP_200_OK,
      message=message,
      data=data
    )
