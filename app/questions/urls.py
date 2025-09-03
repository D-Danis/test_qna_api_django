from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import QuestionViewSet, AnswerCreateAPIView, AnswerDetailAPIView, AnswerViewSet

router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'answers', AnswerViewSet, basename='answer')

urlpatterns = [
    path('', include(router.urls)),
    path('questions/<int:question_id>/answers/', AnswerCreateAPIView.as_view(), name='answer-create'),
    path('answers/<int:id>/', AnswerDetailAPIView.as_view(), name='answer-detail'),
]
