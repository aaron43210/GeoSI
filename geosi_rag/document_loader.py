"""
GeoSI RAG — Document Loader
═══════════════════════════════════════════════════════════════════

Loads documents from multiple formats for the RAG pipeline:
    - Markdown (.md)
    - Plain text (.txt)
    - HTML (.html, .htm)
    - PDF (.pdf)
    - reStructuredText (.rst)

Each loaded document is returned as a Document dataclass containing
the extracted text, source path, format, and metadata.
"""

import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("geosi_rag.document_loader")

# Supported file extensions → format label
_SUPPORTED_FORMATS = {
    ".md": "markdown",
    ".txt": "text",
    ".html": "html",
    ".htm": "html",
    ".pdf": "pdf",
    ".rst": "rst",
}


@dataclass
class Document:
    """
    A loaded document ready for chunking and embedding.

    Attributes:
        content: Extracted text content
        source_path: Original file path
        format: Document format (markdown, text, html, pdf, rst)
        metadata: Extra metadata (title, author, page count, etc.)
    """

    content: str
    source_path: str = ""
    format: str = "text"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __repr__(self):
        length = len(self.content)
        return f"Document(source={self.source_path!r}, format={self.format}, chars={length})"

    def __len__(self):
        return len(self.content)


class DocumentLoader:
    """
    Loads documents from files and directories.

    Supports: .md, .txt, .html, .htm, .pdf, .rst

    Usage:
        loader = DocumentLoader()
        doc = loader.load_file("docs/qgis_buffer.md")
        docs = loader.load_directory("data/qgis_docs/")
    """

    def load_file(self, path: str) -> Optional[Document]:
        """
        Load a single file into a Document.

        Args:
            path: Path to the file.

        Returns:
            Document with extracted text, or None if format unsupported.
        """
        path = str(path)
        ext = os.path.splitext(path)[1].lower()

        if ext not in _SUPPORTED_FORMATS:
            logger.warning(f"Unsupported format '{ext}' for file: {path}")
            return None

        fmt = _SUPPORTED_FORMATS[ext]

        try:
            if fmt in ("markdown", "text"):
                content = self._load_text(path)
            elif fmt == "html":
                content = self._load_html(path)
            elif fmt == "pdf":
                content = self._load_pdf(path)
            elif fmt == "rst":
                content = self._load_rst(path)
            else:
                content = self._load_text(path)

            if not content or not content.strip():
                logger.warning(f"Empty content from file: {path}")
                return None

            doc = Document(
                content=content.strip(),
                source_path=path,
                format=fmt,
                metadata={
                    "filename": os.path.basename(path),
                    "size_bytes": os.path.getsize(path),
                },
            )
            logger.debug(f"Loaded {fmt} document: {path} ({len(content)} chars)")
            return doc

        except Exception as e:
            logger.error(f"Failed to load file '{path}': {e}")
            return None

    def load_directory(
        self,
        dir_path: str,
        recursive: bool = True,
    ) -> List[Document]:
        """
        Load all supported documents from a directory.

        Args:
            dir_path: Directory to scan.
            recursive: If True, scan subdirectories too.

        Returns:
            List of loaded Documents.
        """
        documents = []
        dir_path = str(dir_path)

        if not os.path.isdir(dir_path):
            logger.error(f"Directory not found: {dir_path}")
            return documents

        pattern = "**/*" if recursive else "*"
        for filepath in Path(dir_path).glob(pattern):
            if filepath.is_file():
                ext = filepath.suffix.lower()
                if ext in _SUPPORTED_FORMATS:
                    doc = self.load_file(str(filepath))
                    if doc:
                        documents.append(doc)

        logger.info(f"Loaded {len(documents)} documents from '{dir_path}'")
        return documents

    # ── Format-specific loaders ────────────────────────────────────────

    @staticmethod
    def _load_text(path: str) -> str:
        """Load plain text or markdown file."""
        with open(path, encoding="utf-8", errors="ignore") as f:
            return f.read()

    @staticmethod
    def _load_html(path: str) -> str:
        """Load HTML file, extract text via BeautifulSoup."""
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            logger.warning(
                "beautifulsoup4 not installed — falling back to raw text "
                "for HTML files. Install with: pip install beautifulsoup4"
            )
            with open(path, encoding="utf-8", errors="ignore") as f:
                return f.read()

        with open(path, encoding="utf-8", errors="ignore") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        # Remove script and style elements
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        # Extract text with newlines between block elements
        text = soup.get_text(separator="\n", strip=True)
        # Collapse multiple blank lines
        lines = [line.strip() for line in text.splitlines()]
        return "\n".join(line for line in lines if line)

    @staticmethod
    def _load_pdf(path: str) -> str:
        """Load PDF file, extract text via pdfplumber."""
        try:
            import pdfplumber
        except ImportError:
            logger.warning("pdfplumber not installed — cannot load PDF files. " "Install with: pip install pdfplumber")
            return ""

        text_parts = []
        try:
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
        except Exception as e:
            logger.error(f"PDF extraction failed for '{path}': {e}")
            return ""

        return "\n\n".join(text_parts)

    @staticmethod
    def _load_rst(path: str) -> str:
        """
        Load reStructuredText file.

        Tries docutils for proper parsing, falls back to raw text.
        """
        try:
            from docutils.core import publish_parts

            with open(path, encoding="utf-8", errors="ignore") as f:
                rst_content = f.read()
            parts = publish_parts(rst_content, writer_name="html")
            # Parse the HTML output to get clean text
            try:
                from bs4 import BeautifulSoup

                soup = BeautifulSoup(parts["html_body"], "html.parser")
                return soup.get_text(separator="\n", strip=True)
            except ImportError:
                return rst_content
        except ImportError:
            logger.debug("docutils not installed — loading RST as plain text")
            with open(path, encoding="utf-8", errors="ignore") as f:
                return f.read()
