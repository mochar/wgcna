FROM ubuntu:16.04

# Install some packages
RUN apt-get update -y && apt-get install -y python3-pip apt-transport-https

# Install R 3.5 and WGCNA
RUN echo "deb https://cloud.r-project.org/bin/linux/ubuntu xenial-cran35/" >> /etc/apt/sources.list
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys E084DAB9
RUN apt-get update -y && apt-get install -y r-base 
RUN R -e "install.packages(c('BiocManager'), repos='https://cloud.r-project.org/');BiocManager::install('WGCNA')"

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENV FLASK_APP ./app/__init__.py
CMD flask run
