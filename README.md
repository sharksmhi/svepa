# Pythonpaket för att söka ut information och relationer mellan aktiviteter (event) i Sveas eventsystem SVEPA

## Installera: 
- Senaste version från från github: 
```cmd 
pip install git+git+https://github.com/sharksmhi/svepa.git@v1.0.0
```
- Lokalt wheel: 
```cmd 
pip install <sökväg till wheel>
```

## Kom igång:
```python 
import svepa 

# Uppdaterar till senast tillgängliga informationen från Svepa (datamängd ligger på github)
svepa.update_local_svepa_data()  

# Hämta event baserat på platform/station och tid
ctd_event = svepa.get_svepa_event('ctd', time='2024-01-11 17:00') 
print(ctd_event)
``` 

```cmd 
>>>
==============================================================================================================
SvepaEvent: CTD.00008 [2024-01-11 16:59:34 - 2024-01-11 17:22:00] (416a5c52-7b27-4b52-9861-61e6debd9d24)
--------------------------------------------------------------------------------------------------------------
  event_id                      416a5c52-7b27-4b52-9861-61e6debd9d24
  event_type                    Event
  full_name                     CTD.00008
  id                            00008
  name                          CTD
  ongoning_event_names          ['FERRYBOX', 'BOTTLE']
  parent_event_id               2bb711e8-9f10-44b6-893c-aadc5701984c
  start_lat                     56.23333035
  start_lon                     12.3699217
  start_time                    2024-01-11 16:59:34
  stop_lat                      56.2333248166667
  stop_lon                      12.3699247
  stop_time                     2024-01-11 17:22:00
```


```python 
# Lista tillgängliga attribut för ett event 
ctd_event.attributes
```

```cmd
>>>
['event_id', 'event_type', 'full_name', 'id', 'name', 'ongoning_event_names', 'parent_event_id', 'start_lat', 'start_lon', 'start_time', 'stop_lat', 'stop_lon', 'stop_time']
``` 

```python 
# Plocka ut eventet som är överordnat. I det här fallet får vi ut eventet för stationen
# Motsvarande finns för ctd_event.children (just för ctd är den tom men för t.ex en station får man ut alla event som loggats vid stationen. 
ctd_event.parent
```

```cmd
>>>
SvepaEvent: Kullen.0008 [2024-01-11 16:59:29 - 2024-01-11 17:22:00] (2bb711e8-9f10-44b6-893c-aadc5701984c)
``` 

```python 
# Plocka ut ett event som pågick samtidigt
ferrybox_event = ctd_event.get_ongoing_event('ferrybox')
print(ferrybox_event)
```

```cmd 
>>>
==============================================================================================================
SvepaEvent: Ferrybox.001 [2024-01-11 06:35:15 - 2024-01-17 13:11:48] (2524462b-7045-4271-ac73-beb5d5e85c21)
--------------------------------------------------------------------------------------------------------------
  event_id                      2524462b-7045-4271-ac73-beb5d5e85c21
  event_type                    Event
  full_name                     Ferrybox.001
  id                            001
  name                          FERRYBOX
  ongoning_event_names          []
  parent_event_id               6655e2e8-75d4-44ea-8fce-eda167337449
  start_lat                     57.2477621333333
  start_lon                     11.5495611333333
  start_time                    2024-01-11 06:35:15
  stop_lat                      58.2753082666667
  stop_lon                      11.4475457333333
  stop_time                     2024-01-17 13:11:48
```


```python 
# Få ut en lista på alla event med givet kriterie 
# Följande val finns:
#     platform
#     time
#     lat
#     lon
#     year
#     month
all_events = svepa.get_svepa_events(time='2024-01-11 17:00')
print(all_events)
```

```cmd 
>>>
[SvepaEvent: ADCP.001 [2024-01-10 21:15:23 - 2024-01-17 01:45:00] (cf32d985-d5d3-47da-91c0-a582efb14185), SvepaEvent: Bottle.0004 [2024-01-11 16:59:37 - 2024-01-11 17:22:00] (de18982b-aab2-4623-81be-f1e3d16980cc), SvepaEvent: CTD.00008 [2024-01-11 16:59:34 - 2024-01-11 17:22:00] (416a5c52-7b27-4b52-9861-61e6debd9d24), SvepaEvent: Ferrybox.001 [2024-01-11 06:35:15 - 2024-01-17 13:11:48] (2524462b-7045-4271-ac73-beb5d5e85c21), SvepaEvent: Kullen.0008 [2024-01-11 16:59:29 - 2024-01-11 17:22:00] (2bb711e8-9f10-44b6-893c-aadc5701984c), SvepaEvent: SVEA.2024.002 [2024-01-10 18:10:31 - 2024-01-17 13:11:52] (6655e2e8-75d4-44ea-8fce-eda167337449), SvepaEvent: Trip Position (Cruise-event) [2024-01-11 02:00:00 - 2024-01-17 01:45:00] (8b812920-0cd5-4fe8-8388-5482f26a3b5a), SvepaEvent: Weather_QNH [2024-01-11 16:59:40 - 2024-01-11 17:22:00] (ac7b2c66-2d14-4429-b807-c7bca2cbbce8)]
```