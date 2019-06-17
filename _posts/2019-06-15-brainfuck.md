---
layout : post 
title : BrainFuckkkkkkkk
subtitle : Rookiss Pwnable.kr
image : /Pwnable/pwnable.kr/rookiss/brainfuck/brain%20fuck.png
--- 

# Mở đầu
Khá là tiếc khi mình không làm được bài này. Nguyên nhân chủ yếu là minning chưa đủ , tư duy về khai thác lỗ hổng còn kém, chưa có cái nhìn tổng quát hơn mà chỉ nhìn một phía dẫn tới bó tay bó chân. Cần luyện tập nhiều thì mới lên trình được. Về kiến thức cần thiết thì bài này chỉ sử dụng các hàm cơ bản nên không yêu cầu kiến thức cao siêu, như mình nói ở trên thì chỉ cần cái đầu là ok :v 

# Phân tích binary 

Lúc đầu mình đi vào ngõ cụt là do chỉ chú tâm vào hàm **do_brainfuck**

![hinh1](/Pwnable/pwnable.kr/rookiss/brainfuck/hinh1.PNG) 

Hàm này xử lí giá trị input đầu vào và cho phép chúng ta thực hiện các chức năng như thay đổi các giá trị của biến **tape** .Lỗi mà 
chúng ta có thể exploit ở đây là chúng ta có thể sửa các giá trị đằng trước biến **tape** luôn . Lúc đầu hướng của mình là thay đổi giá trị của **p** thành địa chỉ trở về của hàm nào đó, cơ mà điều đó là bất khả thì vì chúng ta chỉ có thể thay đổi từng char một lúc, và khi thay đổi giá trị **p** cũng là lúc ta không thể can thiệp vào nó nữa. 
Max Input là 1024 cho nên chúng ta chỉ có thể thay đổi p trong khoảng 1024 giá trị xung quanh **tape** .
Trong lúc vô tình nhìn lên thì mình nhận ra là phía trên **p** chính là địa chỉ của GOT table .

![hinh2](/Pwnable/pwnable.kr/rookiss/brainfuck/hinh2.PNG)

![hinh3]( /Pwnable/pwnable.kr/rookiss/brainfuck/hinh3.PNG)

😀😀😀 Haha thế là có khả năng dễ dàng thay đổi GOT thành hàm tùy ý . Cái này phải tự tìm ra thì mới biết được tìm được nó là lucky như nào 😬😬😬 Chứ cứ tương luôn writeup thì lại tưởng dễ xong sau ra lại đéo làm được haha 😂😂😂 Mình hồi xưa hay đọc writeup phết cơ mà do không luyện nhiều nên kiến thức nó cứ trôi đi thế là trình mãi không lên được  😁  😁  😁 

Mình đi loanh quanh một hồi tận dụng các hàm trong **do_brainfuck** mà vẫn đi vào ngõ cụt. Trong đầu hình dung ra một triệu khả năng tấn công nhưng mọi thứ đi vào tuyệt vọng  😣😣😣 Hihi lại mở witeup ra đọc :)) và nhận ra nó dùng cái hàm mà mình không mấy chú ý : 


![hinh4](/Pwnable/pwnable.kr/rookiss/brainfuck/hinh4.PNG)  


- Ý tưởng là : Thay đổi putchar -> start , memset -> gets , fgets -> system . 

Tham khảo code của mình ở [đây](https://github.com/hacmao/hacmao.github.io/tree/master/Pwnable/pwnable.kr/rookiss/brainfuck)

# Kết 

Đúng là chuột dâng tận miệng rồi mà không ăn được. Cơ mà cũng cảm thấy trình mình đang tăng 👍 👍 👍  Mọi thứ vẫn là OK . 
   

![ket](https://ichef.bbci.co.uk/news/660/cpsprodpb/17D39/production/_96439579_whatsubject.jpg)
