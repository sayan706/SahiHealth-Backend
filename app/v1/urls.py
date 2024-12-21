from django.urls import path
from app.v1.profile.views import upload_dp
from app.v1.doctor.views import DoctorAPIView
from app.v1.assistant.views import AssistantAPIView
from app.v1.disease.views import DiseaseAPIView
from app.v1.habit.views import HabitAPIView
from app.v1.patient.views import PatientAPIView
from app.v1.auth.views import LoginAPIView, LogoutAPIView
from app.v1.patient.views import PatientAPIView


urlpatterns=[
  path('auth/login', LoginAPIView.as_view()),
  path('auth/logout', LogoutAPIView.as_view()),
  path('profile/upload-dp', upload_dp),
  path('doctor', DoctorAPIView.as_view()),
  path('doctor/<int:pk>', DoctorAPIView.as_view()),
  path('assistant', AssistantAPIView.as_view()),
  path('assistant/<int:pk>', AssistantAPIView.as_view()),
  path('patient', PatientAPIView.as_view()),
  path('patient/<int:pk>', PatientAPIView.as_view()),
  path('disease', DiseaseAPIView.as_view()),
  path('disease/<int:pk>', DiseaseAPIView.as_view()),
  path('habit', HabitAPIView.as_view()),
  path('habit/<int:pk>', HabitAPIView.as_view()),
]
