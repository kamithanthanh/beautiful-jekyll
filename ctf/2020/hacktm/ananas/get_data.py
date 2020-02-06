import pyshark 
from binascii import unhexlify 
from pwn import u32 

def get_data() : 
    pcap = pyshark.FileCapture("ananas.pcapng")  

    """seed""" 
    cap0 = pcap[978] 
    seed = u32(unhexlify(str(cap0.data.data)))

    """data"""
    cap1 = pcap[979] 
    cap2 = pcap[981] 
    data = unhexlify(cap1.data.data + cap2.data.data)
    return seed, list(data)