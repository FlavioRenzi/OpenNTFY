import subprocess
import sys
import time
import pyte


command = 'watch date'

screen = pyte.Screen(80, 24)
stream = pyte.Stream(screen)


process = subprocess.Popen(
    'stdbuf -oL ' + command,
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    universal_newlines=True
)
message_p = ''
for c in iter(lambda: process.stdout.read(1), b""):
    print(c,end="", flush=True)
    message_p += c
    stream.feed(c)