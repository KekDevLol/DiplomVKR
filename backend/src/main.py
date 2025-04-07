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
SECRET_KEY = "your-secret-key"  # Замените на безопасный ключ
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

fake_db = {"users": {}, "agents": {}, "tasks": {}, "messages": {}, "integrations": {}} # Пока нет бд и агентов выыглядит так

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

# 1. Регистрация агентов
@app.post("/agents", response_model=AgentResponse, summary="Регистрация нового агента")
async def register_agent(agent: AgentCreate, current_user: dict = Depends(get_current_user)):
    """Регистрирует нового агента в системе."""
    agent_id = len(fake_db["agents"]) + 1
    fake_db["agents"][agent_id] = {
        "agent_type": agent.agent_type,
        "status": agent.status,
        "priority_level": agent.priority_level,
        "configuration": agent.configuration,
        "last_heartbeat": datetime.utcnow()
    }
    return {"agent_id": agent_id, "message": "Agent registered successfully"}

# 2. Управление жизненным циклом агентов
@app.post("/agents/{agent_id}/start", response_model=AgentResponse, summary="Запуск агента")
async def start_agent(agent_id: int, current_user: dict = Depends(get_current_user)):
    """Запускает указанного агента."""
    if agent_id not in fake_db["agents"]:
        raise HTTPException(status_code=404, detail="Agent not found")
    fake_db["agents"][agent_id]["status"] = AgentStatus.ACTIVE
    fake_db["agents"][agent_id]["last_heartbeat"] = datetime.utcnow()
    return {"agent_id": agent_id, "message": "Agent started successfully"}

@app.post("/agents/{agent_id}/stop", response_model=AgentResponse, summary="Остановка агента")
async def stop_agent(agent_id: int, current_user: dict = Depends(get_current_user)):
    """Останавливает указанного агента."""
    if agent_id not in fake_db["agents"]:
        raise HTTPException(status_code=404, detail="Agent not found")
    fake_db["agents"][agent_id]["status"] = AgentStatus.STOPPED
    return {"agent_id": agent_id, "message": "Agent stopped successfully"}

@app.post("/agents/{agent_id}/restart", response_model=AgentResponse, summary="Перезапуск агента")
async def restart_agent(agent_id: int, current_user: dict = Depends(get_current_user)):
    """Перезапускает указанного агента."""
    if agent_id not in fake_db["agents"]:
        raise HTTPException(status_code=404, detail="Agent not found")
    fake_db["agents"][agent_id]["status"] = AgentStatus.ACTIVE
    fake_db["agents"][agent_id]["last_heartbeat"] = datetime.utcnow()
    return {"agent_id": agent_id, "message": "Agent restarted successfully"}

@app.delete("/agents/{agent_id}", response_model=AgentResponse, summary="Удаление агента")
async def delete_agent(agent_id: int, current_user: dict = Depends(get_current_user)):
    """Удаляет указанного агента из системы."""
    if agent_id not in fake_db["agents"]:
        raise HTTPException(status_code=404, detail="Agent not found")
    del fake_db["agents"][agent_id]
    return {"agent_id": agent_id, "message": "Agent deleted successfully"}

# 3. Мониторинг агентов
@app.get("/agents/{agent_id}/status", response_model=AgentStatusResponse, summary="Получение статуса агента")
async def get_agent_status(agent_id: int, current_user: dict = Depends(get_current_user)):
    """Возвращает текущий статус и время последнего обновления агента."""
    if agent_id not in fake_db["agents"]:
        raise HTTPException(status_code=404, detail="Agent not found")
    agent = fake_db["agents"][agent_id]
    return {
        "agent_id": agent_id,
        "status": agent["status"],
        "last_heartbeat": agent["last_heartbeat"]
    }

@app.get("/agents/{agent_id}/metrics", response_model=AgentMetricsResponse, summary="Получение метрик агента")
async def get_agent_metrics(agent_id: int, current_user: dict = Depends(get_current_user)):
    """Возвращает метрики производительности агента."""
    if agent_id not in fake_db["agents"]:
        raise HTTPException(status_code=404, detail="Agent not found")
    metrics = [
        {"metric_type": "CPU", "value": 75.5},
        {"metric_type": "Memory", "value": 512.0}
    ]
    return {"agent_id": agent_id, "metrics": metrics}

