FROM python:3.8.3
LABEL maintainer="https://github.com/ryarasi"
# ENV MICRO_SERVICE=/app
# RUN addgroup -S $APP_USER && adduser -S $APP_USER -G $APP_USER
# set work directory


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
# create root directory for our project in the container
RUN mkdir /shuddhi
# COPY ./scripts /scripts
WORKDIR /shuddhi

# Copy the current directory contents into the container at /shuddhi
ADD . /shuddhi/
# Install any needed packages specified in requirements.txt

# This is to create the collectstatic folder for whitenoise
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /requirements.txt && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media

# ENV PATH="/scripts:$PATH"
# CMD ["run.sh"]

CMD python manage.py collectstatic --noinput && python manage.py migrate && gunicorn shuddhi.wsgi:application --timeout 90 --keep-alive 5 --bind 0.0.0.0:$PORT

# uwsgi --socket :9000 --workers 4 --master --enable-threads --module shuddhi.wsgi


