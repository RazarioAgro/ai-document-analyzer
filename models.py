from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base
import uuid

class DocumentTask(Base):
    # Указываем реальное имя таблицы в PostgreSQL
    __tablename__ = "document_tasks"

    # Описываем колонки:
    # primary_key=True - уникальный идентификатор строки
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Название документа (строка)
    title = Column(String, nullable=False)
    
    # Текст документа (Text позволяет хранить большие объемы в отличие от String)
    content = Column(Text, nullable=False)
    
    # Статус обработки
    status = Column(String, default="processing")
    
    # Результат анализа (может быть пустым, пока задача не выполнена)
    result = Column(Text, nullable=True)
    
    # Время создания записи. func.now() заставит саму БД подставить текущее время
    created_at = Column(DateTime(timezone=True), server_default=func.now())



