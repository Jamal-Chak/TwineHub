"""HTTP and media verification; browser behavior is not tested here."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from urllib.request import urlopen
from urllib.error import HTTPError
import json, re, subprocess, struct
from PIL import Image, ImageChops, ImageStat
import imageio_ffmpeg
from build_media import VIDEOS
ROOT = Path(__file__).resolve().parent
OUT = ROOT/'dist'
BASE = 'http://127.0.0.1:8080/'
class References(HTMLParser):
    def __init__(self): super().__init__(); self.refs=[]; self.active=[]; self.ids=[]
    def handle_starttag(self,tag,attrs):
        data=dict(attrs)
        for key in ['src','href']:
            if data.get(key): self.refs.append(data[key])
        if data.get('aria-current')=='page': self.active.append(data.get('href'))
        if data.get('id'): self.ids.append(data['id'])
for name in ['index','about','services','gallery','contact']:
    path=name+'.html'; html=urlopen(BASE+path).read().decode()
    parser=References(); parser.feed(html)
    assert parser.active==[path,path], (path,parser.active)
    assert len(parser.ids)==len(set(parser.ids)), 'Duplicate IDs'
    assert 'tel:+27692403008' in html and 'https://wa.me/27692403008' in html
    assert 'mailto:tone4dmedia@gmail.com' in html and 'Norkem' not in html
    for ref in parser.refs:
        if urlsplit(ref).scheme or ref.startswith('#'): continue
        target=unquote(urlsplit(ref).path)
        assert (OUT/target).is_file(), (path,ref)
        assert urlopen(BASE+target).status==200
    print('PASS page links/contact/active indicators:',path)
metadata=json.loads(urlopen(BASE+'assets/metadata.json').read())
assert len(metadata)==30 and len({x['id'] for x in metadata})==30
assert {x['category'] for x in metadata}=={'branding','signage','printing','vehicle','banners'}
for item in metadata:
    for ref in [item['src']]+([item['poster']] if 'poster' in item else []):
        assert urlopen(BASE+ref).status==200
        if not ref.endswith('.mp4'):
            with Image.open(OUT/ref) as im: im.verify()
for ref in re.findall(r"url\(['\"]?([^)'\"]+)", (OUT/'style.css').read_text()):
    assert (OUT/ref).is_file(), ref
for private in ['images/logo.png','images/VID_20250901_162957.mp4','gallery/image1.jpg','gallery/metadata.json','admin.html','images-map.html','build_media.py','IMPLEMENTATION_GUIDE.md','.git/config']:
    try: urlopen(BASE+private)
    except HTTPError as e: assert e.code==404
    else: raise AssertionError('Public source leak: '+private)
print('PASS public references and private source paths return 404')
ff=imageio_ffmpeg.get_ffmpeg_exe(); qa=ROOT/'qa'; qa.mkdir(exist_ok=True)
for source,video,poster in VIDEOS:
    p=OUT/'assets/videos'/video
    result=subprocess.run([ff,'-v','error','-i',str(p),'-f','null','-'],capture_output=True,text=True)
    assert result.returncode==0, result.stderr
    boxes=[]
    with p.open('rb') as stream:
        while True:
            header=stream.read(8)
            if len(header)<8: break
            size,kind=struct.unpack('>I4s',header); boxes.append(kind)
            header_size=8
            if size==1: size=struct.unpack('>Q',stream.read(8))[0]; header_size=16
            if size==0: break
            stream.seek(size-header_size,1)
    assert boxes.index(b'moov')<boxes.index(b'mdat')
    frame=qa/(video+'.jpg')
    subprocess.run([ff,'-v','error','-y','-ss','00:00:01','-i',str(ROOT/'images'/source),'-frames:v','1','-vf','scale=960:-2','-q:v','4',str(frame)],check=True)
    im=Image.open(frame); im.thumbnail((960,960),Image.Resampling.LANCZOS)
    expected=qa/(poster+'.expected.jpg'); im.save(expected,'JPEG',quality=70,progressive=True,optimize=True)
    actual=Image.open(OUT/'assets/posters'/poster).convert('RGB'); expected_im=Image.open(expected).convert('RGB')
    assert actual.size==expected_im.size
    error=sum(ImageStat.Stat(ImageChops.difference(actual,expected_im)).mean)/3
    assert error<2, (video,'poster mismatch',error)
    print('PASS decode, faststart and corresponding poster:',video,'mean error',round(error,3))
audit=json.loads((ROOT/'media-audit.json').read_text())
assert all(not entry['exif_fields'] for entry in audit)
print('Image bytes:',sum(x['source_bytes'] for x in audit),'->',sum(x['output_bytes'] for x in audit))
print('PASS static/HTTP/media checks. Browser rendering and interaction unverified.')
