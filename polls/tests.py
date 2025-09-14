from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
import json
from .models import Poll, Question, AnswerOption, QuestionCondition, UserResponse


class PollTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()
        self.client.force_login(self.user)
        
        self.poll = Poll.objects.create(
            title='Test Poll',
            author=self.user
        )
        
        self.question = Question.objects.create(
            poll=self.poll,
            text='Test question?',
            order=1
        )
        
        self.option = AnswerOption.objects.create(
            question=self.question,
            text='Yes',
            order=1
        )

    def test_get_next_question(self):
        response = self.client.get(f'/polls/{self.poll.id}/next-question/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('question', data)

    def test_submit_answer(self):
        data = {
            'question_id': self.question.id,
            'answer_id': self.option.id
        }
        response = self.client.post(
            f'/polls/{self.poll.id}/submit-answer/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_poll_statistics(self):
        response = self.client.get(f'/polls/{self.poll.id}/statistics/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('poll_id', data)
