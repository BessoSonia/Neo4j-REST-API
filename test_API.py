import pytest
from unittest.mock import MagicMock
from module import Neo4jHandler  # Импортируем вашу реализацию

@pytest.fixture
def mock_neo4j_handler():
    mock_handler = MagicMock(Neo4jHandler)
    return mock_handler

@pytest.fixture
def create_user_data():
    return {
        "id": 123,
        "screen_name": "john_doe",
        "name": "John Doe",
        "sex": "male",
        "city": "Moscow"
    }

@pytest.fixture
def create_group_data():
    return {
        "id": 456,
        "name": "Test Group",
        "screen_name": "test_group"
    }

# Тест для создания пользователя
def test_create_user(mock_neo4j_handler, create_user_data):
    mock_neo4j_handler.create_user.return_value = None

    # Вызов метода
    mock_neo4j_handler.create_user(create_user_data)

    # Проверки
    mock_neo4j_handler.create_user.assert_called_once_with(create_user_data)

# Тест для создания группы
def test_create_group(mock_neo4j_handler, create_group_data):
    mock_neo4j_handler.create_group.return_value = None

    # Вызов метода
    mock_neo4j_handler.create_group(create_group_data)

    # Проверки
    mock_neo4j_handler.create_group.assert_called_once_with(create_group_data)

# Тест для создания отношения
def test_create_relationship(mock_neo4j_handler):
    mock_neo4j_handler.create_relationship.return_value = None

    # Вызов метода
    mock_neo4j_handler.create_relationship(1, 2, "FOLLOW")

    # Проверки
    mock_neo4j_handler.create_relationship.assert_called_once_with(1, 2, "FOLLOW")
