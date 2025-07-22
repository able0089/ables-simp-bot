import discord
import openai
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OWNER_ID = int(os.getenv("OWNER_ID"))

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

openai.api_key = OPENAI_API_KEY

async def is_owner_afk():
    owner = bot.get_user(OWNER_ID)
    if owner is None:
        return True
    return str(owner.status) in ["offline", "idle", "dnd"]

@bot.event
async def on_ready():
    print(f"Gpt-chan is online as {bot.user} ✨")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    mentioned = bot.user in message.mentions or str(OWNER_ID) in message.content
    if mentioned or message.reference:
        if await is_owner_afk():
            prompt = f"You're Gpt-chan, a friendly AI assistant replying on behalf of Able. They said: '{message.content}'. Reply kindly and naturally."
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100
            )
            reply = response.choices[0].message["content"]
            await message.reply(reply, mention_author=False)

    await bot.process_commands(message)

bot.run(TOKEN)
