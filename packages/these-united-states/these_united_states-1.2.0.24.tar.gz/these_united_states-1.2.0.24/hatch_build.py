
"""Download the US Census data used to compute shapes."""

import logging
import os
import pathlib
import shutil
from typing import Any, Dict

from hatchling.builders.hooks.plugin.interface import BuildHookInterface
import requests


DOWNLOAD_URL = 'https://www2.census.gov/geo/tiger/TIGER{year}/STATE/tl_{year}_us_state.zip'


log = logging.getLogger(__name__)


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version: str, build_data: Dict[str, Any]) -> None:
        year = self.config['year']
        path = download(year, str(pathlib.Path(self.root, '.shapes')))
        shutil.copyfile(path, pathlib.Path('src/united_states', 'shapes.zip'))
        build_data['artifacts'] = ['/src/united_states/shapes.zip']


def download(year: int, build_dir: str, force: bool = False) -> pathlib.Path:
    """Download data for a given year.

    Data for the given year is downloaded to the provided directory and the
    path to the file is returned. If the file already exists, the download is
    skipped, unless force is True.
    """
    url = DOWNLOAD_URL.format(year=year)
    path = pathlib.Path(build_dir, url.rsplit('/', 1)[-1])
    if not force and path.exists():
        log.info(f'Skipping download; {path} exists')
        return path
    if not path.parent.exists():
        path.parent.mkdir(0o755, parents=True)
    log.info(f'Downloading {url} to {path}')
    with requests.get(url, stream=True) as response, path.open('wb') as file:
        response.raise_for_status()
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, file)
    return path
