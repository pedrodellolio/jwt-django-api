# from django.contrib.auth.models import User
from api.models import User
from api.serializers import UserSerializer, MyTokenObtainPairSerializer
from rest_framework import permissions, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create']:
            # Allow GET, POST requests without authentication
            permission_classes = [permissions.AllowAny]
        else:
            # Require authentication for other actions (e.g., PUT, DELETE)
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        '''
        Overrides default POST request, forcing the password sent to be encrypted
        '''
        user = serializer.save()
        user.set_password(self.request.data['password'])
        user.save()
        

class MyTokenObtainPairView(TokenObtainPairView):
    '''
    Overrides default sign in request from Django JWT, including user details
    '''
    serializer_class = MyTokenObtainPairSerializer