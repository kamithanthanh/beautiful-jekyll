---
layout : post 
title : Trainning 
subtitle : SVATTT 2019 
--- 

# Mở đầu 
Kì thi sắp tới và trong đầu mình kiểu wtf 😁😁😁 Không biết mọi chuyện sẽ đi tới đâu :v Từ đợt matesctf 2018 cho tới isitdtu team mình đều chỉ 
còn 1 chút nữa là có thể lọt vô final 😭😭😭 That's a sad story. Vì vậy để tránh lặp lại những thất bại đầy tiếc nuối đó mình sẽ lập lịch 
trainning ngay từ bây giờ. Mục tiêu là mỗi ngày chơi ít nhất 2 bài CTF mọi thể loại :v Mình sẽ note lại nhanh các bài mình làm + những cái new 
mà mình nhận được trong các bài 😁😁😁 

# Ngày 1  
Do nay ngày đầu tiên nên là chỉ có 1 bi thôi :v  
[SvATTT 2018 PyLock](https://drive.google.com/open?id=1CDyi4Ayisgt3hYqwiT4FZlYMEJHErSRx) đây được cho là 1 file exe. Tên bài cho ta gợi ý là đây là 1 file python được convert thành file exe. Việc đầu tiên cần làm là đưa được ngược trở lại thành file python .  
Dùng tool [python-exe-unpacker](https://github.com/countercept/python-exe-unpacker) để convert. Làm theo các bước sau : 
```
python python-exe-unpacker.py -i unlock.exe
python python-exe-unpacker.py -p unlock 
```
Đọc kĩ doc của tool để hiểu tại sao lại có như vậy :v 
Sau đó được file unlock.py có import 1 thư việc PyLock. Trong cái đống được extract trên thì ta vào thư mục library của nó thì tìm được file PyLock.pyc. Dùng tool để convert ngược trở lại file py thì ta decode được hàm main . Từ đó dịch ngược lại là ta có được flag.   
Kết thúc ngày một, mọi thứ cứ gọi là ok :v  
![ngay1](/img/meo2.jpg)

# Ngày 2  
 - [PlaidCTF 2016 : quick](https://github.com/N4NU/Reversing-Challenges-List/blob/master/Medium_Easy/PlaidCTF_2016_quick/quick.7z)   

Bài này khá là ghê được viết bằng swift.Sử dụng skill chính là đọc code. Nói chung là vẫn khá mông lung vì mình tham khảo write up của [yeuchimse](https://ctf.yeuchimse.com/plaid-ctf-2016-quick-re175/) . Đọc rồi đối chiếu với code trong IDA thì ngẫm lại có vẻ cũng đúng. Sau bài này rút ra được 1 điều là đôi khi chúng ta cần đoán được code đó nó viết gì dựa vào mạch code rồi check lại . Chứ không đọc hết sẽ tốn rất nhiều thời gian.  
# Kết thúc  
Tu tiên đại đạo gian nan, mong một ngày có thể quát tháo tiên giới :v  

![hinh1](/Trainning/pham-nhan-tu-tien-vng-phap-bao-02.jpg)
