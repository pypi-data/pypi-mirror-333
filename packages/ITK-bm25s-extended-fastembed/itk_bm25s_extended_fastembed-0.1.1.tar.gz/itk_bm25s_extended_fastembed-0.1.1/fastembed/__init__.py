import importlib.metadata

from fastembed.image import ImageEmbedding
from fastembed.late_interaction import LateInteractionTextEmbedding
from fastembed.sparse import SparseEmbedding, SparseTextEmbedding
from fastembed.text import TextEmbedding

try:
    try:
        version = importlib.metadata.version("fastembed")
    except importlib.metadata.PackageNotFoundError as _:
        version = importlib.metadata.version("fastembed-gpu")
except importlib.metadata.PackageNotFoundError as _:
    version = importlib.metadata.version("ITK-bm25s-extended-fastembed")

__version__ = version
__all__ = [
    "TextEmbedding",
    "SparseTextEmbedding",
    "SparseEmbedding",
    "ImageEmbedding",
    "LateInteractionTextEmbedding",
]
