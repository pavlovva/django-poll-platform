from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from polls.models import Poll, Question, AnswerOption, QuestionCondition


class Command(BaseCommand):
    help = 'Create demo data'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')

        user = User.objects.get(username='admin')
        poll, created = Poll.objects.get_or_create(title='Овощи', defaults={'author': user})

        if created:
            q1 = Question.objects.create(poll=poll, text='Ты любишь помидоры?', order=1)
            AnswerOption.objects.create(question=q1, text='Да', order=1)
            AnswerOption.objects.create(question=q1, text='Нет', order=2)

            q2 = Question.objects.create(poll=poll, text='Ты любишь огурцы?', order=2)
            AnswerOption.objects.create(question=q2, text='Да', order=1)
            AnswerOption.objects.create(question=q2, text='Нет', order=2)

            q3 = Question.objects.create(poll=poll, text='Ты любишь буратту с помидорами?', order=3)
            AnswerOption.objects.create(question=q3, text='Да', order=1)
            AnswerOption.objects.create(question=q3, text='Нет', order=2)

            QuestionCondition.objects.create(
                question=q3,
                depends_on_question=q1,
                required_answer=q1.answeroption_set.get(text='Да')
            )

        self.stdout.write('Demo data created')
