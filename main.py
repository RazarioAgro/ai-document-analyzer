import asyncio
import uuid 
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_async_session, async_session_maker
from models import DocumentTask

app = FastAPI(title='AI Document Analyzer API')

class DocumentRequest(BaseModel):
  title: str = Field(..., min_length=3, max_length=100)
  content: str = Field(..., min_length=10)

class TaskResponse(BaseModel):
  task_id: str
  status: str


@app.post("/analyze", response_model=TaskResponse)
async def analyze_document(
  doc: DocumentRequest,
  session: AsyncSession = Depends(get_async_session) # внедрение зависимости для получения сессии SQLAlchemy
  ):
  # Создаем объект строку для базы данных
  new_task = DocumentTask(title=doc.title, content=doc.content)
  # Добавляем в сессию и коммитим (сохраняем в БД)
  session.add(new_task)
  await session.commit()
  # Передаем ID задач в фоновый процесс
  asyncio.create_task(mock_background_worker(new_task.id, doc.content))
  return TaskResponse(task_id=new_task.id, status=new_task.status)

@app.get("/status/{task_id}")
async def get_task_status(task_id: str, session: AsyncSession = Depends(get_async_session)):
  # Делаем асинхронный SELECT-запрос к базе
  query = select(DocumentTask).where(DocumentTask.id == task_id)
  result = await session.execute(query)
  task = result.scalar_one_or_none() # получаем один объект или None, если не найден
  
  if not task:
    raise HTTPException(status_code=404, detail="Task not found")
  return {"task_id": task.id, "status": task.status, "result": task.result}


async def mock_background_worker(task_id: str, content: str):
  """ Фоновый воркер. 
  открываем новую сессию БД внутри воркера! """
  await asyncio.sleep(5)
  
  # Открываем независимую сессию через нашу фабрику
  async with async_session_marker() as worker_session:
    # ищем задачу по ID
    query = select(DocumentTask).where(DocumentTask.id == task_id)
    result = await worker_session.execute(query)
    task = result.scalar_one_or_none()
    
    if task:
      # Обновляем данные и коммитим изменения
      task.status = "completed"
      task.result = "Текст проанализирован. Успех!"
      await worker_session.commit()

@app.on_event("startup")
async def on_startup():
    from database import engine, Base
    async with engine.begin() as conn:
        # Эта команда создает таблицы по нашим моделям
        await conn.run_sync(Base.metadata.create_all)
