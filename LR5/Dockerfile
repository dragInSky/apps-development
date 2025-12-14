FROM python:3.13

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

RUN apt-get update \
    && apt-get install -y --no-install-recommends netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

COPY LR3/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY LR3 ./LR3
COPY LR6 ./LR6
COPY LR5/entrypoint.sh ./entrypoint.sh
RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
CMD ["uvicorn", "LR3.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
