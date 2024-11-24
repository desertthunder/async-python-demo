"""HTTPx Demo."""

import asyncio
import time
import typing

import click
import httpx
import requests
from rich.console import Console
from rich.progress import track

console = Console()
BASE_URL = "https://statsapi.mlb.com/api/v1/{endpoint}"


def make_request(url: str, params: dict | None = None) -> dict:
    """Make a request and return the JSON response."""
    path = BASE_URL.format(endpoint=url)
    response = requests.get(path, timeout=5, params=params or {})
    return response.json()


def make_httpx_request(url: str, params: dict | None = None) -> dict:
    """Make a request and return the JSON response."""
    path = BASE_URL.format(endpoint=url)
    response = httpx.get(path, timeout=5, params=params or {})
    return response.json()


def timed(func: typing.Callable) -> typing.Callable:
    """Decorator to time function execution."""
    start = time.time()

    def wrapper(*args, **kwargs) -> typing.Any:  # noqa
        result = func(*args, **kwargs)
        end = time.time()
        console.print(f"{func.__name__} completed in {end - start:.3f} seconds.")
        return result

    return wrapper


@click.group(name="http")
def http_command() -> None:
    """Requests & HTTPx demo."""
    pass


@click.command(name="requests", help="Run HTTP requests using the requests library.")
@timed
def sync_requests() -> None:
    """Run HTTP requests."""
    data = make_request("sports")
    mlb: dict = next(
        (
            sport
            for sport in data.get("sports", [])
            if sport.get("name") == "Major League Baseball"
        ),
        {},
    )

    console.print_json(data=data)

    data = make_request("teams", params={"sportId": mlb.get("id")})
    links: list[str] = [
        f"teams/{str(team.get("id"))}" for team in data.get("teams", [])
    ]

    console.print(f"Collected {len(links)} team links.")

    teams: list[dict] = []

    for link in track(links, description="Fetching team data..."):
        data = make_request(link).get("teams", []).pop()
        teams.append({"id": data.get("id"), "name": data.get("name")})

    console.print_json(data=teams)
    console.print(f"Team data fetched from {len(links)} links.")


@click.command(name="sync", help="Run synchronous HTTP requests using HTTPx.")
@timed
def sync_httpx() -> None:
    """Run synchronous HTTP requests."""
    data = make_httpx_request("sports")
    mlb: dict = next(
        (
            sport
            for sport in data.get("sports", [])
            if sport.get("name") == "Major League Baseball"
        ),
        {},
    )

    console.print_json(data={"name": mlb.get("name"), "id": mlb.get("id")})

    data = make_httpx_request("teams", params={"sportId": mlb.get("id")})
    ids = [team.get("id") for team in data.get("teams", [])]

    console.print(f"Collected {len(ids)} teams.")

    teams: list[dict] = []

    with httpx.Client(base_url=BASE_URL.format(endpoint="teams")) as client:
        for id in track(ids, description="Fetching team data..."):
            data = client.get(str(id)).json().get("teams", []).pop()
            teams.append({"id": data.get("id"), "name": data.get("name")})

    console.print_json(data=teams)


@click.command(name="async", help="Run asynchronous HTTP requests using HTTPx.")
@timed
def async_httpx() -> None:
    """Run asynchronous HTTP requests."""

    async def fetch_mlb() -> list[str]:
        async with httpx.AsyncClient() as client:
            response = await client.get(BASE_URL.format(endpoint="sports"))
            data = response.json()
            mlb: dict = next(
                (
                    sport
                    for sport in data.get("sports", [])
                    if sport.get("name") == "Major League Baseball"
                ),
                {},
            )

            response = await client.get(
                BASE_URL.format(endpoint="teams"),
                params={"sportId": mlb.get("id")},
            )

            ids = [team.get("id") for team in response.json().get("teams", [])]

            return [str(id) for id in ids]

    async def fetch(url: str) -> None:
        async with httpx.AsyncClient(
            base_url=BASE_URL.format(endpoint="teams")
        ) as client:
            response = await client.get(url)
            data = response.json().get("teams", []).pop()
            console.print_json(data={"id": data.get("id"), "name": data.get("name")})

    async def run() -> None:
        urls = await fetch_mlb()
        await asyncio.gather(*(fetch(url) for url in urls))

    asyncio.run(run())


http_command.add_command(sync_requests)
http_command.add_command(sync_httpx)
http_command.add_command(async_httpx)
