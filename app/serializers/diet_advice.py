from app.dynamic_serializer import DynamicFieldsModelSerializer
from app.models import DietAdvice


class DietAdviceSerializer(DynamicFieldsModelSerializer):
  class Meta:
    model = DietAdvice
    # fields = '__all__'
    exclude = [
      'prescription',
      'is_active',
      'created_at',
      'updated_at'
    ]
