
import functools
import random
import tempfile
from typing import Callable

from PIL.Image import Image
from rich import print as rprint
from rich.progress import Progress
from rich.table import Table
from rich.tree import Tree

from printer import codePrint
from reader import readCode


def main():
    results = {}
    failures = []
    with Progress() as progress:
        data_tests = progress.add_task("Random Data Tests", total=10)
        
        total = progress.add_task("Running tests", total=60)
        
        # Start random tests
        results["no_alt"] = []
        for i in range(10):
            alter_fn = functools.partial(alter_nothing)
            success, data, res = run_test(encode, decode, alter_fn)
            if success == False:
                failures.append([
                    "[bold]No alteration[/]",
                    data.hex(),
                    res.hex(),
                ])
            
            results['no_alt'].append([
                "[bold]No alteration[/]",
                str(i),
                "[green]Success[/]" if success else "[red]Failure[/]"
            ])

            progress.advance(data_tests)
            progress.advance(total)

    tree = Tree("Result Summary")

    table_res = Table(title="Results")
    table_res.add_column("Alteration")
    table_res.add_column("Test #")
    table_res.add_column("Status")
    all_res = [i for test in results.values() for i in test]
    for result in all_res:
        table_res.add_row(*result)
    
    table_fail = Table(title="Failures")
    table_fail.add_column("Alteration")
    table_fail.add_column("Expected (hex)")
    table_fail.add_column("Got (hex)")
    for failure in failures:
        table_fail.add_row(*failure)


    no_alt_success = len([i for i in results['no_alt'] if i[2] == "[green]Success[/]"])
    tree.add("[bold]No alteration[/]").add(f"[green]{no_alt_success}[/] / {len(results['no_alt'])}")

    rprint(table_res)
    rprint(table_fail)
    rprint(tree)

    


def create_data(n: int = 32) -> bytes:
    return random.randbytes(n)

def run_test(enc_fn: Callable[[bytes], Image], dec_fn: Callable[[Image], bytes], alter_fn: Callable[[Image], Image]) -> bool:
    data = create_data()
    # Encode data
    img = enc_fn(data)

    # Alter the image and decode it
    img = alter_fn(img)
    res = dec_fn(img)

    return data == res, data, res

def alter_nothing(img: Image) -> Image:
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
        img = codePrint(list(map(int, binary_string)), f.name)
        return img

def decode(img: Image) -> bytes:
    with tempfile.NamedTemporaryFile(suffix=".png") as f:
        img.save(f.name)
        return readCode(f.name)


if __name__ == "__main__":
    main()