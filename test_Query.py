import pytest
from unittest.mock import MagicMock
from queries import Neo4jQueries

@pytest.fixture
def mock_neo4j_queries():
    mock_queries = MagicMock(Neo4jQueries)
    return mock_queries


# Тест для метода get_all_nodes
def test_get_all_nodes(mock_neo4j_queries):
    mock_neo4j_queries.get_all_nodes.return_value = [
        {"id": 1, "label": "Person"},
        {"id": 2, "label": "City"}
    ]

    nodes = mock_neo4j_queries.get_all_nodes()

    assert len(nodes) == 2
    assert nodes[0]["id"] == 1
    assert nodes[1]["label"] == "City"
    mock_neo4j_queries.get_all_nodes.assert_called_once()


# Тест для метода create_node
def test_create_node(mock_neo4j_queries):
    label = "Person"
    properties = {"name": "John", "age": 30}

    mock_neo4j_queries.create_node.return_value = {"id": 1, "labels": [label], "properties": properties}

    node = mock_neo4j_queries.create_node(label, properties)

    assert node["id"] == 1
    assert "Person" in node["labels"]
    assert node["properties"]["name"] == "John"
    mock_neo4j_queries.create_node.assert_called_once_with(label, properties)


# Тест для метода delete_node
def test_delete_node(mock_neo4j_queries):
    node_id = 1

    mock_neo4j_queries.delete_node.return_value = {"message": f"Node {node_id} deleted."}

    message = mock_neo4j_queries.delete_node(node_id)

    # Проверки
    assert message["message"] == f"Node {node_id} deleted."
    mock_neo4j_queries.delete_node.assert_called_once_with(node_id)


# Тест для метода close
def test_close(mock_neo4j_queries):
    mock_neo4j_queries.close()

    mock_neo4j_queries.close.assert_called_once()
