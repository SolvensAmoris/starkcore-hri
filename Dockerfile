FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir magika
WORKDIR /app
COPY ca002-check.sh /usr/local/bin/ca002-check
RUN chmod +x /usr/local/bin/ca002-check
ENTRYPOINT ["ca002-check"]
