# легковесный образ Python
FROM python:3.11-alpine

# рабочая директорию
WORKDIR /.

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

COPY . .

# пользователь без привилегий
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# переменные окружения
ENV FLASK_APP=src.web
ENV FLASK_RUN_HOST=0.0.0.0

# миграции, заполнение и запуск приложения
CMD ["sh", "-c", "python -m src.core.utils && python -m src.core.faker_seed && flask run"]