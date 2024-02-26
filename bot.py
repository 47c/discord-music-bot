from utilities.dependencies import *
from utilities.definitions  import *

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1101666836690505819))

    log(f'{client.user} ready')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

@tree.command(
    name="join_voice",
    description="connects to caller voice channel",
    guild=discord.Object(id=1101666836690505819)
)
async def connect_command(interaction: discord.Interaction):
    global guild_data

    caller: discord.Member              = interaction.user
    guild: discord.Guild                = interaction.guild
    voice_channel: discord.VoiceChannel = caller.voice.channel

    if not guild.id in guild_data.keys():
        guild_data[guild.id]            = GuildData(client)

    data: GuildData                     = guild_data[guild.id]

    if not voice_channel:
        await interaction.response.send_message(content="you're not in any voice channel")
        return

    if data.status.connected_to_channel:
        await interaction.response.send_message(content="currently busy")
        return

    data.status.update_status(interaction, 
                              await voice_channel.connect())

if __name__ == '__main__':
    logger_thread.start(); timeout_thread.start()

    client.run(BOT_TOKEN)

    GLOBAL_KILLTHREADS = logger.kill = True
    logger_thread.join(); timeout_thread.join()