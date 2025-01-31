from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Post
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from django.contrib.auth.models import User


class CreateUserView(APIView):
    def post(self, request, *args, **kwargs):
        if User.objects.filter(username=request.data.get('username')).exists():
            return Response(
                {'username': 'A user with that username already exists.'},
                status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class GetUserView(APIView):
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

class GetAllUsersView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreatePostView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        if not user_id or not User.objects.filter(id=user_id).exists():
            return Response({'user': 'Invalid user ID.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetPostView(APIView):
    def get(self, request, id, *args, **kwargs):
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetPostsByUserView(APIView):
    def get(self, request, user_id, *args, **kwargs):

        posts = Post.get_posts_by_user(user_id=user_id)
        if not posts.exists():
            return Response({'error': 'Posts not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateCommentView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        if not user_id or not User.objects.filter(id=user_id).exists():
            return Response({'user': 'Invalid user ID.'}, status=status.HTTP_400_BAD_REQUEST)

        post_id = request.data.get('post')
        if not post_id or not Post.objects.filter(id=post_id).exists():
            return Response({'post': 'Invalid post ID.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)