from random import random
from yandex_music import Track


class RadioMood:
    @staticmethod
    def __gen_p_id():
        return "%s-%s-%s" % (int(random() * 1000), int(random() * 1000), int(random() * 1000))

    def __init__(self, client, mood):
        self.client = client
        self.mood = mood
        self.st_id = None
        self.st_fr = None

        self.current_track = None
        self.i = 0
        self.p_id = None
        self.tracks = None

    def start(self, st_id, st_fr):
        self.st_fr = st_fr
        self.st_id = st_id
        self.__upd_batch(None)
        self.current_track = self.__upd_cur_track()
        return self.current_track

    def play_next(self):
        self.__send_play_end(self.current_track, self.p_id)
        self.__send_play_stop(self.current_track, self.tracks.batch_id)
        self.i += 1
        if self.i >= len(self.tracks.sequence):
            self.__upd_batch(self.current_track.track_id)
        self.current_track = self.__upd_cur_track()
        return self.current_track

    def __upd_batch(self, queue=None):
        self.i = 0
        self.tracks = self.client.rotor_station_tracks(self.st_id, queue=queue)
        self.__send_start(self.tracks.batch_id)

    def __upd_cur_track(self):
        self.p_id = self.__gen_p_id()
        track = self.client.tracks(
            [self.tracks.sequence[self.i].track.track_id])[0]
        self.__send_play_start_track(track, self.p_id)
        self.__send_play_start(track, self.tracks.batch_id)
        return track

    def __send_start(self, batch_id):
        self.client.rotor_station_feedback_radio_started(
            station=self.st_id, from_=self.st_fr, batch_id=batch_id
        )

    def __send_play_start(self, track, batch_id):
        self.client.rotor_station_feedback_track_started(
            station=self.st_id, track_id=track.id, batch_id=batch_id)

    def __send_play_start_track(self, track, p_id):
        total_s = track.duration_ms / 1000
        self.client.play_audio(
            from_="desktop_win-home-playlist_of_the_day-playlist-default",
            track_id=track.id,
            total_played_seconds=0,
            album_id=track.albums[0].id,
            play_id=p_id,
            end_position_seconds=total_s,
            track_length_seconds=0,
        )

    def __send_play_end(self, track, p_id):
        played_s = track.duration_ms / 1000
        total_s = played_s
        self.client.play_audio(
            from_="desktop_win-home-playlist_of_the_day-playlist-default",
            track_id=track.id,
            album_id=track.albums[0].id,
            play_id=p_id,
            track_length_seconds=int(total_s),
            total_played_seconds=played_s,
            end_position_seconds=total_s,
        )

    def __send_play_stop(self, track, batch_id):
        played_s = track.duration_ms / 1000
        self.client.rotor_station_feedback_track_finished(
            station=self.st_id, track_id=track.id, total_played_seconds=played_s, batch_id=batch_id
        )
