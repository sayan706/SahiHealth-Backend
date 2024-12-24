from utils import exceptions
from rest_framework.views import APIView
from utils.response_handler import custom_response_handler
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.models import Profile, Speciality, Doctor
from app.serializers.profile import UpdateProfileSerializer
from app.serializers.doctor import DoctorSerializer, UpdateDoctorSerializer


# Create your views here.
class DoctorAPIView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request, format=None):
    data = None
    message = None
    query_params = request.query_params

    # Retrieve the profile instance
    profile = Profile.objects.get(user=request.user)

    if ('page_size' in query_params or 'page' in query_params):
      pass
    else:
      try:
        doctor = Doctor.objects.get(profile=profile)
        serializedDoctor = DoctorSerializer(
          instance=doctor,
          exclude=[
            'is_active',
            'created_at'
          ],
          profile_exclude=[
            'id',
            'is_active',
            'created_at',
            'updated_at'
          ],
          user_fields=[
            'username',
            'date_joined'
          ]
        )
        data = serializedDoctor.data
        message = "Get Doctor"
      except Doctor.DoesNotExist:
        raise exceptions.DoesNotExistException(
          detail=f'Requested doctor profile not found',
          code='Doctor not found'
        )

    if data is not None:
      pass
    elif not ('page_size' in query_params and 'page' in query_params):
      raise exceptions.GenericException(
        detail='Provide page_size & page in query params',
        code='Page configuration missing'
      )
    else:
      doctors = []
      current_page = 1
      page_size = int(query_params['page_size'])
      speciality_id = query_params.get('speciality_id', None)

      if speciality_id:
        doctors = Doctor.objects.filter(speciality_id=speciality_id)
        message = "Get Doctors by Speciality"
      else:
        doctors = Doctor.objects.all()
        message = "Get All Doctors"

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
        exclude=['created_at'],
        profile_exclude=[
          'id',
          'is_active',
          'created_at',
          'updated_at'
        ],
        user_fields=[
          'username',
          'date_joined'
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

    return custom_response_handler(
      status=status.HTTP_200_OK,
      message=message,
      data=data
    )

  def patch(self, request, format=None):
    data = None
    message = None
    request_data = request.data

    # Retrieve the profile and doctor instance
    doctor = None
    profile = Profile.objects.get(user=request.user)

    if profile.role != 'DOCTOR':
      raise exceptions.PermissionDeniedException(
        detail='Only doctor is allowed to perform edit',
        code='Only doctor is allowed'
      )
    else:
      doctor = Doctor.objects.get(profile=profile)

    # Update profile instance if present
    profile_data = request_data.pop('profile', {})
    serializedUpdateProfile = UpdateProfileSerializer(
      instance=profile,
      data=profile_data,
      partial=True
    )

    if serializedUpdateProfile.is_valid():
      serializedUpdateProfile.save()
    else:
      raise exceptions.InvalidRequestBodyException(
        detail=serializedUpdateProfile.errors,
        code='Invalid profile data'
      )

    # Attach the speciality to the doctor instance if present
    speciality_id = request_data.pop('speciality_id', None)

    if speciality_id is not None:
      doctor.speciality = Speciality.objects.get(id=speciality_id)

    # Update doctor instance at last
    serializedUpdateDoctor = UpdateDoctorSerializer(
      instance=doctor,
      data=request_data,
      partial=True
    )

    if serializedUpdateDoctor.is_valid():
      updatedDoctor = serializedUpdateDoctor.save()
      serializedUpdatedDoctor = DoctorSerializer(
        instance=updatedDoctor,
        exclude=[
          'is_active',
          'created_at'
        ],
        profile_exclude=[
          'id',
          'is_active',
          'created_at',
          'updated_at'
        ],
        user_fields=[
          'username',
          'date_joined'
        ]
      )
      data = serializedUpdatedDoctor.data
      message = "Profile updated successfully"
    else:
      raise exceptions.InvalidRequestBodyException(
        detail=serializedUpdateDoctor.errors,
        code='Invalid doctor data'
      )

    return custom_response_handler(
      status=status.HTTP_200_OK,
      message=message,
      data=data
    )