# 4. Коммуникация между агентами
@app.post("/messages", response_model=MessageResponse, summary="Отправка сообщения между агентами")
async def send_message(message: MessageCreate, current_user: dict = Depends(get_current_user)):
    """Отправляет сообщение от одного агента другому."""
    if message.sender_id not in fake_db["agents"] or message.receiver_id not in fake_db["agents"]:
        raise HTTPException(status_code=404, detail="Sender or receiver not found")
    message_id = len(fake_db["messages"]) + 1
    fake_db["messages"][message_id] = {
        "sender_id": message.sender_id,
        "receiver_id": message.receiver_id,
        "content": message.content,
        "timestamp": datetime.utcnow()
    }
    return {"message_id": message_id, "timestamp": fake_db["messages"][message_id]["timestamp"]}

@app.get("/messages/{agent_id}", response_model=MessageListResponse, summary="Получение сообщений агента")
async def get_messages(agent_id: int, current_user: dict = Depends(get_current_user)):
    """Возвращает все сообщения, отправленные или полученные агентом."""
    if agent_id not in fake_db["agents"]:
        raise HTTPException(status_code=404, detail="Agent not found")
    messages = [
        {
            "message_id": mid,
            "sender_id": msg["sender_id"],
            "content": msg["content"],
            "timestamp": msg["timestamp"].isoformat()
        }
        for mid, msg in fake_db["messages"].items()
        if msg["receiver_id"] == agent_id or msg["sender_id"] == agent_id
    ]
    return {"agent_id": agent_id, "messages": messages}

# 5. Назначение задач
@app.post("/tasks", response_model=TaskResponse, summary="Создание новой задачи")
async def create_task(task: TaskCreate, current_user: dict = Depends(get_current_user)):
    """Создает новую задачу и назначает её агенту."""
    if task.assigned_agent_id not in fake_db["agents"]:
        raise HTTPException(status_code=404, detail="Agent not found")
    task_id = len(fake_db["tasks"]) + 1
    fake_db["tasks"][task_id] = {
        "priority": task.priority,
        "assigned_agent_id": task.assigned_agent_id,
        "deadline": task.deadline,
        "status": task.status
    }
    return {"task_id": task_id, "message": "Task created successfully"}

@app.get("/tasks/{task_id}", response_model=TaskInfo, summary="Получение информации о задаче")
async def get_task(task_id: int, current_user: dict = Depends(get_current_user)):
    """Возвращает информацию о задаче по её ID."""
    if task_id not in fake_db["tasks"]:
        raise HTTPException(status_code=404, detail="Task not found")
    task = fake_db["tasks"][task_id]
    return {
        "task_id": task_id,
        "priority": task["priority"],
        "assigned_agent_id": task["assigned_agent_id"],
        "deadline": task["deadline"],
        "status": task["status"]
    }

# 6. Координация агентов
@app.post("/coordination", response_model=CoordinationResponse, summary="Инициирование координации агентов")
async def coordinate_agents(coord: CoordinationRequest, current_user: dict = Depends(get_current_user)):
    """Инициирует координацию между указанными агентами."""
    for agent_id in coord.agents:
        if agent_id not in fake_db["agents"]:
            raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
    coordination_id = len(fake_db.get("coordinations", {})) + 1
    # Логика координации (заглушка)
    return {"coordination_id": coordination_id, "message": "Coordination initiated"}

# 7. Конфигурирование агентов
@app.put("/agents/{agent_id}/config", response_model=AgentResponse, summary="Обновление конфигурации агента")
async def update_config(agent_id: int, config: ConfigurationUpdate, current_user: dict = Depends(get_current_user)):
    """Обновляет конфигурацию указанного агента."""
    if agent_id not in fake_db["agents"]:
        raise HTTPException(status_code=404, detail="Agent not found")
    fake_db["agents"][agent_id]["configuration"] = config.configuration
    return {"agent_id": agent_id, "message": "Configuration updated"}

