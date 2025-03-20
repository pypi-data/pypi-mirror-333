## tqdmio

`tqdmio` is a tiny IO wrapper for [`tqdm`](https://github.com/tqdm/tqdm).
Use it to wrap any IO object `tqdmio(open(path))` to display a progress bar
while reading or writing files.

Use the convenience function `tqdmio.open(path)` to open a file with a progress bar.
When reading files, it will automatically detect the file size using
`pathlib.Path.stat().st_size`.

By default, the progress will be shown in kb/s, Mb/s, Gb/s, etc.

You can customize the progress bar by passing `tqdm` arguments to the `tqdmio` constructor.

When wrapping compressed files, use `tqdmio.open(file, "rb")` or wrap the raw `IO[bytes]` using `tqdmio(open(file, "rb"))` and pass it to the reader, e.g.:

```python
import gzip
from tqdmio import tqdmio

with tqdmio.open("file.txt", "rt") as fp:
    for line in fp:
        pass

with tqdmio.open("file.gz", "rb") as fgz:
    for line in gzip.open(fgz, "rt"):
        pass
```
