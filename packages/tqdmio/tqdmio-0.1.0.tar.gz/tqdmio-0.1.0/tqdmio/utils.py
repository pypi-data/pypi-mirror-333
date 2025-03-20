from typing import AnyStr, Iterable


def size_of(data: AnyStr | Iterable[AnyStr], encoding: str = "utf-8"):
    if isinstance(data, str):
        return len(data.encode(encoding))
    elif isinstance(data, bytes):
        return len(data)
    elif isinstance(data, Iterable):
        return sum(size_of(el, encoding) for el in data)
    raise ValueError(f"Unsupported type: {type(data)}")
