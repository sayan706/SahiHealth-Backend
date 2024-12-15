from django.urls import path
from app.v1.profile.views import upload_dp
from app.v1.doctor.views import DoctorAPIView
from app.v1.assistant.views import AssistantAPIView
from app.v1.auth.views import LoginAPIView, LogoutAPIView


urlpatterns=[
  path('auth/login', LoginAPIView.as_view()),
  path('auth/logout', LogoutAPIView.as_view()),
  path('profile/upload-dp', upload_dp),
  path('doctor', DoctorAPIView.as_view()),
  path('doctor/<int:pk>', DoctorAPIView.as_view()),
  path('assistant', AssistantAPIView.as_view()),
  path('assistant/<int:pk>', AssistantAPIView.as_view()),
]
