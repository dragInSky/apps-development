FROM python:3.13

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

RUN apt-get update \
    && apt-get install -y --no-install-recommends netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

COPY LR8/requirements.txt ./requirements.txt
COPY LR3/requirements.txt ./LR3/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY LR3 ./LR3
COPY LR6 ./LR6
COPY LR8 ./LR8
COPY LR5/entrypoint.sh ./entrypoint.sh
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
