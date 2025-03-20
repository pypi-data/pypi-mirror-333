import argparse
from itertools import combinations
from typing import Callable, Iterator, Optional


def calculate_fake_hex(word: str) -> Iterator[int]:
    hexA = 10
    for ch in word.strip().upper():
        yield (ord(ch) - ord("A") + hexA)


def calculate_digital_root(number: int) -> Iterator[int]:
    total = sum(map(int, str(number)))
    while len(str(total)) > 1:
        total = sum(map(int, str(total)))
    yield total


def calculate_reverse_digital_root(
    digital_root: str,
    min_length: int,
    max_length: int,
    without: Optional[list[int]] = None,
) -> Iterator[str]:
    dg_int = int(digital_root)

    if not without:
        without = []

    for i in range(min_length, max_length + 1):
        for comb in combinations(range(1, 10), i):
            comb_str = "".join(map(str, comb))

            if any((
                str(x) in comb_str
                for x in without
            )):
                continue

            if next(calculate_digital_root(int(comb_str))) == dg_int:
                yield comb_str
    

def cli_entrypoint():
    parser = argparse.ArgumentParser(
        "nonary",
        description="CLI tool for the 'Zero Escape: The Nonary Games' game",
    )
    subparser = parser.add_subparsers()

    fake_hex = subparser.add_parser(
        "fake_hex",
        help=(
            "Regular Hexadecimal stops at F(15). "
            "Fake Hexadecimal continues forever --> G - 16, H - 17, I - 18.\n"
            "You can think of this as a simple encoding for the Alphabet where A starts at 10."
        )
    )
    fake_hex.set_defaults(fn=calculate_fake_hex)
    fake_hex.add_argument(
        "word",
        help="The word to convert into fake hexadecimal"
    )

    digital_root = subparser.add_parser(
        "digital_root",
        help="Calculates the digital root for a given number"
    )
    digital_root.set_defaults(fn=calculate_digital_root)
    digital_root.add_argument(
        "number",
        type=int,
        help="The number to calculate the digital root for"
    )

    reverse_digital_root = subparser.add_parser(
        "reverse_digital_root",
        help="Generates all the possible combinations of numbers that reach a given digital root"
    )
    reverse_digital_root.set_defaults(fn=calculate_reverse_digital_root)
    reverse_digital_root.add_argument(
        "digital_root",
        help="The digital root the combinations need to reach"
    )
    reverse_digital_root.add_argument(
        "-x", "--without", 
        nargs="*",
        type=int,
        help="List of numbers to not use to calculate combinations",
    )
    reverse_digital_root.add_argument(
        "-l", "--min-length",
        default=2,
        type=int,
        help="The smallest length a combination can have",
    )
    reverse_digital_root.add_argument(
        "-L", "--max-length",
        default=9,
        type=int,
        help="The biggest length a combination can have",
    )

    args = vars(parser.parse_args())
    fn: Optional[Callable[[], Iterator]] = args.pop("fn", None)

    if not fn:
        parser.print_help()
        exit()
    
    for res in fn(**args):
        print(res)
