import pyodbc


# conn = pyodbc.connect(Driver='{SQL Server}', Server='localhost/SQLEXPRESS', Database='SVEPA', Trusted_Connection='yes')
# conn = pyodbc.connect(Driver='{ODBC Driver 17 for SQL Server}', Server='.\sqlexpress', Database='SVEPA', Trusted_Connection='yes') # funkar!
conn = pyodbc.connect(Driver='{ODBC Driver 17 for SQL Server}', Server='.\sqlexpress', Database='SVEPA', UID='svepa', PWD='svepa') # funkar!

cursor = conn.cursor()
#cursor.execute('SELECT * FROM dbo.EventType')
#cursor.execute('SELECT TemplateName FROM dbo.TemplateEvent order by TemplateName ')

serie = str(int('0010'))


cursor.execute("""
-- Code that gets other eventinfo taken at the same time as CTD-type event (event name that starts with CTD) that is started but not stopped
-- maybe try a test with serial number (Counter for station) instead so you can ask for the info after the CTD event might be stopped.
-- Works with serial number (station counter) =D 2021-09-20 /OBac
-- TODO: check if cruise event is running with starttime < starttime for station (if stopped check also if stoptime ADCP > stoptime station/CTD
-- TODO: hose can chl-a and phytoplankton, check against metadata
select *  
from Event
INNER JOIN dbo.EventType 
on dbo.Event.EventTypeID = dbo.EventType.EventTypeID
left outer join Counter
on dbo.Event.EventID = dbo.Counter.owner
-- first where filter gives info about station (parent)
where 1=1
--and EventType.Name not like 'Station'
--and StopTime is not null
and (
    parentEventID = 
	-- Test to use Station-counter ( our serial number instead)
	(Select EventID 
	FROM dbo.Event
	left outer join Counter
	on dbo.Event.EventID = dbo.Counter.owner
	where 1=1 
	and Counter.Name like 'Station.2021'
	and Counter.Value = '"""+serie+"""' --serie som integer
	)

    or parentEventID = (
        Select parentEventID
        from Event
        where 1=1 
        and EventID = 
            -- Test to use Station-counter ( our serial number instead)
            (Select EventID 
            FROM dbo.Event
            left outer join Counter
            on dbo.Event.EventID = dbo.Counter.owner
            where 1=1 
            and Counter.Name like 'Station.2021'
            and Counter.Value = """+serie+""" --serie som integer
            )    
        )

)

""")


for row in cursor:
    print(row,type(row[0]))

cursor.close()
conn.close()


