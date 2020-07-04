from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, mixins, generics, permissions
from posts.models import Post, Tags, PostTags
from posts.serializers import PostSerializer, UserSerializer, TagsSerializer, PostCreateTagSerializer, PostTagSerializer
from rest_framework.views import APIView
from django.http import Http404
from django.contrib.auth.models import User
from posts.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'posts': reverse('post-list', request=request, format=format),
        'tags': reverse('tags-list', request=request, format=format)
    })


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class TagList(generics.ListCreateAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


class PostTagsList(generics.ListCreateAPIView):
    queryset = PostTags.objects.all()
    serializer_class = PostTagSerializer


class PostTagsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PostTags.objects.all()
    serializer_class = PostTagSerializer
