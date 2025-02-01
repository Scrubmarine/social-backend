from rest_framework import serializers
from .models import User, Post, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # pass the password as plaintext so Django can hash it
        password = validated_data.pop('password')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=password
        )
        return user


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'user', 'created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        return Post.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'post', 'created_at']
        read_only_fields = ['created_at']
    def create(self, validated_data):
        return Comment.objects.create(**validated_data)