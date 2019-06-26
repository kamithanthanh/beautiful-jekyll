---
layout : post 
title : Dubblesort 
subtitle : Pwnable.tw
---

# Mở đầu
Bài này là một bài khá hay . Mình đã củng cố thêm một số kiến thức mới khi làm bài này. Đúng như tên gọi bài này là một bài sắp xếp dãy số nhưng có lỗi khiến chúng ta có thể tràn.Điều mà mình học được là cách xác định chính xác hơn địa chỉ của libc.Đồng thời học được một trick nhỏ để vô hiệu hóa **scanf** . Cũng như phải làm thế nào trong lúc tuyệt vọng 😱😱😱 

# Phân tích binary  

**Hàm main**  

![hinh4](/Pwnable/pwnable.tw/dubblesort_/hinh4.PNG)  

Hàm này thực hiện các chức năng : 
 - Nhập tên  
 - In tên  
 - Nhập độ dài array  
 - Nhập từng phần tử của mảng  
 - Sắp xếp các phần tử rồi in ra dãy đã sắp xếp  

Do chương trình không check độ dài mảng nên ta có lỗi tràn . Ở đây ta có thể dễ dàng đưa payload vào sao cho sau khi sắp xếp , payload nằm đúng như vị trí ta mong muốn. 
Chương trình được bật full bảo vệ :  

![hinh5](/Pwnable/pwnable.tw/dubblesort_/hinh5.PNG)  

Chương trình có canary chống tràn như vậy ta cũng phải không được ghi đè lên canary đồng thời đảm bảo rằng canary nằm đúng nơi nó thuộc về. Mà payload của chúng ta phải nằm sau canary nên bắt buộc số phần tử của mảng phải vượt qua canary . Để tránh ghi đè lên canary trong lần nhập vào canary ta thực hiện nhập "-" thì chương trình sẽ tự động bỏ qua 💨 Bùm magic vãi chưởng.  
Công việc tiếp theo là chọn payload nào để có được shell 😀😀😀 Nếu dùng các gadget thì nó sẽ sắp xếp loạn lên sau khi **dubblesort** nên rất khó khả thi . Nên lựa chọn còn lại là dùng hàm ```system``` trong libc. Muốn thế thì chúng ta cần leak địa chỉ của libc  
👉 Lỗi tiếp theo là biến ```buf``` lưu tên không được zero out nên ta có thể leak các giá trị trong stack .  

![hinh1](/Pwnable/pwnable.tw/dubblesort_/hinh1.PNG)  

Trong hình là minh họa hình ảnh mình thử nghiệm cho chương trình với len array là 3 , name là hiep . Có một vấn đề nho nhỏ ở đây là do PIE bật nên ta không biết địa chỉ của các hàm gây khó khăn trong việc DEBUG. 😬 Một phương án khả thi trong trường hợp này là đặt break point bằng cách ```b * puts``` hoặc ``` b * main + 100``` .Quay trở lại bài, ta thấy trong mảng ```buf``` chứa name phía sau có một địa chỉ rất đặc biệt ```0xf7fb7000``` .  
Trong GDB xem vùng nhớ bằng vmmap :  

![hinh2](/Pwnable/pwnable.tw/dubblesort_/hinh2.PNG)  

Ta thấy đó chính là địa chỉ của một phần của libc được nạp vào trong binary . Nhưng đó vẫn chưa phải là địa chỉ chính xác của libc đâu 😛😛😛. Nó là địa chỉ got.plt các hàm trong libc. Lại tìm địa chỉ của got.plt trong libc  :  

![hinh3](/Pwnable/pwnable.tw/dubblesort_/hinh3.PNG)  

Trừ đi offset đó là ta có địa chỉ trong libc. Giờ ta có thể tính toán địa chỉ của hàm ```system``` và chuỗi ```/bin/sh``` trong libc và thu được shell rồi :))) 

# Kết  
Khi tuyệt vọng và không có hướng để đi thì nên bình tâm lại , nhìn ngắm bầu trời xanh và xem lại code cẩn thận từ đầu :)) Có lẽ sẽ có cái mà ta đã bỏ qua . 
