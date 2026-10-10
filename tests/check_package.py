"""Small offline checks for manifests, links, helpers and packaging round-trip."""
from pathlib import Path
import ast
import importlib.util
import json
import re
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/epub-create'

def load(name):
    spec = importlib.util.spec_from_file_location(name, SKILL/'scripts'/f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    manifest = json.loads((ROOT/'plugin.json').read_text())
    claude = json.loads((ROOT/'.claude-plugin/plugin.json').read_text())
    assert manifest['name'] == claude['name'] == 'epub-create'
    assert manifest['version'] == claude['version'] == '0.1.0'
    assert manifest['license'] == claude['license'] == 'MIT'
    for file in (ROOT/'.agents/plugins/marketplace.json', ROOT/'.claude-plugin/marketplace.json'):
        market = json.loads(file.read_text())
        entry = market['plugins'][0]
        assert entry['name'] == manifest['name']
        source = entry['source']
        path = source['path'] if isinstance(source,dict) else source
        assert (ROOT/path).resolve() == ROOT
    frontmatter = (SKILL/'SKILL.md').read_text().split('---',2)[1]
    assert 'name: epub-create' in frontmatter and 'description:' in frontmatter
    for file in ROOT.rglob('*.md'):
        for href in re.findall(r'\]\(([^)]+)\)',file.read_text()):
            if not href.startswith(('https://','http://','#')):
                assert (file.parent/href.split('#')[0]).exists(), (file,href)
    for file in SKILL.rglob('*.py'):
        ast.parse(file.read_text(),filename=str(file))
    for file in ROOT.rglob('*'):
        if file.is_file() and '.git' not in file.parts and file.suffix not in ('.pyc',):
            assert file.suffix.lower() not in ('.epub','.pdf','.ttf','.otf','.odt','.docx'), file
            if file.suffix in ('.py','.md','.json','.yaml'):
                assert not re.search(r'/mnt/[a-z]/(?:Users|Projetos)/',file.read_text()), file
    load('editorial_audit').self_test()
    package = load('epub_package')
    with tempfile.TemporaryDirectory() as temp:
        base = Path(temp)
        epub = base/'test.epub'
        files = {
            'META-INF/container.xml':'<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/package.opf"/></rootfiles></container>',
            'OEBPS/package.opf':'<package xmlns="http://www.idpf.org/2007/opf"><manifest><item id="c" href="chapter.xhtml" media-type="application/xhtml+xml"/></manifest><spine><itemref idref="c"/></spine></package>',
            'OEBPS/chapter.xhtml':'<html xmlns="http://www.w3.org/1999/xhtml"><body><p id="text">Bodhidharma e Zen.</p><a href="#text">Retorno</a></body></html>'
        }
        with zipfile.ZipFile(epub,'w',compression=zipfile.ZIP_DEFLATED) as z:
            z.writestr('mimetype','application/epub+zip',compress_type=zipfile.ZIP_STORED)
            for name,content in files.items(): z.writestr(name,content)
        assert package.check_epub(epub) == {'manifest':1,'spine':1,'xhtml':1,'links':1}
        extracted = base/'extracted'
        package.unpack(epub,extracted)
        rebuilt = base/'rebuilt.epub'
        package.pack(extracted,rebuilt)
        with zipfile.ZipFile(epub) as a, zipfile.ZipFile(rebuilt) as b:
            assert {n:a.read(n) for n in a.namelist()} == {n:b.read(n) for n in b.namelist()}
        with zipfile.ZipFile(base/'unsafe.zip','w') as z:
            z.writestr('../outside.txt','bad')
        try:
            package.unpack(base/'unsafe.zip',base/'unsafe')
        except ValueError:
            pass
        else:
            raise AssertionError('Unsafe ZIP path accepted')
    print('OK: manifests, references, no private paths/assets, editorial audit, EPUB round-trip and unsafe ZIP rejection.')

if __name__ == '__main__':
    main()
