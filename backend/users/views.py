from django.contrib.auth.models import User

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from django.conf import settings

from roles.models import Role
from .serializers import UserSerializer
from projects.models import Member
from projects.permissions import IsProjectAdmin
from projects.models import Project 
class Me(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data)


class ListUsers(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated & IsProjectAdmin]
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("username",)


class RegisterUser(generics.CreateAPIView):
  serializer_class = UserSerializer
  queryset = User.objects.all()
  permission_classes = [
        permissions.AllowAny
  ]

  def post(self, request, format='json'):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        if user:
            token = Token.objects.create(user=user)
            json = serializer.data
            json['token'] = token.key

            print(request.data)

            if request.data['rolename'] == "annotator":

                annotator_role = Role.objects.get(name=settings.ROLE_ANNOTATOR)
                active_project = Project.objects.get(id=request.data['project'])
                
                Member.objects.create(
                    project=active_project,
                    user=user,
                    role=annotator_role,
                )
                
            return Response(json, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
