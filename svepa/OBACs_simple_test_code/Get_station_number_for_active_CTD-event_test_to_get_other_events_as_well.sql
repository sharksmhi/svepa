-- Code that gets eventinfo from a CTD-type event (event name that starts with CTD) that is started but not stopped
-- it also gets info about station event and cruise event
select *  
from Counter
-- first where filter gives info about station (parent)
where owner = (
	SELECT parentEventID
	FROM dbo.Event
	INNER JOIN dbo.EventType
	on dbo.Event.EventTypeID = dbo.EventType.EventTypeID

	LEFT OUTER JOIN dbo.TemplateEvent
	on dbo.Event.OriginTemplateEventID = dbo.TemplateEvent.TemplateEventID 

	where StartTime > '2021-05-24' --use todays date convert(date, getDate()), or todays datetime minus 1h: DATEADD(hour,-1,GETDATE())
	and TemplateEvent.Name like 'CTD%'

	--and to only have those that are not yet started
	and StopTime is null)
-- second where filter gives info about event (owner = eventID)
or owner = (
	SELECT EventID
	FROM dbo.Event
	INNER JOIN dbo.EventType
	on dbo.Event.EventTypeID = dbo.EventType.EventTypeID

	LEFT OUTER JOIN dbo.TemplateEvent
	on dbo.Event.OriginTemplateEventID = dbo.TemplateEvent.TemplateEventID 

	where StartTime > '2021-05-24' --use todays date convert(date, getDate()), or todays datetime minus 1h: DATEADD(hour,-1,GETDATE())
	and TemplateEvent.Name like 'CTD%'

	--and to only have those that are not yet started
	and StopTime is null)
-- third where filter gives info about cruise (event name starting with Svea)
or owner = (
	SELECT EventID
	FROM dbo.Event
	INNER JOIN dbo.EventType
	on dbo.Event.EventTypeID = dbo.EventType.EventTypeID

	LEFT OUTER JOIN dbo.TemplateEvent
	on dbo.Event.OriginTemplateEventID = dbo.TemplateEvent.TemplateEventID 

	where StartTime > '2021-05-24' --use todays date convert(date, getDate()), or todays datetime minus 1h: DATEADD(hour,-1,GETDATE())
	and TemplateEvent.Name like 'SVEA%'


	--and to only have those that are not yet started
	and StopTime is null)

 -- also return ID for CTD-event?