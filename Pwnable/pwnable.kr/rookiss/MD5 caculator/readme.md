---
layout : post
title : MD5 Caculator
--- 

# Mở đầu 

Bài hôm nay điểm cao hơn bài trước vậy mà mình thấy lại có vẻ dễ hơn. Bài này kiến thức yêu cầu chỉ là đọc hiểu C . Đồng thời cũng cần phải
hiểu về cách tràn vào địa chỉ trở về sao cho đúng và pass tham số vào hàm đó như thế nào. Sử dụng kĩ thuật ROP hiệu quả là được . Một khó khăn 
nữa trong bài này là phải vượt qua được canary , chỉ cần có một chút kiến thức basis về toán là có thể leak được canary rồi . 


# Phân tích binary 

Hàm main : 

![hinh1](/Pwnable/pwnable.kr/rookiss/MD5%20caculator/hinh1.PNG) 
