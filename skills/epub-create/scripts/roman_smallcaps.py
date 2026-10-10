"""Romanos devem ser palavras completas, mesmo quando divididas em spans."""
import re
from lxml import etree as E

X = 'http://www.w3.org/1999/xhtml'
BLOCKS = {'p','h1','h2','h3','figcaption','th'}
ROMAN = re.compile(r'\b[IVXLCDM]+\b')
CANONICAL = re.compile(r'M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})')


def mark_roman_smallcaps(root):
    count = 0
    for block in list(root.iter()):
        if not isinstance(block.tag,str) or E.QName(block).localname not in BLOCKS:
            continue
        if any(E.QName(e).localname in BLOCKS for e in block.iterdescendants() if isinstance(e.tag,str)):
            continue
        slots = []
        def collect(node):
            if node.text:
                slots.append((node,False,node.text))
            for child in node:
                collect(child)
                if child.tail:
                    slots.append((child,True,child.tail))
        collect(block)
        text = ''.join(value for _,_,value in slots)
        matches = [m for m in ROMAN.finditer(text) if CANONICAL.fullmatch(m[0])]
        offset = 0
        for node,tail,value in slots:
            selected = [m for m in matches if offset <= m.start() and m.end() <= offset+len(value)]
            if node.get('class') == 'roman-smallcaps' and not tail:
                selected = []
            if selected:
                parent = node.getparent() if tail else node
                position = parent.index(node)+1 if tail else 0
                prefix = value[:selected[0].start()-offset]
                if tail:
                    node.tail = prefix
                else:
                    node.text = prefix
                for i,m in enumerate(selected):
                    span = E.Element(f'{{{X}}}span',{'class':'roman-smallcaps'})
                    span.text = m[0]
                    end = selected[i+1].start()-offset if i+1<len(selected) else len(value)
                    span.tail = value[m.end()-offset:end]
                    parent.insert(position,span)
                    position += 1
                    count += 1
            offset += len(value)
        assert ''.join(block.itertext()) == text
    return count


if __name__ == '__main__':
    root = E.fromstring(f'<div xmlns="{X}"><p><span>I</span><span>mortalidade</span>; cap. XIV; <span>CL</span>areza.</p></div>')
    assert mark_roman_smallcaps(root) == 1
    assert root.xpath('//*[local-name()="span" and @class="roman-smallcaps"]/text()') == ['XIV']
    assert mark_roman_smallcaps(root) == 0
    print('OK: palavras fragmentadas não são romanos; XIV é preservado; aplicação idempotente.')
