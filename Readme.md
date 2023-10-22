# OpenNTFY

A simple command line tool to send notifications to your telegram bot

## Installation

To install OpenNTFY you can use the install script:
just run the following command in your terminal

```bash
wget -O - https://raw.githubusercontent.com/FlavioRenzi/OpenNTFY/master/install.sh | bash
```

Insert your telegram bot token and chat id in the config file

```bash
nano ~/.config/OpenNTFY/config.json
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
python long_program | OpenNTFY "Program terminated with result:"
```

Send a message to your telegram bot after the execution of a command with the result of the command and also a periodic message with the live view of it

```bash
OpenNTFY -p 5m30s "watch ip address" "End message"
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
- [ ] Add initial guided setup
- [ ] Add support for file sending
- [x] Add verbose mode
- [ ] Add installation guide
