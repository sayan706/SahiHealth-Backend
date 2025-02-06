from utils import exceptions
from django.db.models import Q
from rest_framework.views import APIView
from utils.response_handler import custom_response_handler
from rest_framework import status
from app.serializers.medicine_name import MedicineNameSerializer
from app.serializers.medicine_dose_type import MedicineDoseTypeSerializer
from app.serializers.medicine_dose_quantity import MedicineDoseQuantitySerializer
from app.serializers.medicine_dose_regimen import MedicineDoseRegimenSerializer
from app.serializers.medicine_dose_duration import MedicineDoseDurationSerializer
from app.models import (
  MedicineName,
  MedicineDoseType,
  MedicineDoseQuantity,
  MedicineDoseRegimen,
  MedicineDoseDuration
)


class MedicineStuffsAPIView(APIView):
  def get(self, request, *args, **kwargs):
    type_param = request.query_params.get('type')
    search_param = request.query_params.get('search', '').strip()

    if not type_param:
      raise exceptions.GenericException(
        detail="The 'type' query parameter is required",
        code='Parameter missing'
      )

    model_mapping = {
      'name': (MedicineName, MedicineNameSerializer, 'name'),
      'dose_type': (MedicineDoseType, MedicineDoseTypeSerializer, 'name'),
      'dose_quantity': (MedicineDoseQuantity, MedicineDoseQuantitySerializer, 'quantity'),
      'dose_regimen': (MedicineDoseRegimen, MedicineDoseRegimenSerializer, 'name'),
      'dose_duration': (MedicineDoseDuration, MedicineDoseDurationSerializer, 'duration'),
    }

    if type_param not in model_mapping:
      raise exceptions.GenericException(
        detail='Invalid type parameter (valid: name | dose_type | dose_quantity | dose_regimen | dose_duration)',
        code='Invalid parameter value'
      )

    model, serializer_class, search_field = model_mapping[type_param]
    queryset = model.objects.filter(is_active=True)

    if search_param:
      queryset = queryset.filter(Q(**{f'{search_field}__icontains': search_param}))

    queryset = queryset[:50] if type_param == 'name' else queryset
    serializer = serializer_class(queryset, many=True)

    return custom_response_handler(
      status=status.HTTP_200_OK,
      message=f'Get {type_param}(s)',
      data=serializer.data
    )
