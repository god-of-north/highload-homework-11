FROM python:3.9.5-slim-buster

RUN mkdir -p /home/app
WORKDIR /home/app
COPY test.py ./
COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache -r requirements.txt

CMD ["python", "./test.py"]
