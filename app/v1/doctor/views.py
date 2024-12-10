from utils import exceptions
from django.shortcuts import render
from rest_framework.views import APIView
from utils.response_handler import custom_response_handler
from rest_framework import status
from app.models import Doctor
from app.serializers.doctor import DoctorSerializer
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
