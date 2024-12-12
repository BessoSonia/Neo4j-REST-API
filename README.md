# API для работы с Neo4j

### Создание серверного REST API, тестирование

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/BessoSonia/Neo4j-REST-API
   cd директория_для_клонирования
   ```

2. Установите зависимости

    ```bash
    pip install -r requirements.txt
    ```

3. Создайте переменные окружения
   Запустите командную строку от имени администратора

   ```bash
   set NEO4J_URI=ваша_конфигурация_neo4j
   set NEO4J_USER=ваша_конфигурация_neo4j
   set NEO4J_PASSWORD=ваша_конфигурация_neo4j
   ```

4. Запустите API

    ```bash
    uvicorn api:app --reload
    ```

5. Тестирование

    ```bash
    pytest -v
    ```

