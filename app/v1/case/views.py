from utils import exceptions
from rest_framework.views import APIView
from utils.response_handler import custom_response_handler
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.models import Case, Patient
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
