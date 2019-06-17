---
layout : post 
title : Otppppp 
subtitle : Rookiss Pwnable.kr 
image : /Pwnable/pwnable.kr/rookiss/otp/otp.png 
--- 

# Mở đầu
Bài này không đơn thuần là pwn thông thường chỉ sử dụng các câu lệnh của C mà nó liên quan tới các câu lệnh của Linux kết hợp để gây lỗi cho chương trình.
Bài này mình tham khảo ở [đây](https://nickcano.com/pwnables-write-ups-oct17/). Có sử dụng hàm [ulimit](https://ss64.com/bash/ulimit.html) để thực hiện mục
đích của mình. 

# Source Code  
Không giống các bài mình hay làm thì bài này nó cho mình ssh đến server của nó . 😓😓😓 Có một điều khó chịu là mình không có binary để đọc cũng
như việc debug rất khó khi không có GDB-pwndbg mình hay dùng. Đồng thời việc viết exploit cũng khó hơn. 

```C
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>

int main(int argc, char* argv[]){       
	    char fname[128];
        unsigned long long otp[2];

        if(argc!=2){
                printf("usage : ./otp [passcode]\n");
                return 0;
        }

        int fd = open("/dev/urandom", O_RDONLY);
        if(fd==-1) exit(-1);

        if(read(fd, otp, 16)!=16) exit(-1);
        close(fd);

        sprintf(fname, "/tmp/%llu", otp[0]);
        FILE* fp = fopen(fname, "w");
        if(fp==NULL){ exit(-1); }
        fwrite(&otp[1], 8, 1, fp);
        fclose(fp);

        printf("OTP generated.\n");

        unsigned long long passcode=0;
        FILE* fp2 = fopen(fname, "r");
        if(fp2==NULL){ exit(-1); }
        fread(&passcode, 8, 1, fp2);
        fclose(fp2);

        if(strtoul(argv[1], 0, 16) == passcode){
                printf("Congratz!\n");
                system("/bin/cat flag");
        }
        else{
                printf("OTP mismatch\n");
        }

        unlink(fname);
        return 0;
}
```
