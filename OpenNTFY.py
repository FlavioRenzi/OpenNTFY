import sys
import os
import asyncio
from telegram import Bot
import subprocess
import argparse
from datetime import datetime, timedelta
import re
import json


parser = argparse.ArgumentParser(description='Telegram notifier')
parser.add_argument('message', type=str, help='The message to send')
parser.add_argument('-p','--periodic', nargs=2, metavar=('period', 'command'), help='An optional parameter')
parser.add_argument('-v','--verbose', action='store_true', help='Verbose mode')



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
        """ while True:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            for line in process.stdout:
                message += line.strip()+'\n'
            await send_telegram_message(message, TELEGRAM_CHAT_ID, TELEGRAM_BOT_TOKEN)
            await asyncio.sleep(period.total_seconds()) """
    
    # Piped execution      
    if not os.isatty(0):
        cmd = sys.stdin.read()
        message += cmd
    
    
    # Send message
    verboseprint(f"Sending message: {message}")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(bot.send_message(chat_id=config['TELEGRAM_CHAT_ID'], text=message))
        verboseprint("Message sent")
    except Exception as e:
        print(f"Error durig message sending: {str(e)}")
        sys.exit(1)

"""
 #used for getting live update
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: ./il-mio-script.py 'your command'")
        sys.exit(1)

    command = sys.argv[1]
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    loop = asyncio.get_event_loop()
    
    for line in process.stdout:
        message = line.strip()
        print(message)  # Stampa l'output sullo stdout del tuo script
        loop.run_until_complete(send_telegram_message(message, TELEGRAM_CHAT_ID, TELEGRAM_BOT_TOKEN))

    print("Command execution completed.")
"""