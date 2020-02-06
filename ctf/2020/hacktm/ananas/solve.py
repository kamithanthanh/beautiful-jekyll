from get_data import get_data
from z3 import *  

seed, data = get_data()  
len_data = len(data) 

max_int = 1 << 32 
def prng() : 
    global seed 
    seed = (0x47fc96 + 48192 * seed ) % max_int 
    seed ^= (seed >> 7) % max_int
    seed ^= ((seed << 17) % max_int)
    seed ^= ((77 * seed) % max_int)
    return (seed // 1234 ) % 0x10000

print("Generating random number ....")
random_number = [0] * (len_data -1)
for i in range(len_data - 1) : 
    random_number[i] = prng() 

print("Swapping ...")
for i in range(1, len_data - 1) : 
    rdn = random_number[len_data - i - 1] % i
    data[i], data[rdn] = data[rdn], data[i]  

pic = "".join(list(map(chr, data))) 
print(pic[:3])
# for i in range()
# f = open("pic", "w") 
# f.write(pic)
# f.close()  
# https://github.com/ofTheo/videoInput/blob/master/videoInputSrcAndDemos/libs/videoInput/videoInput.cpp