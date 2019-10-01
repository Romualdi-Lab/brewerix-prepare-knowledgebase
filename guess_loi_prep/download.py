import errno
from os import unlink
from subprocess import check_call, CalledProcessError


def download(url, filename):
    try:
        check_call(['wget', '-O', filename , url])
    except CalledProcessError:
        try_unlink(filename)
        raise DownloadError("Failed download of: " + url)


def try_unlink(filename):
    try:
        unlink(filename)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise e


class DownloadError(Exception):
    pass
