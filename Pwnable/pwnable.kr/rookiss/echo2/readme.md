---
layout : post  
title : Echo22222 
subtitle : Rookiss Pwnable.kr  
image : /Pwnable/pwnable.kr/rookiss/echo2/echo2.png 
--- 

# Mở đầu
Phần tiếp theo của echo1 - Pwnable.kr . Cùng chung binary nhưng bài này nó sửa làm cho công cuộc cho shellcode của chúng ta khó khăn hơn . 
Nhưng ở đây mình sẽ không trình bày cách về shellcode mà mình trình bày một cách mình nghĩ ra 😀😀😀 Mặc dù nó hơi lởm vì không exploit trên
 server của người ta được cơ mà cách của mình nên vẫn tâm đắc hơn . 

# Phân tích binary  
Do khá là giống với bài trước nên mình cũng không trình bày nhiều .  
Có hai hàm mới mà chúng ta cần quan tâm :  
**Hàm Echo2**  
![hinh2](/Pwnable/pwnable.kr/rookiss/echo2/hinh2.PNG)  

**Hàm Echo3**  
![hinh3](/Pwnable/pwnable.kr/rookiss/echo2/hinh3.PNG)  

Trong hàm ```echo2``` có lỗi format rất rõ ràng. Nhắc đến format là chúng ta có thể đọc và ghi bất kì địa chỉ nào. Đến đây thì ý tưởng rõ ràng là 
ghi lên một địa chỉ nào đó rồi . 👻👻👻 Ý tưởng của mình là ghi lên địa chỉ GOT của hàm ```free``` thành địa chỉ của hàm ```system``` . Vì 
ở hàm ```echo3``` chúng ta được quyền nhập vào một chuỗi kí tự bất kì 👉👉👉 Chính là chuỗi ```/bin/sh\x00``` 🌟🌟🌟  
Ý tưởng là khá rõ ràng như trên , việc còn lại chỉ là tìm cách leak địa chỉ libc rồi ghi đè lên GOT của ```free``` thôi. Cơ mà cũng lách cách
phết đấy, có cái sai mà mình không biết tại sao nó lại không chạy được mặc dù đã xem bằng debug rồi .  
Cuối cùng sau một time try hard nhiệt tình thì mình cũng thu được thành quả :  
![hinh1](/Pwnable/pwnable.kr/rookiss/echo2/hinh1.PNG)  

Vì không biết trên server nó dùng bản libc nào nên mình đành stop tại đây ✌️✌️✌️

# Kết  
Lại ngắm mèo tí cho đỡ buồn :))  
![hinh](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR4Q0dbeMISi2Mk2JRgoGzoF6m7wm3RQaA3TjqlOGdp17UOs65U)
