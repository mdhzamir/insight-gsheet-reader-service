FROM python:3.7.1

WORKDIR /app
COPY . /app
EXPOSE 5001

ENTRYPOINT  ["python3"]
CMD ["app.py"]
