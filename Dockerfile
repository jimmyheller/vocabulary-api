FROM python:3.8.6-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY /src/requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY /src/ /usr/src/app/

# migrate models
CMD [ "python", "manage.py", "migrate" ]

# initial prepared words
CMD ["python", "manage.py", "loaddata", "fixtures.json"]

# run project
CMD [ "python", "manage.py" , "runserver", "0.0.0.0:8000" ]