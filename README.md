[![GitHub last commit](https://img.shields.io/github/last-commit/aatrubilin/sapozhnikabot.svg)](https://github.com/aatrubilin/sapozhnikabot/commits/master)
[![License](https://img.shields.io/github/license/aatrubilin/sapozhnikabot.svg)](LICENSE.md)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Sapozhnikabot

Бот сапожника - [@sapozhnikabot](https://t.me/sapozhnikabot)

## Getting Started

These instructions will get you a copy of the project up and running on your server.

### Run app in docker-compose

Clone the repo

```bash
git clone https://github.com/aatrubilin/sapozhnikabot
```

Go to project path

```bash
cd sapozhnikabot
```

Copy `.production` environments

```bash
cp .envs/.production_sample .envs/.production
nano .envs/.production
```

Setup envs

```dotenv
BOT_TOKEN=bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TIMEOUT_SEC=7200
SWEARS_DATASET_PATH=swars_jsons/ru.json
LOG_LEVEL=INFO
```

Up docker compose

```bash
docker-compose up -d --build
```

Boom! :fire: It's done! Add your bot to any chat!

## Development

Make sure to have the following on your host:

- [Python 3.9](https://www.python.org/downloads/)

Clone the repo

```bash
git clone https://github.com/aatrubilin/pinger
```

Go to project path

```bash
cd sapozhnikabot
```

Create a virtualenv:

```bash
python3 -m venv venv
```

Activate the virtualenv you have just created:

```bash
source venv/bin/activate
```

Install development requirements:

```bash
pip3 install -r requirements/local.txt
```

Install pre-commit hooks

```bash
pre-commit install
```

Set the environment variables

```bash
export BOT_TOKEN=bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
export TIMEOUT_SEC=10
export SWEARS_DATASET_PATH=swars_jsons/ru.json
export LOG_LEVEL=DEBUG
```

Run the app

```bash
python sapozhnikabot/main.py
```

## Built With

* [pymorphy2](https://pymorphy2.readthedocs.io/en/stable/) - Морфологический анализатор
* [[Jigsaw] Multilingual swear profanity](https://www.kaggle.com/miklgr500/jigsaw-multilingual-swear-profanity) - The set swear phrases
* [Дерзкий telegram бот](https://habr.com/ru/post/327586/) - Пост на Хабре

## Authors

* **Alexandr Trubilin** - *Initial work* - [AATrubilin](https://github.com/aatrubilin)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
