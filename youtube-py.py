import click
import os
from pytube import YouTube
import logging
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import ffmpeg

logging.basicConfig(level=logging.INFO)


def combine(audio_file, video_file, output):
    video_stream = ffmpeg.input(video_file)
    audio_stream = ffmpeg.input(audio_file)
    out = ffmpeg.output(audio_stream, video_stream, 'out.mp4').run()


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
    if yt is None:
        try:
            yt = get_yt(url)
        except Exception as e:
            logging.info("Error retrieving youtube info for URL: " + url + "\n Retrying...")

    download(yt, outputDir)


# Main
if __name__ == '__main__':
    main()
