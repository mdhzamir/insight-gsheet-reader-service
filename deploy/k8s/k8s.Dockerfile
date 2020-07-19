FROM python:3.7.1

WORKDIR /app
COPY . /app
RUN apt-get update
RUN pip install --upgrade pip
RUN pip --no-cache-dir install -r requirements.txt                                                                      
RUN pip install py_eureka_client
EXPOSE 5001

ENTRYPOINT  ["python3"]
CMD ["app.py"]
