from math import floor
from random import random
from yandex_music import Client
from radio_mood import RadioMood


def get_tracks(token, mood):
    client = Client(token, report_new_fields=False)

    _stations = client.rotor_stations_list()
    _station = _stations[0].station
    _station_id = f'{_station.id.type}:{_station.id.tag}'
    client.rotor_station_settings2(_station_id, mood, 'default')
    _station_from = _station.id_for_from

    radio = RadioMood(client, mood)

    first_track = radio.start(_station_id, _station_from)
    track_list = list()
    first_track.download(first_track.title)
    track_list.append(first_track.title)
    for i in range(1):
        next_track = radio.play_next()
        next_track.download(next_track.title)
        track_list.append(next_track.title)
    return track_list
