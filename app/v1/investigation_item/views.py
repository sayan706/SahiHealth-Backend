from utils import exceptions
from rest_framework.views import APIView
from utils.response_handler import custom_response_handler
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from app.models import Investigation, InvestigationItem
from app.serializers.investigation import InvestigationSerializer


class InvestigationAPIView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  # Define search fields at the class level
  search_fields = ['title']

  def get(self, request, format=None):
    investigations = Investigation.objects.all()

    # Apply search filter
    search_filter = SearchFilter()

    if 'search' in request.query_params:
      investigations = search_filter.filter_queryset(request, investigations, self)

    investigations = investigations[:50]
    serializedInvestigations = InvestigationSerializer(investigations, many=True)

    return custom_response_handler(
      status=status.HTTP_200_OK,
      message="Get all investigations",
      data=serializedInvestigations.data
    )

  def post(self, request, *args, **kwargs):
    serializedInvestigation = InvestigationSerializer(data=request.data)

    if serializedInvestigation.is_valid():
      investigation = serializedInvestigation.save()
      serializedInvestigation = InvestigationSerializer(instance=investigation)
    else:
      raise exceptions.InvalidRequestBodyException(
        detail=serializedInvestigation.errors,
        code='Invalid request data'
      )

    return custom_response_handler(
      status=status.HTTP_201_CREATED,
      message="Investigation created successfully",
      data=serializedInvestigation.data
    )

  def patch(self, request, pk, format=None):
    investigation = None

    try:
      investigation = Investigation.objects.get(id=pk)
    except Investigation.DoesNotExist:
      raise exceptions.DoesNotExistException(
        detail=f'No investigation found with id {pk}',
        code=f'Investigation not found'
      )

    serializedInvestigation = InvestigationSerializer(
      instance=investigation,
      data=request.data,
      partial=True
    )

    if serializedInvestigation.is_valid():
      investigation = serializedInvestigation.save()
      serializedInvestigation = InvestigationSerializer(instance=investigation)
    else:
      raise exceptions.InvalidRequestBodyException(
        detail=serializedInvestigation.errors,
        code='Invalid request data'
      )

    return custom_response_handler(
      status=status.HTTP_200_OK,
      message="Investigation updated successfully",
      data=serializedInvestigation.data
    )


class InvestigationItemAPIView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def delete(self, request, pk, format=None):
    investigation_item = None

    try:
      investigation_item = InvestigationItem.objects.get(id=pk)
      investigation_item.delete()
    except InvestigationItem.DoesNotExist:
      raise exceptions.DoesNotExistException(
        detail=f'No investigation item found with id {pk}',
        code='Investigation item not found'
      )

    return custom_response_handler(
      status=status.HTTP_200_OK,
      message=f'1 item has been deleted',
      data=None
    )
