"""Generate the README directory and validate local Markdown without dependencies."""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import quote, urlsplit, parse_qs

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- DIRECTORY:START -->'
END = '<!-- DIRECTORY:END -->'
LABELS = {'confirme_source_officielle': '✅ Source officielle', 'a_confirmer': '◐ À confirmer', 'non_identifie': '— Non identifié'}

def table():
    rows = json.loads((ROOT / 'data/organizations.json').read_text(encoding='utf-8'))
    assert len({r['id'] for r in rows}) == len(rows), 'Duplicate IDs'
    result = ['| ID | Pays / territoire | Organisation | Type / élément | Instagram | Facebook | Vérification (IG / FB) | Mise à jour |', '|---|---|---|---|---|---|---|---|']
    for row in rows:
        assert re.fullmatch(r'CW-\d{3,}', row['id'])
        social = []
        for network in ('instagram', 'facebook'):
            url, status = row[network], row[network + '_status']
            assert status in LABELS
            assert bool(url) == (status != 'non_identifie')
            if url:
                parsed = urlsplit(url)
                assert parsed.scheme == 'https' and parsed.netloc == 'www.' + network + '.com'
                assert parsed.path.strip('/') and not parsed.query
            if status == 'confirme_source_officielle':
                assert row['sources'], 'Confirmed profiles require a source'
            social.append(f'[@{urlsplit(url).path.strip("/")}]({url})' if url else 'Non identifié')
        subject = f"Cadet World — mise à jour {row['id']} — {row['organization']}"
        mail = 'mailto:sprudhom@gmail.com?subject=' + quote(subject, safe='')
        assert parse_qs(urlsplit(mail).query)['subject'] == [subject]
        status = ' / '.join(LABELS[row[n + '_status']] for n in ('instagram', 'facebook'))
        status += ''.join(f' [Source {i}]({url})' for i, url in enumerate(row['sources'], 1))
        cells = [row['id'], row['country'], row['organization'], row['type'], *social, status, f'[✉ Signaler]({mail})']
        assert all('|' not in x and '\n' not in x for x in cells)
        result.append('| ' + ' | '.join(cells) + ' |')
    return '\n'.join(result)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    path = ROOT / 'README.md'
    old = path.read_text(encoding='utf-8')
    assert old.count(START) == old.count(END) == 1
    new = old.split(START)[0] + START + '\n\n' + table() + '\n\n' + END + old.split(END)[1]
    if args.check:
        assert old == new, 'README is out of sync; run python scripts/directory.py'
    else:
        path.write_text(new, encoding='utf-8')
    for md in ROOT.rglob('*.md'):
        content = md.read_text(encoding='utf-8')
        assert content.endswith('\n')
        assert not any(line.rstrip() != line for line in content.splitlines()), md
        assert sum(line.startswith('```') for line in content.splitlines()) % 2 == 0, md
        for target in re.findall(r'\]\(([^)]+)\)', content):
            parsed = urlsplit(target)
            if parsed.scheme:
                assert parsed.scheme in ('https', 'mailto'), (md, target)
                if parsed.scheme == 'https': assert parsed.netloc
            elif parsed.path:
                assert (md.parent / parsed.path).is_file(), (md, target)
    print('OK: data, unique IDs, Markdown structure, local links, README sync and mailto subjects.')

if __name__ == '__main__':
    main()
