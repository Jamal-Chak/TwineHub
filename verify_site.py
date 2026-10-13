"""Verify the static build, authoritative inventory and source preservation.

Run after building and serving dist: python verify_site.py --base http://127.0.0.1:8080/
Filesystem/HTTP/decoder results do not replace browser rendering or interaction QA.
"""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.error import HTTPError
from urllib.parse import parse_qs, quote, unquote, unquote_plus, urljoin, urlsplit
from urllib.request import urlopen
import json
import re
import struct
import subprocess
from PIL import Image, ImageChops, ImageOps, ImageStat
import imageio_ffmpeg
from build_media import VIDEOS
from build_site import PAGES

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'dist'
ADDRESS = '11 Bunyan Street Benoni'
# Only this removal was authorized by the owner; a manifest cannot silently
# waive preservation of any other previously published project.
AUTHORIZED_REMOVALS = {
    28: {
        'src': 'assets/videos/studio-tour.mp4',
        'poster': 'assets/posters/poster-studio-tour.jpg',
    },
}
SOCIAL_LINKS = {
    'https://www.facebook.com/share/1Ea1pMmF7w/',
    'https://www.instagram.com/tone4dmedia?igsh=cDgxM3NrYTZvNnBp',
}


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def digest(path):
    checksum = sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            checksum.update(chunk)
    return checksum.hexdigest()


def relative_path(name):
    path = Path(name.replace('\\', '/'))
    assert not path.is_absolute() and '..' not in path.parts and not urlsplit(name).scheme, name
    return path


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.active, self.ids, self.filters, self.images, self.service_cards = [], [], [], [], [], []
        self.featured_ids = []
        self._card, self._article_depth = None, 0

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        self.refs.extend(data[key] for key in ('src', 'href', 'poster') if data.get(key))
        if data.get('aria-current') == 'page':
            self.active.append(data.get('href'))
        if data.get('id'):
            self.ids.append(data['id'])
        if 'data-filter' in data:
            self.filters.append(data['data-filter'])
        if data.get('id') == 'galleryPreview':
            self.featured_ids = [int(value.strip()) for value in data.get('data-featured-ids', '').split(',') if value.strip()]
        if tag == 'article':
            if self._card is not None:
                self._article_depth += 1
            elif 'service-card' in data.get('class', '').split():
                self._card, self._article_depth = {'images': [], 'links': []}, 1
        if tag == 'img':
            self.images.append(data)
            if self._card is not None:
                self._card['images'].append(data)
        if tag == 'a' and self._card is not None:
            self._card['links'].append(data.get('href', ''))

    def handle_endtag(self, tag):
        if tag == 'article' and self._card is not None:
            self._article_depth -= 1
            if not self._article_depth:
                self.service_cards.append(self._card)
                self._card = None


def check_address(html, parser, name):
    decoded = ' '.join(unquote_plus(unescape(html)).split())
    assert ADDRESS in decoded, (name, 'Missing full business address')
    assert not re.search(r'\bBunya\b|Norkem', decoded, re.I), (name, 'Obsolete address')
    for match in re.finditer(r'\b11\s+Bunyan\b', decoded):
        assert decoded[match.start():].startswith(ADDRESS), (name, 'Incomplete address')
    maps = []
    for ref in parser.refs:
        parsed = urlsplit(ref)
        if 'google.' in parsed.netloc and '/maps' in parsed.path:
            queries = parse_qs(parsed.query)
            destinations = [value for key in ('q', 'query', 'destination') for value in queries.get(key, [])]
            assert destinations and all(value == ADDRESS for value in destinations), (name, ref)
            maps.append(ref)
    if name == 'contact.html':
        assert maps, 'Contact directions must use an address-search link'


