docker build -t <image_name> .
sudo docker run -d --rm --name <docker_name> -v $(pwd):/ctf/work -p <port>:<port> --cap-add=SYS_PTRACE <image_name>
