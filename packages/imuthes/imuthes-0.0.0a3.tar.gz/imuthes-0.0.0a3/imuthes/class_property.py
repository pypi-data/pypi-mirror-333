from typing import Any, Callable, Generic, TypeVar

T = TypeVar("T")


# noinspection PyPep8Naming
class class_property(property, Generic[T]):
    """Decorator for a Class-level property.

    Credit to Denis Rhyzhkov on Stackoverflow: https://stackoverflow.com/a/13624858/1280629
    """

    def __init__(self, func: Callable[[Any], T]) -> None:
        super().__init__(func)

    def __get__(self, owner_self: object, owner_cls: type | None = None) -> T:
        return self.fget(owner_cls)
