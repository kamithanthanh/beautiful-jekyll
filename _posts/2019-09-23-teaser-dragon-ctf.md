---
layout : post 
title : Teaser Dragon CTF RsaChain 
--- 

Trong kì thi có 1 bài crypto duy nhất và cũng là bài duy nhất mình làm được.  Các bạn có thể dowload challenge tại [đây](https://github.com/hacmao/hacmao.github.io/tree/master/Crypto/ctf/teaser_dragon)

# Enryption  

Đây là một bài rsa 😬😬😬. Trước tiên nó thiết lập 4 key :  

```python
# rsa1: p - 700 bits q - 1400 bits

p = genPrime(700)
q = genPrime(1400)

n = p*q
phi = (p-1)*(q-1)
d = gmpy2.powmod(e, -1, phi)

rsa1 = (n, d)
``` 

Mấy key còn lại tương tự nhưng có thay đổi một chút. 😁  
Sau đó thì nó có hàm encrypt flag 4 lớp rồi in ra flag encrypt :  

```python 

for n, d in rsa:
    print 'pubkey:', n, d % (2**1050)
    flag = pow(flag, e, n)

print 'encrypted flag', flag
``` 
Đồng thời chúng ta có được từng module và partial private key d.  
Đến đây ta đã biết rõ được kiểu tấn công của bài này là ```Partial Key Exposure Attack```. Có thể đọc paper ở [đây](Partial Key Exposure Attack). Mục 4.5.   

# Partial Key Exposure Attack 

Trong mục 4.5 kia ta chú ý phần này :  

![](/Crypto/ctf/teaser_dragon/hinh1.PNG)  

Phần đầu tiên trong kiểu attack này là recovery lại một phần p hoặc q. Ta làm trường hợp đơn giản trước là n = p * q.  
Do ```ed = 1 [mod phi]``` nên tồn tại một số k thỏa mãn phương trình trên. Cùng với đó, ta có d < phi(n) nên k < e.  
Gọi kb là số bits đã biết d0 của d.Ta có :  

```python
    e * d0 - k*(N - p - q + 1) = 1 [mod 2^kb] 
->  e * d0 * p - k * (N * p - p^2 - N + p) = p [mod 2^kb]   # Nhan ca hai ve voi p 
```

Tại sao lại nhân cả hai về với p. Vì khi đó chúng ta chỉ còn lại một biến chưa biết là ```p```. Ta có phương trình đồng dư bậc hai.  
Điều mà đã được giải bằng [Hennsel lift](https://github.com/gmossessian/Hensel) trong thời gian khá nhanh.  
Nói chung cũng không cần hiểu rõ cách hoạt động của hennsel lift. Dùng code chạy giải ra nghiệm là được. Hennsel lift là cách giải tối ưu nhất cho những phương trình đa thức đồng dư một p^k.  

# Factor modules  

Các key bị đảo lộn nên ta không biết module nào được tạo theo kiểu nào. Chú ý là với các modules có kiểu là ```n = p*q*r``` thì r lại chỉ được tạo một lần. Cho nên bằng phép lấy ước chung chúng ta có thể xác định hai thằng này. Chính là hai thằng đầu. Sau đó tiến hành viết script giải cho từng dạng. Hai thằng sau không biết nó là dạng nào thì thử cả hai , cái nào ra thì nó là nó.  

Script solve viết như trên kia ấy.Nhưng dạng modules của các key này có hơi khác với trên. Tuy nhiên cùng một kiểu biến đổi là tạo phương trình đồng dư như trên thì chúng ta cũng có thể biến đổi một cách tương tự và dùng hennsel lift để giải ra nghiệm. Nghiệm này có 1050 bits mà p của chúng ta chỉ có 700 bits nên đó chính là p mà ta cần tìm. Check lại xem có là ước của modules tương ứng không là được.   
Trong giai đoạn gen phương trình nên làm cẩn thận để tránh mất time bruteforce 😭😭😭.   
Lúc đầu mình không dùng hennsel lift mà dùng cái ```solve_mod``` của sage ngồi đợi hơn tiếng mà chưa xong nổi một phương trình. Chưa bao giờ bruteforce lại gian nan như vậy. May mà có tiền bối chỉ bảo cho cái kia công việc mới nhẹ nhàng hơn. 😌😌😌   

# Get flags  
Factor được rồi thì còn đợi gì mà không lấy flag.  😁😁😁  



