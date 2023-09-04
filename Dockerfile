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
    pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:$PATH"

USER django-user

CMD ["run.sh"]