"""Create an allowlisted public output. Never serve the repository root."""
from pathlib import Path
import json
import shutil
ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'dist'
PAGES = ['index.html', 'about.html', 'services.html', 'gallery.html', 'contact.html']
def copy(name):
    destination = OUT / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / name, destination)
def build():
    if OUT.resolve().parent != ROOT or OUT.name != 'dist':
        raise RuntimeError('Invalid output directory')
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for name in PAGES + ['style.css', 'script.js', 'assets/metadata.json']:
        copy(name)
    media = {'assets/images/logo.png', 'assets/images/background.jpg'}
    for item in json.loads((ROOT / 'assets/metadata.json').read_text(encoding='utf-8')):
        media.add(item['src'])
        if item.get('poster'): media.add(item['poster'])
    for name in sorted(media):
        if not name.startswith('assets/') or '..' in Path(name).parts: raise ValueError('Media must be inside assets/')
        copy(name)
    print(f'Built {len(PAGES)} pages and {len(media)} public media files in {OUT}')
if __name__ == '__main__': build()
