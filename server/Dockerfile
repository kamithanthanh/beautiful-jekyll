# docker build -t no_canary .
# docker run -d --name bin -p 9999:9999 -it bin 

FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install xinetd -y
RUN apt-get install netcat -y

RUN useradd -m ctf

COPY ./service.conf /etc/xinetd.d/service
COPY ./flag.txt /home/ctf/flag.txt
COPY ./bin /home/ctf/bin
COPY ./run.sh /home/ctf/run.sh
COPY ./init.sh /home/ctf/init.sh

RUN chmod +x /home/ctf/init.sh
RUN chmod +x /home/ctf/run.sh

RUN chown -R root:ctf /home/ctf
RUN chmod -R 755 /home/ctf
RUN chmod 640 /home/ctf/flag.txt

WORKDIR /home
ENTRYPOINT  ["/home/ctf/init.sh"]
EXPOSE 9999
