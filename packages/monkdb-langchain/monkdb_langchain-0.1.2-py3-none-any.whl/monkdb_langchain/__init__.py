# ruff: noqa: E402  # Module level import not at top of file
from importlib import metadata

from monkdb_langchain.patches import patch_sqlalchemy_dialect

patch_sqlalchemy_dialect()

from monkdb_langchain.caching import MonkDBCache, MonkDBSemanticCache
from monkdb_langchain.store_chat import MonkDBChatMessageHistory
from monkdb_langchain.data_loaders import MonkDBLoader
from monkdb_langchain.vector_datastores import (
    MonkDBVectorStore,
    MonkDBVectorStoreMultiCollection,
)

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:  # pragma: no cover
    # Case where package metadata is not available.
    __version__ = ""
del metadata  # optional, avoids polluting the results of dir(__package__)

__all__ = [
    "MonkDBCache",
    "MonkDBChatMessageHistory",
    "MonkDBLoader",
    "MonkDBSemanticCache",
    "MonkDBVectorStore",
    "MonkDBVectorStoreMultiCollection",
    "__version__",
]