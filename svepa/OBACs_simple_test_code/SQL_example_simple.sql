USE SVEPA
GO
SELECT [TimeCollected]
      ,[TelegramID]
      ,[Value01]
      ,[Value03]
  FROM [SVEPA].[dbo].[Sample]
  where TimeCollected > '2021-05-24' and TimeCollected < '2021-05-26'
  and TelegramID like '%GGA%'
  order by TimeCollected

/*För SOG körde jag följande:
SELECT [TimeCollected]
      ,[TelegramID]
      ,[Value04]
  FROM [SVEPA].[dbo].[Sample]
  where TimeCollected > '2020-03-27' and TimeCollected < '2020-04-05'
  and TelegramID like '%VTG%'
  order by TimeCollected
  */

 