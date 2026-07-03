import discord
from discord import app_commands
from discord.ext import commands
import random
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, application_id=1512716074074902548)

@bot.event
async def on_ready():
    print(f'{bot.user} is ready!')
    print(f'Bout ID: {bot.user.id}')
    print(f'Servers: {len(bot.guilds)}')
    local_commands = bot.tree.get_commands()
    local_names = [cmd.name for cmd in local_commands]
    print('Local slash command count:', len(local_commands))
    print('Local slash command names:', local_names)
    try:
        for guild in bot.guilds:
            print(f'Copying global commands to guild {guild.id} and syncing...')
            bot.tree.copy_global_to(guild=guild)
            guild_synced = await bot.tree.sync(guild=guild)
            print(f'Synced {len(guild_synced)} guild command(s) to guild {guild.id}')

            remote_commands = await bot.tree.fetch_commands(guild=guild)
            remote_names = [c.name for c in remote_commands]
            print(f'Guild {guild.id} remote commands after sync:', remote_names)
    except Exception as e:
        print(f'Error syncing commands: {e}')

# ===== RAID COMMANDS =====

@bot.tree.command(name='ra1d', description='RA1D THE FUCKING SERVER')
@app_commands.describe(times='How many times to send', use_emojis='Add emojis to the message')
async def ra1d(interaction: discord.Interaction, times: int = 4, use_emojis: bool = True):
    base_message = "Putinka V1 just destroyed your server join us and start raid!\n\nNOW JOIN THIS SERVER: https://discord.gg/aYqEkkjkQ"
    
    if use_emojis:
        emojis = ["💀", "🔥", "⚡", "💥", "🚀", "😈", "👹"]
        message = f"{random.choice(emojis)} {base_message} {random.choice(emojis)}"
    else:
        message = base_message
    
    await interaction.response.defer()
    
    for i in range(times):
        await interaction.followup.send(message)
        await asyncio.sleep(0.5)  # Small delay to avoid rate limits

@bot.tree.command(name='spam', description='Spam a message multiple times')
@app_commands.describe(message='Message to spam', times='How many times to spam')
async def spam(interaction: discord.Interaction, message: str, times: int = 10):
    await interaction.response.defer()
    
    for i in range(times):
        await interaction.followup.send(message)
        await asyncio.sleep(0.3)

@bot.tree.command(name='massping', description='Ping everyone in the server')
async def massping(interaction: discord.Interaction):
    await interaction.response.defer()
    
    guild = interaction.guild
    if guild is None:
        await interaction.followup.send('This command must be used in a server.', ephemeral=True)
        return

    members = [member.mention for member in guild.members if not member.bot]
    if members:
        await interaction.followup.send(f"@everyone {' '.join(members[:50])}")
    else:
        await interaction.followup.send("No members to ping!")

@bot.tree.command(name='nuke', description='Delete all messages in the channel')
async def nuke(interaction: discord.Interaction):
    await interaction.response.defer()
    
    channel = interaction.channel
    if channel is None:
        await interaction.followup.send('This command must be used in a server channel.', ephemeral=True)
        return

    deleted = 0
    async for message in channel.history(limit=None):
        try:
            await message.delete()
            deleted += 1
            await asyncio.sleep(0.1)
        except:
            pass
    
    await interaction.followup.send(f"Deleted {deleted} messages!")

@bot.tree.command(name='everyone', description='Send @everyone message')
@app_commands.describe(message='Message to send with @everyone')
async def everyone(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(f"@everyone {message}")

# ===== UTILITY COMMANDS =====

@bot.tree.command(name='say', description='Make the bot say something')
@app_commands.describe(message='The message you want the bot to say')
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message)

@bot.tree.command(name='serverinfo', description='Get server information')
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    if guild is None:
        await interaction.response.send_message('This command must be used inside a server.', ephemeral=True)
        return

    embed = discord.Embed(title=f"Server Info: {guild.name}", color=discord.Color.red())
    embed.add_field(name="Server ID", value=guild.id, inline=True)
    embed.add_field(name="Members", value=guild.member_count, inline=True)
    embed.add_field(name="Channels", value=len(guild.channels), inline=True)
    embed.add_field(name="Roles", value=len(guild.roles), inline=True)
    embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name='userinfo', description='Get user information')
@app_commands.describe(user='User to get info about (optional)')
async def userinfo(interaction: discord.Interaction, user: discord.Member = None):
    target = user or interaction.user
    embed = discord.Embed(title=f"User Info: {target.name}", color=discord.Color.blue())
    embed.add_field(name="User ID", value=target.id, inline=True)
    embed.add_field(name="Joined", value=target.joined_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Created", value=target.created_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Roles", value=len(target.roles), inline=True)
    embed.set_thumbnail(url=target.avatar.url if target.avatar else None)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name='dm_user', description='Send a DM to a user')
