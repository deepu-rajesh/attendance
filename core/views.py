from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserCreateSerializer, PublicUserCreateSerializer

User = get_user_model()

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')

class IsManagerOrAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in ['manager', 'admin'])

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == 'manager':
            return User.objects.filter(role='employee').order_by('id')
        return User.objects.all().order_by('id')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'me':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'signup':
            permission_classes = [permissions.AllowAny]
        elif self.action in ['list', 'toggle_active']:
            permission_classes = [IsManagerOrAdminUser]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = PublicUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def verify(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response(self.get_serializer(user).data)

    @action(detail=True, methods=['patch'])
    def toggle_active(self, request, pk=None):
        user = self.get_object()
        if user.role == 'admin' and request.user.role != 'admin':
            return Response({'detail': 'Not allowed to modify admin users.'}, status=status.HTTP_403_FORBIDDEN)
        user.is_active = not user.is_active
        user.save()
        return Response(self.get_serializer(user).data)
