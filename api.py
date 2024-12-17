import os
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from queries import Neo4jQueries

DB_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
DB_PASSWORD = os.getenv("NEO4J_PASSWORD", "neo4j")
API_TOKEN = os.getenv("API_TOKEN", "your-secret-token")

uri = "bolt://localhost:7687"

app = FastAPI()

neo4j_queries = Neo4jQueries(uri, DB_USERNAME, DB_PASSWORD)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Node(BaseModel):
    id: int
    label: str
    properties: dict = {}

class NodeWithRelationships(BaseModel):
    node: dict
    relationship: dict
    connected_node: dict

class NodeProperties(BaseModel):
    label: str
    properties: dict

def verify_token(token: str = Depends(oauth2_scheme)):
    if token != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

@app.get("/nodes/", response_model=list[Node])
async def get_nodes():
    try:
        nodes = neo4j_queries.get_all_nodes()
        return [{"id": node["id"], "label": node["label"]} for node in nodes]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/nodes/{node_id}", response_model=Node)
async def get_node(node_id: int):
    try:
        node = neo4j_queries.get_node(node_id)
        if node is None:
            raise HTTPException(status_code=404, detail="Node not found")
        if 'label' not in node:
            raise HTTPException(status_code=500, detail="Missing 'label' field in node data")
        return node
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")



@app.get("/nodes/{node_id}/relationships", response_model=list[NodeWithRelationships])
async def get_node_with_relationships(node_id: int):
    try:
        relationships = neo4j_queries.get_node_with_relationships(node_id)
        print(relationships)
        result = [
            {
                "node": relationship["node"],
                "relationship": {"type": relationship["relationship"]},
                "connected_node": relationship["connected_node"]
            }
            for relationship in relationships
        ]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/nodes/", response_model=Node, dependencies=[Depends(verify_token)])
async def create_node(node_properties: NodeProperties):
    try:
        node = neo4j_queries.create_node(node_properties.label, node_properties.properties)
        return {"id": node["id"], "label": node_properties.label}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/nodes/{node_id}", response_model=dict, dependencies=[Depends(verify_token)])
async def delete_node(node_id: int):
    try:
        message = neo4j_queries.delete_node(node_id)
        return message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/relationships/", response_model=dict, dependencies=[Depends(verify_token)])
async def create_relationship(from_id: int, to_id: int, rel_type: str, from_label: str = "Node", to_label: str = "Node"):
    try:
        neo4j_queries.create_relationship(from_id, to_id, rel_type, from_label, to_label)
        return {"message": f"Relationship {rel_type} created between {from_id} and {to_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("shutdown")
def shutdown():
    """Закрытие соединения с базой данных при завершении работы приложения."""
    neo4j_queries.close()

# Запуск приложения:
# uvicorn api:app --reload
