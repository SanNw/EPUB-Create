"""Read-only lexical audit. Classification comes from a researched JSON registry.

python editorial_audit.py BOOK.epub registry.json [--forbid-bold]
python editorial_audit.py --self-test
Reports markup/inline styles, not the computed CSS cascade of an EPUB reader.
"""
import argparse
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

BLOCKS = {'p', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'figcaption', 'td', 'th'}

def local(e):
    return e.tag.rsplit('}', 1)[-1]

def flatten(e, italic=False, bold=False):
    tag = local(e)
    style = dict(re.findall(r'([\w-]+)\s*:\s*([^;]+)', e.get('style', '').lower()))
    italic = italic or tag in ('em', 'i')
    bold = bold or tag in ('strong', 'b')
    if 'font-style' in style:
        italic = style['font-style'].strip() in ('italic', 'oblique')
    if 'font-weight' in style:
        weight = style['font-weight'].strip()
        bold = weight in ('bold', 'bolder') or (weight.isdigit() and int(weight) > 400)
    text = e.text or ''
    flags = [(italic, bold)] * len(text)
    for child in e:
        value, child_flags = flatten(child, italic, bold)
        if local(child) == 'br':
            value, child_flags = '\n', [(italic, bold)]
        text += value
        flags += child_flags
        tail = child.tail or ''
        text += tail
        flags += [(italic, bold)] * len(tail)
    return text, flags

def audit_document(data, terms, forbid_bold=False):
    root = ET.fromstring(data)
    findings, counts, states = [], {}, {}
    for block in root.iter():
        if local(block) not in BLOCKS or any(local(c) in BLOCKS for c in list(block.iter())[1:]):
            continue
        text, flags = flatten(block)
        title_ranges = []
        for term in terms:
            if term['kind'] == 'work':
                title_ranges += [m.span() for m in re.finditer(r'(?<!\w)'+re.escape(term['text'])+r'(?!\w)', text)]
        for term in terms:
            name = term['text']
            for match in re.finditer(r'(?<!\w)'+re.escape(name)+r'(?!\w)', text):
                counts[name] = counts.get(name, 0)+1
                marks = [flags[i][0] for i in range(*match.span()) if not text[i].isspace()]
                actual = 'italic' if all(marks) else 'roman' if not any(marks) else 'partial'
                states.setdefault(name, set()).add(actual)
                expected = term['style']
                if term['kind'] in ('person', 'place', 'institution') and any(a <= match.start() and match.end() <= b for a,b in title_ranges):
                    expected = 'italic'
                if actual != expected:
                    findings.append({'term': name, 'expected': expected, 'actual': actual, 'context': text[max(0,match.start()-35):match.end()+35]})
        if forbid_bold and any(b for _,b in flags):
            findings.append({'issue': 'bold_markup', 'context': text[:100]})
    return findings, counts, states

def self_test():
    terms = [{'text':'Bodhidharma','kind':'person','style':'roman'},
             {'text':'Zen','kind':'tradition','style':'roman'},
             {'text':'Vida de Bodhidharma','kind':'work','style':'italic'}]
    good = '<html><p>Bodhi<span>dharma</span>; Zen.</p><p><em>Vida de Bodhidharma</em></p></html>'
    assert not audit_document(good,terms)[0]
    bad = '<html><p><em>Bodhi</em>dharma; <em>Zen</em>; <strong>texto</strong></p><p>Zen</p></html>'
    errors,counts,states = audit_document(bad,terms,True)
    assert len(errors) == 3 and counts['Zen'] == 2 and states['Zen'] == {'italic','roman'}
    assert not audit_document('<html><p>Bodhi</p><p>dharma</p></html>',terms)[1]
    print('OK: nomes fragmentados, título contendo pessoa, inconsistência, negrito e limites de parágrafo.')

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('epub', nargs='?')
    p.add_argument('registry', nargs='?')
    p.add_argument('--forbid-bold', action='store_true')
    p.add_argument('--self-test', action='store_true')
    args = p.parse_args()
    if args.self_test:
        self_test()
        return
    if not args.epub or not args.registry:
        p.error('Supply EPUB and registry JSON')
    terms = json.loads(Path(args.registry).read_text(encoding='utf-8'))['terms']
    for t in terms:
        if not t.get('text') or t.get('style') not in ('roman','italic') or t.get('kind') not in ('person','place','institution','tradition','foreign','work') or not re.match(r'https?://',t.get('source','')):
            p.error('Each term needs text, kind, style and researched HTTP(S) source')
    findings,counts,states,css = [],{}, {}, []
    with zipfile.ZipFile(args.epub) as z:
        for name in z.namelist():
            if name.endswith(('.xhtml','.html','.htm')):
                errors,hits,modes = audit_document(z.read(name),terms,args.forbid_bold)
                findings.extend(dict(e,file=name) for e in errors)
                for term,count in hits.items(): counts[term] = counts.get(term,0)+count
                for term,values in modes.items(): states.setdefault(term,set()).update(values)
            elif args.forbid_bold and name.endswith('.css'):
                if re.search(r'font-weight\s*:\s*(?:bold(?:er)?|[5-9]00)\b',z.read(name).decode('utf-8'),re.I):
                    css.append(name)
    report = {'findings':findings,'occurrences':counts,'mixed_terms':{k:sorted(v) for k,v in states.items() if len(v)>1},'css_bold_review':css,'not_found':[t['text'] for t in terms if t['text'] not in counts],'limitation':'Markup and inline styles only; verify computed CSS and unclassified terms separately.'}
    print(json.dumps(report,ensure_ascii=False,indent=2))
    raise SystemExit(1 if findings or css else 0)

if __name__ == '__main__':
    main()
