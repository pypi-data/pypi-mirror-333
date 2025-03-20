#!/usr/bin/env python3
import os
import re
import shutil
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress
from rich.panel import Panel
from rich.filesize import decimal

CHUNK_SIZE = 4096  # 4KB chunks
SIZE_UNITS = {
    "kb": 1024,
    "mb": 1024 * 1024,
    "gb": 1024 * 1024 * 1024,
    "tb": 1024 * 1024 * 1024 * 1024,
}


def get_free_space(path: str = ".") -> int:
    """Gets the free space of the disk in bytes."""
    total, used, free = shutil.disk_usage(path)
    return free


def parse_size_input(size_str: str) -> tuple[float, str] | None:
    """Parses the size input string (e.g., "100MB", "2.5GB").

    Returns:
        A tuple containing the size as a float and the unit as a string (lowercase),
        or None if the input is invalid.
    """
    match = re.match(r"([\d.]+)([kKmMgGtT][bB])", size_str)
    if match:
        size = float(match.group(1))
        unit = match.group(2).lower()  # Lowercase the unit for consistency
        return size, unit
    else:
        return None


def generate_dummy_file(filename: str, size_bytes: int) -> None:
    """Generates a dummy file of the specified size in bytes."""
    console = Console()
    try:
        with Progress(transient=True) as progress:
            task = progress.add_task("[green]Generating dummy file...", total=size_bytes)
            with open(filename, "wb") as f:
                while size_bytes > 0:
                    # Check free space before writing each chunk
                    free_space = get_free_space()
                    if free_space < min(CHUNK_SIZE, size_bytes):
                        console.print("[bold red]Disk space is insufficient. File generation stopped.[/]")
                        return  # Stop generation

                    chunk = os.urandom(min(CHUNK_SIZE, size_bytes))  # Generate random data
                    f.write(chunk)
                    size_bytes -= len(chunk)
                    progress.update(task, advance=len(chunk))

        console.print(f"[bold green]Dummy file '{filename}' generated successfully![/]")
    except Exception as e:
        console.print(f"[bold red]Error generating file: {type(e).__name__} - {e}[/]")


def convert_size_to_bytes(size: float, unit: str) -> int:
    """Converts the size from the given unit to bytes."""
    unit = unit.lower()
    if unit in SIZE_UNITS:
        return int(size * SIZE_UNITS[unit])
    else:
        console = Console()
        console.print(f"[bold red]Invalid unit: {unit}. Must be kb, mb, gb, or tb.[/]")
        exit(1)


def main():
    """Main function to handle user input and file generation."""
    console = Console()
    console.print(Panel("[bold blue]Dummy File Generator[/]", border_style="blue"))

    # Get initial free space
    initial_free_space = get_free_space()
    console.print(f"[cyan]Initial free disk space: {decimal(initial_free_space)}[/]")

    while True:
        filename = Prompt.ask("[yellow]Enter the desired filename[/]", default="dummy.txt")
        if os.path.exists(filename):
            confirm = Prompt.ask(f"[yellow]File '{filename}' already exists. Overwrite? (y/n)[/]", choices=["y", "n"], default="n")
            if confirm.lower() != "y":
                continue  # Ask for a different filename
        break

    # Combined size/unit prompt
    while True:
        size_input = Prompt.ask("[yellow]Enter the desired size (e.g., 100MB, 2.5GB)[/]", default="1MB")
        parsed_size = parse_size_input(size_input)

        if parsed_size is None:
            console.print("[bold red]Invalid size format. Please use a format like 100MB or 2.5GB.[/]")
        else:
            size, unit = parsed_size
            size_bytes = convert_size_to_bytes(size, unit)

            if size_bytes > initial_free_space:
                console.print("[bold red]Requested size exceeds available disk space.[/]")
            else:
                break

    generate_dummy_file(filename, size_bytes)

    # Get final free space
    final_free_space = get_free_space()
    console.print(f"[cyan]Final free disk space: {decimal(final_free_space)}[/]")
    console.print(f"[green]Disk space used: {decimal(initial_free_space - final_free_space)}[/]")


if __name__ == "__main__":
    main()