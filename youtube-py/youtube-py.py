import click
import os
from pytube import YouTube
import logging
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .ffmpeg_tools import combine
from pathlib import Path

logging.basicConfig(level=logging.INFO)


def isNone(obj):
    if obj is None:
        return True
    else:
        return False


def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    printProgressBar(iteration=percentage_of_completion, total=100, decimals=15)


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def validateUrl(url):
    validator = URLValidator()
    logging.info("Validating url")
    try:
        b = validator(url)
    except ValidationError as exc:
        raise ValueError("URL provided is invalid " + url) from exc


def download(yt, outputDir, quality):
    # Replace characters that cause issues with file names / dir
    title = yt.title.replace(' ', '')
    title = title.replace('/', '')
    # File Names
    video_dir = outputDir + title + '_video'
    audio_dir = outputDir + title + '_audio'
    if not isNone(quality):
        stream_video = (yt.streams.filter(only_video=True, adaptive=True, res=quality, mime_type='video/mp4'))

        if len(stream_video) < 1:
            logging.info("Error: Nothing found for quality " + quality)
            return
        else:
            logging.info('Downloading ' + yt.title + " to " + outputDir)

            if 'ime_type="video/mp4' in str(stream_video[0]):
                logging.info('Downloading video codec')
                stream_video[0].download(outputDir, filename=title + '_video')
                stream_audio = yt.streams.filter(only_audio=True, mime_type='audio/mp4')

                if len(stream_audio) < 1:
                    logging.info('Cannot find mp4 audio codec to download')
                    return
                else:
                    logging.info('Downloading audio codec')
                    stream_audio[0].download(outputDir, filename=title + "_audio")

                    # Raw file directory
                    video_file = Path(video_dir + '.mp4')
                    audio_file = Path(audio_dir + '.mp4')
                    if video_file.is_file() and audio_file.is_file():
                        combine(audio_file, video_file, outputDir + title)
                    else:
                        raise FileNotFoundError('Video / Audio file cannot be found to process. Check output directory')
                        return

                    # ffmpeg.output(audio_stream, video_stream, yt.title + ".mp4").run()

    # Check arguments for None inputs


def get_yt(url):
    yt = YouTube(url, on_progress_callback=progress_function)
    return yt


@click.command()
@click.argument('url', required=True, type=click.STRING)
@click.option('--output', '-o', 'outputDir', required=False, default=os.getcwd(), type=click.Path(exists=True))
@click.option('-q', '--quality', 'quality', required=False, default='720p', show_default=True,
              help='Quality of stream to download. Example: 1080p')
def main(outputDir, url, quality):
    # Validate URL
    logging.info('Starting... ')
    logging.debug("output dir: " + outputDir)
    validateUrl(url)
    yt = None

    # Reattempts, sometimes requests drop
    while yt is None:
        try:
            yt = get_yt(url)
        except Exception as e:
            logging.info("Error retrieving youtube info for URL: " + url + "\n Retrying...")

    download(yt, outputDir, quality)


# Main
if __name__ == '__main__':
    main()
