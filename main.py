import os
import click
from parser.extractor import PhoneExtractor
from loguru import logger


@click.command()
@click.option('--filepath', required=True, help='Path to the input text file')
def main(filepath: str) -> None:
    """Extract phone numbers from the specified file."""
    os.makedirs("logs", exist_ok=True)

    logger.remove()
    logger.add(
        "logs/phone_parser.log",
        rotation="500 KB",
        retention="7 days",
        compression="zip",
        encoding="utf-8",
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    )

    logger.info(f"Starting extraction from file: {filepath}")

    extractor = PhoneExtractor(filepath)
    numbers = extractor.extract()

    click.echo("📞 Unique phone numbers:")
    for number in numbers:
        click.echo(number)


if __name__ == "__main__":
    main()
