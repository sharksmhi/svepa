from svepa.svepa_information.svepa_export_file import SvepaExportFile
from svepa.svepa_information.svepa_info import StoredSvepaInfo

from svepa.svepa_information import helpers
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


def get_svepa_info(platform: str = None, time: datetime.datetime = None, event_id: str = None):
    ssi = StoredSvepaInfo()
    return ssi.get_info(platform=platform, time=time, event_id=event_id)


def get_svepa_event(platform: str = None, time: datetime.datetime = None, event_id: str = None):
    ssi = StoredSvepaInfo()
    return ssi.get_event(platform=platform, time=time, event_id=event_id)








