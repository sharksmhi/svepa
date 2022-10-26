import datetime
from svepa.svepa_information import helpers
from svepa.svepa_information.svepa_event import SvepaEvent


class StoredSvepaInfo:
    def __init__(self):
        self._load_info()

    def _load_info(self):
        self._info = helpers.load_stored_svepa_info()

    def import_file(self, path):
        helpers.import_svepa_export_file(path)
        self._load_info()

    def get_info(self, platform: str = None, time: datetime.datetime = None, event_id: str = None):
        if not event_id and not (platform and time):
            raise Exception('Missing platform and time or event_id when trying to get svepa information')
        info = {}
        found = False
        if event_id:
            for key in self._info:
                if found:
                    break
                for _id, _info in self._info[key].items():
                    if _id == event_id:
                        info = _info
                        found = True
                        break
        else:
            plat = platform.upper()
            if plat not in self._info:
                return {}
            for _id, _info in self._info[plat].items():
                if _info['start_time'] <= time <= _info['stop_time']:
                    info = _info
                    break
        return info

    def get_event(self, platform: str = None, time: datetime.datetime = None, event_id: str = None):
        info = self.get_info(platform=platform, time=time, event_id=event_id)
        return SvepaEvent(stored_svepa_info=self, info=info)