FROM python:3.9 AS builder
RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --prefix=/install -r /requirements.txt

FROM python:3.9-slim
COPY --from=builder /install /usr/local
WORKDIR /app
COPY . .
EXPOSE 8800:8800
CMD [ "python", "./app.py"]
