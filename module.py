import os
import logging
from neo4j import GraphDatabase

# Конфигурация Neo4j
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "neo4j")

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

class Neo4jHandler:
    def __init__(self, uri, user, password):
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            logger.info("Подключение к Neo4j успешно установлено.")
        except Exception as e:
            logger.error(f"Ошибка подключения к Neo4j: {e}")
            raise

    def close(self):
        if self.driver:
            self.driver.close()
            logger.info("Соединение с Neo4j закрыто.")

    def create_user(self, user):
        query = """
        MERGE (u:User {id: $id})
        SET u.screen_name = $screen_name,
            u.name = $name,
            u.sex = $sex,
            u.city = $city
        """
        try:
            with self.driver.session() as session:
                session.run(query, **user)
            logger.info(f"Пользователь {user['id']} успешно создан в базе.")
        except Exception as e:
            logger.error(f"Ошибка при создании пользователя {user['id']}: {e}")

    def create_group(self, group):
        query = """
        MERGE (g:Group {id: $id})
        SET g.name = $name,
            g.screen_name = $screen_name
        """
        try:
            with self.driver.session() as session:
                session.run(query, **group)
            logger.info(f"Группа {group['id']} успешно создана в базе.")
        except Exception as e:
            logger.error(f"Ошибка при создании группы {group['id']}: {e}")

    def create_relationship(self, from_id, to_id, rel_type, from_label="User", to_label="User"):
        query = f"""
        MERGE (a:{from_label} {{id: $from_id}})
        MERGE (b:{to_label} {{id: $to_id}})
        MERGE (a)-[:{rel_type}]->(b)
        """
        try:
            with self.driver.session() as session:
                session.run(query, from_id=from_id, to_id=to_id)
            logger.info(f"Отношение {rel_type} между {from_id} ({from_label}) и {to_id} ({to_label}) успешно создано.")
        except Exception as e:
            logger.error(f"Ошибка при создании отношения {rel_type} между {from_id} и {to_id}: {e}")
