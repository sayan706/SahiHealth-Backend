from utils import exceptions
from django.shortcuts import render
from rest_framework.views import APIView
from utils.response_handler import custom_response_handler
from rest_framework import status
from app.models import Profile, Doctor, Patient
from app.serializers.patient import PatientSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class PatientAPIView(APIView):
  def get(self, request, pk=None, format=None):
    data = None
    message = None
    assigned_doctor_id = None
    creator_profile_id = None
    query_params = request.query_params

    if 'assigned_doctor_id' in query_params:
      assigned_doctor_id = query_params['assigned_doctor_id']
    elif 'creator_profile_id' in query_params:
      creator_profile_id = query_params['creator_profile_id']

    if pk is not None:
      try:
        patient = Patient.objects.get(id=pk)
        serializedPatient = PatientSerializer(instance=patient)
        data = serializedPatient.data
        message = "Get Patient"
      except Patient.DoesNotExist:
        raise exceptions.DoesNotExistException(
          detail=f'No patient found with id {pk}',
          code='Patient not found'
        )
    elif assigned_doctor_id is not None:
      try:
        Doctor.objects.get(id=assigned_doctor_id)
        patients = Patient.objects.filter(assigned_doctor=assigned_doctor_id)
        serializedPatients = PatientSerializer(instance=patients, many=True)
        data = serializedPatients.data
        message = "Get Patients by Assigned Doctor"
      except Doctor.DoesNotExist:
        raise exceptions.DoesNotExistException(
          detail=f'No doctor found with id {assigned_doctor_id}',
          code='Doctor not found'
        )
    elif creator_profile_id is not None:
      try:
        Profile.objects.get(id=creator_profile_id)
        patients = Patient.objects.filter(created_by=creator_profile_id)
        serializedPatients = PatientSerializer(instance=patients, many=True)
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

      serializedPatients = PatientSerializer(instance=patients, many=True)
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
