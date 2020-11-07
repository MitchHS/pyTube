import click
import os
from pytube import YouTube
import logging
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

logging.basicConfig(level=logging.INFO)

def ifNone(obj):
    if obj is None:
        return False


def validateUrl(url):
    validator = URLValidator()
    logging.info("Validating url")
    try:
        b= validator(url)
    except ValidationError:
        raise ValueError("URL provided is invalid " + url)


@click.command()
@click.argument('url', required=True, type=click.STRING)
@click.option('--output', '-o', 'outputDir', required=False, default=os.getcwd())
def main(outputDir, url):
    # Validate URL
    logging.warning("Warning")
    validateUrl(url)
    yt = YouTube(url)
    try:
        yt = YouTube(url)
    except Exception as e:
        logging.debug(e)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

