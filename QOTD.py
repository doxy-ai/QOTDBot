import schedule
import time
import pytz
import discord
import asyncio
import config
from discord import app_commands
from discord.ext import tasks
from datetime import datetime, timedelta

class QOTDClient(discord.Client):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.tree = app_commands.CommandTree(self)
		self.target_channel = ""
		self.index = 0
		self.initalized = asyncio.Event()

	async def setup_hook(self) -> None:
		# start the task to run in the background
		self.poll_daily_send_background_task.start()

	def read_lines(self):
		with open(config.qotd_file, "r") as f:
			lines = f.read().splitlines()
		return lines

	def write_lines(self, lines):
		with open(config.qotd_file, "w") as f:
			f.write("\n".join(lines))

	def print_next_tomorrow(self):
		loop = asyncio.get_event_loop()
		lines = self.read_lines()
		size = len(lines)
		if size == 0:
			loop.create_task(self.target_channel.send(content="Error: There are no questions to ask!"))
			print("There are no questions to ask!")
			return

		global index
		if size == self.index + 1:
			if config.should_loop:
				loop.create_task(self.target_channel.send(content="Last question looping"))
				print("Last question looping")
			else:
				loop.create_task(self.target_channel.send(content="Error: There are no more questions to ask!"))
				print("There are no more questions to ask!")
				return

		print(lines[self.index])
		embed = discord.Embed(title=config.qotd_title, description=lines[self.index])
		loop.create_task(self.target_channel.send(content=config.qotd_message, embed=embed))
		self.index = (self.index + 1) % size

	async def on_ready(self):
		await self.tree.sync()
		self.target_channel = self.get_channel(config.discord_target_channel)

		# Make sure the qotd file exists!
		open(config.qotd_file, "a").close()

		# Schedule printing
		local_tz = pytz.timezone(config.timezone)
		now = datetime.now(local_tz)
		next_run = now.replace(hour=config.hour_of_day, minute=0, second=0, microsecond=0) + timedelta(days=1)
		schedule.every().day.at(next_run.strftime("%H:%M")).do(self.print_next_tomorrow)

		print(f'Logged in as {self.user} (ID: {self.user.id})')
		print(self.target_channel)
		print(config.discord_target_channel)
		self.initalized.set()

	@tasks.loop(seconds=1800) # task runs every 30 minutes
	# @tasks.loop(seconds=5)
	async def poll_daily_send_background_task(self):
		schedule.run_pending()
		# self.print_next_tomorrow()

	@poll_daily_send_background_task.before_loop
	async def before_poll(self):
		await self.wait_until_ready()  # wait until the bot logs in
		await self.initalized.wait()

intents = discord.Intents.default()
intents.message_content = True

client = QOTDClient(intents=intents)

@client.tree.command(
	name="add_question",
	description="Adds a question to the end of the list of questions",
)
@app_commands.describe(text='Question to ask')
async def add_question(interaction, text: str):
	print("adding question")
	lines = client.read_lines()

	if text in lines:
		await interaction.response.send_message("Question already added!", ephemeral=True)
		return

	lines.append(text.strip())
	client.write_lines(lines)
	await interaction.response.send_message("Question successfully added!", ephemeral=True)

@client.tree.command(
	name="add_question_tomorrow",
	description="Adds a question that will be run tomorrow to the list of questions",
)
@app_commands.describe(text='Question to ask')
async def add_question_tomorrow(interaction, text: str):
	print("adding question tomorrow")
	lines = client.read_lines()

	if text in lines:
		await interaction.response.send_message("Question already added!", ephemeral=True)
		return

	lines.insert(index + 1, text.strip())
	client.write_lines(lines)
	await interaction.response.send_message("Question successfully added!", ephemeral=True)

client.run(config.discord_token)
