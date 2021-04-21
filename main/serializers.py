from rest_framework import serializers
from .models import Problem, CodeImage, Reply, Comment


class CodeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeImage
        fields = ['image',]

    def _get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            url = obj.image.url
            if request is not None:
                url = request.build_absolute_uri(url)
            return url
        return ''

    def to_representation(self, instance):
        representation = super(CodeImageSerializer, self).to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation


class ProblemSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d %B %Y %H:%M", read_only=True)
    images = CodeImageSerializer(many=True, read_only=True)

    class Meta:
        model = Problem
        fields = ['title', 'description', 'images', 'created_at', 'author']

    def create(self, validated_data, instance):
        request = self.context.get('request')
        images_data = request.FILES
        author = request.user
        problem = Problem.objects.create(author=author, **validated_data)
        for image in images_data.getlist('images'):
            CodeImage.objects.create(problem=problem, image=image)
        return problem

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.images.all().delete()
        images_data = request.FILES
        for image in images_data.getlist('images'):
            CodeImage.objects.create(problem=instance, image=image)
        return instance


class ReplySerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Reply
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        reply = Reply.objects.create(author=author, **validated_data)
        return reply

    def to_representation(self, instance):
        representation = super(ReplySerializer, self).to_representation(instance)
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        return representation


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source = 'author.email')

    class Meta:
        model = Comment
        fields = ['comment']

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        comment = Comment.objects.create(author=author, **validated_data)
        return comment
