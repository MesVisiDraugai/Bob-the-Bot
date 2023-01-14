import discord
from discord import app_commands
from discord import Role
from colorama import init, Fore, Back, Style
import random
import requests
import bs4
import json
import math


guildId = 123456 # Replace with Guild Id

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

tree = app_commands.CommandTree(client)
# colors of text in terminal: yellow=quote.

import json

# Create an empty dictionary to store user data
user_data = {}

# Function to get a user's data from the JSON file
def get_user_data(user_id):
    if user_id not in user_data:
        # If the user doesn't exist in the dictionary, try to read their data from the JSON file
        try:
            with open(f'{user_id}.json', 'r') as file:
                user_data[user_id] = json.load(file)
        except FileNotFoundError:
            # If the JSON file doesn't exist, create a new entry for the user with level 1 and 0 experience points
            user_data[user_id] = {'level': 1, 'xp': 0}
    return user_data[user_id]

# Function to save a user's data to the JSON file
def save_user_data(user_id, data):
    user_data[user_id] = data
    with open(f'{user_id}.json', 'w') as file:
        json.dump(data, file)

# Command to award XP to a user
@tree.command(name="givexp", description="Give XP to a user.", guild=discord.Object(id=guildId))
async def command(interaction, user: discord.Member, xp: int):
    user_data = get_user_data(user.id)
    user_data['xp'] += xp
    save_user_data(user.id, user_data)
    await interaction.response.send_message(f"{user.mention} has been awarded {xp} XP!")

# Command to check a user's level and XP
@tree.command(name="level", description="Check a user's level and XP.", guild=discord.Object(id=guildId))
async def command(interaction, user: discord.Member):
    user_data = get_user_data(user.id)
    await interaction.response.send_message(f"{user.mention} is level {user_data['level']} with {user_data['xp']} XP.")


# Ping Command
@tree.command(name="ping", description="Check the bot's ping.", guild=discord.Object(id=guildId))
async def command(interaction):
    await interaction.response.send_message(f"Pong! Latency: {client.latency:.2f}s")


@tree.command(name="giverole", description="give users a role", guild=discord.Object(id=guildId))
async def command(interaction, role: Role, member: discord.Member):
    await member.add_roles(role)
    await interaction.response.send_message(f"{member.mention} now has the {role.name} role!")

@tree.command(name="announce", description="Make an announcement.", guild=discord.Object(id=guildId))
async def command(interaction, *, message: str):
    guild = client.get_guild(guildId)
    await interaction.response.send_message(message)


@tree.command(name="quote", description="Get a random quote.", guild=discord.Object(id=guildId))
async def command(interaction):
    # Fetch a random quote from a website
    res = requests.get("https://www.goodreads.com/quotes")
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    quote_tags = soup.select('.quoteText')
    author_tags = soup.select('.authorOrTitle')
    quote = quote_tags[random.randint(0, len(quote_tags) - 1)].getText().strip()
    author = author_tags[random.randint(0, len(author_tags) - 1)].getText().strip()

    # Create an embed with the quote and its author
    embed = discord.Embed(title="Quote of the day", description=quote, color=0x00ff33)
    embed.set_author(name='quote')
    await interaction.response.send_message(embed=embed)


# Hello command

@tree.command(name="hello", description="Say hi!", guild=discord.Object(id=guildId))
async def command(interaction):
    await interaction.response.send_message("Howdy!")


# Info Command
@tree.command(name="info", description="Get info about the bot", guild=discord.Object(id=guildId))
async def command(interaction):
    embed = discord.Embed(title="Info",
                          description="I am a Top G bot made in python, I am an open source project and anyone can contribute!",
                          color=0x00ff33)
    embed.set_author(name="Bob the Bot")
    embed.add_field(name="Develpers", value="ExplodeCode \n OpenSourceSimon \n Tim \n Cattopy The Web", inline=False)
    await interaction.response.send_message(embed=embed)


# Calendar Command
@tree.command(name="calendar", description="View the calendar", guild=discord.Object(id=guildId))
async def command(interaction):
    import calendar
    yy = 2023
    mm = 1
    await interaction.response.send_message(calendar.month(yy, mm))


# Search Command
@tree.command(name="search", description="Search the internet.", guild=discord.Object(id=guildId))
async def command(interaction, query: app_commands.Range[str, 1]):
    # Perform the search
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(f"https://google.com/search?q={query}", headers=headers)
    res.raise_for_status()
    # Parse the search results
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    links = soup.select('.r a')

    # Send the results to the channel
    embed = discord.Embed(title="Search", description=f"Search results for '{query}'", color=0x00ff33)

    await interaction.response.send_message(embed=embed)



#8ball command


@tree.command(name="8ball", description="Ask the magic 8-ball a question.", guild=discord.Object(id=guildId))
async def command(interaction, query:str):
    # Get the question from the message
    question = query

    # Check if the question is empty
    if len(question) == 0:
        await interaction.response.send_message("You didn't ask a question!")
        return

    # Select a random response
    responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes - definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
    ]
    response = random.choice(responses)

    # Send the response
    await interaction.response.send_message(f"Question: {question}\nAnswer: {response}")

# Math command
@tree.command(name="math", description="Solve a math problem", guild=discord.Object(id=guildId))
async def command(interaction, problem: app_commands.Range[str, 1]):
    # Split the message into a list of words
    words = problem.split()
    # Make sure we have enough arguments
    if len(words) != 3:
        await interaction.response.send_message("Invalid number of arguments. Use -math [number] [operation] [number]")
        return
    # Get the first number and operation from the message
    number1 = float(words[0])
    operation = words[1]
    # Get the second number from the message
    number2 = float(words[2])
    # Perform the requested operation
    if operation == "+":
        result = number1 + number2
    elif operation == "-":
        result = number1 - number2
    elif operation == "*":
        result = number1 * number2
    elif operation == "/":
        if number2 == 0:
            await interaction.response.send_message("Error: Cannot divide by zero.")
            return
        result = number1 / number2

    else:
        await interaction.response.send_message("Invalid operation. Use +, -, *, or /.")
        return
    # Send the result to the channel
    await interaction.response.send_message(f"Result: {result}")


# When Bot is ready.
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=guildId))
    print(Fore.CYAN + f'Successfully logged in as {client.user}!')
    print('-------------------')
    print('Commands now online')
client.run('ADD_YOU_BOT_TOKEN_HERE')
