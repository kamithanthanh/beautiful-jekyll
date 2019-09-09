---
layout : post 
title : Setup Enviroment 
subtitle : Debug heap binary  
--- 

Khi chơi mấy bài heap thì việc đau đầu là không có bản libc phù hợp vs bài để mà debug.Vì vậy nhờ một thanh niên nào đó đã tạo ra một docker dành riêng cho việc này. [**Docker**](https://github.com/skysider/pwndocker) này có thể setup bằng câu lệnh : 
```
docker run -d \
	--rm \
	-h ${ctf_name} \
	--name ${ctf_name} \
	-v $(pwd)/${ctf_name}:/ctf/work \
	-p 23946:23946 \
	--cap-add=SYS_PTRACE \
	skysider/pwndocker
```  
Có thể thay ```ctf_name``` bằng bất kì tên nào. Khi cần tạo một tên khác thì thay bằng tên đó thôi.  
Sau đó run bằng cách :  
```
sudo docker exec -it ${ctf_name} /bin/bash
```  
Lưu ý là cái port kia thì khi cài một cái khác thì cũng phải thay port. Mình chưa ngâm cứu ra cách tắt port nhưng chắc cũng ko khó.  
