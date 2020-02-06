from PIL import Image
import struct 
from binascii import unhexlify 


seed = 0 

max_int = 1 << 32 
len_data = 14400
def prng() : 
    global seed 
    seed = (0x47fc96 + 48192 * seed ) % max_int 
    seed ^= (seed >> 7) % max_int
    seed ^= ((seed << 17) % max_int)
    seed ^= ((77 * seed) % max_int)
    return (seed // 1234 ) % 0x10000


def decrypt(key, data) : 
    global seed 
    seed = key[0] 
    random_number = [0] * (len_data -1)
    for i in range(len_data - 1) : 
        random_number[i] = prng() 

    for i in range(1, len_data - 1) : 
        rdn = random_number[len_data - i - 1] % i
        data[i], data[rdn] = data[rdn], data[i]  

    img = Image.new('L', (160, 90))
    pixels = img.load()
    for h in range(90):
        for w in range(160):
            pixels[w, h] = int(data[160 * h + w])
    global _ 
    img.save("flag/img%i.png" % (_//4))
    return img 

f = open("data.txt", "r") 
datas = f.readlines() 


print(len(datas))
for _ in range(0, len(datas), 4) : 
    print(_//4)
    key = struct.unpack('<I', unhexlify(datas[_].strip("\n")))
    data = list(unhexlify(datas[_+1].strip("\n")))
    data += list(unhexlify(datas[_+2].strip("\n")))
    decrypt(key, data)

