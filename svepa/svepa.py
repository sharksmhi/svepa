
from abc import ABC, abstractmethod
import datetime
import pathlib
import logging
import pypyodbc
import yaml
import numpy as np
try:
    from svepa import exceptions
except:
    import exceptions

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

    def __init__(self,
                 dbadress=None,
                 dbname=None,
                 user=None,
                 password=None,
                 driver=None):

        # self.dbadress = dbadress,
        # self.dbname = dbname,
        # self.user = user,
        # self.password = password,
        # self.driver = driver

        self.dbadress = dbadress
        self.dbname = dbname
        self.user = user
        self.password = password
        self.driver = driver

        self.cursor = False
        self.cnxn = False

    def connect(self):

        if not self.cnxn:
            try:
                # print(f'{self.driver=}')
                # print(f'{self.dbadress=}')
                # print(f'{self.dbname=}')
                # print(f'{self.user=}')
                # print(f'{self.password=}')
                self.cnxn = pypyodbc.connect(DRIVER=self.driver, server=self.dbadress,
                                           database=self.dbname, uid=self.user, pwd=self.password, autocommit=True)
            except:
                raise exceptions.SvepaConnectionError(message='unable to connect, check input information')

        if not self.cursor:
            self.cursor = self.cnxn.cursor()
            # print('Connected to %s' % dbname)
            logger.debug('Connected to %s' % self.dbname)
        else:
            # print('Already connected to %s' % dbname)
            logger.debug('Already connected to %s' % self.dbname)
        # ===========================================================================

    def disconnect(self):
        ''' Closes the connection and cursor'''

        # cursor first
        if self.cursor:
            self.cursor.close()
            self.cursor = False
            logger.debug('Cursor closed')
            #print('Cursor closed')
        else:
            #print('No cursor to close.. ')
            logger.debug('No cursor to close.. ')
        import pypyodbc

        if self.cnxn:
            self.cnxn.close()
            self.cnxn = False
            #print('Disconnected from db')
            logger.debug('Disconnected from db')

        else:
            #print('Not connected.. nothing to close')
            logger.debug('Not connected.. nothing to close')


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
        #logger.debug('Test')
        pass

    def event_type_is_running(self, event_type, db):
        """
        Returns True if an event of the given event_type is running (started but not ended) 
        :param event_type: Type of event (CTD, MVP etc...)
        :return: boolean
        """

        # TODO: korta ner denna och använd koden i annan funktion

        if event_type is None:
            event_type = "CTD"

        active_time = '1' # 1 hour for CTD.. set time for every event? or allow time as input? or don't use time at all?
        # as an example a ferrybox event can run for the entire cruise, up to two weeks.
        # - return time but make no check or warning in this method

        query = """SELECT EventID, cast(StartTime as datetime) as "date", datediff(hour, cast(StartTime as datetime), GETDATE()) as "hours"
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

        db.cursor.execute(query)

        counter = 0
        eventid = []
        eventdate = []
        eventlength = []
        for row in db.cursor.fetchall():
            counter +=1
            #print(row,type(row),len(row))
            #print(row[0],row[1],row[2])
            eventid.append(row[0])
            eventdate.append(row[1])
            eventlength.append(row[2])
            #pp.pprint(dict(zip(columns, row)))

        if counter == 0:
            return False
        elif counter == 1:
            return True, eventid[0], eventdate[0], eventlength[0]
        else: # several active events...
            logger.warning('!!! %i active events of type %s !!! -- It is highly advised to stop the older events!' % (len(eventid),event_type))
            return True, eventid, eventdate, eventlength

    def get_running_event_types(self):
        """
        Returns all running event types as a list.
        :return: list
        """

        return ['CTD', 'ADCP', 'FERRYBOX']

    def get_info_for_running_event_type(self, event_type, db):
        event_id, _ = self.get_event_id_for_running_event_type(event_type, db) # Returns a tuple...
        return self.get_info_for_event(event_id, db)

    def get_event_id_for_running_event_type(self, event_type, db):
        """
        Returns the information of the running event_type, ID, start_time, etc.
        Raise SvepaEventTypeNotRunningError if the event_type is not running.
        :param event_type:
        :param db:
        :return: dict
        """

        if event_type is None:
            event_type = "CTD"

        if not self.event_type_is_running(event_type, db):
            raise exceptions.SvepaEventTypeNotRunningError(event_type=event_type)

        query = """
            SELECT cast(EventID as varchar(36)),
            TemplateEvent.Name
            FROM dbo.Event
            INNER JOIN dbo.EventType
            on dbo.Event.EventTypeID = dbo.EventType.EventTypeID
            LEFT OUTER JOIN dbo.TemplateEvent
            on dbo.Event.OriginTemplateEventID = dbo.TemplateEvent.TemplateEventID
            where 1=1
            and StartTime is not null
            and TemplateEvent.Name like '"""+event_type+""".%'
            and StopTime is null
            and HasBeenStarted = 1"""

        db.cursor.execute(query)
        data_list = []
        for row in db.cursor.fetchall():

            #print(row,type(row),len(row))
            #print(row[0],row[1],row[2])
            data = dict()
            data['event_id'] = row[0]
            data['event_template_type'] = row[1]
            data_list.append(data)
            #pp.pprint(dict(zip(columns, row)))

        if len(data_list) == 0:
            return False
        elif len(data_list) == 1:
            return data_list[0]['event_id'], data_list[0]['event_template_type']
        else:  # several active events...
            raise exceptions.SeveralSvepaEventsRunningError(event_ids=[d['event_id'] for d in data_list])

    def get_info_for_event(self, event_id, db):
        """
        Returns the information of the event: ID, start_time, etc.
        :param event_type:
        :return: dict
        """
        print(f'{event_id=}')

        if event_id is None:
            raise exceptions.SvepaNoInformationError()

        query = """SELECT cast(EventID as varchar(36)) "eventid", 
                cast(StartTime as datetime) as "starttime", 
                cast(StopTime as datetime) as "stoptime", 
                datediff(minute, cast(StartTime as datetime), cast(StopTime as datetime)) as "minutes",
                StartLongitude as "lon",
                StartLatitude as "lat",
                EventType.Name as "eventtype", 
                TemplateEvent.Name "templatename",
                Counter.value as "counter", 
                cast(parentEventID as varchar(36)) as "parent_eventid"
                
                FROM dbo.Event
                INNER JOIN dbo.EventType
                on dbo.Event.EventTypeID = dbo.EventType.EventTypeID
                LEFT OUTER JOIN dbo.TemplateEvent
                on dbo.Event.OriginTemplateEventID = dbo.TemplateEvent.TemplateEventID
                Join dbo.Counter
                on dbo.Event.EventID = dbo.Counter.Owner
                where 1=1
                and StartTime is not null
                and EventID = '""" + event_id + """'
                --and StopTime is null
                and HasBeenStarted = 1"""

        # run query
        db.cursor.execute(query)

        data_list = []
        for row in db.cursor.fetchall():
            data = dict()
            data['longitude'] = ''
            data['latitude'] = ''

            data['event_id'] = row[0]
            data['event_start_time'] = row[1]
            data['event_stop_time'] = row[2]
            data['event_length_minutes'] = row[3]
            if row[4] is not None:
                data['longitude'] = ('%02i' % float(row[4])) + ('%05.2f' % ((float(row[4])-(np.floor(float(row[4]))))*60))
            else:
                logger.warning('No longitude given from Svepa')
            if row[5] is not None:
                data['latitude'] = ('%02i' % float(row[5])) + ('%05.2f' % ((float(row[5])-(np.floor(float(row[5]))))*60))
            else:
                logger.warning('No latitude given from Svepa')
            data['event_type'] = row[6]
            data['event_template_type'] = row[7]
            data['counter'] = row[8]
            data['parent_event_id'] = row[9]  # Added 2023-09-14  //MagW
            data_list.append(data)
            # pp.pprint(dict(zip(columns, row)))

        if len(data_list) == 0:
            return False
        elif len(data_list) == 1:
            return data_list[0]
        else:  # several active events...
            raise exceptions.SeveralSvepaEventsRunningError(event_ids=[d['event_id'] for d in data_list])

    def get_parent_event_id_for_running_event_type(self, event_type):
        # TODO: get parent for running event type is probably ok, but also write a function to get get parent event_id for any event_id
        """
        Returns the EventID of the parent to the running event_type.
        Also return counter (for station) which is used as serial number for CTD
        Raise SvepaEventTypeNotRunningError if the event_type is not running.
        :param event_type:
        :return: str
        """
        if not self.event_type_is_running(event_type):
            raise # SvepaEventTypeNotRunningError(event_type=event_type)
        import uuid
        return uuid.uuid4()

    def get_parent_event_id(self, event_id, db, info_level = 'basic'):
        """
       Returns the EventID of the parent and the EventType name of the parent as default (info_level = 'basic').
       If you set info_level = 'full' start time, stop time and counter for the parent are also returned.
       Raise SvepaNoInformationError if the EventID is missing in database or if no EventID is supplied.
       :param eventID:
       :return: str
       """
        if event_id is None:
            raise exceptions.SvepaNoInformationError()

        query = """SELECT cast(parentEventID as varchar(36)),
                EventType.Name, cast(StartTime as datetime), 
                cast(StopTime as datetime), 
                Counter.Value
                FROM dbo.Event
                left outer JOIN dbo.EventType
                on dbo.Event.EventTypeID = dbo.EventType.EventTypeID
                Join dbo.Counter
                on dbo.Event.EventID = dbo.Counter.Owner
                where 1=1
                and EventID = '""" + event_id + """'
                """


        # run query
        db.cursor.execute(query)

        # result = db.cursor.fetchall()
        # print(f'get_parent_event_id: {event_id=}')
        # print(f'get_parent_event_id: {result=}')
        # if not result:
        #     raise Exception

        parent_event_id = None
        parent_event_type = None
        parent_event_start = None
        parent_event_stop = None
        parent_event_counter = None

        for row in  db.cursor.fetchall():
            if row is None:
                print('row is None')
                raise exceptions.SvepaNoInformationError()
            elif not row:
                print('row is empty')
                raise exceptions.SvepaNoInformationError()
            else:
                parent_event_id = row[0]

                if parent_event_id:
                    query_type = """SELECT EventType.Name,
                                    cast(StartTime as datetime), 
                                    cast(StopTime as datetime), 
                                    Counter.Value
                                    FROM dbo.Event
                                    left outer JOIN dbo.EventType
                                    on dbo.Event.EventTypeID = dbo.EventType.EventTypeID
                                    Join dbo.Counter
                                    on dbo.Event.EventID = dbo.Counter.Owner
                                    where 1=1
                                    and EventID = '""" + parent_event_id + """'
                                    """

                    db.cursor.execute(query_type)

                    result = db.cursor.fetchall()
                    if not result:
                        raise Exception

                    for row_parent in db.cursor.fetchall():
                        parent_event_type = row_parent[0]

                        parent_event_start = row_parent[1]
                        parent_event_stop = row_parent[2]
                        parent_event_counter = row_parent[3]

                return dict(
                    child_event_id=event_id,
                    event_id=parent_event_id,
                    event_type=parent_event_type,
                    event_start=parent_event_start,
                    event_stop=parent_event_stop,
                    event_counter=parent_event_counter 
                )

        if info_level.upper() == 'FULL':
            return dict(
                event_id=event_id,
                parent_event_id=parent_event_id,
                parent_event_type=parent_event_type,
                parent_event_start=parent_event_start,
                parent_event_stop=parent_event_stop,
                parent_event_counter=parent_event_counter
            )
        else:
            return dict(
                event_id=event_id,
                parent_event_id=parent_event_id,
                parent_event_type=parent_event_type
            )


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


def get_current_station_info(path_to_svepa_credentials=None, **cred):
    svp = Svepa()
    all_cred = {}
    if path_to_svepa_credentials:
        with open(path_to_svepa_credentials) as fid:
            all_cred = yaml.safe_load(fid)
    all_cred.update(cred)
    db = DBCommunication(**all_cred)
    db.connect()
    data = {}
    event_info = svp.get_info_for_running_event_type('CTD', db=db)
    # trip_info = svp.get_info_for_running_event_type('Trip', db=db)
    trip_info = svp.get_info_for_running_event_type('SVEA', db=db)  # Added 2023-09-14  //MagW
    data.update(event_info)
    # data['event_id'] = event_info['event_id']
    data['lat'] = event_info['latitude']
    data['lon'] = event_info['longitude']
    # data['parent_event_id'] = svp.get_parent_event_id(event_info['parent_event_id'], db)
    data['parent_event_info'] = svp.get_info_for_event(event_info['parent_event_id'], db)  # // MagW
    data['trip_info'] = trip_info  # // MagW
    db.disconnect()
    return data
