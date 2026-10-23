import zipfile,sys
src,dst,assets=sys.argv[1:4]
zi=zipfile.ZipFile(src)
rep={'assets/home.html':assets+'/home.html','assets/player.html':assets+'/player.html'}
with zipfile.ZipFile(dst,'w') as zo:
    for it in zi.infolist():
        if it.filename.startswith('META-INF/'): continue
        data=open(rep[it.filename],'rb').read() if it.filename in rep else zi.read(it.filename)
        n=zipfile.ZipInfo(it.filename,date_time=it.date_time)
        n.compress_type=it.compress_type; n.external_attr=it.external_attr
        if n.compress_type==zipfile.ZIP_STORED:
            hdr=zo.fp.tell()+30+len(it.filename.encode())
            n.extra=b'\0'*((4-hdr%4)%4)
        zo.writestr(n,data)
