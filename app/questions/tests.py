import pytest
import uuid
from typing import Any, Optional, Dict
from rest_framework.test import APIClient

from questions.models import Question, Answer


@pytest.fixture
def api_client() -> APIClient:
    """
    Фикстура для клиента API.
    """
    return APIClient()

@pytest.fixture
def sample_question() -> Question:
    """
    Фикстура создает тестовый вопрос.
    """
    return Question.objects.create(text="Sample question?")

@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload,expected_status,expected_error_field",
    [
        ({"text": "Valid question?"}, 201, None), # валидный случай
        ({}, 400, "text"),                        # пустой payload (нет текста)
        ({"text": ""}, 400, "text"),              # пустая строка
    ],
)
def test_create_question_param(
    api_client: APIClient,
    payload: Dict[str, Any],
    expected_status: int,
    expected_error_field: Optional[str],
    ) -> None:
    """
    Тест создания вопроса с разными payload, включая негативные.
    """
    response = api_client.post("/questions/", data=payload, format="json")
    assert response.status_code == expected_status
    if expected_status == 201:
        assert "id" in response.data
        assert response.data["text"] == payload["text"]
    else:
        assert expected_error_field in response.data
        assert isinstance(response.data[expected_error_field], list)

@pytest.mark.django_db
def test_get_questions_list(
    api_client: APIClient, 
    sample_question: Question
    ) -> None:
    """
    Проверяем, что вопрос в списке вопросов.
    """
    response = api_client.get("/questions/")
    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert any(q["id"] == sample_question.id for q in response.data)

@pytest.mark.django_db
@pytest.mark.parametrize(
    "question_id, user_id, text,expected_status",
    [
        (lambda q: q.id, str(uuid.uuid4()), "Valid answer", 201),
        (9999, str(uuid.uuid4()), "Answer to non-existing question", 404),  # несуществующий вопрос
        (lambda q: q.id, "", "Empty user id", 400),                         # пустой user_id
        (lambda q: q.id, str(uuid.uuid4()), "", 400),                       # пустой текст ответа
    ],
)
def test_create_answer_param(
    api_client: APIClient,
    sample_question: Question,
    question_id: Any,
    user_id: str,
    text: str,
    expected_status: int,
    ) -> None:
    """
    Тест создания ответов на вопрос, включая негативные сценарии.
    """
    q_id = question_id(sample_question)\
        if callable(question_id) else question_id

    url = f"/questions/{q_id}/answers/"
    payload = {"user_id": user_id, "text": text}
    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == expected_status
    if expected_status == 201:
        assert response.data["question"] == q_id
        assert response.data["text"] == text
        assert response.data["user_id"] == user_id
    elif expected_status == 400:
        if not user_id:
            assert "user_id" in response.data
        if not text:
            assert "text" in response.data
    elif expected_status == 404:
        assert "detail" in response.data

@pytest.mark.django_db
def test_delete_answer_and_question_cascade(
    api_client: APIClient, 
    sample_question: Question
    ) -> None:
    """
    Тест каскадного удаления: удаляем ответ, потом вопрос с ответами.
    """
    answer = Answer.objects.create(question=sample_question, 
                                   user_id=uuid.uuid4(), 
                                   text="Answer to delete")

    response = api_client.delete(f"/answers/{answer.id}/")
    assert response.status_code == 204
    assert not Answer.objects.filter(id=answer.id).exists()

    answer2 = Answer.objects.create(question=sample_question, 
                                    user_id=uuid.uuid4(), 
                                    text="Answer delete cascade")
    response = api_client.delete(f"/questions/{sample_question.id}/")
    assert response.status_code == 204
    assert not Question.objects.filter(id=sample_question.id).exists()
    assert not Answer.objects.filter(id=answer2.id).exists()
