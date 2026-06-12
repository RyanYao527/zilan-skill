import re
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGAMA_DIR = ROOT / "context" / "agama"
SOURCE_DIR = AGAMA_DIR / "_source"

NS = {"tei": "http://www.tei-c.org/ns/1.0"}
XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"

SKIP_TAGS = {"note", "sic", "orig", "teiHeader", "back"}
BLOCK_TAGS = {"p", "head", "byline", "lg", "l", "item", "list", "trailer"}

OUTPUTS = {
    "T01n0001": {
        "file": "T0001-chang-agama.md",
        "title": "長阿含經",
        "common": "长阿含经 / 阿含经长部",
        "note": "后秦佛陀耶舍共竺佛念译，22 卷",
    },
    "T01n0026": {
        "file": "T0026-zhong-agama.md",
        "title": "中阿含經",
        "common": "中阿含经 / 阿含经中部",
        "note": "东晋瞿昙僧伽提婆译，60 卷",
    },
    "T02n0099": {
        "file": "T0099-za-agama.md",
        "title": "雜阿含經",
        "common": "杂阿含经",
        "note": "刘宋求那跋陀罗译，50 卷",
    },
    "T02n0125": {
        "file": "T0125-ekottarika-agama.md",
        "title": "增壹阿含經",
        "common": "增壹阿含经 / 增一阿含经",
        "note": "东晋瞿昙僧伽提婆译，51 卷",
    },
}


def local_name(tag: str) -> str:
    return tag.split("}", 1)[-1] if "}" in tag else tag


def normalize_space(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"(?<!\n)\n(?!\n)", "", text)
    return text.strip()


def title_author_extent(root: ET.Element) -> tuple[str, str, str]:
    title = ""
    for item in root.findall(".//tei:titleStmt/tei:title", NS):
        if item.attrib.get(XML_LANG) == "zh-Hant" and item.attrib.get("level") == "m":
            title = "".join(item.itertext()).strip()
            break
    if not title:
        titles = root.findall(".//tei:titleStmt/tei:title", NS)
        title = "".join(titles[0].itertext()).strip() if titles else ""

    author_el = root.find(".//tei:titleStmt/tei:author", NS)
    extent_el = root.find(".//tei:extent", NS)
    author = "".join(author_el.itertext()).strip() if author_el is not None else ""
    extent = "".join(extent_el.itertext()).strip() if extent_el is not None else ""
    return title, author, extent


def append_text(elem: ET.Element, out: list[str]) -> None:
    name = local_name(elem.tag)
    if name in SKIP_TAGS:
        return
    if name == "milestone" and elem.attrib.get("unit") == "juan":
        n = elem.attrib.get("n", "")
        if n:
            label = int(n) if n.isdigit() else n
            out.append(f"\n\n## 卷 {label}\n\n")
        return
    if name == "pb":
        n = elem.attrib.get("n")
        if n:
            out.append(f"\n\n[{n}]\n")
        return
    if name == "lb":
        return
    if name in {"anchor", "mulu"}:
        return
    if name == "choice":
        preferred = elem.find("tei:corr", NS) or elem.find("tei:reg", NS)
        if preferred is not None:
            if preferred.text:
                out.append(preferred.text)
            for child in list(preferred):
                append_text(child, out)
                if child.tail:
                    out.append(child.tail)
        elif elem.text:
            out.append(elem.text)
        if elem.tail:
            out.append(elem.tail)
        return

    if name in BLOCK_TAGS:
        out.append("\n")
    if elem.text:
        out.append(elem.text)
    for child in list(elem):
        append_text(child, out)
        if child.tail:
            out.append(child.tail)
    if name in BLOCK_TAGS:
        out.append("\n")


def build_text_file(xml_path: Path) -> Path:
    root = ET.parse(xml_path).getroot()
    work_id = root.attrib.get(XML_ID, xml_path.stem)
    meta = OUTPUTS[work_id]
    title, author, extent = title_author_extent(root)
    body = root.find(".//tei:text/tei:body", NS)

    chunks: list[str] = []
    if body is not None:
        append_text(body, chunks)
    text = normalize_space("".join(chunks))

    md = [
        f"# {title or meta['title']}",
        "",
        "## 来源与使用边界",
        "",
        f"- 来源：CBETA XML-P5，`{work_id}`，原始 XML 保留于 `_source/{xml_path.name}`。",
        "- 使用：CBETA 资料要求非营利用途，并在传播、节录引用或再加工发行时保留说明与版本资讯；本文件仅作为 zilan-agent 的按需参考文本。",
        f"- 原始标题：{title or meta['title']}",
    ]
    if author:
        md.append(f"- 作译者：{author}")
    if extent:
        md.append(f"- 卷数：{extent}")
    md.extend(["", "## 正文", "", text, ""])

    out_path = AGAMA_DIR / meta["file"]
    out_path.write_text("\n".join(md), encoding="utf-8", newline="\n")
    return out_path


def build_index(paths: list[Path]) -> Path:
    rows = []
    for work_id, meta in OUTPUTS.items():
        rows.append(f"| {meta['common']} | {work_id.replace('n', 'n ')} | `{meta['file']}` | {meta['note']} |")

    index = "\n".join(
        [
            "# 阿含经文本索引",
            "",
            "## 加载时机",
            "",
            "当用户讨论《阿含经》、四阿含、早期佛教经典、九分教、十二分教、结集、声闻乘教法结构，或需要逐段引用《长阿含经》《中阿含经》《杂阿含经》《增壹阿含经》时，读取本索引，再按需读取对应经文文件。",
            "",
            "## 来源与版权说明",
            "",
            "- 文本来源：CBETA 正式 XML-P5 经文，官方仓库 `cbeta-org/xml-p5`。",
            "- CBETA 官方说明：该仓库为正式 TEI P5 XML 经文；版权说明要求非营利用途，传播、节录引用或再加工发行时保留说明与版本资讯。",
            "- 本目录保留 `_source/` 原始 XML 文件，以保留 CBETA 头部、版本和版权信息；Markdown 文件为便于 zilan-agent 按需阅读而生成的纯文本视图。",
            "- 讨论义理时，应以传承、注疏、师承讲解和上下文为准；本地文本主要用于检索、引用定位和结构分析。",
            "",
            "## 经文文件",
            "",
            "| 常用名 | CBETA 编号 | 文件 | 说明 |",
            "|---|---:|---|---|",
            *rows,
            "",
            "## 使用建议",
            "",
            "1. 若用户说“阿含经”但未指定部类，先确认问题对象；若只是总体讨论，使用本索引和 `SKILL.md` 中的《大藏经》映射模型即可。",
            "2. 若用户问具体经文、段落、主题或名相，先在四个 Markdown 文件中检索关键词，再读取相关上下文。",
            "3. 若用户要求逐字引用，优先引用短段，并注明经名、CBETA 编号和卷数。",
            "4. 若用户讨论传播史、结集或模因机制，可同时读取 `../模因机器视角下的佛教结集与传播.md`。",
            "",
        ]
    )
    out_path = AGAMA_DIR / "agama-index.md"
    out_path.write_text(index, encoding="utf-8", newline="\n")
    return out_path


def main() -> None:
    AGAMA_DIR.mkdir(parents=True, exist_ok=True)
    generated = []
    for xml_path in sorted(SOURCE_DIR.glob("T*.xml")):
        generated.append(build_text_file(xml_path))
    generated.append(build_index(generated))
    for path in generated:
        print(f"{path.name}\t{path.stat().st_size}")


if __name__ == "__main__":
    main()
