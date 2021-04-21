from django.db import models
from account.models import MyUser


class Problem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='problems')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class CodeImage(models.Model):
    image = models.ImageField(upload_to='images')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='images')


class Reply(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='replies') #'Problem'
    author = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING, related_name='replies')
    body = models.TextField()
    image = models.ImageField(upload_to='reply_images')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body

    class Meta:
        ordering = ['-created_at', ]


class Comment(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.DO_NOTHING, related_name='comments')
    author = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING, related_name='comments')
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ['-created_at']