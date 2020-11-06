# Setup debug mips  

## Cài đặt môi trường 

Download tools [arm-now](https://github.com/nongiach/arm_now).  

Khi install sẽ bị một lỗi do conflict bản `quemu-system-arm`. Do đó, cần vào thư mục install của `arm-now` trong python, rồi sửa file `arm_now.py`.  
Trong `vim`, tìm đến đoạn `nic` rồi sửa list `args` thành :  

```
 args = ["-net nic -net user,hostfwd=tcp::80-:80,hostfwd=tcp::443-:443,hostfwd=tcp::2222-:22,hostfwd=tcp::8080-:8080,hostfwd=tcp::9999-:9999,hostfwd=tcp::9998-:9998"]
```

Ở đây, ngoài kết nối các port thông dụng như ssh, http, ... thì mình còn thực hiện mở portforward với 2 port là `9998 - 9999`.  

Sau đó, thiết lập môi trường giả lập `mips` bằng lệnh :  

```
arm_now start mips32el 
```
## Debug  

Tiếp đến, download [socat](http://pkg.musl.cc/socat/mipsel-linux-musln32/bin/) cho mips rồi chạy file với lệnh :  

```
./socat TCP-LISTEN:9998,reuseaddr,fork EXEC:"./bin" &
```

Khi đó, ta sẽ mở được một server tại localhost tại port 9998.  
```
nc localhost 9998
```

Khi tiến hành `nc` đến, thì trên máy ảo `mips` sẽ có tiến trình của hàm đang chạy.  

```
44 root     /sbin/syslogd -n
47 root     /sbin/klogd -n
63 root     -sh
64 root     [kworker/u2:1]
72 root     ./socat TCP-LISTEN:9998,reuseaddr,fork EXEC:./callme_mipsel
76 root     ./socat TCP-LISTEN:9998,reuseaddr,fork EXEC:./callme_mipsel
77 root     ./callme_mipsel
78 root     ps
```

Sử dụng lệnh `gdbserver` để mở gdb về local để debug.  

```
gdbserver :9999 --attach 77
```

Tại local, ta chạy `gdb-multiarch` :  

```
$ gdb 
(gdb) set architecture mips32el
(gdb) set endian little
(gdb) target remote localhost:9999
```

Ta sẽ thực hiện được debug trên server. Làm cách này, chúng ta có thể mở được server debug và giao tiếp với tiến trình bằng python.

# LD_LIBRARY_PATH

LD_LIBRARY_PATH=$LD_LIBRARY_PATH:./
