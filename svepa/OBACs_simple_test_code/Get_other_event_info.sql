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
and (parentEventID = 
	-- Test to use Station-counter ( our serial number instead)
	(Select EventID 
	FROM dbo.Event
	left outer join Counter
	on dbo.Event.EventID = dbo.Counter.owner
	where 1=1 
	and Counter.Name like 'Station.2021'
	and Counter.Value = 10 --serie som integer
	)
	--(SELECT parentEventID --get station event ID
	--FROM dbo.Event
	--INNER JOIN dbo.EventType
	--on dbo.Event.EventTypeID = dbo.EventType.EventTypeID

	--LEFT OUTER JOIN dbo.TemplateEvent
	--on dbo.Event.OriginTemplateEventID = dbo.TemplateEvent.TemplateEventID 

	--where StartTime > '2021-05-24' --use todays date convert(date, getDate()), or todays datetime minus 1h: DATEADD(hour,-1,GETDATE())
	--and TemplateEvent.Name like 'CTD%'

	----and to only have those that are not yet started
	--and StopTime is null)

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
			and Counter.Value = 10 --serie som integer
			)
			
			--(SELECT parentEventID
			--FROM dbo.Event
			--INNER JOIN dbo.EventType
			--on dbo.Event.EventTypeID = dbo.EventType.EventTypeID
			--LEFT OUTER JOIN dbo.TemplateEvent
			--on dbo.Event.OriginTemplateEventID = dbo.TemplateEvent.TemplateEventID 

			--where StartTime > '2021-05-24' --use todays date convert(date, getDate()), or todays datetime minus 1h: DATEADD(hour,-1,GETDATE())
			--and TemplateEvent.Name like 'CTD%'
			---- Test to use Station-counter ( our serial number instead)


			----and to only have those that are not yet started
			--and StopTime is null)

			)

)
-- second where filter gives info about event (owner = eventID)
--or owner = (
--	SELECT EventID
--	FROM dbo.Event
--	INNER JOIN dbo.EventType
--	on dbo.Event.EventTypeID = dbo.EventType.EventTypeID

--	LEFT OUTER JOIN dbo.TemplateEvent
--	on dbo.Event.OriginTemplateEventID = dbo.TemplateEvent.TemplateEventID 

--	where StartTime > '2021-05-24' --use todays date convert(date, getDate()), or todays datetime minus 1h: DATEADD(hour,-1,GETDATE())
--	and TemplateEvent.Name like 'CTD%'

--	--and to only have those that are not yet started
--	and StopTime is null)
---- third where filter gives info about cruise (event name starting with Svea)
--or owner = (
--	SELECT EventID
--	FROM dbo.Event
--	INNER JOIN dbo.EventType
--	on dbo.Event.EventTypeID = dbo.EventType.EventTypeID

--	LEFT OUTER JOIN dbo.TemplateEvent
--	on dbo.Event.OriginTemplateEventID = dbo.TemplateEvent.TemplateEventID 

--	where StartTime > '2021-05-24' --use todays date convert(date, getDate()), or todays datetime minus 1h: DATEADD(hour,-1,GETDATE())
--	and TemplateEvent.Name like 'SVEA%'


--	--and to only have those that are not yet started
--	and StopTime is null)

-- -- also return ID for CTD-event?