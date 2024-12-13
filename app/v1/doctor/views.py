from utils import exceptions
from django.shortcuts import render
from rest_framework.views import APIView
from utils.response_handler import custom_response_handler
from rest_framework import status
from app.models import Doctor
from app.serializers.doctor import DoctorSerializer , ProfileSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



# Create your views here.
class DoctorAPIView(APIView):
  def get(self, request, pk=None, format=None):
    data = None
    message = None
    query_params = request.query_params

    if pk is not None:
      try:
        doctor = Doctor.objects.get(id=pk)
        serializedDoctor = DoctorSerializer(instance=doctor)
        data = serializedDoctor.data
        message = "Get Doctor"
      except Doctor.DoesNotExist:
        raise exceptions.DoesNotExistException(
          detail=f'No doctor found with id {pk}',
          code="Doctor Not Found"
        )
    elif 'doctor_id' in query_params:
      try:
        doctor = Doctor.objects.get(id=query_params['doctor_id'])
        serializedDoctor = DoctorSerializer(instance=doctor)
        data = serializedDoctor.data
        message = "Get Doctor"
      except Doctor.DoesNotExist:
        raise exceptions.DoesNotExistException(
          detail=f'No doctor found with id {query_params["doctor_id"]}',
          code="Doctor Not Found"
        )
    elif not ('page_size' in query_params and 'page' in query_params):
      raise exceptions.GenericException(detail='Provide page_size & page in query params')
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
      
      serializedDoctors = DoctorSerializer(instance=doctors, many=True)
      data = {
        'values': serializedDoctors.data,
        'total_count': total_count,
        'page_size': page_size,
        'current_page': current_page,
        'next_page': None if (paginator.num_pages - current_page) <= 0 else current_page + 1,
        'total_pages': paginator.num_pages,
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
    query_params = request.query_params

    
    if 'doctor_id' not in query_params:
        raise exceptions.GenericException(detail='Provide doctor_id in query params')

    try:
        doctor = Doctor.objects.get(id=query_params['doctor_id'])
    except Doctor.DoesNotExist:
        raise exceptions.DoesNotExistException(
            detail=f'No doctor found with id {query_params["doctor_id"]}',
            code="Doctor Not Found"
        )

    request_data = request.data

  
    profile_data = request_data.get('profile', {})
    if profile_data:
        # Get the existing profile linked to the doctor
        profile_instance = doctor.profile  # doctor.profile gives the associated profile

        # Make sure that we are only updating the existing profile and not creating a new one
        
        print(f"Updating Profile for Doctor: {doctor.id}")
        profile_serializer = ProfileSerializer(instance=profile_instance, data=profile_data, partial=True)
        print(f"Profile data: {profile_data}")
        if profile_serializer.is_valid(raise_exception=True):
            profile_serializer.save()  # This will update the existing profile, not create a new one

    # Handle doctor data (e.g., updating speciality)
    doctor_data = {}
    if 'speciality' in request_data:
        doctor_data['speciality'] = request_data['speciality']

    if doctor_data:
        # Use the DoctorSerializer to update the Doctor instance (but NOT the Profile!)
        doctor_serializer = DoctorSerializer(instance=doctor, data=doctor_data, partial=True)
        if doctor_serializer.is_valid(raise_exception=True):
            doctor_serializer.save()  # Update the doctor instance

    # Serialize the updated doctor instance
    serialized_doctor = DoctorSerializer(instance=doctor)
    data = serialized_doctor.data
    message = "Doctor updated successfully"

    return custom_response_handler(
        status=status.HTTP_200_OK,
        message=message,
        data=data
    )