FROM python:3.10-slim
WORKDIR /app
EXPOSE 8501
COPY . .
RUN pip install --no-cache-dir -r requirements.txt && chmod +x ./start.sh
CMD [ "sh", "-c", "./start.sh" ]
