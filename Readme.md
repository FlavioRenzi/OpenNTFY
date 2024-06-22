# OpenNTFY

A simple command line tool to send notifications to your telegram bot

## Installation

OpenNTFY is installed as a python module using pip

```bash
pip install OpenNTFY
```

the first time run the following command to configure OpenNTFY

```bash
OpenNTFY --config
```

This will store your telegram bot token and chat id in the config file in:

```
linux
~/.config/OpenNTFY/config.json
```

```
windows
C:\Users\{username}\AppData\Roaming\OpenNTFY\config.json
```

## Example usage

Send a message to your telegram bot

```bash
OpenNTFY "Test message"
```

Send a message to your telegram bot after the execution of a command

```bash
sudo apt upgrade; OpenNTFY "Upgrade terminated on {N}"
```

Send a message to your telegram bot after the execution of a command with the result of the command

```bash
long_program | OpenNTFY "Program terminated with result:"
```

Send a message to your telegram bot after the execution of a command and also a periodic message with the live view of it
> :warning: this is not supported on Windows

```bash
OpenNTFY -p 5m30s "watch ip address" "End message"
```

Send a file to your telegram bot

```bash
OpenNTFY -f /path/to/file "Message with file"
```

## Supported placeholders

You can use the following placeholders in your messages:

- `{N}` - Name of the computer running the command
- `{T}` - Time of the command execution
- `{D}` - Date of the command execution

## ToDo

- [x] Add config file
- [x] Add install script
- [x] Implement periodic notifications
- [x] Add initial guided setup
- [x] Add support for file sending
- [x] Add verbose mode
- [x] Add installation guide
- [ ] Fix periodic send support for windows
