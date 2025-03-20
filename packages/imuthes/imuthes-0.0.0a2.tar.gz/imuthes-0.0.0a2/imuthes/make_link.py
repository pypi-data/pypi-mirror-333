import os
import pathlib
import subprocess
import sys

from hakisto import Logger

logger = Logger("imuthes.make_link")


def make_link(
    target: pathlib.Path,
    link: pathlib.Path,
) -> None:
    """Create a link pointing to target.

    For Windoze, this will be a ``Junction``, for all other OS, a soft link
    :param target: Target path, this will be pointed to.
    :param link: Link path, this will be created.
    """
    logger.debug(f"{link} -> {target}")
    if sys.platform != "win32":
        logger.debug("This is not Windoze - using soft link")
        link = link.resolve()
        target = target.resolve()
        link.symlink_to(target)
    else:
        cmd = ["mklink", "/j", os.fsdecode(link), os.fsdecode(target)]
        logger.debug(f'calling {" ".join(cmd)}')
        proc = subprocess.run(cmd, shell=True, capture_output=True)
        if proc.returncode:
            raise OSError(proc.stderr.decode().strip())
