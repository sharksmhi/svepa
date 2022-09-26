from .svepa_export_file import SvepaExportFile
from . import helpers
import datetime


def import_svepa_export_file(path):
    sef = SvepaExportFile(path)
    file_info = sef.get_platforms_info()
    all_info = helpers.load()
    for plat, plat_info in file_info.items():
        all_info.setdefault(plat, {})
        for _id, info in plat_info.items():
            all_info[plat][_id] = info
    helpers.save(all_info)


def load_stored_svepa_info():
    return helpers.load()


def get_svepa_info(platform: str = None, time: datetime.datetime = None, event_id: str = None) -> dict:
    ssi = StoredSvepaInfo()
    return ssi.get_info(platform=platform, time=time, event_id=event_id)


class StoredSvepaInfo:
    def __init__(self):
        self._load_info()

    def _load_info(self):
        self._info = load_stored_svepa_info()

    def import_file(self, path):
        import_svepa_export_file(path)
        self._load_info()

    def get_info(self, platform: str = None, time: datetime.datetime = None, event_id: str = None) -> dict:
        if event_id:
            result = {}
            for info in self._info.values():
                value = info.get(event_id)
                if value:
                    result = value
            return result
        if not (platform and time):
            raise Exception('Missing platform and time or event_id when trying to get svepa information')
        plat = platform.upper()
        if plat not in self._info:
            return {}
        for _id, info in self._info[plat].items():
            if info['start_time'] <= time <= info['stop_time']:
                return info
        return {}


