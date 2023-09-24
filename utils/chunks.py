from collections.abc import Iterator


def divide_chunks(list_item: list, chunk_size: int) -> Iterator[list]:
    """Разбить список на части."""
    for i in range(0, len(list_item), chunk_size):
        yield list_item[i : i + chunk_size]
