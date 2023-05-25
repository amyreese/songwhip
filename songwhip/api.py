# Copyright Amethyst Reese
# Licensed under the MIT license

import json
import logging
from dataclasses import dataclass
from urllib.request import Request, urlopen

import munch

LOG = logging.getLogger(__name__)
SONGWHIP_API = "https://songwhip.com/"


@dataclass(frozen=True)
class Artist:
    name: str
    image: str
    url: str


@dataclass(frozen=True)
class Album:
    name: str
    artists: list[Artist]
    image: str
    url: str


@dataclass(frozen=True)
class Track:
    name: str
    artists: list[Artist]
    image: str
    url: str


def get(url: str) -> Artist | Album | Track:
    params = {
        "url": url,
    }
    headers = {
        "User-Agent": "curl/7.87.0",
    }
    data = json.dumps(params).encode("utf-8")

    request = Request(
        SONGWHIP_API,
        data=data,
        headers=headers,
        method="POST",
    )

    LOG.info("Sending request...")
    response = urlopen(request, timeout=10)
    result = munch.Munch.fromJSON(response.read().decode("utf-8"))
    LOG.debug("Result: %s", result)

    if "artists" in result:
        artists = [
            Artist(name=obj.name, image="", url=SONGWHIP_API + obj.path)
            for obj in result.artists
        ]

    if result.type == "artist":
        return Artist(name=result.name, image=result.image, url=result.url)
    elif result.type == "album":
        return Album(
            name=result.name, artists=artists, image=result.image, url=result.url
        )
    elif result.type == "track":
        return Track(
            name=result.name, artists=artists, image=result.image, url=result.url
        )
    else:
        raise ValueError("unknown result value", result)
