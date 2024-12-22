from rest_framework import serializers


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
  def __init__(self, *args, **kwargs):
    # Extract 'fields' and 'exclude' from kwargs
    fields = kwargs.pop('fields', None)
    exclude = kwargs.pop('exclude', None)
    super().__init__(*args, **kwargs)

    if fields is not None:
      # Drop any fields that are not in the 'fields' list
      allowed = set(fields)
      existing = set(self.fields)

      for field_name in existing - allowed:
        self.fields.pop(field_name)

    if exclude is not None:
      # Drop any fields that are in the 'exclude' list
      for field_name in set(exclude):
        self.fields.pop(field_name, None)
