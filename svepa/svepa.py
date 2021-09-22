
from abc import ABC, abstractmethod
import datetime
import pathlib
import pandas as pd


class PlatformMetadata(ABC):

    @property
    @abstractmethod
    def name_in_svepa(self):
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


class Svepa:
    """
    """

    def __init__(self):
        pass

    def event_type_is_running(self, event_type):
        """
        Returns True if an event of the given event_type is running (started but not ended) 
        :param event_type: Type of event (CTD, MVP etc...)
        :return: boolean
        """
        return True

    def get_running_event_types(self):
        """
        Returns all running event types as a list.
        :return: list
        """
        return ['CTD', 'ADCP', 'FERRYBOX']

    def get_event_id_for_running_event_type(self, event_type):
        """
        Returns the EventID of the running event_type.
        Raise SvepaEventTypeNotRunningError if the event_type is not running.
        :param event_type:
        :return: str
        """
        if not self.event_type_is_running(event_type):
            raise # SvepaEventTypeNotRunningError(event_type=event_type)
        import uuid
        return uuid.uuid4()

    def get_parent_event_id_for_running_event_type(self, event_type):
        """
        Returns the EventID of the parent to the running event_type.
        Raise SvepaEventTypeNotRunningError if the event_type is not running.
        :param event_type:
        :return: str
        """
        if not self.event_type_is_running(event_type):
            raise # SvepaEventTypeNotRunningError(event_type=event_type)
        import uuid
        return uuid.uuid4()

    def get_position(self):
        """
        Returns the current position.
        :return: lat, lon
        """
        # raise SvepaNoInformationError('position')
        return 5432.23, 1112.44

    def get_cruise(self):
        """
        Returns the current cruise number. Format???
        :return: str
        """
        # raise SvepaNoInformationError('cruise')
        return '02'

    def get_serno(self):
        """
        Any input parameters???
        Returns the active serno
        :return:
        """
        # raise SvepaNoInformationError('series')
        return '0099'

    def get_station(self):
        """
        Returns the current station name.
        :return:
        """
        # raise SvepaNoInformationError('station')
        return ''
