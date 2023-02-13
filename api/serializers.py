from rest_framework import serializers
from base.models import Post, User


class PostListSerializer (serializers.ModelSerializer):
    class Meta:
        model= Post
        fields = ('category', 'title', 'author', 'excerpt', 'content', 'status', 'published')


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance