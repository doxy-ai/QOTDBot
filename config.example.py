# Copy this file to config.py and adjust before running the bot for the first time!

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

# Weather or not the bot should loop back to the beginning of the file when it reaches the end
should_loop = True

# Timezone to schedule in
timezone = 'America/Los_Angeles'

# Hour of the day to post a question
hour_of_day = 6