"""Remplace l'icône de l'appli par le logo Kick (K vert en blocs sur fond noir).
usage: patch_icon.py in.apk out.apk — réécrit res/drawable/ic_launcher_fg.xml (vector binaire)."""
import sys,struct,zipfile
# logo Kick, viewBox 24x24 (K en blocs)
K=[(1.333,0),(9.333,0),(9.333,5.333),(12,5.333),(12,2.667),(14.667,2.667),(14.667,0),(22.667,0),(22.667,8),(20,8),(20,10.667),
   (17.333,10.667),(17.333,13.333),(20,13.333),(20,16),(22.667,16),(22.667,24),(14.667,24),(14.667,21.333),(12,21.333),(12,18.667),
   (9.333,18.667),(9.333,24),(1.333,24)]
S=2.0   # 24 -> 108 : le K occupe ~48x43 sur 108, bien dans la zone visible des icônes adaptatives
pts=[(54+(x-12)*S,54+(y-12)*S) for x,y in K]
fmt=lambda v:('%.2f'%v).rstrip('0').rstrip('.')
PATH='M'+' L'.join(fmt(x)+','+fmt(y) for x,y in pts)+' Z'
NOP='M0,0 Z'
GREEN=0xFF53FC18
def read_pool(d):
    n,_,flags,sstart,_=struct.unpack_from('<IIIII',d,16)
    offs=struct.unpack_from('<%dI'%n,d,36); out=[]
    for o in offs:
        p=8+sstart+o
        if d[p]&0x80:p+=1
        p+=1; l=d[p]
        if l&0x80: l=((l&0x7f)<<8)|d[p+1]; p+=1
        p+=1; out.append(d[p:p+l].decode('utf8'))
    return out,struct.unpack_from('<I',d,12)[0]
def enc(s):
    b=s.encode('utf8'); cl=len(s)
    f=lambda n:bytes([n]) if n<128 else bytes([(n>>8)|0x80,n&0xff])
    return f(cl)+f(len(b))+b+b'\0'
def patch(d):
    strs,psz=read_pool(d)
    i=strs.index('M30,29 L65,29 Q69,29 69,33 L69,54 Q69,58 65,58 L30,58 Q26,58 26,54 L26,33 Q26,29 30,29 Z')
    assert strs[i:i+4]==[s for s in strs[i:i+4]] and i==8
    strs[8]=PATH; strs[9]=strs[10]=strs[11]=NOP
    blobs=[enc(s) for s in strs]; offs=[];o=0
    for b in blobs: offs.append(o); o+=len(b)
    body=b''.join(blobs); body+=b'\0'*((4-len(body)%4)%4)
    sstart=28+4*len(strs)
    pool=struct.pack('<HHIIIIII',1,28,sstart+len(body),len(strs),0,0x100,sstart,0)+struct.pack('<%dI'%len(offs),*offs)+body
    rest=bytearray(d[8+psz:]); 
    # attributs : positions relatives à la fin du pool
    shift=len(pool)-psz
    def setv(pos,val): struct.pack_into('<I',rest,pos-(8+psz),val)   # pos absolu dans l'ancien fichier
    # path1 : remplissage vert, sans contour ; chemins 2-4 : invisibles
    setv(804+8-8+0,GREEN)  # fillColor path1 (@804 = octet de data)
    setv(844,0x00000000)   # strokeColor path1 -> transparent
    setv(944,0x00000000); setv(984,0x00000000)
    setv(1084,0x00000000); setv(1184,0x00000000)
    out=bytearray(d[:8])+pool+rest
    struct.pack_into('<I',out,4,len(out))
    return bytes(out)
if __name__=='__main__':
    src,dst=sys.argv[1:3]
    zi=zipfile.ZipFile(src)
    with zipfile.ZipFile(dst,'w') as zo:
        for it in zi.infolist():
            data=zi.read(it.filename)
            if it.filename=='res/drawable/ic_launcher_fg.xml': data=patch(data)
            n=zipfile.ZipInfo(it.filename,date_time=it.date_time); n.compress_type=it.compress_type; n.external_attr=it.external_attr
            if n.compress_type==0: n.extra=b'\0'*((4-(zo.fp.tell()+30+len(it.filename.encode()))%4)%4)
            zo.writestr(n,data)
    print(PATH)
