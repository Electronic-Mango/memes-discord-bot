# Memes Discord bot

[![CodeQL](https://github.com/Electronic-Mango/memes-discord-bot/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Electronic-Mango/memes-discord-bot/actions/workflows/codeql-analysis.yml)
[![Black](https://github.com/Electronic-Mango/memes-discord-bot/actions/workflows/black.yml/badge.svg)](https://github.com/Electronic-Mango/memes-discord-bot/actions/workflows/black.yml)
[![Flake8](https://github.com/Electronic-Mango/memes-discord-bot/actions/workflows/flake8.yml/badge.svg)](https://github.com/Electronic-Mango/memes-discord-bot/actions/workflows/flake8.yml)

A simple Discord bot sending memes and copypastas via Discord, build with [`discord.py`](https://github.com/Rapptz/discord.py) and [`deep_translator`](https://github.com/nidhaloff/deep-translator).



## Requirements

This bot was built using `Python 3.10`.
Full list of requirements is in `requirements.txt` file.



## Running the bot

You can run the bot from source, or in a Docker container.


### From source

 1. Create a Discord bot.
 1. Install all packages from `requirements.txt`.
 1. Fill missing values in `settings.yml` (mainly Discord bot token), or supply custom `settings.yml` file with overwritting values.
 1. Execute `src/main.py` via Python.


### Docker

 1. Create a Discord bot.
 1. Create and fill `custom_settings.yml` file with overwritting values from `settings.yml`, mainly Discord bot token.
    You can also fill `settings.yml` directly.
    Or you can modify `docker-compose.yml` to load custom `settings.yml` from a mounted volume, rather than from a file in the docker image.
 1. Run `docker compose up -d --build` in terminal.

You can skip the `--build` flag if you didn't modify the source code (or `custom_settings.yml` file).

By default all YAML files from the project root are added to the Docker image.
If you don't want to rebuild the image every time you modify `settings.yml` or `custom_settings.yml` you can load custom one from a mounted volume.
This will require modification to `docker-compose.yml`.



## Commands

(Almost) all command names and their aliases can be configured through `settings.yml`, or through a custom settings YAML.
There are present default values in `settings.yml` which can be used as-is.

 * `help` - prints help message, its name cannot be modified through `settings.yml`
 * `media` - sends back a media item (image, GIF, video, etc)
 * `text` - sends back a text message
 * `setlanguage` - sets language of text messages
 * `resetlanguage` - resets language of text messages to default
 * `deepfriedtext` - sends back a "deep-fried" text message

Sources for media and texts are in `sources.yml` file, or whichever file is configured in `settings.yml`.


### Text message language

Setting text messages language doesn't change a source, it just translates the text received from a source.
Translation is done through [`deep_translator`](https://github.com/nidhaloff/deep-translator) and Google Translate.


### Deep-fried text messages

What does it mean?
Before a text from a source is send back, it's translated through multiple languages, then to either original language or target language configured via `setlanguage` command.

Translating between multiple different languages causes texts to be weirdly distorted and strange, which is the point of this command.

Intermediate languages can be configured via `settings.yml`.
It can be however many languages as you'd like, just keep in mind, that each translation does take some time.
