FROM ubuntu:16.04
RUN apt-get update -y && apt-get install -y software-properties-common libxslt1-dev libffi-dev libxml2-dev python3-dev python3-pip python3-lxml python3-cffi libcairo2 libpango1.0-0 libgdk-pixbuf2.0-0 shared-mime-info python3-tk
RUN add-apt-repository universe
RUN apt-get update -y && apt-get install -y python3 python3-pip r-base
RUN pip3 install flask flask-script flask-cors pandas weasyprint matplotlib cherrypy
RUN R -e "source('http://bioconductor.org/biocLite.R');biocLite(c('AnnotationDbi', 'impute', 'GO.db', 'preprocessCore'));install.packages('WGCNA', repos='http://cran.rstudio.com/')"
# install more packages:
RUN pip3 install flask-session
RUN pip3 install scipy
RUN pip3 install redis
RUN pip3 install rpy2==2.8.2
RUN apt-get install -y redis-server
RUN pip3 install requests
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
COPY . /app
WORKDIR /app
ENV FLASK_APP ./app/__init__.py
#CMD service redis-server start && flask run
CMD flask run
