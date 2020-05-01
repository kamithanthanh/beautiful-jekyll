docker build -t <image_name> .
sudo docker run -d --rm --name <image_name>  -p <port>:<port> --cap-add=SYS_PTRACE <image_name>
