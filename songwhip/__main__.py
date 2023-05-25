# Copyright Amethyst Reese
# Licensed under the MIT license

import logging
import sys

import click
from rich import print

from .api import Artist, get


@click.command("songwhip")
@click.option("--verbose / --quiet", "-v / -q", default=False)
@click.argument("song_url", required=False, default="")
def main(verbose: bool, song_url: str) -> None:
    logging.basicConfig(
        stream=sys.stderr,
        level=logging.DEBUG if verbose else logging.WARNING,
    )

    if not song_url:
        song_url = click.prompt("Enter song url")

    item = get(song_url)
    if verbose:
        print(item)

    print(f"{item.__class__.__name__}:", item.name)
    if not isinstance(item, Artist):
        print("Artist:", ", ".join(a.name for a in item.artists))

    print("Songwhip url:", item.url)


if __name__ == "__main__":
    main()
