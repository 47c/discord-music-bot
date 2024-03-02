from utilities.dependencies import *

@tree.command(
    name="play",
    description="pushes song to queue and plays instantly if queue previously empty",
    guild=discord.Object(id=1101666836690505819),
)
async def comm_play(interaction: discord.Interaction, query: str):
    global guild_data

    caller: discord.Member              = interaction.user
    guild: discord.Guild                = interaction.guild

    voice_channel: discord.VoiceChannel = None
    try:
        voice_channel: discord.VoiceChannel = caller.voice.channel
    except:
        pass

    if not guild.id in guild_data.keys():
        guild_data[guild.id]            = GuildData(client)

    data: GuildData                     = guild_data[guild.id]

    await interaction.response.defer(thinking=True)
    if not voice_channel:
        await interaction.followup.send(content="you're not in any voice channel")
        return

    if data.status.connected_to_channel:
        if not voice_channel == data.status.voice_client.channel:
            await interaction.followup.send(content="currently busy")
            return

    if not data.status.voice_client or not data.status.voice_client.is_connected():
        data.status.voice_client = (await voice_channel.connect())

    data.status.update_status()
    await data.audio_queue.play(query, data.status, interaction.followup)
