
import functools
import random
import tempfile
from typing import Callable, Tuple

from PIL.Image import Image
from rich import print as rprint
from rich.progress import Progress
from rich.table import Table
from rich.tree import Tree

from printer import codePrint
from reader import readCode

TESTS_PER_ALTERATION = 10


def main():
    alterations = {
        "no_alt": ("No alteration", alter_nothing),
    }

    results = {}
    failures = []
    with Progress() as progress:
        total = progress.add_task("Running all tests", total=TESTS_PER_ALTERATION*len(alterations))
        
        # Start random tests
        for k, v in alterations.items():
            progress_bar = progress.add_task(f"Running tests for [bold]{v[0]}[/]", total=TESTS_PER_ALTERATION)

            name = k
            hr_name = v[0]
            alter_fn = v[1]
            results[name] = []

            for i in range(10):
                alter_partial = functools.partial(alter_fn, amount=i)
                success, data, res = run_test(encode, decode, alter_partial)
                if success == False:
                    failures.append([
                    f"[bold]{hr_name}[/]",
                        str(i),
                        data.hex(),
                        res.hex(),
                    ])

                results[name].append([
                    f"[bold]{hr_name}[/]",
                    str(i),
                    "[green]Success[/]" if success else "[red]Failure[/]"
                ])

                progress.advance(progress_bar)
                progress.advance(total)
            
            progress.remove_task(progress_bar)

    tree = Tree("Result Summary")

    table_res = Table(title="Results")
    table_res.add_column("Alteration")
    table_res.add_column("Alteration #")
    table_res.add_column("Result")
    all_res = [i for test in results.values() for i in test]
    for result in all_res:
        table_res.add_row(*result)
    
    table_fail = Table(title="Failures")
    table_fail.add_column("Alteration")
    table_fail.add_column("Alteration #")
    table_fail.add_column("Expected (hex)")
    table_fail.add_column("Got (hex)")
    for failure in failures:
        table_fail.add_row(*failure)

    for k, v in alterations.items():
        successes = len([i for i in results[k] if 'success' in i[2].lower()])
        tree.add(f"[bold]{v[0]}[/]").add(f"[green]{successes}[/] / {len(results[k])}")

    rprint(table_res)
    rprint(table_fail)
    rprint(tree)    


def create_data(n: int = 16) -> bytes:
    return random.randbytes(n)

def run_test(enc_fn: Callable[[bytes], Image], dec_fn: Callable[[Image], bytes], alter_fn: Callable[[Image], Image]) -> Tuple[bool, bytes, bytes]:
    data = create_data()
    # Encode data
    img = enc_fn(data)

    # Alter the image and decode it
    img = alter_fn(img)
    res = dec_fn(img)

    return data == res, data, res

# Alter nothing, keep i to keep signature the same
def alter_nothing(img: Image, amount: int=0) -> Image:
    return img

def alter_rotation(img: Image, amount: int=1) -> Image: ...
def alter_distortion(): ...
def alter_noise(): ...
def alter_blur(): ...
def alter_background(): ...


def encode(data: bytes) -> Image:
    # Create temp file for image, then delete it :)
    with tempfile.NamedTemporaryFile(suffix=".png") as f:
        binary_string = "{:08b}".format(int(data.hex(),16))
        img = codePrint(list(map(int, binary_string)), f, type="raw")
        return img

def decode(img: Image) -> bytes:
    with tempfile.NamedTemporaryFile(suffix=".png") as f:
        img.save(f)
        r = readCode(f)
        l = r.pop()
        return l


if __name__ == "__main__":
    main()