# from svepa import svepa
import svepa

# DB = svepa.DBCommunication()

# DB.DBConnect(dbadress = 'localhost\\SQLEXPRESS', dbname = 'SVEPA', user = 'svepareader', password = 'svepareader', driver = 'ODBC Driver 17 for SQL Server')

# DB.DBDisconnect()

SVP = svepa.Svepa()

connected_test = SVP._event_type_is_running(event_type = 'CTD')

print(connected_test, connected_test[1], type(connected_test[1]))