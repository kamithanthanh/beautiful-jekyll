---
layout : post
title : Insomnihack CTF 
---

# Mở đầu   
Kì thi này được tổ chức gần tết, anh em trong team đã cùng nhau chiến đầu giải xuyên màn đêm. Nói chung là cũng khá là vui khi mọi người ngồi lại với nhau và cùng làm một điều gì đó.   
> Tương lai đang ở phía trước và việc của chúng ta là tiếp tục bước đi.   

Trong kì thi mình chẳng làm được bài nào 🥴 what's a shame. Giờ thì đi review writeup để bổ túc lại kiến thức thôi. 

# List   
   - [**[Reverse] Kaboom**](#wu1)

<a name="wu1"></a> 
# Kaboom    

[Đây](https://github.com/hacmao/hacmao.github.io/raw/master/ctf/insomnihack/kaboom/kaboom-orig.bin) là một file PE32 được pack bằng UPX. Nếu giải nén bằng một phần mềm UPX chuyên dụng thì sẽ thu được đoạn binary có hàm main như sau :   

![](/ctf/insomnihack/kaboom/hinh2.PNG)   

Trong khoảng thời gian đầu tiên, và một khoảng thời gian rất dài sau đó 🙄 mình chỉ tập trung reverse hàm này.Các hàm khác đều là các hàm khá cơ bản của C và có thể đoán dựa trên chức năng của nó. Chỉ có hàm **str_cmp_obfucate** là hơi khác một chút. Nó vẫn là hàm strcmp trông thường tuy nhiên được viết theo cách rất chi là phức tạp 😥 Nhưng nói chung sau khi đọc qua hàm này cũng có thêm được kinh nghiệm khi đối đầu với những bài bị obfucate.Mặc dù hàm này chỉ là một mục tiêu để đánh lừa chúng ta mà thôi.   

Sau đó là quãng thời gian tuyệt vọng vì không có hướng giải khi đã dịch ngược toàn bộ chương trình sau khi unpack và vẫn không thu được gì. Nhưng cuối cùng team(Một bạn trong team) đã tìm ra hướng và giải trọn vẹn được bài này. Đó là trong quá trình unpack UPX, người ta đã inject một đoạn code mới nhằm sửa đổi flag. Mình thì cứ nghĩ là người ta sửa bằng IDA hay một công cụ nào đó 🤣   
Tiếp đến là tìm sự khác biệt giữa hai chương trình UPX này bằng công cụ [Diaphora](https://www.notion.so/Diaphora-8f8d0c45259f4c69b70c6bb22d39c03d)    


