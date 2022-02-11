#!/usr/bin/env python3

from typing import Dict, Optional, Tuple, Iterator
from pathlib import Path

import pandas as pd

from itaxotools.inputchecker import FileChecker, InvalidFileType, SequenceCount
from itaxotools.inputchecker.library.filetypes import FileType

EXTENSION_DICT: Dict[str, FileType] = {
    ".tab": FileType.Tab,
    ".txt": FileType.Tab,
    ".fas": FileType.Fasta,
}


def type_from_extension(ext: str) -> Optional[FileType]:
    return EXTENSION_DICT.get(ext)


def file_summary(filepath: Path) -> Tuple[str, str, int]:
    filetype = type_from_extension(filepath.suffix) or FileType.Tab
    messages = (
        FileChecker()
        .check_filetype(filepath, filetype)
        .count_sequences(filepath, filetype)
    )
    if InvalidFileType(filetype) in messages:
        return filepath.name, "", 0
    seq_count, _ = messages
    return filepath.name, filetype, seq_count.count


def make_summary(files: Iterator[Path]) -> pd.DataFrame:
    return pd.DataFrame(
        (file_summary(file) for file in files),
        columns=["File", "File type", "N sequences"],
    )
