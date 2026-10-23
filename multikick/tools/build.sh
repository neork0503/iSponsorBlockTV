#!/bin/sh
# usage: build.sh Kick-v115.apk keystore.p12 mot_de_passe alias   (outils: python3 + cryptography, jarsigner)
# produit ../Kick-v115-ui.apk et ../Kick-v115-ui-cote-a-cote.apk (autre identifiant)
set -e
ORIG=$1; KS=$2; PW=$3; AL=${4:-multikick}
T=$(dirname "$0"); W=$(mktemp -d)
python3 "$T/repack.py" "$ORIG" "$W/a.apk" "$T/../assets"
python3 "$T/patch_icon.py" "$W/a.apk" "$W/b.apk" >/dev/null
python3 "$T/rename_package.py" "$W/b.apk" "$W/c.apk"
sign() {  # $1 entrée  $2 sortie
  cp "$1" "$W/t.apk"
  jarsigner -keystore "$KS" -storetype PKCS12 -storepass "$PW" -sigalg SHA256withRSA -digestalg SHA-256 -sigfile MULTIKIC "$W/t.apk" "$AL" >/dev/null 2>&1
  python3 - "$1" "$W/t.apk" "$W/v1.apk" <<'PY'
import sys,zipfile
src=zipfile.ZipFile(sys.argv[1]); sg=zipfile.ZipFile(sys.argv[2])
with zipfile.ZipFile(sys.argv[3],'w') as zo:
    for name in ('META-INF/MANIFEST.MF','META-INF/MULTIKIC.SF','META-INF/MULTIKIC.RSA'):
        it=sg.getinfo(name); n=zipfile.ZipInfo(name,date_time=it.date_time); n.compress_type=8; zo.writestr(n,sg.read(name))
    for it in src.infolist():
        n=zipfile.ZipInfo(it.filename,date_time=it.date_time); n.compress_type=it.compress_type; n.external_attr=it.external_attr
        if n.compress_type==0: n.extra=b'\0'*((4-(zo.fp.tell()+30+len(it.filename.encode()))%4)%4)
        zo.writestr(n,src.read(it.filename))
PY
  python3 "$T/v2sign.py" "$W/v1.apk" "$2" "$KS" "$PW"
}
sign "$W/b.apk" "$T/../Kick-v115-ui.apk"
sign "$W/c.apk" "$T/../Kick-v115-ui-cote-a-cote.apk"
rm -rf "$W"
