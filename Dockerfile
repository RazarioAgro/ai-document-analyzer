# Берем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл с библиотеками и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=100 --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Копируем весь наш код в контейнер
COPY . .

# Команда для запуска нашего сервера
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]