From alpine:3.7
LABEL maintainer="LucyB"

# Application folder
ENV APP_DIR /app

# Install dependencies
RUN apk add --update --no-cache python3-dev supervisor g++ && \
    ln -s /usr/include/locale.h /usr/include/xlocale.h && \
    pip3 install --upgrade pip && \
    pip3 install gunicorn && \
    # Work around for bug in current version of numpy
    pip3 install numpy==1.14.0 && \
    mkdir -p ${APP_DIR}/web && \
    mkdir -p ${APP_DIR}/conf && \
    mkdir -p ${APP_DIR}/logs && \
    rm -rf /var/cache/apk/*

# copy app files
COPY ./app ${APP_DIR}

# Setup flask/Dash application
RUN pip3 --no-cache-dir install -r ${APP_DIR}/requirements.txt && \
    echo "files = ${APP_DIR}/conf/*.ini" >> /etc/supervisord.conf

EXPOSE 5000

CMD ["supervisord", "-c", "/etc/supervisord.conf"]
