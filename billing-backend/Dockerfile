FROM python:3.9
LABEL maintainer twtrubiks
ENV PYTHONUNBUFFERED 1
RUN mkdir /docker_api
WORKDIR /docker_api
COPY . /docker_api/
RUN pip install -r requirements.txt
RUN apt-get update & apt-get install apt-transport-https & apt-get -y install vim

# for entry point
RUN chmod +x /docker_api/docker-entrypoint.sh