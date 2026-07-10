from django.contrib import admin
from .models import LeaveType, LeaveRequest, Attendance

admin.site.register(LeaveType)
admin.site.register(LeaveRequest)
admin.site.register(Attendance)
