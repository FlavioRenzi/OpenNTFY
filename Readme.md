# OpenNTFY

## Installation

```bash
wget -O - https://raw.githubusercontent.com/FlavioRenzi/OpenNTFY/master/install.sh | bash
```

Insert your token and chat id in the config file

```bash
nano ~/.config/OpenNTFY/config.json
```

## Example usage

```bash
OpenNTFY "Test message"
```

```bash
sudo apt upgrade; OpenNTFY "Upgrade terminated on {N}"
```

```bash
python long_program | OpenNTFY "Program terminated with result:"
```

```bash
OpenNTFY -p 5m30s "watch ip address" "Ip at time {T} is:"
```

## ToDo

- [x] Add config file
- [x] Add install script
- [ ] Implement periodic notifications
- [ ] Add initial guided setup
- [ ] Add support for file sending
- [x] Add verbose mode
- [ ] Add installation guide
