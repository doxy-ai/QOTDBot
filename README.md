# QOTDBot

A lightweight, configurable "Question of the Day" bot implemented in Python. QOTDBot selects a question from a configured source and posts it on a schedule to Discord.

This repository contains the core logic and utilities for scheduling, selecting, and delivering quotes. It aims to be simple to run locally.

## Features
- Pick a quote daily
- Lightweight — single-language Python codebase

## Quick start

1. Clone the repository
```bash
git clone https://github.com/doxy-ai/QOTDBot.git
cd QOTDBot
```

1. Create a virtual environment and install dependencies
```bash
python -m venv .venv
source .venv/bin/activate       # Linux / macOS
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

1. Create a configuration file (config.py — see [Configuration](#configuration)) with API tokens and schedule.

2. Run the bot
```bash
python QOTD.py
```

Requirements
- Python 3.8+
- pip

## Configuration

QOTDBot reads configuration from a `config.py` file. First copy the `config.example.py` file to `config.py` and then fill in the nessicary values

Example config.py
```
# Token for the bot (Can be created here: https://discord.com/developers)
discord_token = "<YOURS GOES HERE>"

# Channel ID to target
discord_target_channel : int = <YOURS GOES HERE>

# Message that should be sent before the bot embed... maybe an @role?
qotd_message = "@bob"

# Title of the embed
qotd_title = "Question of the Day"

# File where questions are/should be stored
qotd_file = "qotd.txt"

# File storing the current index (Add a single number in this file to indicate where in the qotd_file the bot should start)
index_file = "index.txt"

# Weather or not the bot should loop back to the beginning of the file when it reaches the end
should_loop = True

# Timezone to schedule in
timezone = 'America/Los_Angeles'

# Hour of the day to post a question
hour_of_day = 6
```

The qotd.txt file (or whatever you rename it to) should be filled with questions with each one appearing on its own line.

## License

[MIT](LICENSE)