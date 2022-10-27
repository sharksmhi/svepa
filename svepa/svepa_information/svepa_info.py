import datetime
from svepa.svepa_information import helpers
from svepa.svepa_information.svepa_event import SvepaEvent
from functools import lru_cache
from typing import List


class StoredSvepaInfo:
    def __init__(self):
        self._load_info()

    def _load_info(self):
        self._info = helpers.load_stored_svepa_info()

    def import_file(self, path):
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

    @lru_cache
    def get_infos(self, platform: str = None, time: datetime.datetime = None, lat: float = None, lon: float = None):
        lst = []
        for key in self._info:
            if platform and key != platform:
                continue
            for _id, _info in self._info[key].items():
                if time and not (_info['start_time'] <= time <= _info['stop_time']):
                    continue
                if lat:
                    if not (_info['start_lat'] and _info['stop_lat']):
                        continue
                    if not (_info['start_lat'] <= lat <= _info['stop_lat']):
                        continue
                if lon:
                    if not (_info['start_lon'] and _info['stop_lon']):
                        continue
                    if not (_info['start_lon'] <= lon <= _info['stop_lon']):
                        continue
                lst.append(_info)
        return lst

    def get_events(self, platform: str = None, time: datetime.datetime = None, lat: float = None, lon: float = None):
        info_lst = self.get_infos(platform=platform, time=time, lat=lat, lon=lon)
        return [SvepaEvent(stored_svepa_info=self, info=info) for info in info_lst]

    def get_children_info(self, event_id: str) -> List[str]:
        lst = []
        for key in self._info:
            for _id, _info in self._info[key].items():
                if _info['parent_event_id'] == event_id:
                    lst.append(_info)
        return lst

    def get_children_events(self, event_id: str) -> List[SvepaEvent]:
        info_lst = self.get_children_info(event_id=event_id)
        return [SvepaEvent(stored_svepa_info=self, info=info) for info in info_lst]

    @lru_cache
    def get_ongoing_events(self, event: SvepaEvent) -> List[SvepaEvent]:
        event_lst = []
        for key in self._info:
            for _id, _info in self._info[key].items():
                ev = None
                if _info['start_time'] and event.start_time <= _info['start_time'] <= event.stop_time:
                    ev = SvepaEvent(stored_svepa_info=self, info=_info)
                elif _info['stop_time'] and event.start_time <= _info['stop_time'] <= event.stop_time:
                    ev = SvepaEvent(stored_svepa_info=self, info=_info)
                elif _info['start_time'] and _info['stop_time']:
                    if _info['start_time'] <= event.start_time <= _info['stop_time']:
                        ev = SvepaEvent(stored_svepa_info=self, info=_info)
                if not ev:
                    continue
                if ev.event_id == event.event_id:
                    continue
                event_lst.append(ev)
        return event_lst

