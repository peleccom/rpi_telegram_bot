# RaspberryPi Telegram Bot

A simple telegram bot to control Raspberry Pi box

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

```
sudo pip install -r requirements.txt 
```

### Installing

Setup bot 
Set environment variables 
```

export BOT_TOKEN='YOUR_BOT_TOKEN_HERE'\
export 	BOT_ADMIN_ID='ID_OF_YOUR_TELEGRAM_PROFILE'
```

Only your can send commands to this bot

to start bot in polling mode (if you placed behind NAT)

```
python telegram_bot.py
```

send commands to bot


## Built With

* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Python wrapper for telegram BOT API

## TODO
* Add plugin system
* Add permission sytem
* New	 functionality

## Authors

* **Alexander Pitkin** - *Initial work* - [GitHub Profile](https://github.com/peleccom)

See also the list of [contributors](https://github.com/peleccom/rpi_telegram_bot/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
