From alpine:3.7
LABEL maintainer="LucyB"

# Application folder
ENV APP_DIR /app

# Install dependencies
RUN apk add --update --no-cache python3-dev supervisor g++ postgresql-dev musl-dev && \
    ln -s /usr/include/locale.h /usr/include/xlocale.h && \
    pip3 install --upgrade pip && \
    pip3 install gunicorn && \
    # Work around for bug in current version of numpy
    pip3 install numpy==1.14.0 && \
    mkdir -p ${APP_DIR}/web && \
    mkdir -p ${APP_DIR}/conf && \
    mkdir -p ${APP_DIR}/logs && \
    rm -rf /var/cache/apk/*

# Install flask/Dash application dependancies
COPY ./app/requirements.txt ${APP_DIR}/
RUN pip3 --no-cache-dir install -r ${APP_DIR}/requirements.txt

# Copy config
COPY ./app/conf/supervisor_dash.ini /etc/supervisord.conf

# copy app files
COPY ./app ${APP_DIR}

EXPOSE 5000

CMD ["supervisord", "-c", "/etc/supervisord.conf"]
