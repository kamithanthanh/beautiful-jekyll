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

![](/ctf/insomnihack/kaboom/hinh3.PNG)   

Những vùng màu đỏ là sự khác nhau của hai chương trình. Điểm cần chú ý là vùng màu đỏ khác nhau đầu tiên. Đoạn này xử lí dữ liệu liên quan tới flag.   

![](/ctf/insomnihack/kaboom/hinh4.PNG)   

**byte_46D1A7** là đoạn mã hóa của flag fake. Trong khi **byte_46F160** là đoạn mã hóa của flag thật. Trong một điều kiện xác định nếu như đoạn mã này(vùng được khoanh) được thực hiện thì chương trình tiến hành ghi đè flag thật lên flag ảo.   
tại đây mình viết script [getData](https://www.notion.so/Get-Data-7f980b816256425984d20e2cf0cdd3b8) và [setData](https://www.notion.so/Set-Data-6f445e8b365444619df544fb48b6cf5e) để đổi chỗ thủ công flag thật thay cho flag giả. Sau đó tiến hành unpack thủ công (vì unpack bằng tool không được) bằng x64dbg.   
Chạy lại chương trình trong IDA thì ta thu được flag:    

![](/ctf/insomnihack/kaboom/hinh1.PNG)   


