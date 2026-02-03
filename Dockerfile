FROM python:3.10-slim
RUN apt-get update && apt-get install -y golang-go nodejs npm default-jdk g++ rustc curl && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY bug_rescue.py /usr/local/bin/bug-rescue
RUN chmod +x /usr/local/bin/bug-rescue
ENTRYPOINT ["python3", "/usr/local/bin/bug-rescue"]
