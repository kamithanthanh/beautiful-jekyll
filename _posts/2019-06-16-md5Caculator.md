---
layout : post
title : MD5 Caculator Pwnable.kr
image : /Pwnable/pwnable.kr/rookiss/MD5%20caculator/md5%20calculator.png
bigimg : /img/meorenga.jpg
--- 

# Mở đầu
Bài hôm nay điểm cao hơn bài trước vậy mà mình thấy lại có vẻ dễ hơn. Bài này kiến thức yêu cầu chỉ là đọc hiểu C . Đồng thời cũng cần phải hiểu về cách tràn vào địa chỉ trở về sao cho đúng và pass tham số vào hàm đó như thế nào. Sử dụng kĩ thuật ROP hiệu quả là được . Một khó khăn nữa trong bài này là phải vượt qua được canary , chỉ cần có một chút kiến thức basis về toán là có thể leak được canary rồi . 

# Phân tích binary 

Hàm main : 

![hinh1](/Pwnable/pwnable.kr/rookiss/MD5%20caculator/hinh1.PNG) 

Hàm main khá sạch sẽ và dễ đọc, nó bao gồm hai hàm cơ bản  : 

- hàm **my_hash** :   
Hàm này trả về giá trị là một chuỗi các biểu thức được tạo ra bằng hàm ```rand()``` cộng với canary .😐😐😐 Thế chẳng phải chúng ta có thể leak canary nếu biết các giá trị còn lại sao ??? 

![hinh2](/Pwnable/pwnable.kr/rookiss/MD5%20caculator/hinh2.PNG) 

- hàm **process_hash** :   
Kinh nghiệm của mình là cái gì khó hiểu quá thì đừng có cố tìm hiểu 😀😀😀 Như con gái chẳng hạn , ta không thể hiểu hết được đâu. Cho nên một mẹo là cứ nhìn tên hàm rồi đoán chức năng. Kết hợp với GDB nữa để hiểu rõ hàm của nó làm gì.  

![hinh3](/Pwnable/pwnable.kr/rookiss/MD5%20caculator/hinh3.PNG) 

Đầu tiên chúng ta nhập 1024 kí tự vào ```g_buf``` được đặt ở bss. Sẽ không có tràn ở đây. Tiếp đó nó sẽ decode base64 biến g_buf rồi lưu vào biến s , trả về độ dài của s . Chúng ta có thể thấy biến s có độ dài max là 0x200 mà max của b64decode của ```g_buf``` lại là 0x300 . Ta có lỗi overflow ở đây . Từ đó có thể dễ dàng thực hiện các kĩ thuật tràn cơ bản để có được shell khi đã có đủ nguyên liệu cần thiêt. 

Các bạn có thể tham khảo thêm code của mình ở [đây](https://github.com/hacmao/hacmao.github.io/tree/master/Pwnable/pwnable.kr/rookiss/MD5%20caculator)

# Kết  
Bài này mình thấy ez hơn bài brainfuckk :)) mặc dù lại nhiều điểm hơn. Cơ mà là tự làm nên vui vl :)) 

