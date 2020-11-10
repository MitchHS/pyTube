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
        return True
    else:
        return False


def validateUrl(url):
    validator = URLValidator()
    logging.info("Validating url")
    try:
        b = validator(url)
    except ValidationError as exc:
        raise ValueError("URL provided is invalid " + url) from exc


def download(yt, outputDir, quality):

    if not isNone(quality):
        stream_video = (yt.streams.filter(only_video=True, adaptive=True, res=quality, mime_type='video/mp4'))

        if len(stream_video) < 1:
            logging.info("Error: Nothing found for quality " + quality)
            return
        else:
            logging.info('Downloading ' + yt.title + " to " + outputDir)
            print(str(stream_video[0]))
            if 'ime_type="video/mp4' in str(stream_video[0]):
                logging.info('Downloading video codec')
                # stream_video[0].download(outputDir)
                stream_audio = yt.streams.filter(only_audio=True, mime_type='audio/mp4')
                print(stream_audio)
                if len(stream_audio) < 1:
                    logging.info('Cannot find mp4 audio codec to download')
                    return
                else:
                    logging.info('Downloading audio codec')
                    stream_audio[0].download(outputDir)


             
        

    # Check arguments for None inputs


def get_yt(url):
    yt = YouTube(url)
    return yt


@click.command()
@click.argument('url', required=True, type=click.STRING)
@click.option('--output', '-o', 'outputDir', required=False, default=os.getcwd(), type=click.Path(exists=True))
@click.option('-q', '--quality', 'quality', required=False, default='720p', show_default=True, help='Quality of stream to download. Example: 1080p')
def main(outputDir, url, quality):
    # Validate URL
    logging.info('Starting... ')
    logging.debug("output dir: " + outputDir)
    validateUrl(url)
    yt = None

    # Reattempts
    while yt is None:
        try:
            yt = get_yt(url)
        except Exception as e:
            logging.info("Error retrieving youtube info for URL: " + url + "\n Retrying...")

    download(yt, outputDir, quality)


# Main
if __name__ == '__main__':
    main()
