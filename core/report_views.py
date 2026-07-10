from rest_framework.views import APIView
from rest_framework import permissions
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from leaves.models import Attendance, LeaveRequest
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime

User = get_user_model()

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')

class GenerateReportView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        start_date = None
        end_date = None
        if start_date_str and end_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            except ValueError:
                return HttpResponse("Invalid date format. Use YYYY-MM-DD.", status=400)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="attendance_report.pdf"'

        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        elements.append(Paragraph("System Report", styles['Title']))
        if start_date and end_date:
            elements.append(Paragraph(f"Period: {start_date} to {end_date}", styles['Normal']))
        elements.append(Spacer(1, 12))

        # Users
        elements.append(Paragraph("Users List", styles['Heading2']))
        users = User.objects.all()
        user_data = [['ID', 'Username', 'Role', 'Status']]
        for u in users:
            user_data.append([str(u.id), u.username, u.role, 'Active' if u.is_active else 'Disabled'])
        
        t = Table(user_data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 24))

        # Attendance
        elements.append(Paragraph("Attendance History", styles['Heading2']))
        attendance_qs = Attendance.objects.all().order_by('-date')
        if start_date:
            attendance_qs = attendance_qs.filter(date__gte=start_date)
        if end_date:
            attendance_qs = attendance_qs.filter(date__lte=end_date)
        
        att_data = [['Employee', 'Date', 'Check In', 'Check Out']]
        for a in attendance_qs:
            att_data.append([a.employee.username, str(a.date), str(a.check_in), str(a.check_out) if a.check_out else '--'])

        if len(att_data) > 1:
            t2 = Table(att_data)
            t2.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.grey),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('GRID', (0,0), (-1,-1), 1, colors.black),
            ]))
            elements.append(t2)
        else:
            elements.append(Paragraph("No attendance records found.", styles['Normal']))
        elements.append(Spacer(1, 24))

        # Leaves
        elements.append(Paragraph("Leave History", styles['Heading2']))
        leave_qs = LeaveRequest.objects.all().order_by('-applied_on')
        if start_date:
            leave_qs = leave_qs.filter(start_date__gte=start_date)
        if end_date:
            leave_qs = leave_qs.filter(end_date__lte=end_date)
            
        leave_data = [['Employee', 'Type', 'Start', 'End', 'Status']]
        for l in leave_qs:
            leave_data.append([l.employee.username, l.leave_type.name if l.leave_type else 'N/A', str(l.start_date), str(l.end_date), l.status])
            
        if len(leave_data) > 1:
            t3 = Table(leave_data)
            t3.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.grey),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('GRID', (0,0), (-1,-1), 1, colors.black),
            ]))
            elements.append(t3)
        else:
            elements.append(Paragraph("No leave requests found.", styles['Normal']))

        doc.build(elements)
        return response
