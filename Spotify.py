import sublime_plugin
import subprocess
import threading


class Runner(threading.Thread):
    def __init__(self, command):
        self.stdout = None
        self.stderr = None
        self.command = command or ''
        threading.Thread.__init__(self)

    def run(self):
        subprocess.Popen(
            [
                'dbus-send',
                '--print-reply=literal',
                '--dest=org.mpris.MediaPlayer2.spotify',
                '/org/mpris/MediaPlayer2',
                'org.mpris.MediaPlayer2.Player.%s' % self.command
            ],
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            env=self.env
        )


class Base(sublime_plugin.WindowCommand):
    command = 'PlayPause'

    def run(self):
        runner = Runner(self.command)
        runner.start()


class PlaypauseCommand(Base):
    command = 'PlayPause'


class NextCommand(Base):
    command = 'Next'


class PreviousCommand(Base):
    command = 'Previous'


class StopCommand(Base):
    command = 'Stop'
