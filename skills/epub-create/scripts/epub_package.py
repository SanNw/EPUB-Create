#!/usr/bin/env python3
"""Extrai, confere e reempacota EPUBs sem dependências externas."""

from __future__ import annotations

import argparse
import tempfile
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET


XML_SUFFIXES = {".xml", ".xhtml", ".opf", ".ncx", ".svg"}
JUNK_NAMES = {".DS_Store", "Thumbs.db"}
CONTAINER_NS = {"c": "urn:oasis:names:tc:opendocument:xmlns:container"}
OPF_NS = {"opf": "http://www.idpf.org/2007/opf"}
XHTML_NS = "http://www.w3.org/1999/xhtml"


def safe_members(archive: zipfile.ZipFile) -> list[zipfile.ZipInfo]:
    members = archive.infolist()
    for member in members:
        path = PurePosixPath(member.filename)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"Caminho inseguro no ZIP: {member.filename}")
    return members


def check_archive(path: Path) -> None:
    with zipfile.ZipFile(path) as archive:
        members = safe_members(archive)
        if not members or members[0].filename != "mimetype":
            raise ValueError("mimetype não é o primeiro item do EPUB")
        if members[0].compress_type != zipfile.ZIP_STORED:
            raise ValueError("mimetype está comprimido")
        if archive.read("mimetype") != b"application/epub+zip":
            raise ValueError("conteúdo de mimetype inválido")
        bad = archive.testzip()
        if bad:
            raise ValueError(f"CRC inválido: {bad}")


def parse(path: Path) -> ET.Element:
    try:
        return ET.parse(path).getroot()
    except ET.ParseError as error:
        raise ValueError(f"XML inválido em {path}: {error}") from error


def local_target(base_file: Path, href: str) -> tuple[Path | None, str]:
    split = urlsplit(href)
    if split.scheme or split.netloc:
        return None, ""
    decoded = unquote(split.path)
    target = (base_file.parent / decoded).resolve() if decoded else base_file.resolve()
    return target, unquote(split.fragment)


def inside(root: Path, path: Path) -> bool:
    return path == root or root in path.parents


def check_tree(root: Path) -> dict[str, int]:
    root = root.resolve()
    mimetype = root / "mimetype"
    if not mimetype.is_file() or mimetype.read_bytes() != b"application/epub+zip":
        raise ValueError("mimetype ausente ou inválido")
    container = root / "META-INF" / "container.xml"
    if not container.is_file():
        raise ValueError("META-INF/container.xml ausente")

    for path in root.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"Link simbólico não permitido no pacote: {path}")
        if path.is_file() and path.suffix.lower() in XML_SUFFIXES:
            parse(path)

    rootfiles = parse(container).findall("c:rootfiles/c:rootfile", CONTAINER_NS)
    if not rootfiles:
        raise ValueError("Nenhum rootfile declarado em container.xml")

    manifest_count = spine_count = xhtml_count = link_count = 0
    xhtml_files: set[Path] = set()
    for rootfile in rootfiles:
        full_path = rootfile.attrib.get("full-path", "")
        opf_path = (root / unquote(full_path)).resolve()
        if not inside(root, opf_path) or not opf_path.is_file():
            raise ValueError(f"Rootfile ausente ou inseguro: {full_path}")
        opf = parse(opf_path)
        manifest: dict[str, Path] = {}
        for item in opf.findall("opf:manifest/opf:item", OPF_NS):
            item_id = item.attrib.get("id")
            href = item.attrib.get("href")
            if not item_id or not href:
                raise ValueError(f"Item incompleto no manifesto: {opf_path}")
            target, _ = local_target(opf_path, href)
            if target is None or not inside(root, target) or not target.is_file():
                raise ValueError(f"Recurso do manifesto ausente ou inseguro: {href}")
            manifest[item_id] = target
            if item.attrib.get("media-type") == "application/xhtml+xml":
                xhtml_files.add(target)
        manifest_count += len(manifest)
        for itemref in opf.findall("opf:spine/opf:itemref", OPF_NS):
            idref = itemref.attrib.get("idref", "")
            if idref not in manifest:
                raise ValueError(f"Item da spine ausente do manifesto: {idref}")
            spine_count += 1

    ids_by_file: dict[Path, set[str]] = {}
    for path in xhtml_files:
        ids: set[str] = set()
        for element in parse(path).iter():
            element_id = element.attrib.get("id")
            if element_id and element_id in ids:
                raise ValueError(f"ID duplicado em {path}: {element_id}")
            if element_id:
                ids.add(element_id)
        ids_by_file[path] = ids
        xhtml_count += 1

    anchor_tag = f"{{{XHTML_NS}}}a"
    for path in xhtml_files:
        for element in parse(path).iter(anchor_tag):
            href = element.attrib.get("href")
            if not href:
                continue
            target, fragment = local_target(path, href)
            if target is None:
                continue
            if not inside(root, target) or not target.is_file():
                raise ValueError(f"Link quebrado em {path.relative_to(root)}: {href}")
            if fragment and target in ids_by_file and fragment not in ids_by_file[target]:
                raise ValueError(f"Âncora inexistente em {path.relative_to(root)}: {href}")
            link_count += 1

    return {
        "manifest": manifest_count,
        "spine": spine_count,
        "xhtml": xhtml_count,
        "links": link_count,
    }


def unpack(source: Path, destination: Path) -> None:
    if destination.exists() and (not destination.is_dir() or any(destination.iterdir())):
        raise ValueError(f"Destino não está vazio: {destination}")
    destination.mkdir(parents=True, exist_ok=True)
    check_archive(source)
    with zipfile.ZipFile(source) as archive:
        archive.extractall(destination, safe_members(archive))
    check_tree(destination)


def pack(source: Path, output: Path) -> None:
    if output.exists():
        raise ValueError(f"Saída já existe; escolha outro nome: {output}")
    check_tree(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w") as archive:
        archive.write(source / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
        for path in sorted(source.rglob("*")):
            if not path.is_file() or path == source / "mimetype":
                continue
            relative = path.relative_to(source)
            if path.name in JUNK_NAMES or "__MACOSX" in relative.parts:
                continue
            archive.write(path, relative.as_posix(), compress_type=zipfile.ZIP_DEFLATED)
    check_archive(output)


def check_epub(path: Path) -> dict[str, int]:
    check_archive(path)
    with tempfile.TemporaryDirectory(prefix="epub_refinado_") as temporary:
        root = Path(temporary)
        with zipfile.ZipFile(path) as archive:
            archive.extractall(root, safe_members(archive))
        return check_tree(root)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    unpack_parser = commands.add_parser("unpack", help="extrair e conferir um EPUB")
    unpack_parser.add_argument("source", type=Path)
    unpack_parser.add_argument("destination", type=Path)
    pack_parser = commands.add_parser("pack", help="conferir e criar um EPUB")
    pack_parser.add_argument("source", type=Path)
    pack_parser.add_argument("output", type=Path)
    check_parser = commands.add_parser("check", help="conferir um EPUB ou pasta extraída")
    check_parser.add_argument("target", type=Path)
    args = parser.parse_args()

    if args.command == "unpack":
        unpack(args.source.resolve(), args.destination.resolve())
        print(args.destination.resolve())
    elif args.command == "pack":
        pack(args.source.resolve(), args.output.resolve())
        print(args.output.resolve())
    else:
        target = args.target.resolve()
        result = check_tree(target) if target.is_dir() else check_epub(target)
        print("OK " + " ".join(f"{key}={value}" for key, value in result.items()))


if __name__ == "__main__":
    main()
