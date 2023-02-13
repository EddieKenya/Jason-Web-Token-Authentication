from rest_framework import generics
from base.models import Post
from.serializers import PostListSerializer, CreateSerializer, RegistrationSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import BasePermission, SAFE_METHODS,AllowAny
from rest_framework.views import APIView
from rest_framework import status

class PostUserPermissions(BasePermission):
    message = "youre not authenticated to edit this post"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class UserRegistration(APIView):

    def post (self, request):
        register = RegistrationSerializer(data=request.data)
        if register.is_valid():
            user = register.save()
            if user:
                return Response(status=status.HTTP_201_CREATED) 
        return Response(register.errors, status=status.HTTP_400_BAD_REQUEST )

class PostList(generics.ListAPIView):
    queryset = Post.postobjects.all()
    serializer_class = PostListSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView, PostUserPermissions):
    permission_classes = [PostUserPermissions]
    queryset = Post.postobjects.all()
    serializer_class = PostListSerializer

class CreatePost(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = CreateSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer