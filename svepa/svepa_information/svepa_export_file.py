import datetime
import pathlib
import pandas as pd
import logging


logger = logging.getLogger(__file__)

FILTERED_EVENTS = ['HOSE', 'PHYTOPLANKTON', 'SECCHI', 'ZOOPLANKTON', 'BOTTLE', 'FERRYBOX', 'MVP', 'CTD']


class Event:
    def __init__(self, all_events: dict, event_info: pd.Series):
        self._all_events = all_events
        self._parent = None
        self._children = []

        self._info = {}
        for key in event_info.keys():
            value = str(event_info[key])
            if key in ['StartTime', 'StopTime'] and value:
                value = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            self._info[key] = value

    def __str__(self):
        return '\n'.join([
            '='*100,
            f'Platform:      {self.full_name}',
            f'EventID:       {self.event_id}',
            f'ParentEventID: {self.parent_event_id}',
            f'StartTime:     {self._info["StartTime"]}',
            f'StopTime:      {self._info["StopTime"]}',
            '-' * 100,
        ])

    def __repr__(self):
        return f'Event: {self.full_name} ({self.event_id})'

    def __eq__(self, other):
        if self.event_id == other.event_id:
            return True
        return False

    def _add_child(self, event):
        self._children.append(event)

    def add_parent_and_children(self):
        for event in self._all_events.values():
            if event == self:
                continue
            if self.parent_event_id == event.event_id:
                self._parent = event
                event._add_child(self)
                break

    def check_name_and_time(self, name: str, time: datetime.datetime):
        return self.check_name(name) and self.check_time(time)

    def check_time(self, time: datetime.datetime):
        if not (self.start_time and self.start_time):
            return False
        if self.start_time <= time <= self.stop_time:
            return True
        return False

    def check_name(self, name: str):
        if self.name == name:
            return True
        return False

    @property
    def event_type(self):
        return self._info['EventType']

    @property
    def full_name(self):
        return self._info['Name']

    @property
    def name(self):
        return self.full_name.split('.')[0].upper()

    @property
    def event_id(self):
        return self._info['EventID']

    @property
    def parent_event_id(self):
        value = self._info['ParentEventID']
        if not value:
            value = None
        return value

    @property
    def start_time(self):
        return self._info['StartTime']

    @property
    def stop_time(self):
        return self._info['StopTime']

    @property
    def parent(self):
        return self._parent

    @property
    def children(self):
        return list(self._children)

    def get_children(self, name: str = None) -> list:
        if name:
            return [event for event in self.children if event.name == name]
        return self.children

    def get_ongoing_events(self, **kwargs):
        ongoing_events = []
        for event in self._all_events.values():
            if self == event:
                continue
            if event.check_time(self.start_time) or event.check_time(self.stop_time):
                ongoing_events.append(event)
        if kwargs.get('filter'):
            ongoing_events = [event for event in ongoing_events if event.name in FILTERED_EVENTS]
        return ongoing_events

    def get_ongoing_event_names(self, **kwargs):
        return [event.name for event in self.get_ongoing_events(**kwargs)]

    def get_info(self) -> dict:
        """Returns a dict with information about the event"""
        info = dict(
            event_type=self.event_type,
            name=self.name,
            full_name=self.full_name,
            event_id=self.event_id,
            parent_event_id=self.parent_event_id,
            start_time=self.start_time,
            stop_time=self.stop_time,
            ongoning_events=self.get_ongoing_event_names(filter=True)
        )
        return info


class SvepaExportFile:
    def __init__(self, path):
        self._path = pathlib.Path(path)
        self._events = {}
        self.root_event = None
        self._load_information()
        self._save_hierarchy()

    def __repr__(self):
        return f'Svepa export file: {self.path}'

    @property
    def path(self):
        return self._path
    
    @property
    def events(self):
        return self._events

    @property
    def cruise(self):
        return self.root_event.full_name.split('.')[-1].strip('0')

    def _load_information(self):
        """ Loads the information in self._path """
        logger.info(f'Loading Svepa export file: {self.path}')
        df = pd.read_excel(self._path, dtype=str, keep_default_na=False)
        for i in df.index:
            event = Event(self._events, df.iloc[i])
            if not event.start_time:
                continue
            self._events[event.event_id] = event

    def _save_hierarchy(self):
        for event in self._events.values():
            event.add_parent_and_children()
            if not event.parent_event_id:
                if not event.event_id:
                    continue
                self.root_event = event

    def get_name_list(self):
        return sorted(set([event.name for event in self._events.values()]))

    def get_platform_events(self, name: str):
        events = []
        for event in self._events.values():
            if event.check_name(name):
                events.append(event)
        return events

    def get_event(self, event_id: str = None, name: str = None, time: datetime.datetime = None):
        if event_id:
            return self._events.get(event_id)
        for event in self._events.values():
            if event.check_name_and_time(name=name, time=time):
                return event

    def _add_general_info(self, info: dict) -> None:
        info['cruise'] = self.cruise

    def get_platforms_info(self):
        all_info = {}
        # for plat in FILTERED_EVENTS:
        for plat in self.get_name_list():
            events = self.get_platform_events(plat)
            if not events:
                continue
            all_info[plat] = {}
            for event in events:
                info = event.get_info()
                all_info[plat][info['event_id']] = info
        return all_info


