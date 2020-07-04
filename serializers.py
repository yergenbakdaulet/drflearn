from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Post, Tags, PostTags
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedRelatedField(many=True, view_name='post-detail', read_only=True,)

    # owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = User
        fields = ['id', 'username', 'posts']


class PostCreateTagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tags
        fields = ('url', 'id', 'name')


class PostTagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostTags
        fields = ('id', )
        extra_kwargs = {'tag_id': {'read_only': False}}


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    tags = PostTagSerializer(many=True, read_only=False, required=False,)

    class Meta:
        model = Post
        fields = ('id', 'url', 'owner', 'name', 'content', 'created', 'tags')
        read_only_field = ('created',)

    def to_representation(self, instance):
        representation = super(PostSerializer, self).to_representation(instance)
        representation['tags'] = PostTagSerializer(instance.tags.all(), many=True).data
        return representation

    def create(self, validated_data):
        s = validated_data.pop('tags')
        tag_data = self.context['request'].data.get('tags')
        post = Post.objects.create(**validated_data)
        for tag in tag_data:
            PostTags.objects.create(post=post, **tag)
        return post

    def update(self, instance, validated_data):
        s = validated_data.pop('tags')
        tag_data = self.context['request'].data.get('tags')
        for item in validated_data:
            if Post._meta.get_field(item):
                setattr(instance, item, validated_data[item])
        PostTags.objects.filter(post=instance).delete()
        for tag in tag_data:
            PostTags.objects.create(post=instance, **tag)
        instance.save()
        return instance


class TagsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tags
        fields = ('url', 'id', 'name', 'created', 'posts')
        read_only_field = ('created',)
