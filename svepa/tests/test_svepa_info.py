import svepa
import datetime


def test_event_id():
    platform = 'BOTTLE'
    time = datetime.datetime(2022, 8, 14, 14)
    expected_event_id = 'd1b81dee-f8ff-44ed-a0a6-e530521958d6'
    data = svepa.get_svepa_info(platform=platform, time=time)
    assert data['event_id'] == expected_event_id