def check_manifest(metadata):
    assert isinstance(metadata, list) and metadata, 'Empty portfolio'
    for field in ('id', 'src'):
        assert len(metadata) == len({item[field] for item in metadata}), ('Duplicate portfolio field', field)
    categories = {item['category'] for item in metadata}
    assert all(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', value) for value in categories)
    for item in metadata:
        assert item['type'] in ('image', 'video'), item
        assert all(isinstance(item.get(key), str) and item[key].strip()
                   for key in ('title', 'alt', 'description', 'category')), item
        assert relative_path(item['src']).parts[0] == 'assets', item
        if item['type'] == 'video':
            assert item.get('poster') and relative_path(item['poster']).parts[0] == 'assets', item
    return categories


def check_dist(metadata):
    expected = set(PAGES + ['style.css', 'script.js', 'assets/metadata.json',
                            'assets/images/logo.png', 'assets/images/background.jpg'])
    for item in metadata:
        expected.add(item['src'])
        if item.get('poster'):
            expected.add(item['poster'])
    actual = {path.relative_to(OUT).as_posix() for path in OUT.rglob('*') if path.is_file()}
    assert actual == expected, {'missing': sorted(expected - actual), 'unexpected': sorted(actual - expected)}
    for name in expected:
        path = OUT / relative_path(name)
        assert not path.is_symlink(), ('Public symlink', name)
        assert digest(path) == digest(ROOT / name), ('Stale or altered build', name)
    print(f'PASS exact dist allowlist: {len(expected)} files; originals and development utilities excluded')


def check_preservation(metadata, mapping):
    snapshot = read_json(ROOT / 'qa/media-before.json')
    by_id = {item['id']: item for item in metadata}
    removal_records = mapping.get('intentional_removals', [])
    removed_ids = [item['entry_id'] for item in removal_records]
    assert len(removed_ids) == len(set(removed_ids)), 'Duplicate intentional removal records'
    removed_refs = set()
    for removal in removal_records:
        entry_id = removal['entry_id']
        assert entry_id in AUTHORIZED_REMOVALS, ('Unapproved portfolio removal', entry_id)
        assert removal.get('reason', '').strip(), ('Removal needs a documented reason', entry_id)
        before = next(item for item in snapshot['entries'] if item['id'] == entry_id)
        for field, expected in AUTHORIZED_REMOVALS[entry_id].items():
            assert removal[field] == before[field] == expected, ('Wrong removal asset', entry_id, field)
            removed_refs.add(expected)
        assert removal['title'] == before['title'], ('Wrong removal title', entry_id)
        assert entry_id not in by_id, ('Removed entry is still published', entry_id)
    for item in metadata:
        assert item['src'] not in removed_refs and item.get('poster') not in removed_refs, ('Removed media reused publicly', item)
    for ref in removed_refs:
        assert not (OUT / ref).exists(), ('Removed media still in dist', ref)
        for name in PAGES + ['style.css', 'script.js', 'assets/metadata.json']:
            assert ref not in (OUT / name).read_text(encoding='utf-8'), ('Removed media reference in public output', name, ref)
    for before in snapshot['entries']:
        # Archived removals must remain byte-identical in the repository too.
        assert digest(ROOT / before['src']) == before['src_sha256'], ('Published media altered', before['src'])
        if before['type'] == 'video':
            assert digest(ROOT / before['poster']) == before['poster_sha256'], before['poster']
        if before['id'] in removed_ids:
            continue
        assert before['id'] in by_id, ('Previously published entry removed', before['id'])
        current = by_id[before['id']]
        for field in ('src', 'type'):
            assert current[field] == before[field], ('Published source changed', before['id'], field)
        if before['type'] == 'video':
            assert current['poster'] == before['poster']
    originals_path = ROOT / 'qa/original-media-before.json'
    if originals_path.exists():
        originals = read_json(originals_path)
        actual = {path.relative_to(ROOT).as_posix()
                  for folder in ('images', 'gallery') for path in (ROOT / folder).rglob('*') if path.is_file()}
        assert actual == set(originals), 'Original source inventory changed'
        for name, checksum in originals.items():
            assert digest(ROOT / name) == checksum, ('Original altered', name)
        print(f'PASS originals inventory and hashes unchanged: {len(originals)} files')
    else:
        print('UNVERIFIED full originals hashes: qa/original-media-before.json not present')
    for entry in snapshot.get('source_files', []):
        assert digest(ROOT / entry['source']) == entry['sha256'], ('Original changed', entry['source'])
    retained = Counter(item['type'] for item in snapshot['entries'] if item['id'] not in removed_ids)
    print(f"PASS prior public entries retained unchanged: {retained['image']} images, {retained['video']} videos")
    if removal_records:
        print(f'PASS {len(removal_records)} owner-requested removal(s): repository archives unchanged; public metadata/references/files excluded')
    return snapshot, removed_refs


def old_sources(public_asset):
    audit = ROOT / 'media-audit.json'
    if not audit.exists():
        return []
    return [ROOT / relative_path(entry['source']) for entry in read_json(audit)
            if entry['output'].replace('\\', '/') == public_asset]


def check_new_inventory(metadata, snapshot, mapping):
    records = mapping['new_images']
    sources = [entry['source'].replace('\\', '/') for entry in records]
    assert len(sources) == len(set(sources)), 'Repeated source mapping'
    # Path.rglob includes hidden files; all files inside owner subfolders need a disposition.
    actual = {path.relative_to(ROOT).as_posix() for path in (ROOT / 'images').rglob('*')
              if path.is_file() and path.parent != ROOT / 'images'}
    assert actual == set(sources), {'unmapped': sorted(actual - set(sources)), 'missing': sorted(set(sources) - actual)}
    by_id = {item['id']: item for item in metadata}
    old_ids = {item['id'] for item in snapshot['entries']}
    added_assets, added_ids, status_counts = set(), set(), Counter()
    for record in records:
        source = ROOT / relative_path(record['source'])
        assert digest(source) == record['source_sha256'], ('New original altered', record['source'])
        status = record['status']
        status_counts[status] += 1
        assert status in ('added', 'exact-duplicate', 'unprocessed'), record
        if status == 'unprocessed':
            assert record.get('reason'), ('Unprocessed file needs a reported reason', record)
            raise AssertionError(('UNRESOLVED supplied file', record['source'], record['reason']))
        item = by_id[record['entry_id']]
        assert item['type'] == 'image'
        for mapping_key, metadata_key in [('public_asset', 'src'), ('category', 'category'),
                                          ('title', 'title'), ('description', 'description'), ('alt', 'alt')]:
            assert record[mapping_key] == item[metadata_key], ('Mapping mismatch', record['source'], mapping_key)
        public_asset = record['public_asset']
        if status == 'exact-duplicate':
            candidates = old_sources(public_asset)
            candidates.extend(ROOT / relative_path(other['source']) for other in records
                              if other['source'] != record['source'] and other.get('public_asset') == public_asset)
            assert any(digest(path) == record['source_sha256'] for path in candidates), ('Duplicate is not byte-identical', record)
            continue
        assert record['entry_id'] not in old_ids, ('New image overwrites prior entry', record)
        assert public_asset not in added_assets, ('New filename collision', public_asset)
        added_assets.add(public_asset)
        added_ids.add(record['entry_id'])
        output = ROOT / relative_path(public_asset)
        assert output != source
        assert output.stat().st_size < source.stat().st_size, ('Image was not reduced', record['source'])
        assert record['source_bytes'] == source.stat().st_size and record['output_bytes'] == output.stat().st_size
        with Image.open(source) as original, Image.open(output) as optimized:
            oriented = ImageOps.exif_transpose(original)
            oriented.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
            assert optimized.size == oriented.size, ('Aspect ratio/orientation dimensions', record['source'])
            assert max(optimized.size) <= 1600 and not optimized.getexif(), ('Dimensions/EXIF', public_asset)
            assert (record['width'], record['height']) == optimized.size, record
            # This detects wrong 180-degree orientation that matching dimensions cannot catch.
            if 'A' in oriented.getbands():
                expected = Image.new('RGB', oriented.size, 'white')
                expected.paste(oriented.convert('RGB'), mask=oriented.getchannel('A'))
            else:
                expected = oriented.convert('RGB')
            error = sum(ImageStat.Stat(ImageChops.difference(optimized.convert('RGB'), expected)).mean) / 3
            assert error < 18, ('Unexpected content/orientation', record['source'], error)
    assert set(by_id) - old_ids == added_ids, 'New portfolio entries not fully accounted for'
    counts = Counter(item['type'] for item in metadata)
    actual_after = {'images': counts['image'], 'videos': counts['video'], 'total': len(metadata),
                    'by_category': dict(sorted(Counter(item['category'] for item in metadata).items()))}
    assert mapping['after'] == actual_after, ('Mapping final counts differ from public portfolio', mapping['after'], actual_after)
    print(f'PASS recursive supplied-file mapping: {len(records)} files; {dict(status_counts)}')
    print('PASS new optimization, aspect ratios, EXIF stripping and orientation/content comparison')
    return mapping


def check_http(base, metadata, categories, removed_refs=()):
    def request(name):
        return urlopen(urljoin(base, quote(name, safe='/?=&:#%')), timeout=30)
    by_asset = {item['src']: item for item in metadata}
    by_id = {item['id']: item for item in metadata}
    for name in PAGES:
        with request(name) as response:
            assert response.status == 200
            contents = response.read()
        assert contents == (OUT / name).read_bytes(), ('HTTP not serving current dist', name)
        html = contents.decode('utf-8')
        parser = References()
        parser.feed(html)
        assert parser.active == [name, name], (name, parser.active)
        assert len(parser.ids) == len(set(parser.ids)), (name, 'Duplicate IDs')
        assert {'tel:+27692403008', 'https://wa.me/27692403008',
                'mailto:tone4dmedia@gmail.com'} | SOCIAL_LINKS <= set(parser.refs)
        assert '069 240 3008' in html
        check_address(html, parser, name)
        for ref in parser.refs:
            if urlsplit(ref).scheme or ref.startswith('#'):
                continue
            target = unquote(urlsplit(ref).path)
            assert (OUT / relative_path(target)).is_file(), (name, ref)
            with request(target) as response:
                assert response.status == 200
            category = parse_qs(urlsplit(ref).query).get('category')
            if category:
                assert target == 'gallery.html' and category[0] in categories, (name, ref)
        if name == 'gallery.html':
            assert len(parser.filters) == len(set(parser.filters))
            assert set(parser.filters) == categories | {'all'}, ('Gallery filters mismatch', parser.filters, categories)
        if name == 'index.html':
            assert parser.featured_ids and len(parser.featured_ids) == len(set(parser.featured_ids)), 'Missing/duplicate homepage previews'
            assert all(value in by_id for value in parser.featured_ids), 'Broken homepage preview IDs'
        for card in parser.service_cards:
            links = [parse_qs(urlsplit(link).query)['category'][0] for link in card['links']
                     if 'category' in parse_qs(urlsplit(link).query)]
            assert links and set(links) <= categories and card['images'], (name, card)
            for image in card['images']:
                assert by_asset[image['src']]['category'] in links, ('Wrong service thumbnail category', name, image['src'], links)
                assert image.get('loading') == 'lazy' and image.get('alt', '').strip(), ('Missing thumbnail lazy/alt', image['src'])
        for image in parser.images:
            with Image.open(OUT / unquote(urlsplit(image['src']).path)) as decoded:
                assert (int(image['width']), int(image['height'])) == decoded.size, ('HTML image dimensions', name, image['src'])
        print('PASS page references, contact/social/address, active indicators and category thumbnails:', name)
    with request('assets/metadata.json') as response:
        assert json.load(response) == metadata
    for item in metadata:
        for ref in [item['src']] + ([item['poster']] if item.get('poster') else []):
            with request(ref) as response:
                assert response.status == 200
    for name in ('style.css', 'script.js'):
        with request(name) as response:
            assert response.read() == (OUT / name).read_bytes(), ('Stale HTTP asset', name)
    for ref in re.findall(r"url\(['\"]?([^)'\"]+)", (OUT / 'style.css').read_text(encoding='utf-8')):
        if not urlsplit(ref).scheme:
            assert (OUT / relative_path(ref)).is_file(), ref
    private = ['images/logo.png', 'images/VID_20250901_162957.mp4', 'gallery/image1.jpg', 'gallery/metadata.json',
               'admin.html', 'images-map.html', 'build_media.py', 'build_site.py', 'IMPLEMENTATION_GUIDE.md',
               'media-update-mapping.json', 'qa/media-before.json', '.git/config']
    private.extend(path.relative_to(ROOT).as_posix() for path in (ROOT / 'images').rglob('*')
                   if path.is_file() and path.parent != ROOT / 'images')
    private.extend(sorted(removed_refs))
    for name in private:
        try:
            with request(name):
                pass
        except HTTPError as error:
            assert error.code == 404, (name, error.code)
        else:
            raise AssertionError('Public source leak: ' + name)
    print('PASS current HTTP media references; original/mapping/development paths return 404')
    if removed_refs:
        print('PASS owner-removed public video/poster HTTP paths return 404')


def check_images(metadata):
    for item in metadata:
        ref = item['poster'] if item['type'] == 'video' else item['src']
        fields = ('posterWidth', 'posterHeight') if item['type'] == 'video' else ('width', 'height')
        with Image.open(OUT / ref) as image:
            assert tuple(item[field] for field in fields) == image.size, ('Metadata dimensions', ref)
            assert not image.getexif(), ('Public portfolio EXIF leak', ref)
            image.verify()
    print('PASS decoding, exact dimensions and stripped EXIF for all portfolio images/posters')


def check_videos(metadata):
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    sources = {f'assets/videos/{video}': (source, poster) for source, video, poster in VIDEOS}
    with TemporaryDirectory(prefix='tone4d-media-check-') as temporary:
        qa = Path(temporary)
        for item in (entry for entry in metadata if entry['type'] == 'video'):
            source, poster = sources[item['src']]
            path = OUT / item['src']
            result = subprocess.run([ffmpeg, '-v', 'error', '-i', str(path), '-f', 'null', '-'], capture_output=True, text=True)
            assert result.returncode == 0, result.stderr
            boxes = []
            with path.open('rb') as stream:
                while True:
                    header = stream.read(8)
                    if len(header) < 8:
                        break
                    size, kind = struct.unpack('>I4s', header)
                    boxes.append(kind)
                    header_size = 8
                    if size == 1:
                        size = struct.unpack('>Q', stream.read(8))[0]
                        header_size = 16
                    if size == 0:
                        break
                    assert size >= header_size
                    stream.seek(size - header_size, 1)
            assert boxes.index(b'moov') < boxes.index(b'mdat'), ('Missing faststart', path.name)
            frame = qa / (path.name + '.jpg')
            subprocess.run([ffmpeg, '-v', 'error', '-y', '-ss', '00:00:01', '-i', str(ROOT / 'images' / source),
                            '-frames:v', '1', '-vf', 'scale=960:-2', '-q:v', '4', str(frame)], check=True)
            with Image.open(frame) as image:
                image.thumbnail((960, 960), Image.Resampling.LANCZOS)
                expected = qa / (poster + '.expected.jpg')
                image.save(expected, 'JPEG', quality=70, progressive=True, optimize=True)
            with Image.open(OUT / item['poster']) as actual, Image.open(expected) as expected_image:
                assert actual.size == expected_image.size
                error = sum(ImageStat.Stat(ImageChops.difference(actual.convert('RGB'), expected_image.convert('RGB'))).mean) / 3
                assert error < 2, (path.name, 'Poster mismatch', error)
            print('PASS full decoding, faststart and corresponding poster:', path.name, 'mean error', round(error, 3))


def check_consumers_and_deployment():
    for name in ('script.js', 'admin.html', 'images-map.html', 'build_site.py'):
        text = (ROOT / name).read_text(encoding='utf-8')
        assert 'assets/metadata.json' in text and 'gallery/metadata.json' not in text, ('Wrong metadata consumer', name)
    config = read_json(ROOT / 'vercel.json')
    assert config['framework'] is None and config['outputDirectory'] == 'dist'
    assert config['buildCommand'] == 'python3 build_site.py'
    assert not config.get('builds') and 'entrypoint' not in json.dumps(config).lower()
    print('PASS authoritative metadata consumers and preserved static Vercel configuration')


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--base', default='http://127.0.0.1:8080/', help='URL serving generated dist')
    args = parser.parse_args()
    assert OUT.is_dir(), 'Run python build_site.py first'
    metadata = read_json(ROOT / 'assets/metadata.json')
    mapping = read_json(ROOT / 'media-update-mapping.json')
    categories = check_manifest(metadata)
    check_dist(metadata)
    snapshot, removed_refs = check_preservation(metadata, mapping)
    check_new_inventory(metadata, snapshot, mapping)
    check_consumers_and_deployment()
    check_http(args.base.rstrip('/') + '/', metadata, categories, removed_refs)
    check_images(metadata)
    check_videos(metadata)
    print('Portfolio counts:', dict(Counter(item['type'] for item in metadata)))
    print('Images by category:', dict(sorted(Counter(item['category'] for item in metadata if item['type'] == 'image').items())))
    print('New images by category:', dict(sorted(Counter(item['category'] for item in mapping['new_images'] if item['status'] == 'added').items())))
    print('PASS filesystem, HTTP, source preservation and media checks.')
    print('UNVERIFIED here: browser layouts, interactive filters/viewer/keyboard focus, native playback, console errors and external map destination.')


if __name__ == '__main__':
    main()
