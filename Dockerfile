FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip --no-cache-dir \
 && pip install --index-url https://download.pytorch.org/whl/cpu \
    torch==2.1.0 torchvision==0.16.0 --no-cache-dir

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
 && pip install -r requirements_docker.txt --no-cache-dir

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "src/web.py", "--server.address=0.0.0.0", "--server.port=8501"]
