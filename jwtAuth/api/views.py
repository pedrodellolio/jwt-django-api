# from django.contrib.auth.models import User
from api.models import User
from rest_framework import permissions, viewsets

from api.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        '''
        Overrides default POST request, forcing the password sent to be encrypted
        '''
        user = serializer.save()
        user.set_password(self.request.data['password'])
        user.save()
