from .svepa_export_file import SvepaExportFile
from . import helpers
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


@lru_cache
def load_stored_svepa_info():
    return helpers.load()


def get_svepa_info(platform: str = None, time: datetime.datetime = None, event_id: str = None):
    ssi = StoredSvepaInfo()
    return ssi.get_info(platform=platform, time=time, event_id=event_id)


def get_svepa_event(platform: str = None, time: datetime.datetime = None, event_id: str = None):
    ssi = StoredSvepaInfo()
    return ssi.get_event(platform=platform, time=time, event_id=event_id)


class StoredSvepaInfo:
    def __init__(self):
        self._load_info()

    def _load_info(self):
        self._info = load_stored_svepa_info()

    def import_file(self, path):
        import_svepa_export_file(path)
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


class SvepaEvent:
    def __init__(self, stored_svepa_info: StoredSvepaInfo = None, info: dict = None):
        self._stored_svepa_info = stored_svepa_info
        self._info = info

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.full_name} [{self.start_time} - {self.stop_time}] ({self.event_id})'

    def __str__(self):
        lst = []
        ljust = 30
        for key in sorted(self._info):
            lst.append(f'{key.ljust(ljust)}{self._info[key]}')
        return '\n'.join(lst)

    def __getattr__(self, item):
        if item not in self._info:
            raise AttributeError(item)
        return self._info.get(item)

    @property
    def parent(self):
        if not self.parent_event_id:
            return
        return self._stored_svepa_info.get_event(event_id=self.parent_event_id)

    @property
    def station_event(self):
        event = self
        while True:
            event = event.parent
            if event.event_type.upper() == 'STATION':
                return event
            if not event:
                return

    @property
    def cruise_event(self):
        event = self
        while True:
            event = event.parent
            if event.event_type.upper() == 'TRIP':
                return event
            if not event:
                return





