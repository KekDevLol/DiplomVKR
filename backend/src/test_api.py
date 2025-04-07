import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from main import app, fake_db, create_access_token  # Замените "your_app_file" на имя файла с API

client = TestClient(app)

# Фикстура для очистки fake_db перед каждым тестом
@pytest.fixture(autouse=True)
def reset_db():
    fake_db.clear()
    fake_db.update({"users": {}, "agents": {}, "tasks": {}, "messages": {}, "integrations": {}})

# Тесты для аутентификации
def test_login_success():
    fake_db["users"]["testuser"] = {"user_id": 1, "password": "testpass", "role": "admin"}
    response = client.post("/auth/login", data={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_failure():
    fake_db["users"]["testuser"] = {"user_id": 1, "password": "testpass", "role": "admin"}
    response = client.post("/auth/login", data={"username": "testuser", "password": "wrongpass"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

# Тесты для текущего пользователя
def test_get_current_user():
    fake_db["users"]["testuser"] = {"user_id": 1, "password": "testpass", "role": "admin"}
    token = create_access_token(data={"sub": "testuser"}, expires_delta=timedelta(minutes=30))
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["role"] == "admin"

# Тесты для регистрации агента
def test_register_agent():
    fake_db["users"]["testuser"] = {"user_id": 1, "password": "testpass", "role": "admin"}
    token = create_access_token(data={"sub": "testuser"}, expires_delta=timedelta(minutes=30))
    response = client.post(
        "/agents",
        json={
            "agent_type": "ML",
            "status": "active",
            "priority_level": 2,
            "configuration": {"model": "neural_network"}
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "agent_id" in response.json()
    assert response.json()["message"] == "Agent registered successfully"

# Тесты для управления жизненным циклом агента
def test_start_agent():
    fake_db["users"]["testuser"] = {"user_id": 1, "password": "testpass", "role": "admin"}
    token = create_access_token(data={"sub": "testuser"}, expires_delta=timedelta(minutes=30))
    agent_response = client.post(
        "/agents",
        json={"agent_type": "ML", "status": "stopped", "priority_level": 2, "configuration": {}},
        headers={"Authorization": f"Bearer {token}"}
    )
    agent_id = agent_response.json()["agent_id"]
    response = client.post(f"/agents/{agent_id}/start", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Agent started successfully"

def test_stop_agent():
    fake_db["users"]["testuser"] = {"user_id": 1, "password": "testpass", "role": "admin"}
    token = create_access_token(data={"sub": "testuser"}, expires_delta=timedelta(minutes=30))
    agent_response = client.post(
        "/agents",
        json={"agent_type": "ML", "status": "active", "priority_level": 2, "configuration": {}},
        headers={"Authorization": f"Bearer {token}"}
    )
    agent_id = agent_response.json()["agent_id"]
    response = client.post(f"/agents/{agent_id}/stop", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Agent stopped successfully"

def test_restart_agent():
    fake_db["users"]["testuser"] = {"user_id": 1, "password": "testpass", "role": "admin"}
    token = create_access_token(data={"sub": "testuser"}, expires_delta=timedelta(minutes=30))
    agent_response = client.post(
        "/agents",
        json={"agent_type": "ML", "status": "stopped", "priority_level": 2, "configuration": {}},
        headers={"Authorization": f"Bearer {token}"}
    )
    agent_id = agent_response.json()["agent_id"]
    response = client.post(f"/agents/{agent_id}/restart", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Agent restarted successfully"

def test_delete_agent():
    fake_db["users"]["testuser"] = {"user_id": 1, "password": "testpass", "role": "admin"}
    token = create_access_token(data={"sub": "testuser"}, expires_delta=timedelta(minutes=30))
    agent_response = client.post(
        "/agents",
        json={"agent_type": "ML", "status": "active", "priority_level": 2, "configuration": {}},
        headers={"Authorization": f"Bearer {token}"}
    )
    agent_id = agent_response.json()["agent_id"]
    response = client.delete(f"/agents/{agent_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Agent deleted successfully"

# Тесты для мониторинга агентов
def test_get_agent_status():
    fake_db["users"]["testuser"] = {"user_id": 1, "password": "testpass", "role": "admin"}
    token = create_access_token(data={"sub": "testuser"}, expires_delta=timedelta(minutes=30))
    agent_response = client.post(
        "/agents",
        json={"agent_type": "ML", "status": "active", "priority_level": 2, "configuration": {}},
        headers={"Authorization": f"Bearer {token}"}
    )
    agent_id = agent_response.json()["agent_id"]
    response = client.get(f"/agents/{agent_id}/status", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["status"] == "active"

def test_get_agent_metrics():
    fake_db["users"]["testuser"] = {"user_id": 1, "password": "testpass", "role": "admin"}
    token = create_access_token(data={"sub": "testuser"}, expires_delta=timedelta(minutes=30))
    agent_response = client.post(
        "/agents",
        json={"agent_type": "ML", "status": "active", "priority_level": 2, "configuration": {}},
        headers={"Authorization": f"Bearer {token}"}
    )
    agent_id = agent_response.json()["agent_id"]
    response = client.get(f"/agents/{agent_id}/metrics", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()["metrics"]) == 2

# Тесты для коммуникации между агентами
def test_send_message():
    fake_db["users"]["testuser"] = {"user_id": 1, "password": "testpass", "role": "admin"}
    token = create_access_token(data={"sub": "testuser"}, expires_delta=timedelta(minutes=30))
    agent1_response = client.post(
        "/agents",
        json={"agent_type": "ML", "status": "active", "priority_level": 2, "configuration": {}},
        headers={"Authorization": f"Bearer {token}"}
    )
    agent2_response = client.post(
        "/agents",
        json={"agent_type": "BDI", "status": "active", "priority_level": 1, "configuration": {}},
        headers={"Authorization": f"Bearer {token}"}
    )
    sender_id = agent1_response.json()["agent_id"]
    receiver_id = agent2_response.json()["agent_id"]
    response = client.post(
        "/messages",
        json={"sender_id": sender_id, "receiver_id": receiver_id, "content": "Hello"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "message_id" in response.json()

def test_get_messages():
    fake_db["users"]["testuser"] = {"user_id": 1, "password": "testpass", "role": "admin"}
    token = create_access_token(data={"sub": "testuser"}, expires_delta=timedelta(minutes=30))
    agent_response = client.post(
        "/agents",
        json={"agent_type": "ML", "status": "active", "priority_level": 2, "configuration": {}},
        headers={"Authorization": f"Bearer {token}"}
    )
    agent_id = agent_response.json()["agent_id"]
    client.post(
        "/messages",
        json={"sender_id": agent_id, "receiver_id": agent_id, "content": "Self message"},
        headers={"Authorization": f"Bearer {token}"}
    )
    response = client.get(f"/messages/{agent_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()["messages"]) == 1

# Тесты для назначения задач
def test_create_task():
    fake_db["users"]["testuser"] = {"user_id": 1, "password": "testpass", "role": "admin"}
    token = create_access_token(data={"sub": "testuser"}, expires_delta=timedelta(minutes=30))
    agent_response = client.post(
        "/agents",
        json={"agent_type": "ML", "status": "active", "priority_level": 2, "configuration": {}},
        headers={"Authorization": f"Bearer {token}"}
    )
    agent_id = agent_response.json()["agent_id"]
    response = client.post(
        "/tasks",
        json={
            "priority": 3,
            "assigned_agent_id": agent_id,
            "deadline": "2023-12-31T23:59:59",
            "status": "pending"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "task_id" in response.json()

def test_get_task():
    fake_db["users"]["testuser"] = {"user_id": 1, "password": "testpass", "role": "admin"}
    token = create_access_token(data={"sub": "testuser"}, expires_delta=timedelta(minutes=30))
    agent_response = client.post(
        "/agents",
        json={"agent_type": "ML", "status": "active", "priority_level": 2, "configuration": {}},
        headers={"Authorization": f"Bearer {token}"}
    )
    agent_id = agent_response.json()["agent_id"]
    task_response = client.post(
        "/tasks",
        json={
            "priority": 3,
            "assigned_agent_id": agent_id,
            "deadline": "2023-12-31T23:59:59",
            "status": "pending"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = task_response.json()["task_id"]
    response = client.get(f"/tasks/{task_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["task_id"] == task_id

# Тесты для координации агентов
def test_coordinate_agents():
    fake_db["users"]["testuser"] = {"user_id": 1, "password": "testpass", "role": "admin"}
    token = create_access_token(data={"sub": "testuser"}, expires_delta=timedelta(minutes=30))
    agent1_response = client.post(
        "/agents",
        json={"agent_type": "ML", "status": "active", "priority_level": 2, "configuration": {}},
        headers={"Authorization": f"Bearer {token}"}
    )
    agent2_response = client.post(
        "/agents",
        json={"agent_type": "BDI", "status": "active", "priority_level": 1, "configuration": {}},
        headers={"Authorization": f"Bearer {token}"}
    )
    agent1_id = agent1_response.json()["agent_id"]
    agent2_id = agent2_response.json()["agent_id"]
    response = client.post(
        "/coordination",
        json={"agents": [agent1_id, agent2_id], "action": "collaborate"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "coordination_id" in response.json()

# Тесты для обновления конфигурации агента
def test_update_config():
    fake_db["users"]["testuser"] = {"user_id": 1, "password": "testpass", "role": "admin"}
    token = create_access_token(data={"sub": "testuser"}, expires_delta=timedelta(minutes=30))
    agent_response = client.post(
        "/agents",
        json={"agent_type": "ML", "status": "active", "priority_level": 2, "configuration": {}},
        headers={"Authorization": f"Bearer {token}"}
    )
    agent_id = agent_response.json()["agent_id"]
    response = client.put(
        f"/agents/{agent_id}/config",
        json={"configuration": {"model": "decision_tree"}},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Configuration updated"

# Тесты для интеграции внешних систем
def test_add_integration():
    fake_db["users"]["testuser"] = {"user_id": 1, "password": "testpass", "role": "admin"}
    token = create_access_token(data={"sub": "testuser"}, expires_delta=timedelta(minutes=30))
    response = client.post(
        "/integrations",
        json={"system_name": "External", "api_url": "https://example.com", "auth_details": {"token": "abc"}},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "integration_id" in response.json()

def test_get_integrations():
    fake_db["users"]["testuser"] = {"user_id": 1, "password": "testpass", "role": "admin"}
    token = create_access_token(data={"sub": "testuser"}, expires_delta=timedelta(minutes=30))
    client.post(
        "/integrations",
        json={"system_name": "External", "api_url": "https://example.com", "auth_details": {"token": "abc"}},
        headers={"Authorization": f"Bearer {token}"}
    )
    response = client.get("/integrations", headers={"Authorization": f"Bearer Angled brackets < > are used instead of square brackets [ ] to avoid interpretation as markup by the renderer."})
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import jwt  # PyJWT для работы с токенами
from enum import Enum

# Инициализация приложения FastAPI
app = FastAPI(
    title="AI Agent Management System API",
    description="API для управления ИИ-агентами: регистрация, жизненный цикл, мониторинг, задачи, коммуникация и интеграция.",
    version="1.0.0"
)

# Конфигурация для JWT
SECRET_KEY = "1"  # Замените на безопасный ключ
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Схема OAuth2 для аутентификации
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Перечисления для статусов
class AgentStatus(str, Enum):
    ACTIVE = "active"
    STOPPED = "stopped"
    PAUSED = "paused"

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

# Модели данных (Pydantic)
class AgentCreate(BaseModel):
    agent_type: str = Field(..., max_length=255, description="Тип агента (например, BDI, ML)")
    status: AgentStatus = Field(..., description="Статус агента")
    priority_level: int = Field(..., ge=1, le=3, description="Уровень приоритета (1-3)")
    configuration: Dict = Field(..., description="Конфигурация агента в формате JSON")

    class Config:
        schema_extra = {
            "example": {
                "agent_type": "ML",
                "status": "active",
                "priority_level": 2,
                "configuration": {"model": "neural_network", "params": {"learning_rate": 0.01}}
            }
        }

class AgentResponse(BaseModel):
    agent_id: int
    message: str

class AgentStatusResponse(BaseModel):
    agent_id: int
    status: AgentStatus
    last_heartbeat: datetime

class Metric(BaseModel):
    metric_type: str = Field(..., max_length=50, description="Тип метрики (например, CPU, Memory)")
    value: float

class AgentMetricsResponse(BaseModel):
    agent_id: int
    metrics: List[Metric]

class MessageCreate(BaseModel):
    sender_id: int
    receiver_id: int
    content: str

class MessageResponse(BaseModel):
    message_id: int
    timestamp: datetime

class MessageListResponse(BaseModel):
    agent_id: int
    messages: List[Dict[str, str]]

class TaskCreate(BaseModel):
    priority: int = Field(..., ge=1, le=5, description="Приоритет задачи (1-5)")
    assigned_agent_id: int
    deadline: datetime
    status: TaskStatus

class TaskResponse(BaseModel):
    task_id: int
    message: str

class TaskInfo(BaseModel):
    task_id: int
    priority: int
    assigned_agent_id: int
    deadline: datetime
    status: TaskStatus

class CoordinationRequest(BaseModel):
    agents: List[int]
    action: str

class CoordinationResponse(BaseModel):
    coordination_id: int
    message: str

class ConfigurationUpdate(BaseModel):
    configuration: Dict

class IntegrationCreate(BaseModel):
    system_name: str
    api_url: str
    auth_details: Dict

class IntegrationResponse(BaseModel):
    integration_id: int
    message: str

class IntegrationInfo(BaseModel):
    integration_id: int
    system_name: str
    api_url: str

class UserCreate(BaseModel):
    username: str
    password: str
    role_id: int

class UserResponse(BaseModel):
    user_id: int
    message: str

class UserInfo(BaseModel):
    user_id: int
    username: str
    role: str

class Role(BaseModel):
    role_id: int
    role_name: str

class LogEntry(BaseModel):
    timestamp: datetime
    level: str
    message: str

class SystemMetrics(BaseModel):
    cpu_usage: float
    memory_usage: float
    active_agents: int

fake_db = {"users": {}, "agents": {}, "tasks": {}, "messages": {}, "integrations": {}}

# Функция создания JWT-токена
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Проверка токена и получение текущего пользователя
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username not in fake_db["users"]:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"username": username, "role": fake_db["users"][username]["role"]}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Тесты для управления пользователями и ролями
def test_create_user():
    fake_db["users"]["admin"] = {"user_id": 1, "password": "adminpass", "role": "admin"}
    token = create_access_token(data={"sub": "admin"}, expires_delta=timedelta(minutes=30))
    response = client.post(
        "/users",
        json={"username": "newuser", "password": "newpass", "role_id": 1},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "user_id" in response.json()
    assert response.json()["message"] == "User created"

def test_create_user_non_admin():
    fake_db["users"]["user"] = {"user_id": 1, "password": "userpass", "role": "user"}
    token = create_access_token(data={"sub": "user"}, expires_delta=timedelta(minutes=30))
    response = client.post(
        "/users",
        json={"username": "newuser", "password": "newpass", "role_id": 1},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"

def test_update_user():
    fake_db["users"]["admin"] = {"user_id": 1, "password": "adminpass", "role": "admin"}
    fake_db["users"]["testuser"] = {"user_id": 2, "password": "testpass", "role": "user"}
    token = create_access_token(data={"sub": "admin"}, expires_delta=timedelta(minutes=30))
    response = client.put(
        "/users/2",
        json={"username": "testuser", "password": "newpass", "role_id": 2},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "User updated"

def test_get_roles():
    fake_db["users"]["testuser"] = {"user_id": 1, "password": "testpass", "role": "admin"}
    token = create_access_token(data={"sub": "testuser"}, expires_delta=timedelta(minutes=30))
    response = client.get("/roles", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["role_name"] == "user"
    assert response.json()[1]["role_name"] == "admin"

# Тесты для логирования и мониторинга
def test_get_logs():
    fake_db["users"]["testuser"] = {"user_id": 1, "password": "testpass", "role": "admin"}
    token = create_access_token(data={"sub": "testuser"}, expires_delta=timedelta(minutes=30))
    response = client.get("/logs", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["level"] == "INFO"

def test_get_system_metrics():
    fake_db["users"]["testuser"] = {"user_id": 1, "password": "testpass", "role": "admin"}
    token = create_access_token(data={"sub": "testuser"}, expires_delta=timedelta(minutes=30))
    response = client.get("/metrics", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "cpu_usage" in response.json()
    assert response.json()["active_agents"] == 0

if __name__ == "__main__":
    pytest.main(["-v"])