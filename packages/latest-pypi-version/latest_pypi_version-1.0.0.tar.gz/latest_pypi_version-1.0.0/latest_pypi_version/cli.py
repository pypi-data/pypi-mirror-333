from typing import Any, cast

import requests
import typer
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(help="CLI tool to check the latest version of a PyPI package")
console = Console()


def get_package_info(package_name: str) -> dict[str, Any] | None:
    """Fetch package information from PyPI."""
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url, timeout=20)
    if response.status_code == 200:  # noqa: PLR2004
        return cast(dict[str, Any], response.json())
    else:
        return None


@app.command()
def version(
    package: str = typer.Argument(..., help="Name of the PyPI package to check"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show additional package information"),
) -> None:
    """Get the latest version of a PyPI package."""
    with console.status(f"Fetching information for {package}...", spinner="dots"):
        package_info = get_package_info(package)

    if not package_info:
        console.print(f"[bold red]Error:[/bold red] Package '{package}' not found on PyPI")
        raise typer.Exit(1)

    latest_version = package_info["info"]["version"]

    if verbose:
        author = package_info["info"]["author"] or "Unknown"
        summary = package_info["info"]["summary"] or "No description available"
        home_page = package_info["info"]["home_page"] or "N/A"
        release_date = "N/A"

        if "releases" in package_info and latest_version in package_info["releases"]:
            releases = package_info["releases"][latest_version]
            if releases and "upload_time" in releases[0]:
                release_date = releases[0]["upload_time"].split("T")[0]

        rprint(
            Panel.fit(
                f"[bold cyan]Package:[/bold cyan] {package}\n"
                f"[bold cyan]Version:[/bold cyan] {latest_version}\n"
                f"[bold cyan]Author:[/bold cyan] {author}\n"
                f"[bold cyan]Released:[/bold cyan] {release_date}\n"
                f"[bold cyan]Homepage:[/bold cyan] {home_page}\n\n"
                f"[bold cyan]Summary:[/bold cyan] {summary}",
                title="PyPI Package Info",
            )
        )
    else:
        console.print(f"[bold green]{package}[/bold green] latest version: [bold yellow]{latest_version}[/bold yellow]")


if __name__ == "__main__":
    app()
