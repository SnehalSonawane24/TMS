from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import User, Appointment
from app.serializers import UserSerializer, AppointmentSerializer
from app.utils import format_response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(format_response(
                True, 
                "User Registerd Successfully",
                data={
                    "id": user.id
                }),
                status=status.HTTP_201_CREATED
            )
        return Response(format_response(
            False,
            "Validation Failed",
            error_fields=serializer.errors),
            status=status.HTTP_400_BAD_REQUEST
        )
    

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "Success": True,
                "Message": "Login successful",
                "Data": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "username": user.username
                },
                "Error": None
            })
        return Response({
            "Success": False,
            "Message": "Invalid credentials",
            "Data": None,
            "Error": {
                "code": "401",
                "message": "Invalid username or password",
                "fields": []
            }
        }, status=401)
    

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        return Response(format_response(
            True,
            "User list fetched successfully",
            data={"users": serializer.data}
        ))

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(format_response(
            True,
            "User detail fetched successfully",
            data={"user": serializer.data}
        ))

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(format_response(
            True,
            "Appointment list fetched successfully",
            data={"appointments": serializer.data}
        ))

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(format_response(
            True,
            "Appointment detail fetched successfully",
            data={"appointment": serializer.data}
        ))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            appointment = serializer.save()
            return Response(format_response(
                True,
                "Appointment created",
                data={"id": appointment.id}
            ), status=status.HTTP_201_CREATED)
        return Response(format_response(
            False,
            "Validation Error",
            error_fields=serializer.errors
        ), status=status.HTTP_400_BAD_REQUEST)
            

class MyPatientsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'doctor':
            return Response(format_response(
                False,
                "Unauthorized",
                error_code="403",
                error_message="Only doctors can access this endpoint"
            ), status=status.HTTP_403_FORBIDDEN)

        appointments = Appointment.objects.filter(doctor=request.user)
        serializer = AppointmentSerializer(appointments, many=True)

        return Response(format_response(
            True,
            "Patients data fetched successfully",
            data={"patients": serializer.data}
        ))
    

class DoctorListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        doctors = User.objects.filter(role='doctor')
        serializer = UserSerializer(doctors, many=True)
        return Response(format_response(
            True,
            "Doctor list fetched successfully",
            data={"doctors": serializer.data}
        ))
