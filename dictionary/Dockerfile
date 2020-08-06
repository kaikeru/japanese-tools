FROM python:slim

RUN mkdir /app
WORKDIR /app

# --- Install
COPY ./requirements.txt .
RUN pip install -r requirements.txt


COPY ./ .
RUN find /app/ -iname '*.py' | xargs pylint

CMD ["gunicorn", "-b", "0.0.0.0:8000", "--access-logfil", "-", "--error-logfile", "-", "server:api"]
