from rest_framework import serializers
from .models import LeaveType, LeaveRequest, Attendance
from core.serializers import UserSerializer

class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'

class LeaveRequestSerializer(serializers.ModelSerializer):
    employee = UserSerializer(read_only=True)
    leave_type_details = LeaveTypeSerializer(source='leave_type', read_only=True)
    leave_type = serializers.PrimaryKeyRelatedField(queryset=LeaveType.objects.all(), write_only=True)

    class Meta:
        model = LeaveRequest
        fields = '__all__'
        read_only_fields = ('employee', 'status', 'applied_on', 'reviewed_by')

class LeaveRequestActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ('status', 'remarks')

class AttendanceSerializer(serializers.ModelSerializer):
    employee = UserSerializer(read_only=True)
    
    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ('employee', 'date', 'check_in', 'check_out')
