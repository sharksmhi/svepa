import logging

from svepa.svepa_information.svepa_export_file import SvepaExportFile
from svepa.svepa_information.svepa_info import StoredSvepaInfo
from svepa.svepa_information.svepa_event import SvepaEvent

from svepa.svepa_information import helpers
import datetime
import pathlib
import requests

# from functools import lru_cache

logger = logging.getLogger(__name__)


def update_local_svepa_data() -> None:
    """Downloads config files from github"""
    try:
        name = pathlib.Path(helpers.SVEPA_INFO_URL).name
        target_path = helpers.DATA_DIR / name
        res = requests.get(helpers.SVEPA_INFO_URL)
        if res.status_code == 404:
            logger.warning(f'Svepa info file not found: {helpers.SVEPA_INFO_URL}. Cannot update local info!')
            return
        print(f'{target_path=}')
        with open(target_path, 'w', encoding='utf8') as fid:
            fid.write(res.text)
            logger.info(f'Svepa info file "{name}" updated from {helpers.SVEPA_INFO_URL}')
        helpers.save_pickle_from_yaml()
    except requests.exceptions.ConnectionError:
        logger.warning('Connection error. Could not update svepa info file!')
    except Exception:
        raise


def import_svepa_export_file(path: pathlib.Path | str) -> None:
    sef = SvepaExportFile(path)
    file_info = sef.get_platforms_info()
    all_info = helpers.load()
    for plat, plat_info in file_info.items():
        all_info.setdefault(plat, {})
        for _id, info in plat_info.items():
            all_info[plat][_id] = info
    helpers.save(all_info)


def import_svepa_export_files_in_directory(directory: pathlib.Path | str) -> None:
    all_info = helpers.load()
    directory = pathlib.Path(directory)
    for path in directory.iterdir():
        name = path.name.lower()
        if 'svepa' not in name:
            continue
        if 'export' not in name:
            continue
        sef = SvepaExportFile(path)
        file_info = sef.get_platforms_info()
        for plat, plat_info in file_info.items():
            all_info.setdefault(plat, {})
            for _id, info in plat_info.items():
                all_info[plat][_id] = info
    helpers.save(all_info)


def get_time_range() -> tuple | None:
    """Returns the time range for the entire svepa_info scope in svepa_info.yaml"""
    info = helpers.load_stored_svepa_info()
    if not info:
        return
    start = datetime.datetime.now()
    stop = datetime.datetime(1950, 1, 1)
    for stat in info.values():
        for _id in stat.values():
            try:
                start = min(start, _id['start_time'])
                stop = max(stop, _id['stop_time'])
            except TypeError:
                logging.warning('Different data types when trying to find min and max time')
    return start, stop


def get_svepa_info(platform: str = None, time: datetime.datetime = None, event_id: str = None) -> dict:
    ssi = StoredSvepaInfo()
    return ssi.get_info(platform=platform, time=time, event_id=event_id)


def get_svepa_event(platform: str = None, time: datetime.datetime = None, event_id: str = None) -> SvepaEvent:
    ssi = StoredSvepaInfo()
    return ssi.get_event(platform=platform, time=time, event_id=event_id)


def get_svepa_events(platform: str = None, time: datetime.datetime = None, lat: float = None, lon: float = None,
                     year: int = None, month: int = None) -> list[SvepaEvent]:
    ssi = StoredSvepaInfo()
    return ssi.get_events(platform=platform, time=time, lat=lat, lon=lon, year=year, month=month)










