import datetime
import logging
import pickle
from pathlib import Path
from functools import lru_cache

import yaml


logger = logging.getLogger(__file__)

INFO_FILE_PATH = Path(Path(__file__).parent, 'svepa_info.yaml')
PICKLE_INFO_FILE_PATH = Path(Path(__file__).parent, 'svepa_info.pickle')


@lru_cache
def load_stored_svepa_info():
    return load()


def _load_pickle():
    if not PICKLE_INFO_FILE_PATH.exists():
        return
    with open(PICKLE_INFO_FILE_PATH, 'rb') as fid:
        return pickle.load(fid)


def _load_yaml():
    if not INFO_FILE_PATH.exists():
        return {}
    with open(INFO_FILE_PATH) as fid:
        return yaml.safe_load(fid)


def _save_pickle(all_info):
    with open(PICKLE_INFO_FILE_PATH, 'wb') as fid:
        pickle.dump(all_info, fid)


def _save_yaml(all_info):
    with open(INFO_FILE_PATH, 'w') as fid:
        yaml.safe_dump(all_info, fid)


def load():
    all_info = None
    try:
        all_info = _load_pickle()
        logger.info('Pickle file loaded')
    except:
        pass
    if not all_info:
        all_info = _load_yaml()
        logger.info('YAML file loaded')
        _save_pickle(all_info)
    _convert_to_datetime(all_info)
    return all_info


def save(all_info):
    _convert_to_date_string(all_info)
    _save_pickle(all_info)
    _save_yaml(all_info)


def _convert_to_date_string(info):
    if not isinstance(info, dict):
        return
    for key, value in info.items():
        if 'time' in key:
            info[key] = value.strftime('%Y%m%d%H%M%S')
        _convert_to_date_string(info[key])


def _convert_to_datetime(info):
    if not isinstance(info, dict):
        return
    for key, value in info.items():
        if 'time' in key:
            info[key] = datetime.datetime.strptime(value, '%Y%m%d%H%M%S')
        _convert_to_datetime(info[key])

