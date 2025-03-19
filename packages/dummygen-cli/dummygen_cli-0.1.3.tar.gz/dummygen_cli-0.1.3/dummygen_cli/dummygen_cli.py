#!/usr/bin/env python3
import os
import re
import argparse
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress
from rich.panel import Panel
from rich.filesize import decimal
import shutil

console = Console()


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
    match = re.match(r"([\d.]+)([kKmMgG][bB])", size_str)
    if match:
        size = float(match.group(1))
        unit = match.group(2).lower()  # Lowercase the unit for consistency
        return size, unit
    else:
        return None


def generate_dummy_file(filename: str, size_bytes: int) -> None:
    """Generates a dummy file of the specified size in bytes."""
    try:
        with Progress(transient=True) as progress:
            task = progress.add_task("[green]Generating dummy file...", total=size_bytes)
            with open(filename, "wb") as f:
                chunk_size = 4096  # 4KB chunks
                while size_bytes > 0:
                    chunk = os.urandom(min(chunk_size, size_bytes))  # Generate random data
                    f.write(chunk)
                    size_bytes -= len(chunk)
                    progress.update(task, advance=len(chunk))

        console.print(f"[bold green]Dummy file '{filename}' generated successfully![/]")
    except Exception as e:
        console.print(f"[bold red]Error generating file: {e}[/]")


def convert_size_to_bytes(size: float, unit: str) -> int:
    """Converts the size from the given unit to bytes."""
    unit = unit.lower()  # Ensure unit is lowercase
    if unit == "kb":
        return int(size * 1024)
    elif unit == "mb":
        return int(size * 1024 * 1024)
    elif unit == "gb":
        return int(size * 1024 * 1024 * 1024)
    else:
        console.print(f"[bold red]Invalid unit: {unit}.  Must be kb, mb, or gb.[/]")
        exit(1)


def main():
    """Main function to handle user input and file generation."""
    console.print(Panel("[bold blue]Dummy File Generator[/]", border_style="blue"))

    # Get initial free space
    initial_free_space = get_free_space()
    console.print(f"[cyan]Initial free disk space: {decimal(initial_free_space)}[/]")

    filename = Prompt.ask("[yellow]Enter the desired filename[/]", default="dummy.txt")

    # Combined size/unit prompt
    size_input = Prompt.ask("[yellow]Enter the desired size (e.g., 100MB, 2.5GB)[/]", default="1MB")
    parsed_size = parse_size_input(size_input)

    if parsed_size is None:
        console.print("[bold red]Invalid size format. Please use a format like 100MB or 2.5GB.[/]")
        return

    size, unit = parsed_size
    size_bytes = convert_size_to_bytes(size, unit)

    generate_dummy_file(filename, size_bytes)

    # Get final free space
    final_free_space = get_free_space()
    console.print(f"[cyan]Final free disk space: {decimal(final_free_space)}[/]")
    console.print(f"[green]Disk space used: {decimal(initial_free_space - final_free_space)}[/]")

if __name__ == "__main__":
    main()
