"""CLI App to Run Queue."""

import asyncio
import queue
import threading
import time

import click
from rich.console import Console

console = Console()
task_queue: queue.Queue = queue.Queue()


@click.group()
def cli() -> None:
    """Main function."""
    pass


def sync_worker() -> None:
    """Synchronous/Blocking worker function."""
    while True:
        task = task_queue.get()

        if task is None:
            break

        console.print(f"Processing task: {task}", style="bold red")

        time.sleep(1)  # Simulate a blocking operation

        console.print(f"Task {task} completed", style="bold cyan")

        task_queue.task_done()


@click.command(name="sync")
@click.option("--num", "-n", default=5, help="Number of tasks to run.")
def sync_command(num: int) -> None:
    """Run synchronous blocking tasks."""
    start = time.time()

    num_workers = 1

    threads = [threading.Thread(target=sync_worker) for _ in range(num_workers)]

    for thread in threads:
        thread.start()

    for i in range(num):
        task_queue.put(i)

    task_queue.join()

    for _ in threads:
        task_queue.put(None)

    for thread in threads:
        thread.join()

    end = time.time()

    console.print(
        f"Blocking tasks completed in {end - start:.3f} seconds.", style="bold green"
    )


async def async_worker(name: str, task_queue: asyncio.Queue) -> None:
    """Asynchronous/Non-blocking worker function."""
    start = time.time()

    while True:
        task = await task_queue.get()
        if task is None:  # Exit signal
            break

        console.print(f"{name} processing task: {task}", style="bold red")

        await asyncio.sleep(1)

        console.print(f"{name} completed task: {task}", style="bold cyan")

        task_queue.task_done()

    end = time.time()

    console.print(f"{name} completed in {end - start:.2f} seconds.")


async def _async_queue(num: int) -> None:
    task_queue: asyncio.Queue = asyncio.Queue()

    for i in range(num):
        await task_queue.put(i)

    workers = [
        asyncio.create_task(async_worker(f"Worker {i}", task_queue)) for i in range(3)
    ]

    await task_queue.join()

    for _ in workers:
        await task_queue.put(None)
    await asyncio.gather(*workers)


@click.command(name="async")
@click.option("--num", "-n", default=5, help="Number of tasks to run.")
def async_command(num: int) -> None:
    """Run asynchronous non-blocking tasks."""
    asyncio.run(_async_queue(num))


cli.add_command(sync_command)
cli.add_command(async_command)
