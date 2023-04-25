# from svepa import svepa
import svepa
import logging

SVP = svepa.Svepa()

# logger = logging.getLogger('DBCommunication')
logging.basicConfig(level=logging.DEBUG)

DB = svepa.DBCommunication()

# anslut på testserver winserv817
#DB.DBConnect(dbadress = 'localhost\\SQLEXPRESS', dbname = 'SVEPA', user = 'svepareader', password = 'svepareader', driver = 'ODBC Driver 17 for SQL Server')
# ta bort användare och lösen och lägg i extern fil, json eller yaml

# Anslut på Svea
DB.DBConnect(dbadress = 'svepadb.svea.slu.se', dbname = 'SVEPA', user = 'svepareader', password = 'svepareader', driver = 'SQL Server')



# ===========  Testing parent id  ===========

parent_test = False
#parent_test = True

if parent_test:

    #info = SVP.get_parent_event_id(event_id='96B29A4F-0FFC-439D-9A73-F08A93B3EAC2', DB=DB)
    info = SVP.get_parent_event_id(event_id='94BA7787-FADA-4888-9C42-271DA44117DD', DB=DB)

    print(info)

    event_id_temp = info[0]
    event_type_temp = info[1]

    print(event_id_temp,type(event_id_temp))

    while event_type_temp != 'Trip' and event_type_temp:
        info = SVP.get_parent_event_id(event_id=event_id_temp, DB=DB)
        event_id_temp = info[0]
        event_type_temp = info[1]
        print(info)

# ===========================================
# test på Svea, output:
# ['9E52F9F9-D75D-4AF9-8E98-D0EB4C38CCCE', 'Trip']


# ===========  Testing running event  ===========

connected_test = False
#connected_test = SVP._event_type_is_running(event_type = 'CTD')

#connected_test = SVP._event_type_is_running(event_type = 'MVP')

connected_test = SVP._event_type_is_running(event_type = 'ADCP')

if connected_test:

    if type(connected_test[1]) == list:
        print('number of active events: %i' % len(connected_test[1]))
        for i in range(len(connected_test[1])):
            print(connected_test[1][i], connected_test[3][i])
    else:
        print('number of active events: 1')
        print(connected_test[1], connected_test[3])
else:
    pass
    print('--- no active event ---')
# ===========================================
# Test på Svea (ADCP som har ett icke avslutat event), output:
# number of active events: 1
# b'94BA7787-FADA-4888-9C42-271DA44117DD' 1012

# Test för CTD och inget aktivt event, output:
# --- no active event ---


# ===========  Testing get info for running event  ===========

active_event_info = SVP.get_info_for_running_event_type('CTD', DB)

active_event_info = SVP.get_info_for_running_event_type('ADCP', DB)

# active_event_info = False

if active_event_info:

    if len(active_event_info['event_id']) > 1:
        print('number of active events: %i, event info below:' % len(active_event_info['event_id'][0]))
        for i in range(len(active_event_info['event_id'])):
            for key in active_event_info.keys():
                print(key, active_event_info[key][i])

    else:
        print('number of active events: 1, event info below:')
        for key in active_event_info.keys():
            print(key, active_event_info[key][0])
else:
    pass
    # print('--- no active event ---')

# ===========================================
# Test på Svea, output:
# number of active events: 1, event info below:
# event_id 94BA7787-FADA-4888-9C42-271DA44117DD
# event_date 2023-03-09 07:01:29.553000
# event_length 1013
# event_type Event
# counter 3

DB.DBDisconnect()
