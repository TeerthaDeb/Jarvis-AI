
# CUDA-enabled development image
FROM nvidia/cuda:12.1.1-devel-ubuntu22.04 AS builder


RUN apt-get update && apt-get install -y --no-install-recommends python3.9 python3-pip && rm -rf /var/lib/apt/lists/*
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

WORKDIR /app


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt



FROM python:3.9-slim-buster

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

COPY . .

EXPOSE 5000

CMD ["python", "app.py"] 