@app_commands.describe(user='User to DM', message='Message to send')
async def dm_user(interaction: discord.Interaction, user: discord.Member, message: str):
    try:
        await user.send(message)
        await interaction.response.send_message(f"Sent DM to {user.display_name}.", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("I cannot DM that user.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Failed to send DM: {e}", ephemeral=True)

@bot.tree.command(name='help', description='Show all available commands')
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="🚀 RAID BOT COMMANDS", color=discord.Color.purple())
    
    embed.add_field(name="🔥 RAID COMMANDS", value="""
    `/ra1d` - Send raid message
    `/spam` - Spam a message
    `/massping` - Ping all members
    `/nuke` - Delete channel messages
    `/everyone` - Send @everyone message
    """, inline=False)
    
    embed.add_field(name="🛠️ UTILITY COMMANDS", value="""
    `/say` - Make bot say something
    `/serverinfo` - Get server info
    `/userinfo` - Get user info
    `/dm_user` - Send a DM to a user
    `/ad_of_server` - Send the server invite link
    `/help` - Show this help
    """, inline=False)
    
    await interaction.response.send_message(embed=embed)

# Discord slash command names cannot contain spaces, so this command is registered as `/ad_of_server`.
@bot.tree.command(name='ad_of_server', description='Send the server invite link')
async def ad_of_server(interaction: discord.Interaction):
    await interaction.response.send_message('https://discord.gg/aYqEkkjkQ')

# Put all your GIFs here - everyone can use them
MY_GIFS = {
    "dog": "https://cdn.discordapp.com/attachments/1437820996647256328/1438590455724900472/CuteDog.mp4?ex=69176f44&is=69161dc4&hm=9704f063056ec2d1831458ef6299daf1fcc8fd70df4a031dda94c91e0200abca&",
    "fat": "https://cdn.discordapp.com/attachments/1408686054419988513/1408688616728690768/trim.8C46EDC0-7AB2-420C-8CBA-D501F251244D.mp4?ex=68ab4fc2&is=68a9fe42&hm=5caa232f36402f0270fda837c61cc1a980b5705a17fdcf32ee691d393640636c&",
    "slut": "https://cdn.discordapp.com/attachments/1437820996647256328/1438591077039738880/m2-res_640p.mp4?ex=69176fd8&is=69161e58&hm=9bf3a4330944faff31bd1c1bc6365b1c68b42a2ecb05d8e8bf0cfddec247ae69&",
    # Add as many as you want here
    # "name": "direct_gif_url",
}

@bot.tree.command(
    name="thug",
    description="Send 18+ content",
)
@app_commands.describe(name="Thug")
async def gif(interaction: discord.Interaction, name: str):
    name = name.lower()
    if name in MY_GIFS:
        await interaction.response.send_message(MY_GIFS[name])
    else:
        await interaction.response.send_message(
            "Enjoy lol hahaha!",
            ephemeral=True
        )

# This makes Discord show a dropdown of all your GIF names
@gif.autocomplete("name")
async def gif_autocomplete(interaction: discord.Interaction, current: str):
    choices = []
    for gif_name in MY_GIFS.keys():
        if current.lower() in gif_name.lower():
            choices.append(app_commands.Choice(name=gif_name.title(), value=gif_name))
    return choices[:25] # Discord max is 25
YOUR_SERVER_ID = 1167915307302670459 # Replace with your server ID
ALLOWED_USERS = [1278266354268372993, 1475479427965128857] # Your ID + your friend's ID

def is_allowed():
    async def predicate(interaction: discord.Interaction) -> bool:
        # Allow everyone by default
        return True
    return app_commands.check(predicate)

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message(
            "You can't use this bot in this server.",
            ephemeral=True
        )
        # const { SlashCommandBuilder } = require('discord.js');

# module.exports = {
#   data: new SlashCommandBuilder()
#     .setName('interact ra1d')
#     .setDescription('Interact with bot to send raid messages')
#     .addStringOption(option =>
#       option.setName('message')
#         .setDescription('What to say')
#         .setRequired(true)),
#
#   async execute(interaction) {
#     const msg = interaction.options.getString('message');
#     await interaction.reply({ content: 'sent', ephemeral: true });
#     await interaction.channel.send(msg);
#   },
#};
@bot.tree.command(name='dm_role', description='DM all users with a role')
@app_commands.describe(role='Role to DM', message='Message to send')
async def dm_role(interaction: discord.Interaction, role: discord.Role, message: str):
    await interaction.response.defer(ephemeral=True)
    count = 0
    for member in role.members:
        try:
            await member.send(message)
            count += 1
            await asyncio.sleep(1)  # avoid rate limit
        except Exception:
            pass
    await interaction.followup.send(f"DM sent to {count} users", ephemeral=True)

bot.run(TOKEN)

export default botConfig;
