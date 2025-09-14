from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('polls/<int:poll_id>/', views.poll_detail, name='poll_detail'),
    path('polls/<int:poll_id>/statistics/', views.poll_statistics, name='poll_statistics'),
    path('api/polls/<int:poll_id>/next-question/', views.get_next_question, name='get_next_question'),
    path('api/polls/<int:poll_id>/submit-answer/', views.submit_answer, name='submit_answer'),
    path('api/polls/<int:poll_id>/statistics/', views.get_poll_statistics, name='get_poll_statistics'),
]
