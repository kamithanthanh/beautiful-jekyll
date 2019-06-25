---
layout : post 
title : 3x17 
subtitle : Pwnable.tw
--- 

# Mở đầu
Bài này đỉnh cao của minning cmnr :)) Bài ở pwnable.tw quả thật nhiều não vc 😵😵😵 Mình hoàn toàn chỉ là đọc lại wu và note lại đây để hiểu 
rõ cũng như khắc sâu lại cách tư duy của người ta thôi . Bài sử dụng hai technique chính là tạo một vòng lặp vô hạn và control EBP . 

# Phân tích binary  

**Hàm main**  

![hinh1](/Pwnable/pwnable.tw/3x17_/hinh1.PNG)  

Hàm main có hai chức năng chính đó là chúng ta có thể chọn một địa chỉ rồi ghi bất kì dữ liệu nào lên đó. Trong các trường hợp khác thì mình 
đã nghĩ đến cách ghi đè lên GOT của một hàm nào đó rồi đấy nhưng bằng một cách magic nào đó mà bằng GDB không thể disassemble được hàm nào cả 
😱😱😱 Như vậy là chả biết địa chỉ GOT của hàm nào luôn .  
Chúng ta được quyền ghi ```0x18``` bytes lên bất kì vùng nhớ nào. Địa chỉ trở về chúng ta cũng không thể leak được vì không có hàm in ra giá
trị. Chỉ còn một phương án có thể khả thi đó là 👉 Ghi đè lên fini.  

**Hàm call_fini**  
![hinh2](/Pwnable/pwnable.tw/3x17_/hinh2.PNG)  

Trong chương trình khi kết thúc luôn có một hàm fini như vậy để hoàn tất các thủ tục còn lại và thoát chương trình. Tuy nhiên không phải chương 
trình nào cũng có hàm call_fini phong phú như chương trình này. Vì bài này được thiết kế để ghi đè lên fini nên nó mới đặc biệt như vậy . Hàm 
```call_fini``` thực hiện call hai hàm có địa chỉ được lưu trong ```fini_array```.  
![hinh3](/Pwnable/pwnable.tw/3x17_/hinh3.PNG)
