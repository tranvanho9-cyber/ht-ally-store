#!/usr/bin/env python3
"""Sinh catalog.json từ plugins.json + các file .rbz trong rbz/.

Quy ước tên file: <rbz_prefix>_v<số>_<số>_<số>.rbz  (vd dc_explode_v5_3_2.rbz).
Với mỗi plugin lấy bản có số phiên bản CAO NHẤT -> version + rbz_url trong catalog.
Chạy tự động bằng GitHub Actions mỗi khi bạn đưa file .rbz mới lên (xem .github/workflows).
Chạy tay:  python tools/build_catalog.py --base https://raw.githubusercontent.com/USER/REPO/main
"""
import argparse, json, os, re, sys, urllib.parse, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def latest(prefix, files):
    pat = re.compile(r'^' + re.escape(prefix) + r'_v(\d+(?:_\d+)*)\.rbz$', re.I)
    best = None
    for f in files:
        m = pat.match(f)
        if not m:
            continue
        ver = tuple(int(x) for x in m.group(1).split('_'))
        if best is None or ver > best[0]:
            best = (ver, f)
    return best


def _str(txt, pat):
    m = re.search(pat + r"""\s*=?\s*(?:'((?:[^'\\]|\\.)*)'|"((?:[^"\\]|\\.)*)")""", txt)
    return (m.group(1) or m.group(2)).replace("\\'", "'") if m else ''


def auto_entry(prefix, fname):
    """Tự đọc thông tin plugin từ chính file .rbz (loader .rb ngoài cùng không mã hóa)."""
    try:
        z = zipfile.ZipFile(os.path.join(ROOT, 'rbz', fname))
        names = z.namelist()
        loaders = [n for n in names if n.endswith('.rb') and '/' not in n]
        if not loaders:
            return None
        loader = loaders[0]
        folder = loader[:-3]
        if not any(n.startswith(folder + '/') for n in names):
            return None
        txt = z.read(loader).decode('utf-8', 'ignore')
        name = _str(txt, r'PLUGIN_NAME') or _str(txt, r'SketchupExtension\.new\(') or prefix
        desc = _str(txt, r'\.description')
        return {'id': prefix.lower(), 'name': name, 'desc': desc, 'category': 'Khác', 'price': 0,
                'loader': loader, 'folder': folder, 'rbz_prefix': prefix}
    except Exception as ex:
        print('! Không đọc được %s: %s' % (fname, ex))
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default=os.environ.get('BASE_URL', ''))
    a = ap.parse_args()
    base = a.base.rstrip('/')
    if not base and os.environ.get('GITHUB_REPOSITORY'):
        branch = os.environ.get('GITHUB_REF_NAME', 'main')
        base = 'https://raw.githubusercontent.com/%s/%s' % (os.environ['GITHUB_REPOSITORY'], branch)
    if not base:
        sys.exit('Thiếu --base (địa chỉ gốc chứa thư mục rbz/)')

    src = json.load(open(os.path.join(ROOT, 'plugins.json'), encoding='utf-8'))
    files = os.listdir(os.path.join(ROOT, 'rbz'))

    def url(fname):
        return base + '/rbz/' + urllib.parse.quote(fname)

    meta = dict(src.get('meta', {}))
    hub = src.get('hub')
    if hub:
        b = latest(hub['rbz_prefix'], files)
        if b:
            meta['hub'] = {'version': '.'.join(map(str, b[0])), 'rbz_url': url(b[1]), 'notes': hub.get('notes', '')}

    plugins = list(src['plugins'])
    known = {p['rbz_prefix'].lower() for p in plugins}
    if hub:
        known.add(hub['rbz_prefix'].lower())
    seen = set()
    for f in sorted(files):
        m = re.match(r'^(.+)_v\d+(?:_\d+)*\.rbz$', f, re.I)
        if not m or m.group(1).lower() in known or m.group(1).lower() in seen:
            continue
        seen.add(m.group(1).lower())
        b = latest(m.group(1), files)
        e = auto_entry(m.group(1), b[1])
        if e:
            print('Tự thêm plugin mới: %s' % e['id'])
            plugins.append(e)

    out = []
    for p in plugins:
        b = latest(p['rbz_prefix'], files)
        paid = int(p.get('price', 0)) > 0
        if not b and not (paid and p.get('version')):
            print('! Bỏ qua %s: không có file %s_vX_Y_Z.rbz trong rbz/ (plugin có phí cần khai báo "version" trong plugins.json)' % (p['id'], p['rbz_prefix']))
            continue
        e = {k: v for k, v in p.items() if k != 'rbz_prefix'}
        # Plugin có phí: file nằm ở kho riêng, version khai báo tay trong plugins.json
        e['version'] = str(p['version']) if (paid and p.get('version')) else '.'.join(map(str, b[0]))
        if int(e.get('price', 0)) <= 0:
            e['rbz_url'] = url(b[1])
        else:
            e['rbz_url'] = ''  # có phí: link tải do máy chủ bản quyền trả về
        if not e.get('icon') and os.path.isfile(os.path.join(ROOT, 'icons', p['id'] + '.png')):
            e['icon'] = base + '/icons/' + urllib.parse.quote(p['id']) + '.png'
        out.append(e)
        print('%s -> %s' % (p['id'], b[1] if b else '(kho riêng, version %s)' % e['version']))

    json.dump({'meta': meta, 'plugins': out}, open(os.path.join(ROOT, 'catalog.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=2)
    print('Đã ghi catalog.json (%d plugin)' % len(out))


if __name__ == '__main__':
    main()
