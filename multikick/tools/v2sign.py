import sys,struct,hashlib
from cryptography.hazmat.primitives.serialization import pkcs12,Encoding,PublicFormat
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
src,dst,p12,pw=sys.argv[1:5]
key,cert,_=pkcs12.load_key_and_certificates(open(p12,'rb').read(),pw.encode())
d=open(src,'rb').read()
e=d.rfind(b'PK\x05\x06')
cdsz,cdoff=struct.unpack_from('<II',d,e+12)
secs=[d[:cdoff],d[cdoff:e],bytearray(d[e:])]
struct.pack_into('<I',secs[2],16,cdoff)   # offset du bloc = ancien début du répertoire central
CH=1<<20
chunks=[]
for s in secs:
    for i in range(0,len(s),CH):
        c=bytes(s[i:i+CH]); chunks.append(hashlib.sha256(b'\xa5'+struct.pack('<I',len(c))+c).digest())
top=hashlib.sha256(b'\x5a'+struct.pack('<I',len(chunks))+b''.join(chunks)).digest()
L=lambda b:struct.pack('<I',len(b))+b
ALG=0x0103
digests=L(L(struct.pack('<I',ALG)+L(top)))
certs=L(L(cert.public_bytes(Encoding.DER)))
signed=digests+certs+L(b'')
sig=key.sign(signed,padding.PKCS1v15(),hashes.SHA256())
pub=key.public_key().public_bytes(Encoding.DER,PublicFormat.SubjectPublicKeyInfo)
signer=L(signed)+L(L(struct.pack('<I',ALG)+L(sig)))+L(pub)
pair=struct.pack('<IQ',0,0)  # placeholder
val=L(L(signer))
pair=struct.pack('<Q',4+len(val))+struct.pack('<I',0x7109871a)+val
size=len(pair)+8+16
block=struct.pack('<Q',size)+pair+struct.pack('<Q',size)+b'APK Sig Block 42'
eocd=bytearray(d[e:]); struct.pack_into('<I',eocd,16,cdoff+len(block))
open(dst,'wb').write(d[:cdoff]+block+d[cdoff:e]+bytes(eocd))
print('v2 ok',len(block))
