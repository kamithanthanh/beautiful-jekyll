---
layout : post 
title : 3x17 
subtitle : Pwnable.tw
--- 

# Mở đầu
Bài này đỉnh cao của minning cmnr :)) Bài ở pwnable.tw quả thật nhiều não vc 😵😵😵 Mình hoàn toàn chỉ là đọc lại wu và note lại đây để hiểu  rõ cũng như khắc sâu lại cách tư duy của người ta thôi . Bài sử dụng hai technique chính là tạo một vòng lặp vô hạn và control EBP . 

# Phân tích binary  

**Hàm main**  

![hinh1](/Pwnable/pwnable.tw/3x17_/hinh1.PNG)  

Hàm main có hai chức năng chính đó là chúng ta có thể chọn một địa chỉ rồi ghi bất kì dữ liệu nào lên đó. Trong các trường hợp khác thì mình  đã nghĩ đến cách ghi đè lên GOT của một hàm nào đó rồi đấy nhưng bằng một cách magic nào đó mà bằng GDB không thể disassemble được hàm nào cả 😱😱😱 Như vậy là chả biết địa chỉ GOT của hàm nào luôn .  
Chúng ta được quyền ghi ```0x18``` bytes lên bất kì vùng nhớ nào. Địa chỉ trở về chúng ta cũng không thể leak được vì không có hàm in ra giá trị. Chỉ còn một phương án có thể khả thi đó là 👉 Ghi đè lên fini.  

**Hàm call_fini**  

![hinh2](/Pwnable/pwnable.tw/3x17_/hinh2.PNG)  

Trong chương trình khi kết thúc luôn có một hàm fini như vậy để hoàn tất các thủ tục còn lại và thoát chương trình. Tuy nhiên không phải chương trình nào cũng có hàm call_fini phong phú như chương trình này. Vì bài này được thiết kế để ghi đè lên fini nên nó mới đặc biệt như vậy . Hàm ```call_fini``` thực hiện call hai hàm có địa chỉ được lưu trong ```fini_array```.  


![hinh3](/Pwnable/pwnable.tw/3x17_/hinh3.PNG)

🍀 Mission 1 : tạo vòng lặp vô hạn để ghi payload  
```
  Func1 : main  
  Func2 : call_fini
```

Sau khi hàm main kết thúc thì chương trình sẽ gọi tới ```call_fini```. Tại đây thì sẽ thực hiện lần lượt ```Func1 -> Func2``` . Tức là lại gọi hàm main lần nữa. Sau đó lại gọi call_fini và cứ như vậy ta có vòng lặp vô hạn  
 
🍀 Mission 2 : ghi payload  
Có một cái rất hay là hàm main sẽ chỉ thực hiện nhận input khi ```byte_4B9330 == 1``` . Bytes này có kiểu là ```int_8``` cho nên rất dễ bị tràn. Tức là cứ 256 lần ta mới thực hiện input 1 lần. Trong lần input này ta sẽ thực hiện ghi các ROP để lấy được ```sys_execve```. Nhưng ghi payload ở đâu và sau này sẽ chạy thế nào là điều mà ta cần phải quan tâm 👊👊👊 Ghi payload sẽ là ngay sau fini_array . Còn tại sao lại thể thì 👇👇👇 hồi sau sẽ rõ.

🍀 Mission 3 : Run payload  
Chúng ta sẽ tiến hành run payload bằng cách control EBP . Sau khi thực hiện ghi xong payload thì ta tiến hành ghi đè lên Func2 
```
  Func2 = Leave_gadget
```
Khi gọi tới leave_gadget , thay vì tạo một hàm mới thì nó sẽ làm thay đổi RSP thành ``` 0x4b40f8 ``` là địa chỉ Func1 của Fini_array . Cũng tức là stack bị chuyển xuống vùng này và nó sẽ thực hiện lần lượt hàm main rồi tới các payload của chúng ta đã ghi được ở phần trước. Đây là cách duy nhất chúng ta có thể run các payload được vì không có lỗi tràn nên rất khó để kiểm soát các register.  

# Kết  
Chỉ là đọc Wu thôi mà đã thấy cần nhiều não rồi , nhưng thế chẳng phải rất thú vị sao 😀😀😀 Mình thích mấy bài nặng tư duy như này , nó là cho đầu óc được thoải mái, phát triển . 
