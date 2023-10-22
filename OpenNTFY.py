import sys
import os
import asyncio
from telegram import Bot
import subprocess
import argparse
from datetime import datetime, timedelta
import re
import json
import pyte
import time
import threading



parser = argparse.ArgumentParser(description='Telegram notifier')
parser.add_argument('message', type=str, help='The message to send')
parser.add_argument('-p','--periodic', nargs=2, metavar=('period', 'command'), help='Execute a command getting periodical updates')
parser.add_argument('-v','--verbose', action='store_true', help='Verbose mode')
parser.add_argument('-f','--file', type=str, help='File to send with relative path')

loop = asyncio.get_event_loop()
config = {}
def send(message):
    loop.run_until_complete(bot.send_message(chat_id=config['TELEGRAM_CHAT_ID'], text=message))

screen = pyte.Screen(80, 24)

def parse_screen():
    msg = ''
    if screen.display != "":
        for line in screen.display:
            msg += line
            msg += '\n'
    return msg

def periodic_send(period):
    time.sleep(1)
    while True:
        message_p = parse_screen()
        if message_p != '': 
            send(message_p)
        time.sleep(period.total_seconds())



def parse_time_string(time_str):
    parts = re.findall('.*?[smhd]', time_str)
    print(parts)
    total_seconds = 0

    for part in parts:
        value = int(part[:-1])
        unit = part[-1]

        if unit == 's':
            total_seconds += value
        elif unit == 'm':
            total_seconds += value * 60
        elif unit == 'h':
            total_seconds += value * 3600
        elif unit == 'd':
            total_seconds += value * 86400
        else:
            raise ValueError(f"Time unit not reconized: {unit}")

    return timedelta(seconds=total_seconds)

if __name__ == '__main__':
    try:
        # Load config
        config = json.load(open(os.path.expanduser('~')+'/.config/OpenNTFY/config.json'))
        #print(config)
        bot = Bot(config['TELEGRAM_TOKEN'])
        
        
        # Parse arguments
        args = parser.parse_args()
        if args.verbose:
            def verboseprint(*args):
                for arg in args:
                    print(arg)
                print
        else:   
            verboseprint = lambda *a: None      # do-nothing function
        #print(args)
        
        
        # Parse placeholders
        dt = datetime.now()
        filds = {
            'N': os.uname()[1],
            'T': dt.strftime("%H:%M:%S"), 
            'D': dt.strftime("%d:%m:%Y")
        }
        message = args.message.format(**filds)+'\n'
        
        
        
        # Periodic execution
        if args.periodic:
            period = parse_time_string(args.periodic[0])
            command = args.periodic[1]
            verboseprint(f"Periodic execution of {command} every {period}")
            
            send_thread = threading.Thread(target=lambda: periodic_send(period))
            send_thread.daemon = True
            send_thread.start()
            
            actual_screen = os.get_terminal_size()
            screen = pyte.Screen(actual_screen.columns, actual_screen.lines)
            stream = pyte.Stream(screen)

            process = subprocess.Popen(
                'stdbuf -oL ' + command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            for c in iter(lambda: process.stdout.read(1), b""):
                print(c,end="", flush=True)
                stream.feed(c)
                screen = screen
            
            

        # Piped execution      
        if not os.isatty(0):
            cmd = sys.stdin.read()
            message += cmd
        
        # Send file
        if args.file:
            verboseprint(f"Sending file: {args.file}")
            try:
                loop.run_until_complete(bot.send_document(chat_id=config['TELEGRAM_CHAT_ID'], document=open(args.file, 'rb'), caption=message))
                verboseprint("File sent")
            except Exception as e:
                print(f"Error durig file sending: {str(e)}")
                sys.exit(1)
        else:
            # Send message
            verboseprint(f"Sending message: {message}")
            try:
                send(message)
                verboseprint("Message sent")
            except Exception as e:
                print(f"Error durig message sending: {str(e)}")
                sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(1)