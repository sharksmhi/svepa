from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from svepa.svepa_information.svepa_info import StoredSvepaInfo


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