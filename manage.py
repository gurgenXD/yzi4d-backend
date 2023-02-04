import click

from cli.migrations import migrations
from cli.start import start


@click.group()
def main() -> None:
    """Команды управления приложением."""


main.add_command(start)
main.add_command(migrations)


if __name__ == "__main__":
    main()
