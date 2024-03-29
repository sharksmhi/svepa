from svepa.svepa_information.svepa_export_file import SvepaExportFile
from svepa.svepa_information.svepa_info import StoredSvepaInfo

from svepa.svepa_information import helpers
import datetime

from functools import lru_cache


def import_svepa_export_file(path):
    sef = SvepaExportFile(path)
    file_info = sef.get_platforms_info()
    all_info = helpers.load()
    for plat, plat_info in file_info.items():
        all_info.setdefault(plat, {})
        for _id, info in plat_info.items():
            all_info[plat][_id] = info
    helpers.save(all_info)


def get_time_range():
    """Returns the time range for the entire svepa_info scope in svepa_info.yaml"""
    info = helpers.load_stored_svepa_info()
    start = datetime.datetime.now()
    stop = datetime.datetime(1950, 1, 1)
    for stat in info.values():
        for _id in stat.values():
            start = min(start, _id['start_time'])
            stop = max(stop, _id['stop_time'])
    return start, stop


@lru_cache
def get_svepa_info(platform: str = None, time: datetime.datetime = None, event_id: str = None):
    ssi = StoredSvepaInfo()
    return ssi.get_info(platform=platform, time=time, event_id=event_id)


@lru_cache
def get_svepa_event(platform: str = None, time: datetime.datetime = None, event_id: str = None):
    ssi = StoredSvepaInfo()
    return ssi.get_event(platform=platform, time=time, event_id=event_id)


@lru_cache
def get_svepa_events(platform: str = None, time: datetime.datetime = None, lat: float = None, lon: float = None,
                     year: int = None, month: int = None):
    ssi = StoredSvepaInfo()
    return ssi.get_events(platform=platform, time=time, lat=lat, lon=lon, year=year, month=month)