# 8. Интеграция внешних систем
@app.post("/integrations", response_model=IntegrationResponse, summary="Добавление новой интеграции")
async def add_integration(integration: IntegrationCreate, current_user: dict = Depends(get_current_user)):
    """Добавляет новую интеграцию с внешней системой."""
    integration_id = len(fake_db["integrations"]) + 1
    fake_db["integrations"][integration_id] = {
        "system_name": integration.system_name,
        "api_url": integration.api_url,
        "auth_details": integration.auth_details
    }
    return {"integration_id": integration_id, "message": "Integration added"}

@app.get("/integrations", response_model=List[IntegrationInfo], summary="Получение списка интеграций")
async def get_integrations(current_user: dict = Depends(get_current_user)):
    """Возвращает список всех интеграций."""
    return [
        {"integration_id": iid, "system_name": i["system_name"], "api_url": i["api_url"]}
        for iid, i in fake_db["integrations"].items()
    ]

# 9. Аутентификация и авторизация
@app.post("/auth/login", summary="Аутентификация пользователя")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Аутентифицирует пользователя и возвращает JWT-токен."""
    user = fake_db["users"].get(form_data.username)
    if not user or user["password"] != form_data.password:  # В реальном проекте используйте хэширование
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserInfo, summary="Получение информации о текущем пользователе")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Возвращает информацию о текущем аутентифицированном пользователе."""
    return {
        "user_id": fake_db["users"][current_user["username"]]["user_id"],
        "username": current_user["username"],
        "role": current_user["role"]
    }

# 10. Управление пользователями и ролями
@app.post("/users", response_model=UserResponse, summary="Создание нового пользователя")
async def create_user(user: UserCreate, current_user: dict = Depends(get_current_user)):
    """Создает нового пользователя (доступно только администраторам)."""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    if user.username in fake_db["users"]:
        raise HTTPException(status_code=409, detail="Username already exists")
    user_id = len(fake_db["users"]) + 1
    fake_db["users"][user.username] = {
        "user_id": user_id,
        "password": user.password,  # В реальном проекте хэшируйте пароль
        "role": "user" if user.role_id == 1 else "admin"
    }
    return {"user_id": user_id, "message": "User created"}

@app.put("/users/{user_id}", response_model=UserResponse, summary="Обновление информации о пользователе")
async def update_user(user_id: int, user: UserCreate, current_user: dict = Depends(get_current_user)):
    """Обновляет информацию о пользователе (доступно только администраторам)."""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    for username, data in fake_db["users"].items():
        if data["user_id"] == user_id:
            fake_db["users"][username] = {
                "user_id": user_id,
                "password": user.password,
                "role": "user" if user.role_id == 1 else "admin"
            }
            return {"user_id": user_id, "message": "User updated"}
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/roles", response_model=List[Role], summary="Получение списка ролей")
async def get_roles(current_user: dict = Depends(get_current_user)):
    """Возвращает список доступных ролей."""
    return [
        {"role_id": 1, "role_name": "user"},
        {"role_id": 2, "role_name": "admin"}
    ]

# 11. Логирование и мониторинг системы
@app.get("/logs", response_model=List[LogEntry], summary="Получение системных логов")
async def get_logs(current_user: dict = Depends(get_current_user)):
    """Возвращает системные логи (с фильтрацией по дате и уровню в реальном проекте)."""
    # Пример логов (в реальном проекте из ELK или базы)
    logs = [
        {"timestamp": datetime.utcnow(), "level": "INFO", "message": "Agent started"},
        {"timestamp": datetime.utcnow(), "level": "ERROR", "message": "Task failed"}
    ]
    return logs

@app.get("/metrics", response_model=SystemMetrics, summary="Получение системных метрик")
async def get_system_metrics(current_user: dict = Depends(get_current_user)):
    """Возвращает метрики производительности системы."""
    # Пример метрик (в реальном проекте из Prometheus)
    return {
        "cpu_usage": 45.5,
        "memory_usage": 2048.0,
        "active_agents": len(fake_db["agents"])
    }

# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)