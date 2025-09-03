import logging

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer

logger = logging.getLogger('questions')


class AnswerCreateAPIView(APIView):
    """
    APIView для добавления ответа к существующему вопросу.

    POST /questions/{question_id}/answers/
    """
    def post(self, request: Request, question_id:int) -> Response:
        logger.debug(f"POST /questions/{question_id}/answers/ data: {request.data}")
        question = get_object_or_404(Question, pk=question_id)
        data = request.data.copy()
        data['question'] = question.id
        serializer = AnswerSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info(f"Ответ добавлен на вопрос {question_id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Не удалось добавить ответ: {e}")
            raise


class AnswerDetailAPIView(APIView):
    """
    APIView для получения или удаления конкретного ответа по ID.

    GET /answers/{id}/
    DELETE /answers/{id}/
    """
    def get(self, request: Request, id:int) -> Response:
        logger.debug(f"GET /answers/{id}/")
        try:
            answer = get_object_or_404(Answer, pk=id)
            serializer = AnswerSerializer(answer)
            logger.info(f"Ответ получен на вопрос id: {id}")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Не удалось получить ответ: {e}")
            raise 

    def delete(self, request: Request, id:int)-> Response:
        logger.debug(f"DELETE /answers/{id}/")
        try:
            answer = get_object_or_404(Answer, pk=id)
            answer.delete()
            logger.info(f"Ответ удален на вопрос id: {id}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Не удалось удалить ответ: {e}")
            raise


class QuestionViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с вопросами:

    GET /questions/ - список вопросов
    POST /questions/ - создать вопрос
    GET /questions/{id}/ - получить вопрос с вложенными ответами
    DELETE /questions/{id}/ - удалить вопрос с каскадным удалением ответов

    Дополнительно:

    POST /questions/{id}/answers/ - добавить ответ к вопросу (через @action)
    """
    queryset = Question.objects.all().order_by('-created_at')
    serializer_class = QuestionSerializer

    @action(detail=True, methods=['post'])
    def answers(self, request: Request, pk=None) -> Response:
        """
        Создать ответ на конкретный вопрос.

        URL: POST /questions/{id}/answers/
        """
        logger.debug(f"POST /questions/{id}/answers/")
        question = self.get_object()
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(question=question)
            logger.info(f"Ответ добавлен на вопрос {id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"Не удалось добавить ответ: {id}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class AnswerViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с ответами:

    GET /answers/ - список всех ответов (опционально)
    GET /answers/{id}/ - получить конкретный ответ
    DELETE /answers/{id}/ - удалить ответ
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
