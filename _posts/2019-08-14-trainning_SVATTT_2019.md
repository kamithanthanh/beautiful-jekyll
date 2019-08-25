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
Skill khác là đôi khi phân tích 1 hàm không cần thiết đọc hết hàm. Căn cứ vào giá trị trả về và giá trị mà ta đang quan tâm đến thì ta đọc từ đó trở đi. Ví dụ ta cần quan tâm xem giá trị trả về là bao nhiêu thì đi ngược từ giá trị trở về lên. Hoặc ta xem giá trị tại con trỏ được truyền vào hàm có thay đổi không thì lần theo đó mà đi.  

# Ngày 3  
Nay chả làm được bài nào cả. Một phần do đi thi đường lối , một phần vì lười, phần vì bài khá khoai :(  
![ngay3](/img/meo4.jpg)  

# Ngày 4  
Nay chơi flare on pass được hai level đầu . Cảm thấy hiện tại nên chuyển hướng hoạt động cách mạng sang một hướng mới, không quan trọng về số lượng mà nên quan trọng chất lượng. Cái flare on này diễn ra trong tới 6 tuần, nên có thời gian để tìm hiểu ngâm cứu. Tiếp theo mình sẽ ngâm cứu về [android pentesting](https://github.com/tsug0d/AndroidMobilePentest101/tree/master/vietnamese) để pass level 3. 😉  
# Ngày 5  
Sau một hồi ngụp lặn trong jadx mà vẫn chẳng hiểu cái gì 😢😢😢 Quay lại cày cơ bản.   
  - [android pentesting](https://github.com/tsug0d/AndroidMobilePentest101/tree/master/vietnamese)  
    + chap 1 : set up enviroment. Mình thử tự xử bằng android studio nhưng méo biết dùng. Cài thử theo người ta v. Hmmm  😓😓😓 ở quê mạng chậm set up lâu vl.  

Somehow nghịch một hồi lại ra được flag nên stop cái turtorial nghiên cứu android pentest tại đây 😃😃😃 Do tem cũng có thằng nhận làm android rồi nên mình cũng ko ngâm cứu sâu.  

# Ngày 6  
Trở lại với pwn một chút.  
 - [MMA CTF 2nd 2016 : greeting-150](https://github.com/ctfs/write-ups-2016/tree/master/mma-ctf-2nd-2016/pwn/greeting-150)  
 Bài này dùng ghi đè lên fini . Không có realloc nên cũng dễ dàng thực hiện hơn.  
 - [[DEFCON CTF 2016] xkcd - Baby's First](https://github.com/smokeleeteveryday/CTF_WRITEUPS/tree/master/2016/DEFCONCTF/babysfirst/xkcd)  
 Bài này không tấn công chiếm quyền mà chỉ tận dụng lỗi tràn vào giá trị null của char để in ra flag thôi.  

# Ngày 7  
 - [SSCTF_2016_Quals_Re2](https://github.com/N4NU/Reversing-Challenges-List/tree/master/Medium_Easy/SSCTF_2016_Quals_Re2)  
 Nay ngồi nghịch lại bài này thì đã fix được đoạn anti disassembly, note lại một số trick đã dùng trong bài : 
   + jmp const : xor eax, eax; jmp .... ,jz + jnz to same addr , not fix into jmp   
   + jmp bỏ qua một đoạn code -> nop all code not execute 
   + nop tất cả đoạn code ko được thực thi.  
 Script nop : 
 ```python 
def n(start,length) : 
	for i in range(0, length) : 
		PatchByte(start+i, 0x90) 
	MakeCode(start) 
 ```  
 - [DEF CON CTF Quals 2017 - mute](https://fadec0d3.blogspot.com/2017/05/def-con-ctf-quals-2017-mute.html)  
 Bài này về side channel attack. Thấy side channel attack là gì trông lạ lạ nên mình đọc qua tí :v Xem ý tưởng thế nào chứ chưa viết cụ thể. Ý tưởng của bài này là người ta cho mình một đoạn shellcode chỉ được gọi một số syscall như đọc , mở nhưng ko có ghi. Idea là sẽ thực hiện mở file flag, đọc file rồi so sánh từng kí tự trong file flag. Nếu mà trùng thì end còn không trùng thì sẽ tạo một vòng lặp vô hạn, tức là thời gian sẽ dài hơn nhiều. Idea hay vc 👍👍👍 Cũng khá là dễ hiểu nhưng để vận dụng được lại rất là khó.  

# Ngày 8  
 - [SSCTF_2016_Quals_Re3](https://github.com/N4NU/Reversing-Challenges-List/blob/master/Medium_Easy/SSCTF_2016_Quals_Re3/Re3.7z)  
 Cả sáng ngồi reverse cái này. Vẫn còn vướng một số chỗ nó chưa có rõ ràng lắm nhưng cơ bản là hiểu được cách nó check flag. Có một cái technique hay dùng khi reverse nhưng binary lớn như này là Ctrl+x rồi flow theo những hàm quan trọng. Ở đây mình flow theo hàm MessageBoxA. Lúc đầu mình flow theo string ```PlsTryAgain``` thì ra được một đoạn code obfucate -> deobfucate cơ mà nó cũng chả liên quan tới chương trình của mình :v  
 - [Defcon 2015 Quals babyecho](https://github.com/ctfs/write-ups-2015/tree/master/defcon-qualifier-ctf-2015/babys-first/babyecho)  
 Bài này nó đặc biệt ở chỗ không có một hàm import nào mà nó kiểu là static linking. Mình phải xác định chức năng của các hàm. Nhưng cũng có thể dựa vào guessing technique 😄😄😄 để có thể tra ra một số hàm cơ bản. Sau đó chúng ta phải leak địa chỉ stack rồi ghi đè lên địa chỉ trở về của main bằng địa chỉ của shellcode bằng lỗi format string. 😤😤😤 Mọi thứ mượt mà đến phút cuối r mà mình tự tìm shellcode thì đéo chạy cho. Lấy shellcode trong wu của người ta ốp vào lại được. Magic vãi.  

# Ngày 9  
 - Nay chỉ chơi với babystack bên pwnable.tw nhưng vẫn chưa ra. Cảm giác đầu tư thời gian chưa đủ.  

# Ngày 10  
  - Nay chơi giải hackonCTF2019 làm được 3 bài reverse. Cảm giác công sức bỏ ra đã có tí thành tựu. Có các kĩ thuật chủ yếu thiên về phân tích tĩnh đọc code là chính, có bài thực hiện kĩ thuật anti disassemble tí thôi :v   

# Ngày 11  
  - [SVATT 2016 C0ffee](https://bo8blog.wordpress.com/2016/11/07/vong-loai-svattt-2016-pwn200-c0ffee-write-up/?fbclid=IwAR1OHLAOMEFnmq8DR4NoqkT_-KanWAmLztW2XPQRe1FNm1ARD_wb2HZlftA)  
  😁😁😁 Nay nổi hứng lên làm pwn của SVATTT vì mấy bài bên pwnable.tw khoai vl. Vừa làm vừa chơi mà bài này xong trong vòng 3 tiếng :v Cũng được ấy chứ . Cũng gọi là có tí hope vào pwn trong tương lai rồi. Bài này là tận dụng lỗi off-byte-one để ghi đè lên biến đếm số lần để có thể ghi vô hạn :v Sau đó thì là basis rop thôi . Cơ mà cái rop mình vẫn còn yếu vl nên làm đoạn đó khá chậm. Với cả vấn đề code cũng hay sai. Luyện nhiều lên là cải thiện được tốc độ :v  

  ![meo5](/img/meo5.jpg)  

# Ngày 12  
**CodeFest** 
  - Linux Re 1 : một file linux bị pack. Dùng Upx unpack được file C++ -> solve  
  - Linux Re 2 : Một loạt phương trình , dùng [Z3](https://stackoverflow.com/questions/55083687/solve-multiple-equations-using-z3) để giải. Chắc có cách ngắn hơn là dùng angr nhưng trình cùi đéo bt dùng :v  

**ConfuserEx**  
  - Một loại pack của file .NET . Dùng [Nofuser2](https://github.com/CodeShark-Dev/NoFuserEx) rồi dùng [de4dot](https://github.com/0xd4d/de4dot)  

**SVATTT 2018 Quals**  
 - [Encoder](https://github.com/chung96vn/writeup/tree/master/SVATTT-2018-Quals/Encoder)  
 Bài này có một lỗi format string khá rõ ràng. Nhưng nó được bật full cơ chế bảo vệ nên cũng khá là khó ăn theo hướng thông thường mình vẫn làm. Mục đích của bài này không phải tấn công chiếm quyền mà tìm cách in ra flag. Lúc đầu mình đọc nhầm nên có những định hướng hơi sai. Một kinh nghiệm rút ra là đôi khi bài không khó như tưởng tượng, đọc lại xem mình có sai ở đâu không cũng là 1 cách khi đang hết nước. Mình cũng rút ra được 1 vài điều khá hay về format string :  
 	+ nó có thể dùng để đọc dữ liệu. Trước đây mình toàn dùng để ghi nên không chú ý đến chức năng này lắm. 😓😓😓  
	+ Khi đọc hết kí tự trên con trỏ truyền vào hàm printf thì nó đọc tiếp tới ```stdin```  



# Kết thúc  
Tu tiên đại đạo gian nan, mong một ngày có thể quát tháo tiên giới :v  

![hinh1](/Trainning/pham-nhan-tu-tien-vng-phap-bao-02.jpg)
