from django.db import models
from django.contrib.auth.models import User


class Poll(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    order = models.PositiveIntegerField()

    class Meta:
        unique_together = ['poll', 'order']
        ordering = ['poll', 'order']

    def __str__(self):
        return self.text


class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    order = models.PositiveIntegerField()

    class Meta:
        unique_together = ['question', 'order']
        ordering = ['question', 'order']

    def __str__(self):
        return self.text


class QuestionCondition(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='conditions')
    depends_on_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    required_answer = models.ForeignKey(AnswerOption, on_delete=models.CASCADE)


class UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    anonymous_user_id = models.CharField(max_length=100, null=True, blank=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(AnswerOption, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['user', 'poll', 'question'], ['anonymous_user_id', 'poll', 'question']]
