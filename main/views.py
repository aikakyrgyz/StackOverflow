from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .permissions import IsAuthorPermission
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from .models import Problem, Reply, Comment
from .serializers import ProblemSerializer, ReplySerializer, CommentSerializer

class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated, ]
        elif self.action in ('update', 'destroy', 'partial_update'):
            permissions = [IsAuthorPermission, ]
        else:
            permissions = []
        return [permission() for permission in permissions]


class ProblemViewSet(PermissionMixin, ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer


class ReplyViewSet(PermissionMixin, ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

class CommentViewSet(PermissionMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
