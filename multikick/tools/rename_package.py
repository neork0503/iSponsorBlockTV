"""Change l'identifiant de l'appli (manifeste + resources.arsc) pour l'installer à côté de l'originale.
usage: rename_package.py in.apk out.apk  — remplacements de même longueur, donc aucun décalage à recalculer."""
import sys,struct,zipfile
OLD,NEW='app.multikick.kick','app.multikick.kic2'
LABEL_OLD,LABEL_NEW='Kick','Kic2'
src,dst=sys.argv[1:3]
def patch_pool(d,pairs):
    d=bytearray(d); off=8
    n,_,flags,sstart,_=struct.unpack_from('<IIIII',d,off+8)
    utf8=flags&0x100
    offs=struct.unpack_from('<%dI'%n,d,off+28)
    for o in offs:
        p=off+sstart+o
        if utf8:
            if d[p]&0x80: p+=1
            p+=1
            l=d[p]
            if l&0x80: l=((l&0x7f)<<8)|d[p+1]; p+=1
            p+=1; cur=bytes(d[p:p+l]).decode('utf8',errors='replace'); enc=lambda s:s.encode('utf8')
        else:
            l=struct.unpack_from('<H',d,p)[0]; p+=2; cur=bytes(d[p:p+l*2]).decode('utf16'); enc=lambda s:s.encode('utf-16-le')
        for a,b in pairs:
            if cur==a: assert len(a)==len(b); d[p:p+len(enc(b))]=enc(b)
    return bytes(d)
zi=zipfile.ZipFile(src)
with zipfile.ZipFile(dst,'w') as zo:
    for it in zi.infolist():
        data=zi.read(it.filename)
        if it.filename=='AndroidManifest.xml':
            data=patch_pool(data,[(OLD,NEW),(LABEL_OLD,LABEL_NEW)])
        elif it.filename=='resources.arsc':
            b=bytearray(data); i=b.find(OLD.encode('utf-16-le')); assert i>0
            b[i:i+len(OLD)*2]=NEW.encode('utf-16-le'); data=bytes(b)
        n=zipfile.ZipInfo(it.filename,date_time=it.date_time); n.compress_type=it.compress_type; n.external_attr=it.external_attr
        if n.compress_type==0: n.extra=b'\0'*((4-(zo.fp.tell()+30+len(it.filename.encode()))%4)%4)
        zo.writestr(n,data)
