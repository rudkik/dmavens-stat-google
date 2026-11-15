FROM python:3.12-slim
WORKDIR /app
COPY server.py index.html style.css ./
EXPOSE 8080
CMD ["python3", "-u", "server.py", "8080"]
