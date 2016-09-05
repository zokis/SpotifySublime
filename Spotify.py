import sublime_plugin
import subprocess
import os
import threading


class Runner(threading.Thread):
    '''https://gist.github.com/duncan-bayne/3f7ef98a15b02b693bf47a03fda79b3a
    '''

    def __init__(self, command):
        self.command = command
        threading.Thread.__init__(self)

    def run(self):
        subprocess.Popen(
            self.command,
            env=os.environ.copy(),
            shell=False,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )


class Base(sublime_plugin.WindowCommand):
    command = 'PlayPause'
    base_command = [
        'dbus-send',
        '--print-reply=literal',
        '--dest=org.mpris.MediaPlayer2.spotify',
        '/org/mpris/MediaPlayer2',
        'org.mpris.MediaPlayer2.Player.%s'
    ]

    def get_command(self):
        command = self.base_command[:]
        command[-1] = command[-1] % self.command
        return command

    def run(self):
        runner = Runner(self.get_command())
        runner.start()


class PlaypausespotifyCommand(Base):
    pass


class NextspotifyCommand(Base):
    command = 'Next'


class PreviousspotifyCommand(Base):
    command = 'Previous'


class StopspotifyCommand(Base):
    command = 'Stop'


class OpenspotifyCommand(Base):
    command = 'spotify'
    base_command = ['%s']


class ClosespotifyCommand(Base):
    base_command = ['kill', '-9', '%s']

    def get_command(self):
        command = self.base_command[:]
        command[-1] = command[-1] % subprocess.check_output(["pidof", "-s", 'spotify'])
        return command


class VolumeCommand(Base):
    base_command = ['amixer', '-D', 'pulse', 'sset', 'Master', '%s']


class Volumeup5Command(VolumeCommand):
    command = '5%+'


class Volumeup10Command(VolumeCommand):
    command = '10%+'


class Volumedown5Command(VolumeCommand):
    command = '5%-'


class Volumedown10Command(VolumeCommand):
    command = '10%-'
