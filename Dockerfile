FROM python:3.9

RUN apt install git

WORKDIR .

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . ./

EXPOSE 8008

ENTRYPOINT ["python3", "webserver.py"]