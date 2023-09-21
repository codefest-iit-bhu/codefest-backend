FROM python:3.7-slim
LABEL maintainer="shukapurv"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./scripts /scripts
COPY . /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN apt-get update && \
    apt-get install -y gcc git && \
    # apt-get install -y default-libmysqlclient-dev && \
    # rm -rf /var/lib/apt/lists/* && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chown -R django-user:django-user /app && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts && \
    chmod -R 777 /app

ENV PATH="/scripts:$PATH"

USER django-user

CMD ["run.sh"]