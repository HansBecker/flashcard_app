FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends build-essential python3.9 python3-pip python3-setuptools python3-dev libpq-dev

WORKDIR /app

ENV PORT 8000
EXPOSE 8000

COPY requirements.txt /app/requirements.txt

# install python dependencies
RUN pip3 install -r requirements.txt

COPY . /app

# add the CMD stuff
CMD ["python", "manage.py", "runserver"]
