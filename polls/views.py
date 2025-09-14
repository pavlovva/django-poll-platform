from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Count
from django.conf import settings
import json
from .models import Poll, Question, AnswerOption, QuestionCondition, UserResponse


def get_next_question(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    user = request.user
    
    # Для анонимных пользователей используем сессию
    if not user.is_authenticated:
        user_id = request.session.get('anonymous_user_id')
        if not user_id:
            user_id = f"anon_{request.session.session_key}"
            request.session['anonymous_user_id'] = user_id
    else:
        user_id = user.id
    
    if user.is_authenticated:
        user_responses = UserResponse.objects.filter(user=user, poll=poll).values_list('question_id', flat=True)
    else:
        user_responses = UserResponse.objects.filter(anonymous_user_id=user_id, poll=poll).values_list('question_id', flat=True)
    
    questions = Question.objects.filter(poll=poll).order_by('order')
    
    for question in questions:
        if question.id in user_responses:
            continue
            
        conditions = QuestionCondition.objects.filter(question=question)
        can_show = True
        
        for condition in conditions:
            if user.is_authenticated:
                user_answer = UserResponse.objects.filter(
                    user=user,
                    poll=poll,
                    question=condition.depends_on_question
                ).first()
            else:
                user_answer = UserResponse.objects.filter(
                    anonymous_user_id=user_id,
                    poll=poll,
                    question=condition.depends_on_question
                ).first()
            
            if not user_answer or user_answer.answer != condition.required_answer:
                can_show = False
                break
        
        if can_show:
            options = AnswerOption.objects.filter(question=question).order_by('order')
            return JsonResponse({
                'question': {
                    'id': question.id,
                    'text': question.text,
                    'order': question.order,
                    'options': [
                        {
                            'id': option.id,
                            'text': option.text,
                            'order': option.order
                        } for option in options
                    ]
                }
            }, json_dumps_params={'ensure_ascii': False})
    
    return JsonResponse({'message': 'No more questions available'})


@csrf_exempt
@require_http_methods(["POST"])
def submit_answer(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    user = request.user
    
    # Для анонимных пользователей используем сессию
    if not user.is_authenticated:
        user_id = request.session.get('anonymous_user_id')
        if not user_id:
            user_id = f"anon_{request.session.session_key}"
            request.session['anonymous_user_id'] = user_id
    else:
        user_id = user.id
    
    try:
        data = json.loads(request.body)
        question_id = data.get('question_id')
        answer_id = data.get('answer_id')
        
        if not question_id or not answer_id:
            return JsonResponse({'error': 'question_id and answer_id are required'}, status=400)
        
        question = get_object_or_404(Question, id=question_id, poll=poll)
        answer = get_object_or_404(AnswerOption, id=answer_id, question=question)
        
        if user.is_authenticated:
            UserResponse.objects.update_or_create(
                user=user,
                poll=poll,
                question=question,
                defaults={'answer': answer}
            )
        else:
            UserResponse.objects.update_or_create(
                anonymous_user_id=user_id,
                poll=poll,
                question=question,
                defaults={'answer': answer}
            )
        
        return JsonResponse({'message': 'Answer submitted successfully'})
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def get_poll_statistics(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    
    # Считаем уникальных пользователей (аутентифицированных и анонимных)
    authenticated_users = UserResponse.objects.filter(poll=poll, user__isnull=False).values('user').distinct().count()
    anonymous_users = UserResponse.objects.filter(poll=poll, anonymous_user_id__isnull=False).values('anonymous_user_id').distinct().count()
    total_responses = authenticated_users + anonymous_users
    
    questions_data = []
    questions = Question.objects.filter(poll=poll).order_by('order')
    
    for question in questions:
        responses = UserResponse.objects.filter(poll=poll, question=question)
        answer_stats = responses.values('answer__text').annotate(count=Count('id')).order_by('-count')
        
        questions_data.append({
            'question_id': question.id,
            'question_text': question.text,
            'order': question.order,
            'total_responses': responses.count(),
            'answer_statistics': [
                {
                    'answer_text': stat['answer__text'],
                    'count': stat['count']
                } for stat in answer_stats
            ]
        })
    
    return JsonResponse({
        'poll_id': poll.id,
        'poll_title': poll.title,
        'total_participants': total_responses,
        'questions': questions_data
    }, json_dumps_params={'ensure_ascii': False})


def index(request):
    polls = Poll.objects.all().order_by('-created_at')
    return render(request, 'polls/index.html', {'polls': polls})


def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    return render(request, 'polls/poll_detail.html', {'poll': poll})


def poll_statistics(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    
    # Считаем уникальных пользователей (аутентифицированных и анонимных)
    authenticated_users = UserResponse.objects.filter(poll=poll, user__isnull=False).values('user').distinct().count()
    anonymous_users = UserResponse.objects.filter(poll=poll, anonymous_user_id__isnull=False).values('anonymous_user_id').distinct().count()
    total_responses = authenticated_users + anonymous_users
    
    questions_data = []
    questions = Question.objects.filter(poll=poll).order_by('order')
    
    for question in questions:
        responses = UserResponse.objects.filter(poll=poll, question=question)
        answer_stats = responses.values('answer__text').annotate(count=Count('id')).order_by('-count')
        
        questions_data.append({
            'question_id': question.id,
            'question_text': question.text,
            'order': question.order,
            'total_responses': responses.count(),
            'answer_statistics': [
                {
                    'answer_text': stat['answer__text'],
                    'count': stat['count']
                } for stat in answer_stats
            ]
        })
    
    return render(request, 'polls/poll_statistics.html', {
        'poll': poll,
        'total_participants': total_responses,
        'authenticated_users': authenticated_users,
        'anonymous_users': anonymous_users,
        'questions': questions_data
    })
