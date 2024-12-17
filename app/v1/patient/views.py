from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from app.models import Patient, Profile
from app.serializers.patient import PatientSerializer
from utils import exceptions
from utils.response_handler import custom_response_handler
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



class PatientAPIView(APIView):
    def post(self, request, format=None):
        data = request.data
        message = None

        required_fields = ["name", "age", "phone_number", "gender", "created_by_username"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise exceptions.InvalidRequestBodyException(
                detail={"missing_fields": missing_fields},
                code="Missing Fields"
            )

        try:
            creator_profile = Profile.objects.get(user__username=data["created_by_username"])
        except Profile.DoesNotExist:
            raise exceptions.DoesNotExistException(
                detail=f"No profile found with username {data['created_by_username']}",
                code="Creator Not Found"
            )
        
        try:
            with transaction.atomic():
                patient_serializer = PatientSerializer(data=data)
                if patient_serializer.is_valid():
                    patient_serializer.save(created_by=creator_profile)
                    message = "Patient Created Successfully"
                    return custom_response_handler(
                        status=status.HTTP_201_CREATED,
                        message=message,
                        data=patient_serializer.data
                    )
                else:
                    raise exceptions.InvalidRequestBodyException(
                        detail=patient_serializer.errors,
                        code="Validation Error"
                    )
        except Exception as e:
            raise exceptions.GenericException(
                detail=str(e),
                code="Patient Creation Failed"
            )
        
    def get(self, request, pk =None, format=None):
        data = None
        message = None
        patient_id = None
        query_params = request.query_params

        if pk is not None:
            patient_id = pk
        elif 'patient_id' in query_params:
            patient_id = query_params['patient_id']

        if patient_id is not None:
            try:
                patient = Patient.objects.get(id=patient_id)
                serializedPatient = PatientSerializer(instance=patient)
                data = serializedPatient.data
                message = "Get Patient"
            except Patient.DoesNotExist:
                raise exceptions.DoesNotExistException(
                    detail=f'No patient found with id {patient_id}',
                    code='Patient Not Found'
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