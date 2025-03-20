import collections
import re
import sys

from .job import Job
from .run import combine, run, run_by_cron, run_periodically

__all__: tuple[str, ...] = (
    # job.py
    "Job",
    # run.py
    "combine",
    "run",
    "run_by_cron",
    "run_periodically",
)

try:
    import aiohttp as _aiohttp  # noqa

    from .aiohttp import is_healthy as aiohttp_is_healthy, setup_ctx as aiohttp_setup_ctx  # noqa

    __all__ += ("aiohttp_is_healthy", "aiohttp_setup_ctx")
except ImportError:
    pass


__version__ = "0.0.11"

version = f"{__version__}, Python {sys.version}"

VersionInfo = collections.namedtuple("VersionInfo", "major minor micro release_level serial")


def _parse_version(v: str) -> VersionInfo:
    version_re = r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<micro>\d+)" r"((?P<release_level>[a-z]+)(?P<serial>\d+)?)?$"
    match = re.match(version_re, v)
    if not match:
        raise ImportError(f"Invalid package version {v}")
    try:
        major = int(match.group("major"))
        minor = int(match.group("minor"))
        micro = int(match.group("micro"))
        levels = {"rc": "candidate", "a": "alpha", "b": "beta", None: "final"}
        release_level = levels[match.group("release_level")]
        serial = int(match.group("serial")) if match.group("serial") else 0
        return VersionInfo(major, minor, micro, release_level, serial)
    except Exception as e:
        raise ImportError(f"Invalid package version {v}") from e


version_info = _parse_version(__version__)
