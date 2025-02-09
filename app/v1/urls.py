from django.urls import path
from app.v1.profile.views import upload_dp
from app.v1.doctor.views import DoctorAPIView
from app.v1.speciality.views import SpecialityAPIView
from app.v1.assistant.views import AssistantAPIView
from app.v1.disease.views import DiseaseAPIView
from app.v1.habit.views import HabitAPIView
from app.v1.patient.views import PatientAPIView
from app.v1.auth.views import LoginAPIView, LogoutAPIView
from app.v1.patient.views import PatientAPIView
from app.v1.appointment.views import AppointmentAPIView
from app.v1.case.views import CaseAPIView
from app.v1.case_chief_complaint.views import CaseChiefComplaintAPIView
from app.v1.case_finding.views import CaseFindingAPIView
from app.v1.finding_image.views import FindingImageAPIView
from app.v1.case_document.views import CaseDocumentAPIView
from app.v1.prescription.views import PrescriptionAPIView
from app.v1.medicine.views import MedicineAPIView, MedicineStuffAPIView
from app.v1.diagnosis_item.views import DiagnosisAPIView, DiagnosisItemAPIView
from app.v1.investigation_item.views import InvestigationAPIView, InvestigationItemAPIView
from app.v1.diet_advice.views import DietAdviceAPIView


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
  path('case', CaseAPIView.as_view()),
  path('case/<int:pk>', CaseAPIView.as_view()),
  path('appointment', AppointmentAPIView.as_view()),
  path('speciality', SpecialityAPIView.as_view()),
  path('case-chief-complaint/<int:pk>', CaseChiefComplaintAPIView.as_view()),
  path('case-finding/<int:pk>', CaseFindingAPIView.as_view()),
  path('finding-image/upload', FindingImageAPIView.as_view(), {'action': 'upload'}),
  path('finding-image/remove/<int:pk>', FindingImageAPIView.as_view(), {'action': 'remove'}),
  path('case-document/upload', CaseDocumentAPIView.as_view(), {'action': 'upload'}),
  path('case-document/rename/<int:pk>', CaseDocumentAPIView.as_view(), {'action': 'rename'}),
  path('case-document/remove/<int:pk>', CaseDocumentAPIView.as_view(), {'action': 'remove'}),
  path('prescription', PrescriptionAPIView.as_view()),
  path('prescription/<int:pk>', PrescriptionAPIView.as_view()),
  path('medicine-stuff', MedicineStuffAPIView.as_view()),
  path('medicine-stuff/<int:pk>', MedicineStuffAPIView.as_view()),
  path('medicine/<int:pk>', MedicineAPIView.as_view()),
  path('diagnosis', DiagnosisAPIView.as_view()),
  path('diagnosis/<int:pk>', DiagnosisAPIView.as_view()),
  path('diagnosis-item/<int:pk>', DiagnosisItemAPIView.as_view()),
  path('investigation', InvestigationAPIView.as_view()),
  path('investigation/<int:pk>', InvestigationAPIView.as_view()),
  path('investigation-item/<int:pk>', InvestigationItemAPIView.as_view()),
  path('diet-advice/<int:pk>', DietAdviceAPIView.as_view())
]
