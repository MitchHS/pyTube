import click
import os
from pytube import YouTube
import logging
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

logging.basicConfig(level=logging.INFO)


def isNone(obj):
    if obj is None:
        return False
    else:
        return True


def validateUrl(url):
    validator = URLValidator()
    logging.info("Validating url")
    try:
        b = validator(url)
    except ValidationError as exc:
        raise ValueError("URL provided is invalid " + url) from exc


def download(yt, outputDir):
    logging.info('Downloading ' + yt.title + " to " + outputDir)
    stream = (yt.streams.filter(adaptive=True))
    for vid in stream:
        print(vid)


def get_yt(url):
    yt = YouTube(url)
    return yt



@click.command()
@click.argument('url', required=True, type=click.STRING)
@click.option('--output', '-o', 'outputDir', required=False, default=os.getcwd())
def main(outputDir, url):
    # Validate URL
    logging.info('Starting... ')
    logging.debug("output dir: " + outputDir)
    validateUrl(url)
    yt = None

    # Reattempts
    while yt is None:
        try:
            yt = getyt(url)
        except Exception as e:
            logging.info("Error retrieving youtube info for URL: " + url + "\n Retrying...")
            yt = None



    download(yt, outputDir)


# Main
if __name__ == '__main__':
    main()
