from copy import copy
from dataclasses import dataclass
from re import Pattern, compile
from typing import Callable, Dict, Optional, Tuple, TypeVar


@dataclass
class Msg:
    method: str
    key: str = None
    value: str | dict = None


@dataclass
class Redirect:
    route: str = None


TYPE_PATTERNS: Dict[str, Tuple[Pattern[str], Callable[[str], Optional[bool]]]] = {
    "int": (compile(r"-?\d+"), int),
    "float": (compile(r"-?\d+\.\d+"), float),
    "str": (compile(r"[^/]+"), str),
    "bool": (compile(r"(true|True|false|False)"), lambda x: x in ["true", "True"]),
}


C = TypeVar("C")


def cache_control(control: C) -> C:
    """
    Creates a copy of the control while preserving its specific type.

    This function is particularly useful when you need to maintain a control's state while navigating between different pages. When you enable the `cache` option on a page,
    shared controls will maintain their state even if they are modified on other pages. Works seamlessly with controls shared through the `view` decorator
    of the `FletEasy` instance, allowing for a consistent user experience throughout the application.

    **Args:**
       - **control:** The control you want to cache, can be of type Control, AppBar, or others.

    **Returns:**
        A copy of the control with the same specific type as the original.

    Example:

    ```python
    # Maintains the control's state even when navigating between pages
    my_control = AppBar(title=Text("My Title"))
    my_cached_control = fs.cache_control(my_control)
    ```
    """
    return copy(control)
