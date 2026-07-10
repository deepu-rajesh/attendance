from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import LeaveType, LeaveRequest, Attendance
from .serializers import LeaveTypeSerializer, LeaveRequestSerializer, LeaveRequestActionSerializer, AttendanceSerializer
from django.utils import timezone

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')

class IsManagerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in ['manager', 'admin'])

class LeaveTypeViewSet(viewsets.ModelViewSet):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

class LeaveRequestViewSet(viewsets.ModelViewSet):
    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['manager', 'admin']:
            return LeaveRequest.objects.all().order_by('-applied_on')
        return LeaveRequest.objects.filter(employee=user).order_by('-applied_on')

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user)

    @action(detail=True, methods=['patch'], permission_classes=[IsManagerUser])
    def status(self, request, pk=None):
        leave_request = self.get_object()
        serializer = LeaveRequestActionSerializer(leave_request, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(reviewed_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['manager', 'admin']:
            return Attendance.objects.all().order_by('-date')
        return Attendance.objects.filter(employee=user).order_by('-date')

    @action(detail=False, methods=['post'])
    def check_in(self, request):
        today = timezone.localdate()
        if Attendance.objects.filter(employee=request.user, date=today).exists():
            return Response({'detail': 'Already checked in today.'}, status=status.HTTP_400_BAD_REQUEST)
        attendance = Attendance.objects.create(employee=request.user)
        return Response(AttendanceSerializer(attendance).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def check_out(self, request):
        today = timezone.localdate()
        attendance = Attendance.objects.filter(employee=request.user, date=today).first()
        if not attendance:
            return Response({'detail': 'Not checked in today.'}, status=status.HTTP_400_BAD_REQUEST)
        if attendance.check_out:
            return Response({'detail': 'Already checked out today.'}, status=status.HTTP_400_BAD_REQUEST)
        
        attendance.check_out = timezone.localtime().time()
        attendance.save()
        return Response(AttendanceSerializer(attendance).data)
