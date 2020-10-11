#!/usr/bin/env python3
# r/NewZealand discord bot
# bleckbleek

# May 2019 - Creation
# October 2020 - Family Tree removed

# Imports
import discord
import pickle

# Constants
# Message to be sent in response to the help command
helpMsg = """
$birb pfp <username> to show someone's profile picture
Say 'kereru' to have the bot respond with 'thwomp'
React to a message with the quote react, and the message will be saved in #quotes
"""
# Dict to hold values so they can be easily changed
settings = {'phrase': '$birb',
            'configPhrase': '$birbConfig',
            'channelQuotes': 520173900584321044,
            'channelBot': 575599407131525120,
            'idBot': 572737682372034561,
            'idDev': 319603023137472512,
            'roleAdmin': 268278295517331457,
            'roleMod': 298325667723083776,
            'channelGeneral': 268296171598905344
            }

# Loads
# Load client secret from file not made public
client_secret = open('client_secret.txt', 'r').read()
# Load config settings that can be changed with the config command
configSettings = pickle.load(open('configSettings.pkl', 'rb'))
# Create the client object
client = discord.Client()

# Startup notification
@client.event
async def on_ready():
    print('Logged in as\n' + client.user.name + '\n' + str(client.user.id) + '\n------')
    await client.change_presence(status=discord.Status.online, activity=discord.Game(settings['phrase'] + " help"))
    await client.get_channel(settings['channelBot']).send("Kereru Bot online!\n*thwomp*")

# Reacting to message being sent anywhere in the server
@client.event
async def on_message(message):
    command = message.content.split()

    # If the message starts with the trigger phrase, identify and run the command
    if command[0] == settings['phrase']:
        choice = command[1]

        # If the command is 'help' then send the help text
        if choice == 'help':
            await message.channel.send(helpMsg)

        # If the command is 'pfp' then send the requested avatar
        if choice == 'pfp':
            await message.channel.send(discord.utils.get(message.guild.members, name=command[2]).avatar_url)

    # If: message starts with the config phrase and
    #     the message was sent by the developer or someone with an approved role
    #     Run the config method
    if command[0] == settings['configPhrase'] and (((settings['roleAdmin'] or settings['roleMod']) in message.author.roles) or
                                                   (message.author.id == settings['idDev'])):

        # If the command was 'flapCount' then change the flapcount variable to the specified number
        if command[1] == "flapCount":
            configSettings['flapCount'] = int(command[2])

        # Save the new settings to a pickle file so they will remain next time the bot is started
        pickle.dump(configSettings, open('configSettings.pkl', 'wb'))

    # Some meme requested by Lazer. I don't get the reference.
    if message.content.lower() == "am i ever gonna see your face again?":
        await message.channel.send("No way, get fucked, fuck off!")

    # If no other code triggers, then check the message for the word kereru and respond with thwomps.
    # The max number of thwomps can be set by changing the flapCount config.
    else:
        flap = ""
        for i in command:
            if ('kereru' in i.lower()) | ("kererū" in i.lower()) and (message.author.id != settings['idBot']) and (
                    flap.count('*thwomp*') < configSettings['flapCount']):
                flap += "*thwomp* "
        if flap != "":
            await message.channel.send(flap)


# Reacting to any reaction being added to any message
@client.event
async def on_reaction_add(reaction, user):
    # If:
    # the reaction is the quote react,
    # and the message was not sent by the bot,
    # and there is only one reaction,
    # then run the quote code
    if (reaction.emoji.name == "quote") and (reaction.message.author.id != settings['idBot']) and (reaction.count == 1):
        msg = reaction.message
        auth = reaction.message.author

        embed = discord.Embed(title=msg.clean_content, color=auth.color)
        embed.set_author(name=auth.display_name, url=msg.jump_url, icon_url = auth.avatar_url)
        embed.set_footer(text="Quoted by: " + user.display_name)

        attach = []
        if msg.attachments:
            attach = msg.attachments[0]
        # If the message is in a nsfw channel, or a spoiler, don't quote the attachment
        if (attach != []) and (msg.channel.is_nsfw() != True) and (attach.is_spoiler() != True):
            embed.set_image(url=attach.url)

        if (embed.title == "") and (embed.image.url == embed.Empty):
            return

        await client.get_channel(settings['channelQuotes']).send(embed=embed)


client.run(client_secret)
