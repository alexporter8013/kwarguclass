from dataclasses import dataclass
from kwarguclass import kwarguclass_enable, kwarguclass


@kwarguclass
class AllTheArgs:
    salutation: str
    trailing_char: str = "!"
    num_trailing_chars: int = 1


@kwarguclass_enable
def make_greeting(name: str, kwargs: AllTheArgs):
    suffix = kwargs.trailing_char * kwargs.num_trailing_chars
    greeting = f"{kwargs.salutation}, {name}{suffix}"
    return greeting

assert make_greeting("Alice") == "Hello, Alice!"
assert make_greeting("Alice", salutation="Bonjour") == "Bonjour, Alice!"
assert make_greeting("Alice", num_trailing_chars=3) == "Hello, Alice!!!"
assert make_greeting("Alice", num_trailing_chars=3, trailing_char = ".") == "Hello, Alice..."
