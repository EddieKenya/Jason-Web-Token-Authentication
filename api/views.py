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
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import filters

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

class UserPost(generics.ListAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self):
        user = self.request.user
        return Post.postobjects.filter(author = user)

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

class BlackListTokenView(APIView):
    def post (self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class PostSearchFilter(generics.ListAPIView):
        queryset = Post.postobjects.all()
        serializer_class = PostListSerializer
        filter_backends = [filters.SearchFilter]
        search_fields = ['^title']