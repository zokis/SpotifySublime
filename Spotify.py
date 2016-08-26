import sublime
import sublime_plugin
import subprocess
import os
import threading

'''
alias pnext='dbus-send --print-reply=literal --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next'
alias pplay='dbus-send --print-reply=literal --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause'
alias ppause='dbus-send --print-reply=literal --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause'
alias pprev='dbus-send --print-reply=literal --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous'
alias pstop='dbus-send --print-reply=literal --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Stop'
sadfasdfasdf
asdfsad
asdfasdf
sadfsadfa
asdfasdfasdf

'''


class Runner(threading.Thread):

    BASE = 'dbus-send --print-reply=literal --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.%s'

    def __init__(self, command, shell, env):
        self.stdout = None
        self.stderr = None
        self.command = command or ''
        self.shell = shell or ''
        self.env = env or ''
        threading.Thread.__init__(self)

    def run(self):
        subprocess.Popen(
            [
                # self.shell,
                # '-ic',
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
        runner = Runner(self.command, os.environ['SHELL'], os.environ.copy())
        runner.start()


class PlaypauseCommand(Base):
    command = 'PlayPause'


class NextCommand(Base):
    command = 'Next'


class PreviousCommand(Base):
    command = 'Previous'


class StopCommand(Base):
    command = 'Stop'
