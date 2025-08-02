from django.urls import path
from rest_framework.routers import DefaultRouter
from app.views import RegisterView, UserViewSet, AppointmentViewSet, LoginView, MyPatientsView, DoctorListView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'appointments', AppointmentViewSet, basename='appointments')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('my-patients/', MyPatientsView.as_view(), name='my-patients'),
    path('doctor/', DoctorListView.as_view(), name='doctor-list')
] + router.urls