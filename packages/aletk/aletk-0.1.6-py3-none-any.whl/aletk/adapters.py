from typing import Callable, Generator, Iterator


class ReusableGenerator[T]():
    """
    Adapter class to allow consuming a generator more than once. Usage example:

    ```python
    def my_generator() -> Generator[int, None, None]:
        yield 1
        yield 2
        yield 3

    adapter = GeneratorAdapter(my_generator)

    for item in adapter:
        print(item)

    for item in adapter:
        print(item)
    ```
    """

    def __init__(self, iterator_factory: Callable[[], Generator[T, None, None]]) -> None:
        self.iterator_factory = iterator_factory

    def __iter__(self) -> Iterator[T]:
        return self.iterator_factory()
