SELECT Event.EventID
	,dbo."EventType"."Name" as "Event type"
	,dbo.TemplateEvent.Name as "TemplateEvent name"
	,dbo.TemplateEvent.TemplateName as "Template name"
	--,[Event].[EventTypeID]
	,[StartTime]
	,[StopTime]
	,[Event].[Name]
	,[StartLongitude]
	,[StartLatitude]
	,[StopLongitude]
	,[StopLatitude]
	,[parentEventID]
	,[OriginTemplateEventID]
	,[AggregateCount]
	,[HasBeenStarted]
	,[Subdivision]
	,[ICES]
	,Event.Valid
	,Parameter.*
FROM [SVEPA].[dbo].[Event] 
INNER JOIN dbo.EventType 
on dbo.Event.EventTypeID = dbo.EventType.EventTypeID

LEFT OUTER JOIN dbo.TemplateEvent
on dbo.Event.OriginTemplateEventID = dbo.TemplateEvent.TemplateEventID 

LEFT OUTER JOIN dbo.Parameter
on dbo.Event.EventID = dbo.Parameter.EventID

--LEFT OUTER JOIN dbo.Equipment
--on dbo.Parameter.EventID = dbo.Parameter.EventID

where StartTime > '2021-05-24' --use todays date convert(date, getDate()), or todays datetime minus 1h: DATEADD(hour,-1,GETDATE())
and TemplateEvent.Name like 'CTD%'
--and TemplateEvent.Name like 'Station%'

--and to only have those that are not yet started
and StopTime is null


 