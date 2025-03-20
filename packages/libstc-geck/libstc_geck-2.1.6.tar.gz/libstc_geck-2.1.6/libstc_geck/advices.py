from collections import OrderedDict
from typing import Optional

TEMPORAL_RANKING_FORMULA = "original_score * custom_score * fastsigm(abs(now - issued_at) / (86400 * 3) + 5, -1)"
PR_TEMPORAL_RANKING_FORMULA = (
    f"{TEMPORAL_RANKING_FORMULA} * fastsigm(iqpr(quantized_page_rank), 0.15)"
)


default_field_aliases = {
    "author": "authors.family",
    "authors": "authors.family",
    "ev": "metadata.event.name",
    "isbn": "metadata.isbns",
    "isbns": "metadata.isbns",
    "issn": "metadata.issns",
    "issns": "metadata.issns",
    "lang": "languages",
    "language": "language",
    "nid": "id",
    "pub": "metadata.publisher",
    "rd": "references.doi",
    "ser": "metadata.series",
}


default_field_boosts = {
    "authors": 1.7,
    "title": 1.85,
}


def format_document(document: dict):
    parts = []
    if title := document.get("title"):
        parts.append(f"Title: {title}")
    if authors := document.get("authors"):
        parts.append(f"Authors: {authors}")
    if id_ := document.get("id"):
        parts.append(f"ID: {id_}")
    if links := document.get("links"):
        parts.append(f"Links: {links}")
    if abstract := document.get("abstract"):
        parts.append(f"Abstract: {abstract[:200]}")
    return "\n".join(parts)


def plain_author(author):
    text = None
    if "family" in author and "given" in author:
        text = f"{author['given']} {author['family']}"
    elif "family" in author or "given" in author:
        text = author.get("family") or author.get("given")
    elif "name" in author:
        text = author["name"]
    return text


class BaseDocumentHolder:
    def __init__(self, document):
        self.document = document

    def __getattr__(self, name):
        if name in self.document:
            return self.document[name]
        if name == "content":
            return
        elif "metadata" in self.document and name in self.document["metadata"]:
            return self.document["metadata"][name]
        elif "id" in self.document and name in self.document["id"]:
            return self.document["id"][name]

    def has_cover(self):
        return bool(self.isbns and len(self.isbns) > 0)

    def has_field(self, name):
        return name in self.document or name in self.document.get("metadata", {})
