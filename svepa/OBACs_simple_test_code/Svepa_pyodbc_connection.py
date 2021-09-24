import pyodbc


# conn = pyodbc.connect(Driver='{SQL Server}', Server='localhost/SQLEXPRESS', Database='SVEPA', Trusted_Connection='yes')
# conn = pyodbc.connect(Driver='{ODBC Driver 17 for SQL Server}', Server='.\sqlexpress', Database='SVEPA', Trusted_Connection='yes') # funkar!
conn = pyodbc.connect(Driver='{ODBC Driver 17 for SQL Server}', Server='.\sqlexpress', Database='SVEPA', UID='svepa', PWD='svepa') # funkar!

cursor = conn.cursor()
#cursor.execute('SELECT * FROM dbo.EventType')
#cursor.execute('SELECT TemplateName FROM dbo.TemplateEvent order by TemplateName ')



cursor.execute("""
    select value from Counter
    where owner = (
        SELECT parentEventID
        FROM dbo.Event
        INNER JOIN dbo.EventType
        on dbo.Event.EventTypeID = dbo.EventType.EventTypeID
        LEFT OUTER JOIN dbo.TemplateEvent
        on dbo.Event.OriginTemplateEventID = dbo.TemplateEvent.TemplateEventID
        where StartTime > '2021-05-24'
        and TemplateEvent.Name like 'CTD%'
        and StopTime is null)
    """)


for row in cursor:
    print(row[0],type(row[0]))

cursor.close()
conn.close()


# ('02F01728-1228-4C94-BD86-1F8DFC9BB77E', 'SubEvent', True, False)
# ('59389D3E-BDE4-4E13-BFB6-3E616AE27C7D', 'Aggregate', True, True)
# ('571318D1-C4EE-431D-884B-6EE7A5182D18', 'Trip', True, False)
# ('8932A803-7D04-418A-9FE2-7C10C4DF923D', 'Sample', True, True)
# ('7699307C-05DC-4893-B134-8D47A42D1CF3', 'Event', True, False)
# ('9A24A907-E737-4866-877E-EEACCC722E4B', 'Survey', True, False)
# ('D2518E3F-A52E-43A0-B5DD-F33E4907DA10', 'Station', True, False)
