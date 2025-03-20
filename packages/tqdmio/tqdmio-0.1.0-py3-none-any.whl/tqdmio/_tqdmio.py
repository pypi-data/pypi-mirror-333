import sys
from os import PathLike
from pathlib import Path
from typing import IO, AnyStr, Iterable, Iterator, Optional

from tqdm import tqdm

from .utils import size_of


class tqdmio(IO[AnyStr]):
    def __init__(self, io: IO[AnyStr], *args, **kwargs):
        self._io: IO[AnyStr] = io

        kwargs.setdefault("unit", "b")
        kwargs.setdefault("unit_divisor", 1024)
        kwargs.setdefault("unit_scale", True)
        self._init_tqdm(*args, **kwargs)

    def _init_tqdm(self, *args, **kwargs):
        self._tqdm = tqdm(*args, **kwargs)

    def read(self, size: int = -1) -> AnyStr:
        _read = self._io.read(size)
        self._tqdm.update(size if size > 0 else size_of(_read))
        return _read

    def write(self, data) -> int:
        self._tqdm.update(size_of(data))
        return self._io.write(data)

    def close(self):
        try:
            self._io.close()
        finally:
            self._tqdm.close()
            sys.stdout.flush()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def fileno(self) -> int:
        return self._io.fileno()

    def readline(self, limit: int = -1) -> AnyStr:
        line = self._io.readline()
        self._tqdm.update(size_of(line))
        return line

    def readlines(self, hint: int = -1) -> list[AnyStr]:
        lines = self._io.readlines(hint)
        self._tqdm.update(size_of(lines))
        return lines

    def seek(self, offset: int, whence: int = 0) -> int:
        return self._io.seek(offset, whence)

    def seekable(self) -> bool:
        return self._io.seekable()

    def tell(self) -> int:
        return self._io.tell()

    def truncate(self, size: Optional[int] = None) -> int:
        return self._io.truncate()

    def writable(self) -> bool:
        return self._io.writable()

    def writelines(self, lines: Iterable) -> None:
        self._tqdm.update(size_of(lines))
        return self._io.writelines(lines)

    def __next__(self) -> AnyStr:
        _next = next(self._io)
        self._tqdm.update(size_of(_next))
        return _next

    def __iter__(self) -> Iterator[AnyStr]:
        for el in iter(self._io):
            self._tqdm.update(size_of(el))
            yield el

    @classmethod
    def open(
        cls,
        filepath: str | PathLike,
        mode="rb",
        buffering=2**16,
        encoding="utf-8",
        errors=None,
        newline=None,
        **kwargs,
    ) -> "tqdmio":
        """
        Opens a new file handle using `Path.open` with the given mode for the given filepath.
        If the file is to be read, will determine the filesize and pass it on to tqdm.

        Args:
            filepath: The path of the file to open.
            mode: The opening mode. Defaults to 'rb'.
            **kwargs: Additional keyword arguments to pass to the `Path.open` method.

        Returns:
           tqdmio: A tqdmio wrapper around the opened file handle.
        """
        path = Path(filepath)

        if "r" in mode:
            kwargs.setdefault("total", path.stat().st_size)

        return cls(
            path.open(
                mode,
                buffering=buffering,
                errors=errors,
                newline=newline,
            ),
            **kwargs,
        )
