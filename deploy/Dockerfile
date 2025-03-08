FROM python:3.14-rc-bookworm 

RUN apt-get update -y && apt install git -y

#Clone Repo
RUN git clone https://github.com/divteaching/ecs198f_inclass_poker.git

#Change Working Directory
WORKDIR /ecs198f_inclass_poker

#Install Requirements
RUN pip install -r requirements.txt

#Simulate Runnning maybe a Webserver (Long Running Process)
CMD ["tail", "-f", "/etc/os-release"]