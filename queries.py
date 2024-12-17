from neo4j import GraphDatabase

class Neo4jQueries:
    # Инициализация подключения к базе данных Neo4j
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))


    # Закрытие подключения к базе данных
    def close(self):
        self.driver.close()


    # Получение всех узлов с атрибутами id и label
    def get_all_nodes(self):
        query = "MATCH (n) RETURN id(n) AS id, labels(n)[0] AS label"
        with self.driver.session() as session:
            return session.run(query).data()


    # Получение узла и всех его связей с атрибутами узлов и связей
    def get_node_with_relationships(self, node_id):
        query = """
        MATCH (n)-[r]-(m)
        WHERE id(n) = $node_id
        RETURN n AS node, r AS relationship, m AS connected_node
        """
        with self.driver.session() as session:
            result = session.run(query, node_id=node_id)
            data = []
            for record in result:
                node = dict(record["node"].items())  # Узел в словарь
                relationship = {
                    "type": record["relationship"].type  # Добавляем тип связи
                }
                relationship.update(record["relationship"].items())  # Добавляем атрибуты связи
                connected_node = dict(record["connected_node"].items())  # Связанный узел в словарь
                data.append({
                    "node": node,
                    "relationship": relationship,
                    "connected_node": connected_node
                })
            return data

    # Создание нового узла с указанным label и свойствами
    def create_node(self, label, properties):
        query = f"""
        MERGE (n:{label} {{id: $id}})
        SET n += $properties
        RETURN n
        """
        with self.driver.session() as session:
            return session.run(query, id=properties.get("id"), properties=properties).single()


    # Удаление узла и всех его связей
    def delete_node(self, node_id):
        query = """
        MATCH (n)
        WHERE id(n) = $node_id
        DETACH DELETE n
        """
        with self.driver.session() as session:
            session.run(query, node_id=node_id)
            return {"message": f"Node {node_id} and its relationships deleted"}


    # Создание связи между двумя узлами
    def create_relationship(self, from_id, to_id, rel_type, from_label="Node", to_label="Node"):
        query = f"""
        MATCH (a:{from_label} {{id: $from_id}})
        MATCH (b:{to_label} {{id: $to_id}})
        MERGE (a)-[:{rel_type}]->(b)
        """
        with self.driver.session() as session:
            session.run(query, from_id=from_id, to_id=to_id)
