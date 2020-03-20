# docker build -t no_canary .
# docker run -d --name no_canary -p 9999:9999 -it no_canary 

FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install xinetd -y
RUN apt-get install netcat -y

RUN useradd -m nocanary

COPY ./nocanary.conf /etc/xinetd.d/nocanary
COPY ./flag.txt /home/nocanary/flag.txt
COPY ./no_canary /home/nocanary/no_canary
COPY ./run.sh /home/nocanary/run.sh
COPY ./init.sh /home/nocanary/init.sh

RUN chmod +x /home/nocanary/init.sh
RUN chmod +x /home/nocanary/run.sh

RUN chown -R root:nocanary /home/nocanary
RUN chmod -R 755 /home/nocanary
RUN chmod 640 /home/nocanary/flag.txt
RUN chown -R root:nocanary /home/nocanary/flag.txt

WORKDIR /home
#ENTRYPOINT  ["/home/nocanary/init.sh"]
EXPOSE 9999
