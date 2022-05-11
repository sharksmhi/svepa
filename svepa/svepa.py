
from abc import ABC, abstractmethod
import datetime
import pathlib
import logging
import pypyodbc
from svepa import exceptions


logger = logging.getLogger(__name__)


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

class DBCommunication:

    def __init__(self):
        self.cursor = False
        self.cnxn = False

    def DBConnect(self, dbadress = 'pg-shark-int', dbname = 'shark-int', user = 'skint', password = 'Bvcdew21', driver = '{PostgreSQL Unicode(x64)}'):

        if not self.cnxn:
            # TEST
            # cnxn = pyodbc.connect(DRIVER = '{PostgreSQL Unicode}', server = 'postgresiov01',sharktoolbox_database = 'shark-int', uid = 'skint.t', pwd = 'Aesrdt65',  autocommit=True)

            # PROD
            #if db == 'prod':
            try:
                self.cnxn = pypyodbc.connect(DRIVER=driver, server=dbadress,
                                           database=dbname, uid=user, pwd=password, autocommit=True)
            except:
                # Different driver
                # logger.warning('unable to connect, check input information')
                raise exceptions.SvepaConnectionError(message='unable to connect, check input information')
                #print('unable to connect, check input information')
                #self.cnxn = pypyodbc.connect(DRIVER='{PostgreSQL Unicode(x64)}', server='pg-shark-int',
                #                           database='shark-int', uid='skint', pwd='Bvcdew21', autocommit=True)

        if not self.cursor:
            self.cursor = self.cnxn.cursor()
            print('Connected to %s' % dbname)
        else:
            print('Already connected to %s' % dbname)

        # ===========================================================================

    def DBDisconnect(self):

        '''Closes the cursor only'''

        if self.cursor:
            self.cursor.close()
            self.cursor = False
            print('Disconnected from db')
        else:
            print('Not connected.. nothing to close')
        import pypyodbc


class Svepa:

    """
    list of event types (event_type):
    SVEA.{yyyy}.{nnn:SVEA.{yyyy}}               - cruise type

    Station.{nnnn:Station.{yyyy}}               - station type

    ADCP.{nnn:ADCP.{yyyy}}                      - cruise event
    Ferrybox.{nnn:Ferrybox.{yyyy}}              - cruise event
    MVP.{nnn:MVP.{yyyy}}                        - cruise event

    Bottle.{nnnn:Bottle.{yyyy}}                 - station event
    CTD.{nnnnn:CTDcounter.{yyyy}}               - station event
    Ferrybox BTL.{nnn:FerryboxBTL.{yyyy}}       - station event
    Hose.{nnnn:Hose.{yyyy}}                     - station event
    MVPstation.{nnnn:MVPstation.{yyyy}}         - station event
    Phytoplankton.{nnnn:Phytoplankton.{yyyy}}   - station event
    Secchi.{nnnn:Secchi.{yyyy}}                 - station event
    Zooplankton.{nnnn:Zooplankton.{yyyy}}       - station event
    """

    def __init__(self):
        logger.debug('Test')
        pass

    def _event_type_is_running(self, event_type):
        """
        Returns True if an event of the given event_type is running (started but not ended) 
        :param event_type: Type of event (CTD, MVP etc...)
        :return: boolean
        """

        if event_type is null:
            event_type = "CTD"

        active_time = 1 # 1 hour for CTD.. set time for every event? or allow time as input? or don't use time at all?
        # as an example a ferrybox event can run for the entire cruise, up to two weeks.
        # - return time but make no check or warning in this method

        query = """SELECT EventID, starttime, datediff(hour, cast(StartTime as datetime), GETDATE())
            FROM dbo.Event
            INNER JOIN dbo.EventType
            on dbo.Event.EventTypeID = dbo.EventType.EventTypeID
            LEFT OUTER JOIN dbo.TemplateEvent
            on dbo.Event.OriginTemplateEventID = dbo.TemplateEvent.TemplateEventID
            where 1=1
            and StartTime is not null
            --and StartTime > DATEADD(hour,-"""+active_time+""",GETDATE())
            and TemplateEvent.Name like '"""+event_type+""".%'
            and StopTime is null
            and HasBeenStarted = 1"""


        # if query returns nothing (null)? then return false else return True.
        # maybe number of answers and check StartTime?
        # check

        # added HasBeenStarted = 1 and just check that StartTime is not null.

        # connect
        # run query
        # disconnect

        return True

    def get_running_event_types(self):
        """
        Returns all running event types as a list.
        :return: list
        """
        return ['CTD', 'ADCP', 'FERRYBOX']

    def get_info_for_running_event_type(self, event_type):
        """
        Returns the information of the running event_type, ID, start_time, etc.
        Raise SvepaEventTypeNotRunningError if the event_type is not running.
        :param event_type:
        :return: dict
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


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    s = Svepa()
