from abc import ABC, abstractmethod
import datetime
import pathlib
import pandas as pd


class PlatformMetadata(ABC):

    @property
    @abstractmethod
    def base_name_in_svepa(self):
        """ This is the platform name """
        pass

    @abstractmethod
    def get_time(self) -> datetime.datetime:
        """ Should return the time for the measurement as datetime"""
        pass

    @abstractmethod
    def set_event_id(self, event_id: str) -> bool:
        """ Sets the event_id for the measurement """
        pass

    @abstractmethod
    def set_parent_event_id(self, event_id: str) -> bool:
        """ Sets the parent_event_id for the measurement """
        pass


class PlatformMetadataFile(PlatformMetadata):

    @abstractmethod
    def set_file(self, file_path: str):
        """ Sets the file that will be enriched by information from Svepa """
        pass


class Event:
    def __init__(self, all_events: dict, event_info: pd.Series):
        self._all_events = all_events
        self._parent = None
        self._children = set()

        self._info = {}
        for key in event_info.keys():
            value = str(event_info[key])
            if key in ['StartTime', 'StopTime']:
                value = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            self._info[key] = value

    def __repr__(self):
        return '\n'.join([f'Platform:      {self.name}',
                          f'EventID:       {self.event_id}',
                          f'ParentEventID: {self.parent_event_id}',
                          f'StartTime:     {self._info["StartTime"]}',
                          f'StopTime:      {self._info["StopTime"]}'])

    def __str__(self):
        return self.event_id

    def _add_child(self, event):
        self._children.add(event)

    def add_parent_and_children(self):
        for event in self._all_events.values():
            if event.event_id == self.event_id:
                continue
            if self.parent_event_id == event.event_id:
                self._parent = event
                event._add_child(self)
                break

    def check_name_and_time(self, name: str, time: datetime.datetime):
        return self.check_name(name) and self.check_time(time)

    def check_time(self, time: datetime.datetime):
        if self.start_time <= time <= self.stop_time:
            return True
        return False

    def check_name(self, name: str):
        if self.name == name:
            return True
        return False

    def get_event_ids_for_name_and_time(self, name: str, time: datetime.datetime):
        if not self.check_name(name):
            return
        if not self.check_time(time):
            return
        return {'EventID': self._info['EventID'],
                'ParentEventID': self._info['ParentEventID']}

    @property
    def name(self):
        return self._info['Name'].split('.')[0]

    @property
    def event_id(self):
        return self._info['EventID']

    @property
    def parent_event_id(self):
        value =  self._info['ParentEventID']
        if value == 'nan':
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
        return self._children

    def get_children(self, name=None):
        if name:
            return [event for event in self.children if event.name == name]
        return self.children

    def get_related_events(self, name):
        """
        Looks in the relative tree to find related event(s) with the given name.
        Har inte gjort något med dt än!
        """
        events = set()
        for event in self._all_events.values():
            if event.name != name:
                continue
            if event.check_time(self.start_time):
                events.add(event)
            elif self.check_time(event.start_time):
                events.add(event)
        return events


class SvepaInfo(ABC):

    @abstractmethod
    def get_event_ids(self, name: str, time: datetime.datetime):
        """Return EventID and ParentEventID matching the given name and time"""

    @abstractmethod
    def get_event(self, event_id: str = None, name: str = None, time: datetime.datetime = None):
        """ Returns the Event-object matching the given name and time"""


class SvepaInfoFile(SvepaInfo):
    def __init__(self, path):
        self._path = pathlib.Path(path)
        self._event_ids = {}
        self.root_event = None
        self._load_information()
        self._save_hierarchy()

    def _load_information(self):
        """ Loads the information in self._path """
        df = pd.read_excel(self._path, dtype=str)
        for i in df.index:
            event = Event(self._event_ids, df.iloc[i])
            event_id = df.iloc[i]['EventID']
            self._event_ids[event_id] = event

    def _save_hierarchy(self):
        for event in self._event_ids.values():
            event.add_parent_and_children()
            if not event.parent_event_id:
                self.root_event = event

    def get_name_list(self):
        return sorted(set([event.name for event in self._event_ids.values()]))

    def get_event_ids(self, name: str, time: datetime.datetime):
        for event in self._event_ids.values():
            event_ids = event.get_event_ids_for_name_and_time(name=name, time=time)
            if event_ids:
                return event_ids

    def get_event(self, event_id: str = None, name: str = None, time: datetime.datetime = None):
        if event_id:
            return self._event_ids.get(event_id)
        for event in self._event_ids.values():
            if event.check_name_and_time(name=name, time=time):
                return event


if __name__ == '__main__':
    file_path = r'C:\mw\temp_svepa/SVEPAExport_SVEA.2021.013.xlsx'
    df = pd.read_excel(file_path)

    name = 'CTD'
    time = datetime.datetime(2021, 8, 17, 6, 0, 0)

    s = SvepaInfoFile(file_path)

    ctd = s.get_event(event_id='b16ad262-eeec-4c3f-86bb-adafa6c4b2cd')
    st = ctd.parent

